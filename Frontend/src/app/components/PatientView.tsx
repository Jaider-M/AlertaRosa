import { useState } from 'react';
import { FileText, Calendar, Activity, AlertCircle, Download, Eye, User, Heart, LogOut } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useAuth } from '../context/AuthContext';

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

const riskTrend = [
  { month: 'Ene 2025', nivel: 15 },
  { month: 'Abr 2025', nivel: 14 },
  { month: 'Jul 2025', nivel: 15 },
  { month: 'Oct 2025', nivel: 13 },
  { month: 'Ene 2026', nivel: 12 },
  { month: 'Abr 2026', nivel: 12 },
];

export function PatientView() {
  const { user, logout } = useAuth();
  const [selectedHistory, setSelectedHistory] = useState(medicalHistory[0]);

  return (
    <div className="min-h-screen bg-background">
      {/* Top Header */}
      <header className="border-b border-border bg-white sticky top-0 z-50">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold">OncoPrevent</h1>
                <p className="text-sm text-muted-foreground">
                  Portal del Paciente
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium">{user?.name}</p>
                <p className="text-xs text-muted-foreground">Paciente</p>
              </div>
              <button
                onClick={logout}
                className="p-2 hover:bg-muted rounded-lg transition-colors"
                title="Cerrar sesión"
              >
                <LogOut className="w-5 h-5 text-muted-foreground" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="p-6 space-y-6">
        {/* Welcome Header */}
        <div className="bg-gradient-to-r from-pink-500 to-rose-600 rounded-lg p-6 text-white">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center">
                <User className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-2xl font-semibold mb-2">Mi Historia Clínica</h2>
                <p className="text-pink-100">Bienvenido/a, {user?.name}</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-pink-100">ID de Paciente</p>
              <p className="font-medium">{user?.id}</p>
            </div>
          </div>
        </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white border border-border rounded-lg p-5">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-muted-foreground">Nivel de Riesgo</p>
            <Heart className="w-5 h-5 text-green-600" />
          </div>
          <p className="text-2xl font-semibold text-green-600">Bajo</p>
          <p className="text-xs text-muted-foreground mt-1">12% evaluación actual</p>
        </div>

        <div className="bg-white border border-border rounded-lg p-5">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-muted-foreground">Próxima Cita</p>
            <Calendar className="w-5 h-5 text-blue-600" />
          </div>
          <p className="text-2xl font-semibold">15 Abr</p>
          <p className="text-xs text-muted-foreground mt-1">Seguimiento rutinario</p>
        </div>

        <div className="bg-white border border-border rounded-lg p-5">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-muted-foreground">Consultas</p>
            <Activity className="w-5 h-5 text-purple-600" />
          </div>
          <p className="text-2xl font-semibold">3</p>
          <p className="text-xs text-muted-foreground mt-1">Último año</p>
        </div>

        <div className="bg-white border border-border rounded-lg p-5">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-muted-foreground">Resultados</p>
            <FileText className="w-5 h-5 text-orange-600" />
          </div>
          <p className="text-2xl font-semibold">3</p>
          <p className="text-xs text-muted-foreground mt-1">Disponibles</p>
        </div>
      </div>

      {/* Risk Trend */}
      <div className="bg-white border border-border rounded-lg p-6">
        <div className="mb-6">
          <h3 className="font-semibold">Evolución del Nivel de Riesgo</h3>
          <p className="text-sm text-muted-foreground mt-1">
            Tendencia de tu evaluación de riesgo en el tiempo
          </p>
        </div>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={riskTrend}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
            <YAxis stroke="var(--muted-foreground)" fontSize={12} domain={[0, 30]} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'var(--card)',
                border: '1px solid var(--border)',
                borderRadius: '8px',
              }}
            />
            <Line
              type="monotone"
              dataKey="nivel"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ fill: '#10b981', r: 4 }}
              name="Nivel de Riesgo (%)"
            />
          </LineChart>
        </ResponsiveContainer>
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm text-green-800">
            <strong>Excelente:</strong> Tu nivel de riesgo se mantiene estable y bajo. Continúa con tus controles regulares.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Medical History */}
        <div className="bg-white border border-border rounded-lg p-6">
          <h3 className="font-semibold mb-4">Historial Médico</h3>
          <div className="space-y-3 mb-6">
            {medicalHistory.map((record, index) => (
              <button
                key={index}
                onClick={() => setSelectedHistory(record)}
                className={`w-full text-left p-4 rounded-lg border transition-all ${
                  selectedHistory === record
                    ? 'bg-pink-50 border-pink-300'
                    : 'border-border hover:border-pink-200'
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <p className="font-medium">{record.type}</p>
                    <p className="text-xs text-muted-foreground">
                      {new Date(record.date).toLocaleDateString('es-ES', {
                        day: 'numeric',
                        month: 'long',
                        year: 'numeric',
                      })}
                    </p>
                  </div>
                  <Eye className="w-4 h-4 text-muted-foreground" />
                </div>
                <p className="text-xs text-muted-foreground">{record.doctor}</p>
              </button>
            ))}
          </div>

          <div className="p-4 bg-muted/30 rounded-lg">
            <h4 className="font-medium mb-2">Detalles de la Consulta</h4>
            <div className="space-y-2 text-sm">
              <div>
                <p className="text-muted-foreground">Diagnóstico</p>
                <p className="font-medium">{selectedHistory.diagnosis}</p>
              </div>
              <div>
                <p className="text-muted-foreground">Notas</p>
                <p>{selectedHistory.notes}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Test Results */}
        <div className="bg-white border border-border rounded-lg p-6">
          <h3 className="font-semibold mb-4">Resultados de Pruebas</h3>
          <div className="space-y-3">
            {testResults.map((test, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 border border-border rounded-lg hover:border-pink-300 hover:bg-pink-50/50 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-pink-100 to-purple-100 flex items-center justify-center">
                    <FileText className="w-5 h-5 text-pink-600" />
                  </div>
                  <div>
                    <p className="font-medium text-sm">{test.test}</p>
                    <p className="text-xs text-muted-foreground">
                      {new Date(test.date).toLocaleDateString('es-ES', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                      })}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                    {test.result}
                  </span>
                  <button className="p-2 hover:bg-muted rounded-lg transition-colors">
                    <Download className="w-4 h-4 text-muted-foreground" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Upcoming Appointments */}
      <div className="bg-white border border-border rounded-lg p-6">
        <h3 className="font-semibold mb-4">Próximas Citas</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {appointments.map((appointment, index) => (
            <div
              key={index}
              className="p-4 border border-border rounded-lg hover:border-pink-300 hover:bg-pink-50/50 transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center">
                    <Calendar className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium">{appointment.type}</p>
                    <p className="text-sm text-muted-foreground">
                      {appointment.doctor}
                    </p>
                  </div>
                </div>
                <span
                  className={`px-2 py-1 text-xs rounded-full ${
                    appointment.status === 'confirmed'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-orange-100 text-orange-700'
                  }`}
                >
                  {appointment.status === 'confirmed' ? 'Confirmada' : 'Pendiente'}
                </span>
              </div>
              <div className="flex items-center gap-4 text-sm">
                <span className="text-muted-foreground">
                  {new Date(appointment.date).toLocaleDateString('es-ES', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                  })}
                </span>
                <span className="font-medium">{appointment.time}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

        {/* Important Info */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-medium text-blue-900 mb-2">
                Recordatorios Importantes
              </h4>
              <ul className="space-y-1 text-sm text-blue-800">
                <li>• Realizar autoexamen mamario mensual</li>
                <li>• Mantener un estilo de vida saludable</li>
                <li>• Asistir a todas las citas programadas</li>
                <li>
                  • Contactar a tu médico si notas cualquier cambio inusual
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
