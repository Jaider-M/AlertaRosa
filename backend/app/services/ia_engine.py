import asyncio
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from monai.networks.nets import DenseNet121
from monai.transforms import Compose, EnsureChannelFirst, ScaleIntensity, Resize
from app.models.clinical import AIResult

class MedicalIAEngine:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DenseNet121(spatial_dims=2, in_channels=1, out_channels=2)
        app_root = Path(__file__).resolve().parent.parent
        self.weights_path = app_root / "core" / "weights" / "monai_mamografia_model.pth"
        
        if self.weights_path.exists():
            self.model.load_state_dict(torch.load(self.weights_path, map_location=self.device, weights_only=True))
            print(f" [AlertaRosa AI] ¡Éxito! Pesos de Kaggle cargados correctamente desde: {self.weights_path}")
        else:
            print(f" [AlertaRosa AI] ERROR CRÍTICO: No se encontró el archivo de pesos en {self.weights_path}")
            print(f"   Por favor, verifica que el archivo esté en: Backend/app/core/weights/monai_mamografia_model.pth")
            
        self.model.to(self.device)
        self.model.eval()

        self.preprocessing_transforms = Compose([
            EnsureChannelFirst(channel_dim="no_channel"),
            Resize(spatial_size=(256, 256)),
            ScaleIntensity()
        ])

    def _map_to_birads(self, risk_score: float) -> str:
        if risk_score < 0.15: return "BI-RADS 1: Negativo"
        elif risk_score < 0.35: return "BI-RADS 2: Hallazgos Benignos"
        elif risk_score < 0.60: return "BI-RADS 3: Probablemente Benigno"
        elif risk_score < 0.85: return "BI-RADS 4: Sospecha de Anomalía"
        else: return "BI-RADS 5: Altamente Sugestivo de Malignidad"

    async def analyze_image_local(self, file_path: str) -> AIResult:
        """
        Punto de entrada asíncrono que llama tu controlador.
        Ejecuta la IA en un hilo secundario para no congelar FastAPI.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._ejecutar_inferencia, file_path)

    def _ejecutar_inferencia(self, file_path: str) -> AIResult:
        try:
            # 1. Abre el archivo guardado en el disco
            pil_image = Image.open(file_path).convert("L")
            img_array = np.array(pil_image, dtype=np.float32)
            
            # 2. Preprocesa la imagen (256x256)
            img_tensor = self.preprocessing_transforms(img_array)
            img_tensor = img_tensor.unsqueeze(0).to(self.device)
            
            # 3. Inferencia matemática veloz
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilidades = torch.softmax(outputs, dim=1).cpu().numpy()[0]
                
            prob_maligno = float(probabilidades[1])
            birads_sugerido = self._map_to_birads(prob_maligno)
            
            # Devolvemos el modelo de datos exacto que el controlador guardará en Mongo
            return AIResult(
                ai_risk_score=round(prob_maligno, 4),
                birads_classification=birads_sugerido
            )
        except Exception as e:
            raise RuntimeError(f"Fallo en la inferencia médica: {str(e)}")

ia_engine = MedicalIAEngine()