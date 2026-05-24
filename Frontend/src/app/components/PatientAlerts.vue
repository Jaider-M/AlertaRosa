<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { Bell, Send, Mail, MessageSquare, AlertCircle, User, Calendar, Check } from 'lucide-vue-next';
import { useAuth } from '../composables/useAuth';

const { user } = useAuth(); // Se vincula para lógica adicional o de renderizado condicional en el futuro si es necesario.

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

const alerts = ref<Alert[]>([]);
const selectedPatient = ref('');
const message = ref('');
const alertType = ref<'email' | 'platform'>('platform');
const priority = ref<'low' | 'medium' | 'high'>('medium');

onMounted(() => {
  const storedAlerts = localStorage.getItem('patientAlerts');
  if (storedAlerts) {
    alerts.value = JSON.parse(storedAlerts);
  }
});

const handleSendAlert = () => {
  if (!selectedPatient.value || !message.value) {
    alert('Por favor seleccione un paciente y escriba un mensaje');
    return;
  }

  const patient = mockPatients.find(p => p.id === selectedPatient.value);
  if (!patient) return;

  const newAlert: Alert = {
    id: `A${Date.now()}`,
    patientId: selectedPatient.value,
    patientName: patient.name,
    message: message.value,
    type: alertType.value,
    priority: priority.value,
    status: 'sent',
    date: new Date().toISOString(),
  };

  alerts.value.unshift(newAlert);
  localStorage.setItem('patientAlerts', JSON.stringify(alerts.value));

  message.value = '';
  selectedPatient.value = '';
};

