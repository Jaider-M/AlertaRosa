<script setup lang="ts">
import { ref, computed } from 'vue';
import { Brain, Upload, Image as ImageIcon, FileText, AlertCircle, CheckCircle2, Activity, Zap } from 'lucide-vue-next';

interface RiskFactor {
  id: string;
  label: string;
  checked: boolean;
}

interface DiagnosticTest {
  name: string;
  accuracy: string;
  time: string;
  status: 'available' | 'scheduled' | 'pending';
  icon: any;
}

const riskFactorsData: RiskFactor[] = [
  { id: 'age', label: 'Edad > 40 años', checked: false },
  { id: 'family', label: 'Historial familiar', checked: false },
  { id: 'genetic', label: 'Mutación genética (BRCA1/BRCA2)', checked: false },
  { id: 'density', label: 'Tejido mamario denso', checked: false },
  { id: 'hormonal', label: 'Terapia hormonal prolongada', checked: false },
  { id: 'lifestyle', label: 'Factores de estilo de vida', checked: false },
];

const diagnosticTests: DiagnosticTest[] = [
  { name: 'Mamografía Digital', accuracy: '95%', time: '15-20 min', status: 'available', icon: ImageIcon },
  { name: 'Ecografía Mamaria', accuracy: '88%', time: '20-30 min', status: 'available', icon: Activity },
  { name: 'Resonancia Magnética', accuracy: '97%', time: '30-45 min', status: 'scheduled', icon: Brain },
  { name: 'Biopsia Guiada', accuracy: '99%', time: '45-60 min', status: 'pending', icon: Zap },
];

const selectedFactors = ref<string[]>([]);
const uploadedImage = ref(false);
const riskLevel = ref<'low' | 'medium' | 'high' | null>(null);

const handleFactorToggle = (id: string) => {
  if (selectedFactors.value.includes(id)) {
    selectedFactors.value = selectedFactors.value.filter(f => f !== id);
  } else {
    selectedFactors.value.push(id);
  }
};

const calculateRisk = () => {
  const count = selectedFactors.value.length;
  if (count === 0) riskLevel.value = 'low';
  else if (count <= 2) riskLevel.value = 'medium';
  else riskLevel.value = 'high';
};
</script>

