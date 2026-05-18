import { useState } from 'react';
import { Search, Filter, User, Calendar, FileText, Phone, Mail, AlertCircle, TrendingUp } from 'lucide-react';

interface Patient {
  id: string;
  name: string;
  age: number;
  riskLevel: 'low' | 'medium' | 'high';
  lastVisit: string;
  nextAppointment: string;
  status: 'active' | 'followup' | 'urgent';
  phone: string;
  email: string;
  notes: string;
}

const patients: Patient[] = [
  {
    id: 'P001',
    name: 'María García López',
    age: 45,
    riskLevel: 'medium',
    lastVisit: '2026-03-15',
    nextAppointment: '2026-04-15',
    status: 'followup',
    phone: '+34 612 345 678',
    email: 'maria.garcia@email.com',
    notes: 'Historial familiar positivo. Requiere seguimiento semestral.',
  },
  {
    id: 'P002',
    name: 'Ana Martínez Ruiz',
    age: 52,
    riskLevel: 'high',
    lastVisit: '2026-04-08',
    nextAppointment: '2026-04-14',
    status: 'urgent',
    phone: '+34 623 456 789',
    email: 'ana.martinez@email.com',
    notes: 'Resultado de biopsia pendiente. Programar consulta urgente.',
  },
  {
    id: 'P003',
    name: 'Laura Fernández Santos',
    age: 38,
    riskLevel: 'low',
    lastVisit: '2026-02-20',
    nextAppointment: '2026-05-20',
    status: 'active',
    phone: '+34 634 567 890',
    email: 'laura.fernandez@email.com',
    notes: 'Control anual de rutina. Sin antecedentes.',
  },
  {
    id: 'P004',
    name: 'Carmen Rodríguez Díaz',
    age: 48,
    riskLevel: 'medium',
    lastVisit: '2026-03-28',
    nextAppointment: '2026-04-20',
    status: 'followup',
    phone: '+34 645 678 901',
    email: 'carmen.rodriguez@email.com',
    notes: 'Tejido mamario denso. Requiere ecografía complementaria.',
  },
  {
    id: 'P005',
    name: 'Isabel Torres Moreno',
    age: 41,
    riskLevel: 'low',
    lastVisit: '2026-01-10',
    nextAppointment: '2026-07-10',
    status: 'active',
    phone: '+34 656 789 012',
    email: 'isabel.torres@email.com',
    notes: 'Primera consulta preventiva. Sin factores de riesgo.',
  },
];