const recentAlerts = computed(() => alerts.value.slice(0, 10));

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
};
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg p-6 text-white">
      <div class="flex items-start gap-4">
        <div class="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center">
          <Bell class="w-6 h-6" />
        </div>
        <div>
          <h2 class="text-2xl font-semibold mb-2">Sistema de Alertas</h2>
          <p class="text-purple-100">
            Enviar notificaciones y alertas a pacientes - Acceso: {{ user?.role === 'manager' ? 'Administrador' : 'Especialista' }}
          </p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Send Alert Form -->
      <div class="bg-white border border-border rounded-lg p-6">
        <h3 class="font-semibold mb-4">Enviar Nueva Alerta</h3>

        <div class="space-y-4">
          <!-- Select Patient -->
          <div>
            <label class="block text-sm mb-2">Seleccionar Paciente</label>
            <select
              v-model="selectedPatient"
              class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-purple-500"
            >
              <option value="">-- Seleccione un paciente --</option>
              <option v-for="patient in mockPatients" :key="patient.id" :value="patient.id">
                {{ patient.name }}
              </option>
            </select>
          </div>

          <!-- Alert Type -->
          <div>
            <label class="block text-sm mb-2">Tipo de Alerta</label>
            <div class="flex gap-3">
              <button
                @click="alertType = 'platform'"
                :class="`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border transition-all ${
                  alertType === 'platform' ? 'bg-purple-50 border-purple-500 text-purple-700' : 'border-border hover:bg-muted/50'
                }`"
              >
                <MessageSquare class="w-4 h-4" />
                <span class="text-sm">Plataforma</span>
              </button>
              <button
                @click="alertType = 'email'"
                :class="`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border transition-all ${
                  alertType === 'email' ? 'bg-purple-50 border-purple-500 text-purple-700' : 'border-border hover:bg-muted/50'
                }`"
              >
                <Mail class="w-4 h-4" />
                <span class="text-sm">Email</span>
              </button>
            </div>
          </div>

          <!-- Priority -->
          <div>
            <label class="block text-sm mb-2">Prioridad</label>
            <div class="flex gap-2">
              <button
                v-for="p in ['low', 'medium', 'high'] as const"
                :key="p"
                @click="priority = p"
                :class="`flex-1 px-3 py-2 rounded-lg text-sm transition-all ${
                  priority === p
                    ? p === 'low' ? 'bg-green-100 text-green-700 border border-green-300'
                    : p === 'medium' ? 'bg-orange-100 text-orange-700 border border-orange-300'
                    : 'bg-red-100 text-red-700 border border-red-300'
                    : 'bg-muted text-muted-foreground'
                }`"
              >
                {{ p === 'low' ? 'Baja' : p === 'medium' ? 'Media' : 'Alta' }}
              </button>
            </div>
          </div>

          <!-- Message -->
          <div>
            <label class="block text-sm mb-2">Mensaje</label>
            <textarea
              v-model="message"
              rows="6"
              class="w-full px-4 py-3 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-purple-500 resize-none"
              placeholder="Escriba el mensaje de alerta para el paciente..."
            ></textarea>
          </div>

          <!-- Send Button -->
          <button
            @click="handleSendAlert"
            class="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all font-medium"
          >
            <Send class="w-4 h-4" />
            Enviar Alerta
          </button>
        </div>
      </div>

      <!-- Recent Alerts -->
      <div class="bg-white border border-border rounded-lg p-6">
        <h3 class="font-semibold mb-4">Alertas Recientes</h3>

        <div v-if="recentAlerts.length === 0" class="text-center py-12">
          <Bell class="w-12 h-12 text-muted-foreground mx-auto mb-3" />
          <p class="text-muted-foreground">No hay alertas enviadas aún</p>
        </div>

        <div v-else class="space-y-3 max-h-[600px] overflow-y-auto">
          <div
            v-for="alert in recentAlerts"
            :key="alert.id"
            class="p-4 border border-border rounded-lg hover:bg-muted/30 transition-colors"
          >
            <div class="flex items-start justify-between mb-2">
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-purple-100 to-indigo-100 flex items-center justify-center">
                  <User class="w-4 h-4 text-purple-600" />
                </div>
                <div>
                  <p class="font-medium text-sm">{{ alert.patientName }}</p>
                  <p class="text-xs text-muted-foreground">{{ alert.patientId }}</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <span
                  :class="`px-2 py-0.5 text-xs rounded-full ${
                    alert.priority === 'low' ? 'bg-green-100 text-green-700'
                    : alert.priority === 'medium' ? 'bg-orange-100 text-orange-700'
                    : 'bg-red-100 text-red-700'
                  }`"
                >
                  {{ alert.priority === 'low' ? 'Baja' : alert.priority === 'medium' ? 'Media' : 'Alta' }}
                </span>
              </div>
            </div>

            <p class="text-sm mb-3 bg-muted/30 p-3 rounded">{{ alert.message }}</p>

            <div class="flex items-center justify-between text-xs text-muted-foreground">
              <div class="flex items-center gap-4">
                <span class="flex items-center gap-1">
                  <Mail v-if="alert.type === 'email'" class="w-3 h-3" />
                  <MessageSquare v-else class="w-3 h-3" />
                  {{ alert.type === 'email' ? 'Email' : 'Plataforma' }}
                </span>
                <span class="flex items-center gap-1">
                  <Calendar class="w-3 h-3" />
                  {{ formatDate(alert.date) }}
                </span>
              </div>
              <span class="flex items-center gap-1 text-green-600">
                <Check class="w-3 h-3" />
                Enviada
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Info Box -->
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <div class="flex items-start gap-3">
        <AlertCircle class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div>
          <h4 class="font-medium text-blue-900 mb-2">Guías de Uso del Sistema de Alertas</h4>
          <ul class="space-y-1 text-sm text-blue-800">
            <li>• <strong>Plataforma:</strong> El paciente verá la alerta al iniciar sesión en su portal</li>
            <li>• <strong>Email:</strong> Se enviará un correo electrónico a la dirección registrada</li>
            <li>• <strong>Prioridad Alta:</strong> Usar para situaciones urgentes que requieran atención inmediata</li>
            <li>• Todas las alertas quedan registradas en el historial del paciente</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
