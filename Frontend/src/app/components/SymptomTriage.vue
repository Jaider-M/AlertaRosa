<script setup lang="ts">
import { ref } from 'vue';
import { AlertTriangle, CheckCircle2, Send, Calendar } from 'lucide-vue-next';

interface Symptom {
  id: string;
  label: string;
  severity: 'low' | 'medium' | 'high';
}

const availableSymptoms: Symptom[] = [
  { id: 'lump', label: 'Bulto o masa en la mama', severity: 'high' },
  { id: 'pain', label: 'Dolor persistente en mama o axila', severity: 'medium' },
  { id: 'discharge', label: 'Secreción del pezón', severity: 'high' },
  { id: 'skinChanges', label: 'Cambios en la piel (hoyuelos, enrojecimiento)', severity: 'high' },
  { id: 'sizeChange', label: 'Cambio en tamaño o forma', severity: 'medium' },
  { id: 'nippleRetraction', label: 'Retracción del pezón', severity: 'high' },
  { id: 'swelling', label: 'Hinchazón en mama o axila', severity: 'medium' },
  { id: 'tenderness', label: 'Sensibilidad al tacto', severity: 'low' },
];

interface TriageResult {
  level: 'low' | 'medium' | 'high';
  message: string;
  action: string;
}

const selectedSymptoms = ref<string[]>([]);
const additionalInfo = ref('');
const result = ref<TriageResult | null>(null);

const handleSymptomToggle = (symptomId: string) => {
  if (selectedSymptoms.value.includes(symptomId)) {
    selectedSymptoms.value = selectedSymptoms.value.filter(s => s !== symptomId);
  } else {
    selectedSymptoms.value.push(symptomId);
  }
  result.value = null;
};

const handleSubmit = () => {
  if (selectedSymptoms.value.length === 0) {
    alert('Por favor seleccione al menos un síntoma');
    return;
  }

  const selectedSymptomsData = availableSymptoms.filter(s => selectedSymptoms.value.includes(s.id));
  const hasHighSeverity = selectedSymptomsData.some(s => s.severity === 'high');
  const hasMediumSeverity = selectedSymptomsData.some(s => s.severity === 'medium');
  const symptomCount = selectedSymptoms.value.length;

  let triageResult: TriageResult;

  if (hasHighSeverity || symptomCount >= 3) {
    triageResult = {
      level: 'high',
      message: 'Sus síntomas requieren atención médica inmediata',
      action: 'Por favor, contacte a su médico hoy mismo o acuda a urgencias. Los síntomas que ha reportado pueden requerir evaluación urgente.',
    };
  } else if (hasMediumSeverity || symptomCount >= 2) {
    triageResult = {
      level: 'medium',
      message: 'Se recomienda consulta médica en los próximos días',
      action: 'Programe una cita con su especialista dentro de esta semana. Mantenga seguimiento de sus síntomas.',
    };
  } else {
    triageResult = {
      level: 'low',
      message: 'Sus síntomas pueden ser monitoreados',
      action: 'Continúe con el autoexamen mensual y programe una consulta de rutina. Si los síntomas empeoran, contacte a su médico.',
    };
  }

  result.value = triageResult;

  const triageData = {
    date: new Date().toISOString(),
    symptoms: selectedSymptoms.value,
    additionalInfo: additionalInfo.value,
    result: triageResult,
  };

  const existingTriages = localStorage.getItem('patientTriages');
  const triages = existingTriages ? JSON.parse(existingTriages) : [];
  triages.unshift(triageData);
  localStorage.setItem('patientTriages', JSON.stringify(triages));
};

