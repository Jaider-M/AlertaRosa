<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { FileText, Calendar, Activity, AlertCircle, Download, Eye, User, Heart, LogOut, BookOpen, Stethoscope, Bell } from 'lucide-vue-next';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
  CartesianScale
} from 'chart.js';
import { Line } from 'vue-chartjs';
import { useAuth } from '../composables/useAuth';
import Education from './Education.vue';
import SymptomTriage from './SymptomTriage.vue';
import logoImg from '../../imports/AlertaRosa.jpeg';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, ChartTooltip, Legend);

type Tab = 'history' | 'triage' | 'education' | 'alerts';

const { user, logout } = useAuth();
const activeTab = ref<Tab>('history');
const alerts = ref<any[]>([]);

const medicalHistory = [
  {
    date: '2026-04-08',
    type: 'Consulta',
    doctor: 'Dra. María González',
    diagnosis: 'Control de rutina',
    notes: 'Paciente en buen estado general. Se recomienda continuar con seguimiento semestral.',
  },
  {
    date: '2026-03-15',
    type: 'Mamografía',
    doctor: 'Dr. Carlos Ruiz',
    diagnosis: 'Resultado normal',
    notes: 'No se observan anomalías. Tejido mamario normal para la edad.',
  },
  {
    date: '2025-10-20',
    type: 'Consulta',
    doctor: 'Dra. María González',
    diagnosis: 'Evaluación inicial',
    notes: 'Primera consulta. Sin antecedentes familiares. Se programa mamografía de control.',
  },
];

const selectedHistory = ref(medicalHistory[0]);

const appointments = [
  {
    date: '2026-04-15',
    time: '10:00 AM',
    type: 'Seguimiento',
    doctor: 'Dra. María González',
    status: 'confirmed',
  },
  {
    date: '2026-10-15',
    time: '11:30 AM',
    type: 'Mamografía',
    doctor: 'Dr. Carlos Ruiz',
    status: 'pending',
  },
];

const testResults = [
  {
    date: '2026-03-15',
    test: 'Mamografía Digital',
    result: 'Normal',
    file: 'mamografia_2026_03.pdf',
  },
  {
    date: '2025-09-20',
    test: 'Ecografía Mamaria',
    result: 'Normal',
    file: 'ecografia_2025_09.pdf',
  },
  {
    date: '2025-03-10',
    test: 'Análisis de Sangre',
    result: 'Normal',
    file: 'analisis_2025_03.pdf',
  },
];

const riskTrendData = [
  { month: 'Ene 2025', nivel: 15 },
  { month: 'Abr 2025', nivel: 14 },
  { month: 'Jul 2025', nivel: 15 },
  { month: 'Oct 2025', nivel: 13 },
  { month: 'Ene 2026', nivel: 12 },
  { month: 'Abr 2026', nivel: 12 },
];

onMounted(() => {
  const storedAlerts = localStorage.getItem('patientAlerts');
  if (storedAlerts) {
    const allAlerts = JSON.parse(storedAlerts);
    const userAlerts = allAlerts.filter((a: any) => a.patientId === user.value?.id);
    alerts.value = userAlerts;
  }
});

const tabs = computed(() => [
  { id: 'history' as Tab, label: 'Mi Historia', icon: FileText },
  { id: 'triage' as Tab, label: 'Evaluación Síntomas', icon: Stethoscope },
  { id: 'education' as Tab, label: 'Educación', icon: BookOpen },
  { id: 'alerts' as Tab, label: 'Alertas', icon: Bell, badge: alerts.value.length },
]);

// --- CONFIGURACIÓN DEL GRÁFICO (Chart.js) ---
const chartData = {
  labels: riskTrendData.map(d => d.month),
  datasets: [
    {
      label: 'Nivel de Riesgo (%)',
      data: riskTrendData.map(d => d.nivel),
      borderColor: '#10b981',
      backgroundColor: '#10b981',
      tension: 0.3,
      pointRadius: 4,
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#ffffff',
      titleColor: '#000',
      bodyColor: '#000',
      borderColor: '#e5e7eb',
      borderWidth: 1,
    }
  },
  scales: {
    y: {
      min: 0,
      max: 30,
      grid: { color: '#e5e7eb' },
    },
    x: {
      grid: { display: false },
    }
  }
};

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
};

const formatShortDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
};
</script>

