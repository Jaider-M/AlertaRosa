<script setup lang="ts">
import { ref } from 'vue';
import { TrendingUp, Calendar, Users, Target } from 'lucide-vue-next';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line, Bar } from 'vue-chartjs';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const monthlyDetections = [
  { month: 'Ene', detecciones: 12, seguimientos: 45, tasaExito: 92 },
  { month: 'Feb', detecciones: 15, seguimientos: 48, tasaExito: 94 },
  { month: 'Mar', detecciones: 11, seguimientos: 52, tasaExito: 91 },
  { month: 'Abr', detecciones: 18, seguimientos: 55, tasaExito: 95 },
  { month: 'May', detecciones: 14, seguimientos: 58, tasaExito: 93 },
  { month: 'Jun', detecciones: 20, seguimientos: 62, tasaExito: 96 },
];

const ageDistribution = [
  { range: '20-30', casos: 5 },
  { range: '31-40', casos: 18 },
  { range: '41-50', casos: 42 },
  { range: '51-60', casos: 35 },
  { range: '61-70', casos: 22 },
  { range: '71+', casos: 8 },
];

const detectionStages = [
  { stage: 'Estadio 0', casos: 28, porcentaje: 21.5 },
  { stage: 'Estadio I', casos: 45, porcentaje: 34.6 },
  { stage: 'Estadio II', casos: 38, porcentaje: 29.2 },
  { stage: 'Estadio III', casos: 15, porcentaje: 11.5 },
  { stage: 'Estadio IV', casos: 4, porcentaje: 3.1 },
];

const treatmentOutcomes = [
  { mes: 'Ene', remision: 85, mejoria: 10, estable: 5 },
  { mes: 'Feb', remision: 88, mejoria: 8, estable: 4 },
  { mes: 'Mar', remision: 90, mejoria: 7, estable: 3 },
  { mes: 'Abr', remision: 87, mejoria: 9, estable: 4 },
  { mes: 'May', remision: 91, mejoria: 6, estable: 3 },
  { mes: 'Jun', remision: 94, mejoria: 4, estable: 2 },
];

// --- CHARTS DATA & OPTIONS ---

const detectionTrendsData = {
  labels: monthlyDetections.map(d => d.month),
  datasets: [
    {
      label: 'Detecciones',
      data: monthlyDetections.map(d => d.detecciones),
      borderColor: '#ec4899',
      backgroundColor: 'rgba(236, 72, 153, 0.2)',
      fill: true,
      tension: 0.3,
    },
    {
      label: 'Seguimientos',
      data: monthlyDetections.map(d => d.seguimientos),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.2)',
      fill: true,
      tension: 0.3,
    }
  ]
};

const barChartData = {
  labels: ageDistribution.map(d => d.range),
  datasets: [
    {
      label: 'Casos',
      data: ageDistribution.map(d => d.casos),
      backgroundColor: '#8b5cf6',
      borderRadius: 8,
    }
  ]
};

const treatmentOutcomesData = {
  labels: treatmentOutcomes.map(d => d.mes),
  datasets: [
    {
      label: 'Remisión',
      data: treatmentOutcomes.map(d => d.remision),
      borderColor: '#10b981',
      backgroundColor: '#10b981',
      tension: 0.3,
    },
    {
      label: 'Mejoría',
      data: treatmentOutcomes.map(d => d.mejoria),
      borderColor: '#3b82f6',
      backgroundColor: '#3b82f6',
      tension: 0.3,
    },
    {
      label: 'Estable',
      data: treatmentOutcomes.map(d => d.estable),
      borderColor: '#f59e0b',
      backgroundColor: '#f59e0b',
      tension: 0.3,
    }
  ]
};