const handleReset = () => {
  selectedSymptoms.value = [];
  additionalInfo.value = '';
  result.value = null;
};
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-gradient-to-r from-orange-500 to-red-600 rounded-lg p-6 text-white">
      <div class="flex items-start gap-4">
        <div class="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center">
          <AlertTriangle class="w-6 h-6" />
        </div>
        <div>
          <h2 class="text-2xl font-semibold mb-2">Evaluación de Síntomas</h2>
          <p class="text-orange-100">Reporte sus síntomas para recibir orientación inmediata</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Symptom Selection -->
      <div class="bg-white border border-border rounded-lg p-6">
        <h3 class="font-semibold mb-4">Seleccione sus síntomas</h3>

        <div class="space-y-3 mb-6">
          <label
            v-for="symptom in availableSymptoms"
            :key="symptom.id"
            :class="`flex items-center gap-3 p-4 rounded-lg border cursor-pointer transition-all ${
              selectedSymptoms.includes(symptom.id) ? 'bg-orange-50 border-orange-300' : 'border-border hover:border-orange-200'
            }`"
          >
            <input
              type="checkbox"
              :checked="selectedSymptoms.includes(symptom.id)"
              @change="handleSymptomToggle(symptom.id)"
              class="w-4 h-4 rounded border-border text-orange-600 focus:ring-orange-500"
            />
            <div class="flex-1">
              <span class="text-sm">{{ symptom.label }}</span>
            </div>
            <span
              :class="`px-2 py-0.5 text-xs rounded-full ${
                symptom.severity === 'high' ? 'bg-red-100 text-red-700' :
                symptom.severity === 'medium' ? 'bg-orange-100 text-orange-700' : 'bg-yellow-100 text-yellow-700'
              }`"
            >
              {{ symptom.severity === 'high' ? 'Importante' : symptom.severity === 'medium' ? 'Moderado' : 'Leve' }}
            </span>
          </label>
        </div>

        <div class="mb-4">
          <label class="block text-sm mb-2">Información adicional (opcional)</label>
          <textarea
            v-model="additionalInfo"
            rows="4"
            class="w-full px-4 py-3 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-orange-500 resize-none"
            placeholder="Describa cualquier detalle adicional sobre sus síntomas..."
          ></textarea>
        </div>

        <div class="flex gap-3">
          <button
            @click="handleSubmit"
            :disabled="selectedSymptoms.length === 0"
            class="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-lg hover:from-orange-700 hover:to-red-700 transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send class="w-4 h-4" /> Evaluar Síntomas
          </button>
          <button
            v-if="result"
            @click="handleReset"
            class="px-4 py-3 border border-border rounded-lg hover:bg-muted/50 transition-colors"
          >
            Resetear
          </button>
        </div>
      </div>

      <!-- Result -->
      <div class="bg-white border border-border rounded-lg p-6">
        <h3 class="font-semibold mb-4">Resultado de la Evaluación</h3>

        <div v-if="!result" class="flex items-center justify-center h-full min-h-[400px]">
          <div class="text-center">
            <AlertTriangle class="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <p class="text-muted-foreground">Seleccione síntomas y presione "Evaluar Síntomas"</p>
          </div>
        </div>

        <div v-else class="space-y-6">
          <div
            :class="`p-6 rounded-lg border-2 ${
              result.level === 'high' ? 'bg-red-50 border-red-300' :
              result.level === 'medium' ? 'bg-orange-50 border-orange-300' : 'bg-yellow-50 border-yellow-300'
            }`"
          >
            <div class="flex items-start gap-3 mb-4">
              <AlertTriangle v-if="result.level === 'high'" class="w-6 h-6 text-red-600 flex-shrink-0" />
              <AlertTriangle v-else-if="result.level === 'medium'" class="w-6 h-6 text-orange-600 flex-shrink-0" />
              <CheckCircle2 v-else class="w-6 h-6 text-yellow-600 flex-shrink-0" />
              <div class="flex-1">
                <h4
                  :class="`font-semibold mb-2 ${
                    result.level === 'high' ? 'text-red-900' :
                    result.level === 'medium' ? 'text-orange-900' : 'text-yellow-900'
                  }`"
                >
                  {{ result.message }}
                </h4>
                <p
                  :class="`text-sm ${
                    result.level === 'high' ? 'text-red-800' :
                    result.level === 'medium' ? 'text-orange-800' : 'text-yellow-800'
                  }`"
                >
                  {{ result.action }}
                </p>
              </div>
            </div>
          </div>

          <div class="p-4 bg-muted/30 rounded-lg">
            <h5 class="font-medium mb-3">Síntomas reportados:</h5>
            <ul class="space-y-2">
              <li v-for="symptomId in selectedSymptoms" :key="symptomId" class="flex items-center gap-2 text-sm">
                <CheckCircle2 class="w-4 h-4 text-green-600" />
                {{ availableSymptoms.find(s => s.id === symptomId)?.label }}
              </li>
            </ul>
            <div v-if="additionalInfo" class="mt-4 pt-4 border-t border-border">
              <p class="text-sm font-medium mb-1">Información adicional:</p>
              <p class="text-sm text-muted-foreground">{{ additionalInfo }}</p>
            </div>
          </div>

          <div class="flex items-center gap-2 text-sm text-muted-foreground">
            <Calendar class="w-4 h-4" />
            <span>
              Evaluado el {{ new Date().toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' }) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Disclaimer -->
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <div class="flex items-start gap-3">
        <AlertTriangle class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div>
          <h4 class="font-medium text-blue-900 mb-2">Importante: Esta no es una consulta médica</h4>
          <p class="text-sm text-blue-800">
            Este sistema de triage proporciona orientación preliminar basada en sus síntomas reportados. No reemplaza una evaluación médica profesional. Si experimenta síntomas graves o tiene dudas, contacte a su médico inmediatamente o acuda a urgencias.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
