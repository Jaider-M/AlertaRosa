import os
import torch
import numpy as np
from PIL import Image
from io import BytesIO
from pathlib import Path
from monai.networks.nets import DenseNet121
from monai.transforms import Compose, LoadImage, EnsureChannelFirst, ScaleIntensity, Resize

from app.models.clinical import AIResult
from app.core.config import settings

class MedicalIAEngine:
    def __init__(self):
        # 1. Configurar el dispositivo de ejecución (CPU para producción backend estándar)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # 2. Reconstruir la arquitectura exacta utilizada en el entrenamiento de Kaggle
        # spatial_dims=2 para imágenes 2D, in_channels=1 para escala de grises, out_channels=2 (Benigno/Maligno)
        self.model = DenseNet121(spatial_dims=2, in_channels=1, out_channels=2)
        
        # 3. Localizar y cargar los pesos entrenados de forma segura
        # Asume que guardas el archivo 'monai_mamografia_model.pth' en una carpeta 'weights' dentro de 'core' o 'services'
        self.weights_path = Path(__file__).parent.parent / "core" / "weights" / "monai_mamografia_model.pth"
        
        if self.weights_path.exists():
            self.model.load_state_dict(torch.load(self.weights_path, map_location=self.device, weights_only=True))
            print(f" [AlertaRosa AI] Pesos cargados con éxito desde {self.weights_path}")
        else:
            print(f" [AlertaRosa AI] Archivo de pesos NO encontrado en: {self.weights_path}. El modelo usará inicialización aleatoria.")
            
        self.model.to(self.device)
        self.model.eval() # Desactivar Dropout y BatchNorm para inferencia estable

        # 4. Pipeline de preprocesamiento clínico idéntico al set de validación de Kaggle
        self.preprocessing_transforms = Compose([
            EnsureChannelFirst(channel_dim="no_channel"),
            Resize(spatial_size=(256, 256)), # ¡Corregido a 256x256 según el entrenamiento real!
            ScaleIntensity()                 # Copia exacta de la intensidad del pipeline de validación
        ])

    def _map_to_birads(self, risk_score: float) -> str:
        """
        Mapeo heurístico basado en la probabilidad de malignidad para sugerir
        una categoría BI-RADS preliminar en el sistema AlertaRosa.
        """
        if risk_score < 0.15:
            return "BI-RADS 1: Negativo"
        elif risk_score < 0.35:
            return "BI-RADS 2: Hallazgos Benignos"
        elif risk_score < 0.60:
            return "BI-RADS 3: Probablemente Benigno (Seguimiento a corto plazo)"
        elif risk_score < 0.85:
            return "BI-RADS 4: Sospecha de Anomalía (Considerar Biopsia)"
        else:
            return "BI-RADS 5: Altamente Sugestivo de Malignidad"

    def analizar_mamografia(self, image_bytes: bytes) -> dict:
        """
        Recibe los bytes de la imagen desde el controlador de FastAPI,
        realiza el preprocesamiento, ejecuta la inferencia con la DenseNet121
        y retorna las métricas clínicas formateadas.
        """
        try:
            # Convertir bytes en formato PIL Image en escala de grises
            pil_image = Image.open(BytesIO(image_bytes)).convert("L")
            img_array = np.array(pil_image, dtype=np.float32)
            
            # Aplicar transformaciones MONAI en memoria
            img_tensor = self.preprocessing_transforms(img_array)
            
            # Expandir dimensiones para simular el tamaño del Batch (de [1, 256, 256] a [1, 1, 256, 256])
            img_tensor = img_tensor.unsqueeze(0).to(self.device)
            
            # Inferencia sin cálculo de gradientes (optimiza velocidad y memoria)
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilidades = torch.softmax(outputs, dim=1).cpu().numpy()[0]
                
            prob_benigno = float(probabilidades[0])
            prob_maligno = float(probabilidades[1])
            
            # --- Ajuste del Umbral de Sensibilidad Clínica ---
            # Para respetar el récord del modelo con 93.56% de recall y mitigar falsos negativos,
            # bajamos el umbral estándar de 0.50 a 0.35 para priorizar la detección temprana.
            umbral_sensible = 0.35
            clase_predicha = "MALIGNANT" if prob_maligno >= umbral_sensible else "BENIGN"
            
            score_final = prob_maligno
            birads_sugerido = self._map_to_birads(score_final)
            
            return {
                "status": "success",
                "prediction": clase_predicha,
                "confidence_scores": {
                    "benign": round(prob_benigno * 100, 2),
                    "malignant": round(prob_maligno * 100, 2)
                },
                "bi_rads_preliminary": birads_sugerido,
                "execution_device": str(self.device)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Fallo en el motor de inferencia analítica: {str(e)}"
            }

# Instanciar como Singleton para evitar recargar el modelo en cada petición HTTP
ia_engine = MedicalIAEngine()