const successRateData = {
  labels: monthlyDetections.map(d => d.month),
  datasets: [
    {
      label: 'Tasa de Éxito (%)',
      data: monthlyDetections.map(d => d.tasaExito),
      borderColor: '#ec4899',
      backgroundColor: 'rgba(236, 72, 153, 0.3)',
      fill: true,
      tension: 0.3,
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom' as const }
  },
  scales: {
    y: { grid: { color: '#e5e7eb' } },
    x: { grid: { display: false } }
  }
};

const successRateOptions = {
  ...chartOptions,
  scales: {
    ...chartOptions.scales,
    y: { min: 85, max: 100, grid: { color: '#e5e7eb' } }
  }
};

const summaries = [
  { title: "Detecciones Totales", value: "130", subtitle: "últimos 6 meses", trend: "+18%", icon: Target, color: "pink" },
  { title: "Tasa de Éxito", value: "94%", subtitle: "diagnóstico temprano", trend: "+3%", icon: TrendingUp, color: "green" },
  { title: "Pacientes Activos", value: "247", subtitle: "en seguimiento", trend: "+12", icon: Users, color: "blue" },
  { title: "Promedio Detección", value: "16.7", subtitle: "casos por mes", trend: "+2.3", icon: Calendar, color: "purple" }
];

const colorClasses: Record<string, string> = {
  pink: 'from-pink-500 to-rose-600',
  green: 'from-green-500 to-emerald-600',
  blue: 'from-blue-500 to-indigo-600',
  purple: 'from-purple-500 to-violet-600',
};

const stageColors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#dc2626'];
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg p-6 text-white">
      <h2 class="text-2xl font-semibold mb-2">Analíticas y Estadísticas</h2>
      <p class="text-purple-100">
        Visualización completa de métricas, tendencias y resultados clínicos
      </p>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="summary in summaries" :key="summary.title" class="bg-white border border-border rounded-lg p-5 hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between mb-4">
          <p class="text-sm text-muted-foreground">{{ summary.title }}</p>
          <div :class="`w-8 h-8 rounded-lg bg-gradient-to-br ${colorClasses[summary.color]} flex items-center justify-center`">
            <component :is="summary.icon" class="w-4 h-4 text-white" />
          </div>
        </div>
        <div class="space-y-1">
          <p class="text-3xl font-semibold">{{ summary.value }}</p>
          <div class="flex items-center gap-2">
            <span class="text-sm text-green-600 font-medium">{{ summary.trend }}</span>
            <span class="text-xs text-muted-foreground">{{ summary.subtitle }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Detection Trends -->
      <div class="bg-white border border-border rounded-lg p-6">
        <div class="mb-6">
          <h3 class="font-semibold">Tendencia de Detecciones</h3>
          <p class="text-sm text-muted-foreground mt-1">Casos nuevos y seguimientos mensuales</p>
        </div>
        <div class="h-[300px]">
          <Line :data="detectionTrendsData" :options="chartOptions" />
        </div>
      </div>

      <!-- Age Distribution -->
      <div class="bg-white border border-border rounded-lg p-6">
        <div class="mb-6">
          <h3 class="font-semibold">Distribución por Edad</h3>
          <p class="text-sm text-muted-foreground mt-1">Casos detectados por rango etario</p>
        </div>
        <div class="h-[300px]">
          <Bar :data="barChartData" :options="chartOptions" />
        </div>
      </div>
    </div>

    <!-- Detection Stages & Treatment Outcomes -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Detection Stages -->
      <div class="bg-white border border-border rounded-lg p-6">
        <div class="mb-6">
          <h3 class="font-semibold">Detección por Estadio</h3>
          <p class="text-sm text-muted-foreground mt-1">Distribución de casos según etapa de diagnóstico</p>
        </div>
        <div class="space-y-4">
          <div v-for="(stage, index) in detectionStages" :key="stage.stage">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium">{{ stage.stage }}</span>
              <div class="flex items-center gap-3">
                <span class="text-sm text-muted-foreground">{{ stage.casos }} casos</span>
                <span class="text-sm font-medium">{{ stage.porcentaje }}%</span>
              </div>
            </div>
            <div class="w-full h-2 bg-muted rounded-full overflow-hidden">
              <div
                class="h-full rounded-full transition-all"
                :style="`width: ${stage.porcentaje * 1.5}%; background-color: ${stageColors[index]}`"
              ></div>
            </div>
          </div>
        </div>
        <div class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p class="text-sm text-green-800">
            <span class="font-medium">56.1%</span> de los casos detectados en estadios tempranos (0-I)
          </p>
        </div>
      </div>

      <!-- Treatment Outcomes -->
      <div class="bg-white border border-border rounded-lg p-6">
        <div class="mb-6">
          <h3 class="font-semibold">Resultados de Tratamiento</h3>
          <p class="text-sm text-muted-foreground mt-1">Evolución de pacientes bajo tratamiento</p>
        </div>
        <div class="h-[300px]">
          <Line :data="treatmentOutcomesData" :options="chartOptions" />
        </div>
      </div>
    </div>

    <!-- Success Rate Trend -->
    <div class="bg-white border border-border rounded-lg p-6">
      <div class="mb-6">
        <h3 class="font-semibold">Tasa de Éxito en Diagnóstico Temprano</h3>
        <p class="text-sm text-muted-foreground mt-1">Porcentaje de detecciones correctas confirmadas</p>
      </div>
      <div class="h-[250px]">
        <Line :data="successRateData" :options="successRateOptions" />
      </div>
    </div>
  </div>
</template>