export function PatientManagement() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);
  const [filterRisk, setFilterRisk] = useState<'all' | 'low' | 'medium' | 'high'>('all');

  const filteredPatients = patients.filter(patient => {
    const matchesSearch = patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         patient.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterRisk === 'all' || patient.riskLevel === filterRisk;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Patient List */}
      <div className="lg:col-span-1 space-y-4">
        <div className="bg-white border border-border rounded-lg p-4">
          <div className="flex items-center gap-2 mb-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Buscar paciente..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
              />
            </div>
          </div>

          <div className="flex gap-2 mb-4">
            {(['all', 'low', 'medium', 'high'] as const).map((level) => (
              <button
                key={level}
                onClick={() => setFilterRisk(level)}
                className={`px-3 py-1.5 text-xs rounded-lg transition-colors ${
                  filterRisk === level
                    ? 'bg-pink-600 text-white'
                    : 'bg-muted text-muted-foreground hover:bg-muted/80'
                }`}
              >
                {level === 'all' ? 'Todos' : level === 'low' ? 'Bajo' : level === 'medium' ? 'Medio' : 'Alto'}
              </button>
            ))}
          </div>

          <div className="text-sm text-muted-foreground mb-2">
            {filteredPatients.length} pacientes
          </div>
        </div>

        <div className="space-y-2 max-h-[600px] overflow-y-auto">
          {filteredPatients.map((patient) => (
            <button
              key={patient.id}
              onClick={() => setSelectedPatient(patient)}
              className={`w-full text-left p-4 rounded-lg border transition-all ${
                selectedPatient?.id === patient.id
                  ? 'bg-pink-50 border-pink-300 shadow-sm'
                  : 'bg-white border-border hover:border-pink-200 hover:shadow-sm'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <div>
                  <p className="font-medium">{patient.name}</p>
                  <p className="text-xs text-muted-foreground">{patient.id} · {patient.age} años</p>
                </div>
                {patient.status === 'urgent' && (
                  <div className="w-2 h-2 rounded-full bg-red-500" />
                )}
              </div>

              <div className="flex items-center gap-2">
                <span className={`px-2 py-0.5 text-xs rounded-full ${
                  patient.riskLevel === 'low'
                    ? 'bg-green-100 text-green-700'
                    : patient.riskLevel === 'medium'
                    ? 'bg-orange-100 text-orange-700'
                    : 'bg-red-100 text-red-700'
                }`}>
                  {patient.riskLevel === 'low' ? 'Riesgo Bajo' :
                   patient.riskLevel === 'medium' ? 'Riesgo Medio' : 'Riesgo Alto'}
                </span>
                <span className={`px-2 py-0.5 text-xs rounded-full ${
                  patient.status === 'active'
                    ? 'bg-blue-100 text-blue-700'
                    : patient.status === 'followup'
                    ? 'bg-purple-100 text-purple-700'
                    : 'bg-red-100 text-red-700'
                }`}>
                  {patient.status === 'active' ? 'Activo' :
                   patient.status === 'followup' ? 'Seguimiento' : 'Urgente'}
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Patient Details */}
      <div className="lg:col-span-2">
        {selectedPatient ? (
          <div className="space-y-6">
            {/* Header */}
            <div className="bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg p-6 text-white">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  <div className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                    <User className="w-8 h-8" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-semibold mb-1">{selectedPatient.name}</h2>
                    <p className="text-pink-100">ID: {selectedPatient.id} · {selectedPatient.age} años</p>
                  </div>
                </div>
                <span className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                  selectedPatient.riskLevel === 'low'
                    ? 'bg-green-500/20 text-white border border-white/30'
                    : selectedPatient.riskLevel === 'medium'
                    ? 'bg-orange-500/20 text-white border border-white/30'
                    : 'bg-red-500/20 text-white border border-white/30'
                }`}>
                  {selectedPatient.riskLevel === 'low' ? 'Riesgo Bajo' :
                   selectedPatient.riskLevel === 'medium' ? 'Riesgo Moderado' : 'Riesgo Alto'}
                </span>
              </div>
            </div>

            {/* Contact Information */}
            <div className="bg-white border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-4">Información de Contacto</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                    <Phone className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Teléfono</p>
                    <p className="font-medium">{selectedPatient.phone}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                    <Mail className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Email</p>
                    <p className="font-medium">{selectedPatient.email}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Appointments */}
            <div className="bg-white border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-4">Citas</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-muted/30 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Calendar className="w-4 h-4 text-muted-foreground" />
                    <p className="text-sm text-muted-foreground">Última Visita</p>
                  </div>
                  <p className="font-medium">{new Date(selectedPatient.lastVisit).toLocaleDateString('es-ES', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                  })}</p>
                </div>
                <div className="p-4 bg-pink-50 border border-pink-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Calendar className="w-4 h-4 text-pink-600" />
                    <p className="text-sm text-pink-700">Próxima Cita</p>
                  </div>
                  <p className="font-medium text-pink-900">{new Date(selectedPatient.nextAppointment).toLocaleDateString('es-ES', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                  })}</p>
                </div>
              </div>
            </div>

            {/* Clinical Notes */}
            <div className="bg-white border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-4">Notas Clínicas</h3>
              <div className="p-4 bg-muted/30 rounded-lg">
                <div className="flex items-start gap-3">
                  <FileText className="w-5 h-5 text-muted-foreground flex-shrink-0 mt-0.5" />
                  <p className="text-sm">{selectedPatient.notes}</p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button className="flex-1 px-4 py-2.5 bg-gradient-to-r from-pink-600 to-purple-600 text-white rounded-lg hover:from-pink-700 hover:to-purple-700 transition-all">
                Agendar Cita
              </button>
              <button className="flex-1 px-4 py-2.5 border border-border rounded-lg hover:bg-muted/50 transition-colors">
                Ver Historial Completo
              </button>
              <button className="flex-1 px-4 py-2.5 border border-border rounded-lg hover:bg-muted/50 transition-colors">
                Actualizar Información
              </button>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center bg-white border border-border rounded-lg p-12">
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
                <User className="w-8 h-8 text-muted-foreground" />
              </div>
              <p className="text-muted-foreground">Selecciona un paciente para ver sus detalles</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
