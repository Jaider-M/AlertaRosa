<script setup lang="ts">
import { ref } from 'vue';
import { TrendingUp, TrendingDown, Users, Calendar, AlertCircle, CheckCircle } from 'lucide-vue-next';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Line, Doughnut } from 'vue-chartjs';

// Registrar los componentes de Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

// --- DATOS ESTÁTICOS ---
const colorClasses: Record<string, string> = {
  blue: 'from-blue-500 to-blue-600',
  green: 'from-green-500 to-green-600',
  orange: 'from-orange-500 to-orange-600',
  pink: 'from-pink-500 to-rose-600',
};

const metrics = ref([
  {
    title: 'Pacientes Activos',
    value: '247',
    change: '+12',
    trend: 'up',
    icon: Users,
    color: 'blue'
  },
  {
    title: 'Detecciones Tempranas',
    value: '89',
    change: '+8',
    trend: 'up',
    suffix: 'este mes',
    icon: CheckCircle,
    color: 'green'
  },
  {
    title: 'Citas Pendientes',
    value: '23',
    change: '-5',
    trend: 'down',
    suffix: 'hoy',
    icon: Calendar,
    color: 'orange'
  },
  {
    title: 'Tasa de Detección',
    value: '94%',
    change: '+2%',
    trend: 'up',
    suffix: 'precisión',
    icon: TrendingUp,
    color: 'pink'
  }
]);

const riskDistribution = ref([
  { name: 'Bajo Riesgo', value: 65, color: '#10b981' },
  { name: 'Riesgo Moderado', value: 25, color: '#f59e0b' },
  { name: 'Alto Riesgo', value: 10, color: '#ef4444' },
]);

const upcomingAppointments = ref([
  { patient: 'Ana Martínez', type: 'Seguimiento', time: '10:00 AM', priority: 'normal' },
  { patient: 'Laura Fernández', type: 'Diagnóstico', time: '11:30 AM', priority: 'high' },
  { patient: 'Carmen Ruiz', type: 'Resultado', time: '2:00 PM', priority: 'high' },
  { patient: 'Isabel Torres', type: 'Consulta', time: '3:30 PM', priority: 'normal' },
]);

// --- CONFIGURACIÓN DE GRÁFICOS ---
const lineChartData = {
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Casos Nuevos',
      backgroundColor: '#ec4899',
      borderColor: '#ec4899',
      data: [12, 15, 11, 18, 14, 20],
      tension: 0.3
    },
    {
      label: 'En Seguimiento',
      backgroundColor: '#3b82f6',
      borderColor: '#3b82f6',
      data: [45, 48, 52, 55, 58, 62],
      tension: 0.3
    }
  ]
};

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const
    }
  },
  scales: {
    y: {
      grid: {
        color: '#e5e7eb',
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
};

const doughnutChartData = {
  labels: riskDistribution.value.map(r => r.name),
  datasets: [
    {
      backgroundColor: riskDistribution.value.map(r => r.color),
      data: riskDistribution.value.map(r => r.value),
      cutout: '70%',
      borderWidth: 0
    }
  ]
};

const doughnutChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  }
};

// --- UTILIDADES ---
const getInitials = (name: string) => {
  return name.split(' ').map(n => n[0]).join('');
};
</script>

<template>
  <div class="space-y-6">
    <!-- Alert Banner -->
    <div class="bg-pink-50 border border-pink-200 rounded-lg p-4 flex items-start gap-3">
      <AlertCircle class="w-5 h-5 text-pink-600 flex-shrink-0 mt-0.5" />
      <div>
        <p class="font-medium text-pink-900">3 pacientes requieren atención prioritaria</p>
        <p class="text-sm text-pink-700 mt-1">
          Resultados de biopsias pendientes de revisión - Verificar antes de las 5:00 PM
        </p>
      </div>
    </div>

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div 
        v-for="(metric, index) in metrics" 
        :key="index"
        class="bg-white border border-border rounded-lg p-5 hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between mb-4">
          <p class="text-sm text-muted-foreground">{{ metric.title }}</p>
          <div :class="`w-8 h-8 rounded-lg bg-gradient-to-br ${colorClasses[metric.color]} flex items-center justify-center`">
            <component :is="metric.icon" class="w-4 h-4 text-white" />
          </div>
        </div>
        <div class="space-y-1">
          <p class="text-3xl font-semibold">{{ metric.value }}</p>
          <div class="flex items-center gap-2">
            <div :class="`flex items-center gap-1 text-sm ${metric.trend === 'up' ? 'text-green-600' : 'text-orange-600'}`">
              <TrendingUp v-if="metric.trend === 'up'" class="w-3 h-3" />
              <TrendingDown v-else class="w-3 h-3" />
              <span>{{ metric.change }}</span>
            </div>
            <span v-if="metric.suffix" class="text-xs text-muted-foreground">{{ metric.suffix }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Detection Trend -->
      <div class="lg:col-span-2 bg-white border border-border rounded-lg p-6">
        <div class="mb-6">
          <h3 class="font-semibold">Tendencia de Detección</h3>
          <p class="text-sm text-muted-foreground mt-1">Casos nuevos vs. pacientes en seguimiento</p>
        </div>
        <div class="h-[280px]">
          <Line :data="lineChartData" :options="lineChartOptions" />
        </div>
      </div>

      <!-- Risk Distribution -->
      <div class="bg-white border border-border rounded-lg p-6">
        <div class="mb-6">
          <h3 class="font-semibold">Distribución de Riesgo</h3>
          <p class="text-sm text-muted-foreground mt-1">Clasificación actual</p>
        </div>
        <div class="h-[200px] relative flex justify-center">
          <Doughnut :data="doughnutChartData" :options="doughnutChartOptions" />
        </div>
        <div class="mt-4 space-y-2">
          <div 
            v-for="item in riskDistribution" 
            :key="item.name" 
            class="flex items-center justify-between"
          >
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: item.color }" />
              <span class="text-sm">{{ item.name }}</span>
            </div>
            <span class="text-sm font-medium">{{ item.value }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Upcoming Appointments -->
    <div class="bg-white border border-border rounded-lg p-6">
      <div class="mb-4">
        <h3 class="font-semibold">Citas de Hoy</h3>
        <p class="text-sm text-muted-foreground mt-1">{{ upcomingAppointments.length }} citas programadas</p>
      </div>
      <div class="space-y-3">
        <div
          v-for="(appointment, index) in upcomingAppointments"
          :key="index"
          class="flex items-center justify-between p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-pink-100 to-purple-100 flex items-center justify-center">
              <span class="text-sm font-medium text-pink-700">
                {{ getInitials(appointment.patient) }}
              </span>
            </div>
            <div>
              <p class="font-medium">{{ appointment.patient }}</p>
              <p class="text-sm text-muted-foreground">{{ appointment.type }}</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-sm font-medium">{{ appointment.time }}</span>
            <span 
              v-if="appointment.priority === 'high'" 
              class="px-2 py-1 bg-red-100 text-red-700 text-xs rounded-full"
            >
              Prioritaria
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
