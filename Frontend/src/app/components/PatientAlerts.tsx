import { useState, useEffect } from 'react';
import { Bell, Send, Mail, MessageSquare, AlertCircle, User, Calendar, Check } from 'lucide-react';

interface Alert {
  id: string;
  patientId: string;
  patientName: string;
  message: string;
  type: 'email' | 'platform';
  priority: 'low' | 'medium' | 'high';
  status: 'sent' | 'pending';
  date: string;
}

const mockPatients = [
  { id: 'P001', name: 'Ana Martínez Ruiz', email: 'paciente@alertarosa.com' },
  { id: 'P002', name: 'María García López', email: 'maria.garcia@email.com' },
  { id: 'P003', name: 'Laura Fernández Santos', email: 'laura.fernandez@email.com' },
  { id: 'P004', name: 'Carmen Rodríguez Díaz', email: 'carmen.rodriguez@email.com' },
];

export function PatientAlerts() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [selectedPatient, setSelectedPatient] = useState('');
  const [message, setMessage] = useState('');
  const [alertType, setAlertType] = useState<'email' | 'platform'>('platform');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');

  useEffect(() => {
    const storedAlerts = localStorage.getItem('patientAlerts');
    if (storedAlerts) {
      setAlerts(JSON.parse(storedAlerts));
    }
  }, []);

  const handleSendAlert = () => {
    if (!selectedPatient || !message) {
      alert('Por favor seleccione un paciente y escriba un mensaje');
      return;
    }

    const patient = mockPatients.find(p => p.id === selectedPatient);
    if (!patient) return;

    const newAlert: Alert = {
      id: `A${Date.now()}`,
      patientId: selectedPatient,
      patientName: patient.name,
      message,
      type: alertType,
      priority,
      status: 'sent',
      date: new Date().toISOString(),
    };

    const updatedAlerts = [newAlert, ...alerts];
    setAlerts(updatedAlerts);
    localStorage.setItem('patientAlerts', JSON.stringify(updatedAlerts));

    setMessage('');
    setSelectedPatient('');
  };

  const recentAlerts = alerts.slice(0, 10);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg p-6 text-white">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center">
            <Bell className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-2">Sistema de Alertas</h2>
            <p className="text-purple-100">
              Enviar notificaciones y alertas a pacientes
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Send Alert Form */}
        <div className="bg-white border border-border rounded-lg p-6">
          <h3 className="font-semibold mb-4">Enviar Nueva Alerta</h3>

          <div className="space-y-4">
            {/* Select Patient */}
            <div>
              <label className="block text-sm mb-2">Seleccionar Paciente</label>
              <select
                value={selectedPatient}
                onChange={(e) => setSelectedPatient(e.target.value)}
                className="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-purple-500"
              >
                <option value="">-- Seleccione un paciente --</option>
                {mockPatients.map((patient) => (
                  <option key={patient.id} value={patient.id}>
                    {patient.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Alert Type */}
            <div>
              <label className="block text-sm mb-2">Tipo de Alerta</label>
              <div className="flex gap-3">
                <button
                  onClick={() => setAlertType('platform')}
                  className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border transition-all ${
                    alertType === 'platform'
                      ? 'bg-purple-50 border-purple-500 text-purple-700'
                      : 'border-border hover:bg-muted/50'
                  }`}
                >
                  <MessageSquare className="w-4 h-4" />
                  <span className="text-sm">Plataforma</span>
                </button>
                <button
                  onClick={() => setAlertType('email')}
                  className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border transition-all ${
                    alertType === 'email'
                      ? 'bg-purple-50 border-purple-500 text-purple-700'
                      : 'border-border hover:bg-muted/50'
                  }`}
                >
                  <Mail className="w-4 h-4" />
                  <span className="text-sm">Email</span>
                </button>
              </div>
            </div>

            {/* Priority */}
            <div>
              <label className="block text-sm mb-2">Prioridad</label>
              <div className="flex gap-2">
                {(['low', 'medium', 'high'] as const).map((p) => (
                  <button
                    key={p}
                    onClick={() => setPriority(p)}
                    className={`flex-1 px-3 py-2 rounded-lg text-sm transition-all ${
                      priority === p
                        ? p === 'low'
                          ? 'bg-green-100 text-green-700 border border-green-300'
                          : p === 'medium'
                          ? 'bg-orange-100 text-orange-700 border border-orange-300'
                          : 'bg-red-100 text-red-700 border border-red-300'
                        : 'bg-muted text-muted-foreground'
                    }`}
                  >
                    {p === 'low' ? 'Baja' : p === 'medium' ? 'Media' : 'Alta'}
                  </button>
                ))}
              </div>
            </div>

            {/* Message */}
            <div>
              <label className="block text-sm mb-2">Mensaje</label>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows={6}
                className="w-full px-4 py-3 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-purple-500 resize-none"
                placeholder="Escriba el mensaje de alerta para el paciente..."
              />
            </div>

            {/* Send Button */}
            <button
              onClick={handleSendAlert}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all font-medium"
            >
              <Send className="w-4 h-4" />
              Enviar Alerta
            </button>
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-white border border-border rounded-lg p-6">
          <h3 className="font-semibold mb-4">Alertas Recientes</h3>

          {recentAlerts.length === 0 ? (
            <div className="text-center py-12">
              <Bell className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
              <p className="text-muted-foreground">
                No hay alertas enviadas aún
              </p>
            </div>
          ) : (
            <div className="space-y-3 max-h-[600px] overflow-y-auto">
              {recentAlerts.map((alert) => (
                <div
                  key={alert.id}
                  className="p-4 border border-border rounded-lg hover:bg-muted/30 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-100 to-indigo-100 flex items-center justify-center">
                        <User className="w-4 h-4 text-purple-600" />
                      </div>
                      <div>
                        <p className="font-medium text-sm">{alert.patientName}</p>
                        <p className="text-xs text-muted-foreground">
                          {alert.patientId}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span
                        className={`px-2 py-0.5 text-xs rounded-full ${
                          alert.priority === 'low'
                            ? 'bg-green-100 text-green-700'
                            : alert.priority === 'medium'
                            ? 'bg-orange-100 text-orange-700'
                            : 'bg-red-100 text-red-700'
                        }`}
                      >
                        {alert.priority === 'low'
                          ? 'Baja'
                          : alert.priority === 'medium'
                          ? 'Media'
                          : 'Alta'}
                      </span>
                    </div>
                  </div>

                  <p className="text-sm mb-3 bg-muted/30 p-3 rounded">
                    {alert.message}
                  </p>

                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <div className="flex items-center gap-4">
                      <span className="flex items-center gap-1">
                        {alert.type === 'email' ? (
                          <Mail className="w-3 h-3" />
                        ) : (
                          <MessageSquare className="w-3 h-3" />
                        )}
                        {alert.type === 'email' ? 'Email' : 'Plataforma'}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {new Date(alert.date).toLocaleDateString('es-ES', {
                          day: 'numeric',
                          month: 'short',
                        })}
                      </span>
                    </div>
                    <span className="flex items-center gap-1 text-green-600">
                      <Check className="w-3 h-3" />
                      Enviada
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-medium text-blue-900 mb-2">
              Guías de Uso del Sistema de Alertas
            </h4>
            <ul className="space-y-1 text-sm text-blue-800">
              <li>
                • <strong>Plataforma:</strong> El paciente verá la alerta al
                iniciar sesión en su portal
              </li>
              <li>
                • <strong>Email:</strong> Se enviará un correo electrónico a la
                dirección registrada
              </li>
              <li>
                • <strong>Prioridad Alta:</strong> Usar para situaciones urgentes
                que requieran atención inmediata
              </li>
              <li>
                • Todas las alertas quedan registradas en el historial del paciente
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
