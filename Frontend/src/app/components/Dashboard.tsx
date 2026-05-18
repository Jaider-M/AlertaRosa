import { TrendingUp, TrendingDown, Users, Calendar, AlertCircle, CheckCircle } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const detectionTrend = [
  { month: 'Ene', casos: 12, seguimiento: 45 },
  { month: 'Feb', casos: 15, seguimiento: 48 },
  { month: 'Mar', casos: 11, seguimiento: 52 },
  { month: 'Abr', casos: 18, seguimiento: 55 },
  { month: 'May', casos: 14, seguimiento: 58 },
  { month: 'Jun', casos: 20, seguimiento: 62 },
];

const riskDistribution = [
  { name: 'Bajo Riesgo', value: 65, color: '#10b981' },
  { name: 'Riesgo Moderado', value: 25, color: '#f59e0b' },
  { name: 'Alto Riesgo', value: 10, color: '#ef4444' },
];

const upcomingAppointments = [
  { patient: 'Ana Martínez', type: 'Seguimiento', time: '10:00 AM', priority: 'normal' },
  { patient: 'Laura Fernández', type: 'Diagnóstico', time: '11:30 AM', priority: 'high' },
  { patient: 'Carmen Ruiz', type: 'Resultado', time: '2:00 PM', priority: 'high' },
  { patient: 'Isabel Torres', type: 'Consulta', time: '3:30 PM', priority: 'normal' },
];

export function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Alert Banner */}
      <div className="bg-pink-50 border border-pink-200 rounded-lg p-4 flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-pink-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="font-medium text-pink-900">3 pacientes requieren atención prioritaria</p>
          <p className="text-sm text-pink-700 mt-1">
            Resultados de biopsias pendientes de revisión - Verificar antes de las 5:00 PM
          </p>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Pacientes Activos"
          value="247"
          change="+12"
          trend="up"
          icon={Users}
          color="blue"
        />
        <MetricCard
          title="Detecciones Tempranas"
          value="89"
          change="+8"
          trend="up"
          suffix="este mes"
          icon={CheckCircle}
          color="green"
        />
        <MetricCard
          title="Citas Pendientes"
          value="23"
          change="-5"
          trend="down"
          suffix="hoy"
          icon={Calendar}
          color="orange"
        />
        <MetricCard
          title="Tasa de Detección"
          value="94%"
          change="+2%"
          trend="up"
          suffix="precisión"
          icon={TrendingUp}
          color="pink"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Detection Trend */}
        <div className="lg:col-span-2 bg-white border border-border rounded-lg p-6">
          <div className="mb-6">
            <h3 className="font-semibold">Tendencia de Detección</h3>
            <p className="text-sm text-muted-foreground mt-1">Casos nuevos vs. pacientes en seguimiento</p>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={detectionTrend}>
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
              <Line
                type="monotone"
                dataKey="casos"
                stroke="#ec4899"
                strokeWidth={2}
                name="Casos Nuevos"
                dot={{ fill: '#ec4899', r: 4 }}
              />
              <Line
                type="monotone"
                dataKey="seguimiento"
                stroke="#3b82f6"
                strokeWidth={2}
                name="En Seguimiento"
                dot={{ fill: '#3b82f6', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Distribution */}
        <div className="bg-white border border-border rounded-lg p-6">
          <div className="mb-6">
            <h3 className="font-semibold">Distribución de Riesgo</h3>
            <p className="text-sm text-muted-foreground mt-1">Clasificación actual</p>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={riskDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={2}
                dataKey="value"
              >
                {riskDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {riskDistribution.map((item) => (
              <div key={item.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-sm">{item.name}</span>
                </div>
                <span className="text-sm font-medium">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Upcoming Appointments */}
      <div className="bg-white border border-border rounded-lg p-6">
        <div className="mb-4">
          <h3 className="font-semibold">Citas de Hoy</h3>
          <p className="text-sm text-muted-foreground mt-1">4 citas programadas</p>
        </div>
        <div className="space-y-3">
          {upcomingAppointments.map((appointment, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-pink-100 to-purple-100 flex items-center justify-center">
                  <span className="text-sm font-medium text-pink-700">
                    {appointment.patient.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
                <div>
                  <p className="font-medium">{appointment.patient}</p>
                  <p className="text-sm text-muted-foreground">{appointment.type}</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium">{appointment.time}</span>
                {appointment.priority === 'high' && (
                  <span className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded-full">
                    Prioritaria
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

interface MetricCardProps {
  title: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
  suffix?: string;
  icon: React.ElementType;
  color: 'blue' | 'green' | 'orange' | 'pink';
}

function MetricCard({ title, value, change, trend, suffix, icon: Icon, color }: MetricCardProps) {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    orange: 'from-orange-500 to-orange-600',
    pink: 'from-pink-500 to-rose-600',
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
          <div className={`flex items-center gap-1 text-sm ${trend === 'up' ? 'text-green-600' : 'text-orange-600'}`}>
            {trend === 'up' ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
            <span>{change}</span>
          </div>
          {suffix && <span className="text-xs text-muted-foreground">{suffix}</span>}
        </div>
      </div>
    </div>
  );
}
