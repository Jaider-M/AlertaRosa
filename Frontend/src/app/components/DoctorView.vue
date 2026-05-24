<script setup lang="ts">
import { ref } from 'vue';
import { Users, Brain, BarChart3, LogOut, Bell } from 'lucide-vue-next';
import { useAuth } from '../composables/useAuth';
import Dashboard from './Dashboard.vue';
import DiagnosisModule from './DiagnosisModule.vue';
import PatientManagement from './PatientManagement.vue';
import Analytics from './Analytics.vue';
import PatientAlerts from './PatientAlerts.vue';
import logoImg from '../../imports/AlertaRosa.jpeg';

type Tab = 'dashboard' | 'diagnosis' | 'patients' | 'analytics' | 'alerts';

const { user, logout } = useAuth();
const activeTab = ref<Tab>('dashboard');

const tabs = [
  { id: 'dashboard' as Tab, label: 'Dashboard', icon: BarChart3 },
  { id: 'diagnosis' as Tab, label: 'Diagnóstico', icon: Brain },
  { id: 'patients' as Tab, label: 'Pacientes', icon: Users },
  { id: 'analytics' as Tab, label: 'Analíticas', icon: BarChart3 },
  { id: 'alerts' as Tab, label: 'Alertas', icon: Bell },
];
</script>

<template>
  <div class="min-h-screen bg-background">
    <!-- Header -->
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
            <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-50 border border-green-200">
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              <span class="text-sm text-green-700">Sistema Activo</span>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium">{{ user?.name }}</p>
              <p class="text-xs text-muted-foreground">
                {{ user?.specialization || 'Oncología' }}
              </p>
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
          </div>
          <div v-if="activeTab === tab.id" class="absolute bottom-0 left-0 right-0 h-0.5 bg-pink-500"></div>
        </button>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="p-6">
      <transition name="fade" mode="out-in">
        <div :key="activeTab">
          <Dashboard v-if="activeTab === 'dashboard'" />
          <DiagnosisModule v-else-if="activeTab === 'diagnosis'" />
          <PatientManagement v-else-if="activeTab === 'patients'" />
          <Analytics v-else-if="activeTab === 'analytics'" />
          <PatientAlerts v-else-if="activeTab === 'alerts'" />
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