<template>
  <div class="min-h-screen bg-background">
    <!-- Top Header -->
    <header class="border-b border-border bg-white sticky top-0 z-50">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <img :src="logoImg" alt="AlertaRosa" class="h-12 w-auto" />
            <div>
              <h1 class="text-xl font-semibold">AlertaRosa</h1>
              <p class="text-xs text-muted-foreground">Detección temprana, vida salvada</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right">
              <p class="text-sm font-medium">{{ user?.name }}</p>
              <p class="text-xs text-muted-foreground">Paciente</p>
            </div>
            <button @click="logout" class="p-2 hover:bg-muted rounded-lg transition-colors" title="Cerrar sesión">
              <LogOut class="w-5 h-5 text-muted-foreground" />
            </button>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="px-6 flex gap-1 border-t border-border">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="relative px-4 py-3 text-sm font-medium transition-colors hover:text-foreground"
          :style="{ color: activeTab === tab.id ? 'var(--foreground)' : 'var(--muted-foreground)' }"
        >
          <div class="flex items-center gap-2">
            <component :is="tab.icon" class="w-4 h-4" />
            {{ tab.label }}
            <span v-if="tab.badge && tab.badge > 0" class="ml-1 px-1.5 py-0.5 bg-red-500 text-white text-xs rounded-full">
              {{ tab.badge }}
            </span>
          </div>
          <div v-if="activeTab === tab.id" class="absolute bottom-0 left-0 right-0 h-0.5 bg-pink-500"></div>
        </button>
      </nav>
    </header>

    <main class="p-6">
      <transition name="fade" mode="out-in">
        <div :key="activeTab">
          <div v-if="activeTab === 'history'" class="space-y-6">
            <!-- Welcome Header -->
            <div class="bg-gradient-to-r from-pink-500 to-rose-600 rounded-lg p-6 text-white">
              <div class="flex items-start justify-between">
                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center">
                    <User class="w-6 h-6" />
                  </div>
                  <div>
                    <h2 class="text-2xl font-semibold mb-2">Mi Historia Clínica</h2>
                    <p class="text-pink-100">Bienvenido/a, {{ user?.name }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-sm text-pink-100">ID de Paciente</p>
                  <p class="font-medium">{{ user?.id }}</p>
                </div>
              </div>
            </div>

            <!-- Quick Stats -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div class="bg-white border border-border rounded-lg p-5">
                <div class="flex items-center justify-between mb-2">
                  <p class="text-sm text-muted-foreground">Nivel de Riesgo</p>
                  <Heart class="w-5 h-5 text-green-600" />
                </div>
                <p class="text-2xl font-semibold text-green-600">Bajo</p>
                <p class="text-xs text-muted-foreground mt-1">12% evaluación actual</p>
              </div>

              <div class="bg-white border border-border rounded-lg p-5">
                <div class="flex items-center justify-between mb-2">
                  <p class="text-sm text-muted-foreground">Próxima Cita</p>
                  <Calendar class="w-5 h-5 text-blue-600" />
                </div>
                <p class="text-2xl font-semibold">15 Abr</p>
                <p class="text-xs text-muted-foreground mt-1">Seguimiento rutinario</p>
              </div>

              <div class="bg-white border border-border rounded-lg p-5">
                <div class="flex items-center justify-between mb-2">
                  <p class="text-sm text-muted-foreground">Consultas</p>
                  <Activity class="w-5 h-5 text-purple-600" />
                </div>
                <p class="text-2xl font-semibold">3</p>
                <p class="text-xs text-muted-foreground mt-1">Último año</p>
              </div>

              <div class="bg-white border border-border rounded-lg p-5">
                <div class="flex items-center justify-between mb-2">
                  <p class="text-sm text-muted-foreground">Resultados</p>
                  <FileText class="w-5 h-5 text-orange-600" />
                </div>
                <p class="text-2xl font-semibold">3</p>
                <p class="text-xs text-muted-foreground mt-1">Disponibles</p>
              </div>
            </div>

            <!-- Risk Trend -->
            <div class="bg-white border border-border rounded-lg p-6">
              <div class="mb-6">
                <h3 class="font-semibold">Evolución del Nivel de Riesgo</h3>
                <p class="text-sm text-muted-foreground mt-1">Tendencia de tu evaluación de riesgo en el tiempo</p>
              </div>
              <div class="h-[200px]">
                <Line :data="chartData" :options="chartOptions" />
              </div>
              <div class="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                <p class="text-sm text-green-800">
                  <strong>Excelente:</strong> Tu nivel de riesgo se mantiene estable y bajo. Continúa con tus controles regulares.
                </p>
              </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <!-- Medical History -->
              <div class="bg-white border border-border rounded-lg p-6">
                <h3 class="font-semibold mb-4">Historial Médico</h3>
                <div class="space-y-3 mb-6">
                  <button
                    v-for="(record, index) in medicalHistory"
                    :key="index"
                    @click="selectedHistory = record"
                    :class="`w-full text-left p-4 rounded-lg border transition-all ${
                      selectedHistory === record ? 'bg-pink-50 border-pink-300' : 'border-border hover:border-pink-200'
                    }`"
                  >
                    <div class="flex items-start justify-between mb-2">
                      <div>
                        <p class="font-medium">{{ record.type }}</p>
                        <p class="text-xs text-muted-foreground">{{ formatDate(record.date) }}</p>
                      </div>
                      <Eye class="w-4 h-4 text-muted-foreground" />
                    </div>
                    <p class="text-xs text-muted-foreground">{{ record.doctor }}</p>
                  </button>
                </div>

                <div class="p-4 bg-muted/30 rounded-lg">
                  <h4 class="font-medium mb-2">Detalles de la Consulta</h4>
                  <div class="space-y-2 text-sm">
                    <div>
                      <p class="text-muted-foreground">Diagnóstico</p>
                      <p class="font-medium">{{ selectedHistory.diagnosis }}</p>
                    </div>
                    <div>
                      <p class="text-muted-foreground">Notas</p>
                      <p>{{ selectedHistory.notes }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Test Results -->
              <div class="bg-white border border-border rounded-lg p-6">
                <h3 class="font-semibold mb-4">Resultados de Pruebas</h3>
                <div class="space-y-3">
                  <div
                    v-for="(test, index) in testResults"
                    :key="index"
                    class="flex items-center justify-between p-4 border border-border rounded-lg hover:border-pink-300 hover:bg-pink-50/50 transition-all"
                  >
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-pink-100 to-purple-100 flex items-center justify-center">
                        <FileText class="w-5 h-5 text-pink-600" />
                      </div>
                      <div>
                        <p class="font-medium text-sm">{{ test.test }}</p>
                        <p class="text-xs text-muted-foreground">{{ formatShortDate(test.date) }}</p>
                      </div>
                    </div>
                    <div class="flex items-center gap-3">
                      <span class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                        {{ test.result }}
                      </span>
                      <button class="p-2 hover:bg-muted rounded-lg transition-colors">
                        <Download class="w-4 h-4 text-muted-foreground" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Upcoming Appointments -->
            <div class="bg-white border border-border rounded-lg p-6">
              <h3 class="font-semibold mb-4">Próximas Citas</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div
                  v-for="(appointment, index) in appointments"
                  :key="index"
                  class="p-4 border border-border rounded-lg hover:border-pink-300 hover:bg-pink-50/50 transition-all"
                >
                  <div class="flex items-start justify-between mb-3">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center">
                        <Calendar class="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <p class="font-medium">{{ appointment.type }}</p>
                        <p class="text-sm text-muted-foreground">{{ appointment.doctor }}</p>
                      </div>
                    </div>
                    <span
                      :class="`px-2 py-1 text-xs rounded-full ${
                        appointment.status === 'confirmed' ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'
                      }`"
                    >
                      {{ appointment.status === 'confirmed' ? 'Confirmada' : 'Pendiente' }}
                    </span>
                  </div>
                  <div class="flex items-center gap-4 text-sm">
                    <span class="text-muted-foreground">{{ formatDate(appointment.date) }}</span>
                    <span class="font-medium">{{ appointment.time }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Important Info -->
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <div class="flex items-start gap-3">
                <AlertCircle class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 class="font-medium text-blue-900 mb-2">Recordatorios Importantes</h4>
                  <ul class="space-y-1 text-sm text-blue-800">
                    <li>• Realizar autoexamen mamario mensual</li>
                    <li>• Mantener un estilo de vida saludable</li>
                    <li>• Asistir a todas las citas programadas</li>
                    <li>• Contactar a tu médico si notas cualquier cambio inusual</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <SymptomTriage v-else-if="activeTab === 'triage'" />
          <Education v-else-if="activeTab === 'education'" />
          
          <div v-else-if="activeTab === 'alerts'" class="space-y-6">
            <div class="bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg p-6 text-white">
              <div class="flex items-start gap-4">
                <div class="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center">
                  <Bell class="w-6 h-6" />
                </div>
                <div>
                  <h2 class="text-2xl font-semibold mb-2">Mis Alertas</h2>
                  <p class="text-purple-100">Mensajes y notificaciones de tu equipo médico</p>
                </div>
              </div>
            </div>

            <div v-if="alerts.length === 0" class="bg-white border border-border rounded-lg p-12 text-center">
              <Bell class="w-16 h-16 text-muted-foreground mx-auto mb-4" />
              <p class="text-muted-foreground">No tienes alertas pendientes</p>
            </div>
            
            <div v-else class="space-y-3">
              <div
                v-for="alert in alerts"
                :key="alert.id"
                :class="`bg-white border rounded-lg p-6 ${
                  alert.priority === 'high' ? 'border-red-300 bg-red-50' :
                  alert.priority === 'medium' ? 'border-orange-300 bg-orange-50' : 'border-border'
                }`"
              >
                <div class="flex items-start justify-between mb-3">
                  <div class="flex items-center gap-3">
                    <AlertCircle
                      :class="`w-5 h-5 ${
                        alert.priority === 'high' ? 'text-red-600' :
                        alert.priority === 'medium' ? 'text-orange-600' : 'text-blue-600'
                      }`"
                    />
                    <span
                      :class="`px-2 py-1 text-xs rounded-full ${
                        alert.priority === 'high' ? 'bg-red-100 text-red-700' :
                        alert.priority === 'medium' ? 'bg-orange-100 text-orange-700' : 'bg-blue-100 text-blue-700'
                      }`"
                    >
                      {{ alert.priority === 'high' ? 'Urgente' : alert.priority === 'medium' ? 'Importante' : 'Normal' }}
                    </span>
                  </div>
                  <span class="text-xs text-muted-foreground">{{ formatShortDate(alert.date) }}</span>
                </div>
                <p class="text-sm">{{ alert.message }}</p>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </main>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