<template>
  <div class="max-w-6xl space-y-6">
    <!-- Header -->
    <div class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg p-6 text-white">
      <div class="flex items-start gap-4">
        <div class="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center flex-shrink-0">
          <Brain class="w-6 h-6" />
        </div>
        <div class="flex-1">
          <h2 class="text-2xl font-semibold mb-2">Diagnóstico Temprano Inteligente</h2>
          <p class="text-pink-50">
            Sistema de análisis avanzado para la detección precoz de cáncer de mama mediante IA y evaluación de factores de riesgo
          </p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Image Upload Section -->
      <div class="bg-white border border-border rounded-lg p-6">
        <h3 class="font-semibold mb-4">Análisis de Imagen Médica</h3>

        <div class="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-pink-300 hover:bg-pink-50/50 transition-all cursor-pointer">
          <div v-if="!uploadedImage" class="space-y-4">
            <div class="w-16 h-16 rounded-full bg-pink-100 flex items-center justify-center mx-auto">
              <Upload class="w-8 h-8 text-pink-600" />
            </div>
            <div>
              <p class="font-medium mb-1">Subir imagen de mamografía o ecografía</p>
              <p class="text-sm text-muted-foreground">
                Formatos soportados: DICOM, JPG, PNG (máx. 50MB)
              </p>
            </div>
            <button
              @click="uploadedImage = true"
              class="px-4 py-2 bg-pink-600 text-white rounded-lg hover:bg-pink-700 transition-colors"
            >
              Seleccionar Archivo
            </button>
          </div>
          <div v-else class="space-y-4">
            <div class="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto">
              <CheckCircle2 class="w-8 h-8 text-green-600" />
            </div>
            <div>
              <p class="font-medium text-green-700 mb-1">Imagen cargada exitosamente</p>
              <p class="text-sm text-muted-foreground">mamografia_paciente_001.dcm</p>
            </div>
            <button
              @click="uploadedImage = false"
              class="text-sm text-pink-600 hover:underline"
            >
              Cambiar imagen
            </button>
          </div>
        </div>

        <div v-if="uploadedImage" class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div class="flex items-start gap-3">
            <Activity class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div class="w-full">
              <p class="text-sm font-medium text-blue-900 mb-1">Análisis en Progreso</p>
              <p class="text-xs text-blue-700">
                El sistema de IA está procesando la imagen. Tiempo estimado: 2-3 minutos
              </p>
              <div class="mt-3 w-full h-1.5 bg-blue-200 rounded-full overflow-hidden">
                <div class="h-full bg-blue-600 rounded-full animate-pulse" style="width: 60%"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 space-y-2 text-sm text-muted-foreground">
          <p class="flex items-center gap-2">
            <CheckCircle2 class="w-4 h-4 text-green-600" />
            Detección automática de anomalías
          </p>
          <p class="flex items-center gap-2">
            <CheckCircle2 class="w-4 h-4 text-green-600" />
            Comparación con base de datos de patrones
          </p>
          <p class="flex items-center gap-2">
            <CheckCircle2 class="w-4 h-4 text-green-600" />
            Recomendaciones basadas en IA
          </p>
        </div>
      </div>

      <!-- Risk Assessment -->
      <div class="bg-white border border-border rounded-lg p-6">
        <h3 class="font-semibold mb-4">Evaluación de Factores de Riesgo</h3>

        <div class="space-y-3 mb-6">
          <label
            v-for="factor in riskFactorsData"
            :key="factor.id"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-muted/30 cursor-pointer transition-colors"
          >
            <input
              type="checkbox"
              :checked="selectedFactors.includes(factor.id)"
              @change="handleFactorToggle(factor.id)"
              class="w-4 h-4 rounded border-border text-pink-600 focus:ring-pink-500"
            />
            <span class="text-sm">{{ factor.label }}</span>
          </label>
        </div>

        <button
          @click="calculateRisk"
          :disabled="selectedFactors.length === 0 && !uploadedImage"
          class="w-full px-4 py-2.5 bg-gradient-to-r from-pink-600 to-purple-600 text-white rounded-lg hover:from-pink-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Calcular Nivel de Riesgo
        </button>

        <div v-if="riskLevel" :class="`mt-4 p-4 rounded-lg border ${
          riskLevel === 'low' ? 'bg-green-50 border-green-200' :
          riskLevel === 'medium' ? 'bg-orange-50 border-orange-200' :
          'bg-red-50 border-red-200'
        }`">
          <div class="flex items-start gap-3">
            <AlertCircle :class="`w-5 h-5 flex-shrink-0 mt-0.5 ${
              riskLevel === 'low' ? 'text-green-600' :
              riskLevel === 'medium' ? 'text-orange-600' :
              'text-red-600'
            }`" />
            <div>
              <p :class="`font-medium mb-1 ${
                riskLevel === 'low' ? 'text-green-900' :
                riskLevel === 'medium' ? 'text-orange-900' :
                'text-red-900'
              }`">
                Nivel de Riesgo: {{
                  riskLevel === 'low' ? 'Bajo' :
                  riskLevel === 'medium' ? 'Moderado' :
                  'Alto'
                }}
              </p>
              <p :class="`text-sm ${
                riskLevel === 'low' ? 'text-green-700' :
                riskLevel === 'medium' ? 'text-orange-700' :
                'text-red-700'
              }`">
                {{ riskLevel === 'low' ? 'Se recomienda seguimiento anual de rutina' : '' }}
                {{ riskLevel === 'medium' ? 'Se recomienda seguimiento semestral y consulta especializada' : '' }}
                {{ riskLevel === 'high' ? 'Se requiere evaluación inmediata y estudios complementarios' : '' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Diagnostic Tests -->
    <div class="bg-white border border-border rounded-lg p-6">
      <h3 class="font-semibold mb-4">Pruebas Diagnósticas Disponibles</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="test in diagnosticTests" :key="test.name" class="p-4 border border-border rounded-lg hover:shadow-md transition-shadow">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-pink-100 to-purple-100 flex items-center justify-center">
              <component :is="test.icon" class="w-5 h-5 text-pink-600" />
            </div>
            <div class="flex-1">
              <p class="font-medium text-sm">{{ test.name }}</p>
            </div>
          </div>
          <div class="space-y-2 text-xs text-muted-foreground">
            <p>Precisión: <span class="font-medium text-foreground">{{ test.accuracy }}</span></p>
            <p>Duración: <span class="font-medium text-foreground">{{ test.time }}</span></p>
            <span :class="`inline-block px-2 py-1 rounded-full text-xs ${
              test.status === 'available' ? 'bg-green-100 text-green-700' :
              test.status === 'scheduled' ? 'bg-blue-100 text-blue-700' :
              'bg-orange-100 text-orange-700'
            }`">
              {{ test.status === 'available' ? 'Disponible' :
                 test.status === 'scheduled' ? 'Programada' : 'Pendiente' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
