import { BarChart, Bar, LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { TrendingUp, Calendar, Users, Target } from 'lucide-react';

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

export function Analytics() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg p-6 text-white">
        <h2 className="text-2xl font-semibold mb-2">Analíticas y Estadísticas</h2>
        <p className="text-purple-100">
          Visualización completa de métricas, tendencias y resultados clínicos
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <SummaryCard
          title="Detecciones Totales"
          value="130"
          subtitle="últimos 6 meses"
          trend="+18%"
          icon={Target}
          color="pink"
        />
        <SummaryCard
          title="Tasa de Éxito"
          value="94%"
          subtitle="diagnóstico temprano"
          trend="+3%"
          icon={TrendingUp}
          color="green"
        />
        <SummaryCard
          title="Pacientes Activos"
          value="247"
          subtitle="en seguimiento"
          trend="+12"
          icon={Users}
          color="blue"
        />
        <SummaryCard
          title="Promedio Detección"
          value="16.7"
          subtitle="casos por mes"
          trend="+2.3"
          icon={Calendar}
          color="purple"
        />
      </div>

      {/* Main Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Detection Trends */}
        <div className="bg-white border border-border rounded-lg p-6">
          <div className="mb-6">
            <h3 className="font-semibold">Tendencia de Detecciones</h3>
            <p className="text-sm text-muted-foreground mt-1">Casos nuevos y seguimientos mensuales</p>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={monthlyDetections}>
              <defs>
                <linearGradient id="colorDetecciones" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ec4899" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#ec4899" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorSeguimientos" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'var(--card)',
                  border: '1px solid var(--border)',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="detecciones"
                stroke="#ec4899"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorDetecciones)"
                name="Detecciones"
              />
              <Area
                type="monotone"
                dataKey="seguimientos"
                stroke="#3b82f6"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorSeguimientos)"
                name="Seguimientos"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Age Distribution */}
        <div className="bg-white border border-border rounded-lg p-6">
          <div className="mb-6">
            <h3 className="font-semibold">Distribución por Edad</h3>
            <p className="text-sm text-muted-foreground mt-1">Casos detectados por rango etario</p>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ageDistribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="range" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'var(--card)',
                  border: '1px solid var(--border)',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="casos" fill="#8b5cf6" radius={[8, 8, 0, 0]} name="Casos" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detection Stages & Treatment Outcomes */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Detection Stages */}
        <div className="bg-white border border-border rounded-lg p-6">
          <div className="mb-6">
            <h3 className="font-semibold">Detección por Estadio</h3>
            <p className="text-sm text-muted-foreground mt-1">Distribución de casos según etapa de diagnóstico</p>
          </div>
          <div className="space-y-4">
            {detectionStages.map((stage, index) => (
              <div key={stage.stage}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">{stage.stage}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-muted-foreground">{stage.casos} casos</span>
                    <span className="text-sm font-medium">{stage.porcentaje}%</span>
                  </div>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all"
                    style={{
                      width: `${stage.porcentaje * 1.5}%`,
                      backgroundColor: index === 0 ? '#10b981' : index === 1 ? '#3b82f6' : index === 2 ? '#f59e0b' : index === 3 ? '#ef4444' : '#dc2626'
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-green-800">
              <span className="font-medium">56.1%</span> de los casos detectados en estadios tempranos (0-I)
            </p>
          </div>
        </div>

        {/* Treatment Outcomes */}
        <div className="bg-white border border-border rounded-lg p-6">
          <div className="mb-6">
            <h3 className="font-semibold">Resultados de Tratamiento</h3>
            <p className="text-sm text-muted-foreground mt-1">Evolución de pacientes bajo tratamiento</p>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={treatmentOutcomes}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="mes" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'var(--card)',
                  border: '1px solid var(--border)',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="remision"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ fill: '#10b981', r: 4 }}
                name="Remisión"
              />
              <Line
                type="monotone"
                dataKey="mejoria"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ fill: '#3b82f6', r: 4 }}
                name="Mejoría"
              />
              <Line
                type="monotone"
                dataKey="estable"
                stroke="#f59e0b"
                strokeWidth={2}
                dot={{ fill: '#f59e0b', r: 4 }}
                name="Estable"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Success Rate Trend */}
      <div className="bg-white border border-border rounded-lg p-6">
        <div className="mb-6">
          <h3 className="font-semibold">Tasa de Éxito en Diagnóstico Temprano</h3>
          <p className="text-sm text-muted-foreground mt-1">Porcentaje de detecciones correctas confirmadas</p>
        </div>
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={monthlyDetections}>
            <defs>
              <linearGradient id="colorTasa" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ec4899" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#ec4899" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
            <YAxis domain={[85, 100]} stroke="var(--muted-foreground)" fontSize={12} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'var(--card)',
                border: '1px solid var(--border)',
                borderRadius: '8px',
              }}
            />
            <Area
              type="monotone"
              dataKey="tasaExito"
              stroke="#ec4899"
              strokeWidth={3}
              fillOpacity={1}
              fill="url(#colorTasa)"
              name="Tasa de Éxito (%)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

interface SummaryCardProps {
  title: string;
  value: string;
  subtitle: string;
  trend: string;
  icon: React.ElementType;
  color: 'pink' | 'green' | 'blue' | 'purple';
}

function SummaryCard({ title, value, subtitle, trend, icon: Icon, color }: SummaryCardProps) {
  const colorClasses = {
    pink: 'from-pink-500 to-rose-600',
    green: 'from-green-500 to-emerald-600',
    blue: 'from-blue-500 to-indigo-600',
    purple: 'from-purple-500 to-violet-600',
  };

  return (
    <div className="bg-white border border-border rounded-lg p-5 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <p className="text-sm text-muted-foreground">{title}</p>
        <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center`}>
          <Icon className="w-4 h-4 text-white" />
        </div>
      </div>
      <div className="space-y-1">
        <p className="text-3xl font-semibold">{value}</p>
        <div className="flex items-center gap-2">
          <span className="text-sm text-green-600 font-medium">{trend}</span>
          <span className="text-xs text-muted-foreground">{subtitle}</span>
        </div>
      </div>
    </div>
  );
}
