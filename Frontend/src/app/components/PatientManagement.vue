<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { Search, User, Calendar, FileText, Phone, Mail } from 'lucide-vue-next';

interface Patient {
  id: string;
  user_id: string;
  full_name: string;
  medical_record_number: string;
  date_of_birth: string;
  phone: string;
  address: string;
  prioridad: 'Baja' | 'Media' | 'Alta';
}

const patients = ref<Patient[]>([]);
const searchTerm = ref('');
const filterRisk = ref<'all' | 'Baja' | 'Media' | 'Alta'>('all');
const selectedPatient = ref<Patient | null>(null);
const baseUrl = import.meta.env.VITE_API_URL;

const fetchPatients = async () => {
  const token = localStorage.getItem('access_token');
  
  if (!token) {
    console.error("No hay token de sesión. Por favor, inicia sesión.");
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/api/patients/doctor/my-patients`, {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    patients.value = Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Error detallado:", error);
  }
};

onMounted(fetchPatients);

const calculateAge = (dob: string) => {
  const birthDate = new Date(dob);
  const diff = Date.now() - birthDate.getTime();
  return Math.abs(new Date(diff).getUTCFullYear() - 1970);
};

const filteredPatients = computed(() => {
  return patients.value.filter(patient => {
    const matchesSearch = patient.full_name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
                          patient.medical_record_number.toLowerCase().includes(searchTerm.value.toLowerCase());
    const matchesFilter = filterRisk.value === 'all' || patient.prioridad === filterRisk.value;
    return matchesSearch && matchesFilter;
  });
});

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
};
</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <div class="lg:col-span-1 space-y-4">
      <div class="bg-white border border-border rounded-lg p-4">
        <div class="flex items-center gap-2 mb-4">
          <div class="relative flex-1">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Buscar paciente..."
              v-model="searchTerm"
              class="pl-10 pr-4 py-2 w-full bg-white border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 transition-colors"
            />
          </div>
        </div>

        <div class="flex gap-2 mb-4">
          <button
            v-for="level in ['all', 'Baja', 'Media', 'Alta'] as const"
            :key="level"
            @click="filterRisk = level"
            :class="`px-3 py-1.5 text-xs rounded-lg transition-colors ${
              filterRisk === level
                ? 'bg-pink-600 text-white'
                : 'bg-muted text-muted-foreground hover:bg-muted/80'
            }`"
          >
            {{ level }}
          </button>
        </div>

        <div class="text-sm text-muted-foreground mb-2">
          {{ filteredPatients.length }} pacientes
        </div>
      </div>

      <div class="space-y-2 max-h-[600px] overflow-y-auto">
        <button
          v-for="patient in filteredPatients"
          :key="patient.id"
          @click="selectedPatient = patient"
          :class="`w-full text-left p-4 rounded-lg border transition-all ${
            selectedPatient?.id === patient.id
              ? 'bg-pink-50 border-pink-300 shadow-sm'
              : 'bg-white border-border hover:border-pink-200 hover:shadow-sm'
          }`"
        >
          <div class="flex items-start justify-between mb-2">
            <div>
              <p class="font-medium">{{ patient.full_name }}</p>
              <p class="text-xs text-muted-foreground">{{ patient.medical_record_number }} · {{ calculateAge(patient.date_of_birth) }} años</p>
            </div>
          </div>
          <span :class="`px-2 py-0.5 text-xs rounded-full ${
            patient.prioridad === 'Baja' ? 'bg-green-100 text-green-700' :
            patient.prioridad === 'Media' ? 'bg-orange-100 text-orange-700' : 'bg-red-100 text-red-700'
          }`">
            {{ patient.prioridad }}
          </span>
        </button>
      </div>
    </div>

    <div class="lg:col-span-2">
      <div v-if="selectedPatient" class="space-y-6">
        <div class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg p-6 text-white">
          <h2 class="text-2xl font-semibold mb-1">{{ selectedPatient.full_name }}</h2>
          <p class="text-pink-100">ID: {{ selectedPatient.medical_record_number }} · {{ calculateAge(selectedPatient.date_of_birth) }} años</p>
        </div>

        <div class="bg-white border border-border rounded-lg p-6">
          <h3 class="font-semibold mb-4">Información de Contacto</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex items-center gap-3">
              <Phone class="w-5 h-5 text-blue-600" />
              <p class="font-medium">{{ selectedPatient.phone }}</p>
            </div>
            <div class="flex items-center gap-3">
              <Mail class="w-5 h-5 text-purple-600" />
              <p class="font-medium">{{ selectedPatient.address }}</p>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="h-full flex items-center justify-center bg-white border border-border rounded-lg p-12">
        <p class="text-muted-foreground">Selecciona un paciente para ver sus detalles</p>
      </div>
    </div>
  </div>
</template>