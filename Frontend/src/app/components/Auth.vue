<script setup lang="ts">
import { ref, reactive } from 'vue';
import { User, Lock, Mail, Phone, Stethoscope } from 'lucide-vue-next';
import { useAuth } from '../composables/useAuth';
import type { UserRole, RegisterData } from '../types';
import logoImg from '../../imports/AlertaRosa.jpeg';

const isLogin = ref(true);
const formData = reactive<RegisterData>({
  email: '',
  password: '',
  name: '',
  role: 'patient',
  phone: '',
  specialization: '',
});
const error = ref('');

const { login, register } = useAuth();

const handleSubmit = (e: Event) => {
  e.preventDefault();
  error.value = '';

  if (isLogin.value) {
    const success = login(formData.email, formData.password);
    if (!success) {
      error.value = 'Credenciales incorrectas';
    }
  } else {
    if (!formData.email || !formData.password || !formData.name) {
      error.value = 'Por favor complete todos los campos requeridos';
      return;
    }
    const success = register(formData);
    if (!success) {
      error.value = 'El email ya está registrado';
    }
  }
};
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50 flex items-center justify-center p-6">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8 transition-all duration-500 transform translate-y-0 opacity-100">
        <img
          :src="logoImg"
          alt="AlertaRosa"
          class="w-48 h-auto mx-auto mb-4"
        />
        <p class="text-muted-foreground">
          Detección temprana, vida salvada
        </p>
      </div>

      <!-- Form Card -->
      <div class="bg-white rounded-2xl shadow-xl p-8 transition-all duration-500 transform translate-y-0 opacity-100">
        <!-- Tabs -->
        <div class="flex gap-2 mb-6 p-1 bg-muted rounded-lg">
          <button
            @click="isLogin = true"
            :class="[
              'flex-1 py-2 px-4 rounded-md transition-all',
              isLogin ? 'bg-white shadow-sm font-medium' : 'text-muted-foreground hover:text-foreground'
            ]"
          >
            Iniciar Sesión
          </button>
          <button
            @click="isLogin = false"
            :class="[
              'flex-1 py-2 px-4 rounded-md transition-all',
              !isLogin ? 'bg-white shadow-sm font-medium' : 'text-muted-foreground hover:text-foreground'
            ]"
          >
            Registro
          </button>
        </div>

        <form @submit="handleSubmit" class="space-y-4">
          <!-- Email -->
          <div>
            <label class="block text-sm mb-2">Email</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="email"
                v-model="formData.email"
                class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                placeholder="correo@ejemplo.com"
                required
              />
            </div>
          </div>

          <!-- Name (register only) -->
          <div v-if="!isLogin">
            <label class="block text-sm mb-2">Nombre Completo</label>
            <div class="relative">
              <User class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="text"
                v-model="formData.name"
                class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                placeholder="Juan Pérez"
                required
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm mb-2">Contraseña</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="password"
                v-model="formData.password"
                class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                placeholder="••••••••"
                required
              />
            </div>
          </div>

          <!-- Role (register only) -->
          <template v-if="!isLogin">
            <div>
              <label class="block text-sm mb-2">Tipo de Usuario</label>
              <select
                v-model="formData.role"
                class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
              >
                <option value="patient">Paciente</option>
                <option value="doctor">Oncólogo/Especialista</option>
                <option value="manager">Gerente Médico</option>
              </select>
            </div>

            <!-- Phone -->
            <div>
              <label class="block text-sm mb-2">Teléfono (opcional)</label>
              <div class="relative">
                <Phone class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <input
                  type="tel"
                  v-model="formData.phone"
                  class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                  placeholder="+34 600 000 000"
                />
              </div>
            </div>

            <!-- Specialization (doctors only) -->
            <div v-if="formData.role === 'doctor'">
              <label class="block text-sm mb-2">Especialización</label>
              <div class="relative">
                <Stethoscope class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <input
                  type="text"
                  v-model="formData.specialization"
                  class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                  placeholder="Ej: Oncología Mamaria"
                />
              </div>
            </div>
          </template>

          <!-- Error Message -->
          <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-800">{{ error }}</p>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full py-3 bg-gradient-to-r from-pink-600 to-purple-600 text-white rounded-lg hover:from-pink-700 hover:to-purple-700 transition-all font-medium"
          >
            {{ isLogin ? 'Iniciar Sesión' : 'Crear Cuenta' }}
          </button>
        </form>

        <!-- Demo Credentials -->
        <div v-if="isLogin" class="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p class="text-xs font-medium text-blue-900 mb-2">
            Credenciales de demostración:
          </p>
          <div class="space-y-1 text-xs text-blue-800">
            <p><strong>Gerente:</strong> gerente@alertarosa.com / admin123</p>
            <p><strong>Especialista:</strong> doctor@alertarosa.com / doctor123</p>
            <p><strong>Paciente:</strong> paciente@alertarosa.com / paciente123</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
