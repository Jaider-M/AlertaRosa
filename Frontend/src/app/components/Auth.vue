<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { User, Lock, Mail, Phone, Stethoscope, FileText } from 'lucide-vue-next';
import { useAuth } from '../composables/useAuth';
import type { RegisterData } from '../types';
import logoImg from '../../imports/AlertaRosa.jpeg';

const router = useRouter();
const isLogin = ref(true);
const formData = reactive<RegisterData>({
  email: '',
  password: '',
  name: '',
  role: 'patient',
  phone: '',
  specialization: '',
  registro_medico: '',
});
const error = ref('');
const { login, register } = useAuth();

const handleSubmit = async (e: Event) => {
  e.preventDefault();
  error.value = '';

  try {
    // 1. Lógica de Login
    if (isLogin.value) {
      const result = await login(formData.email, formData.password);
      if (result?.access_token) {
        localStorage.setItem('access_token', result.access_token);
        localStorage.setItem('role', result.role);
        const target = result.role === 'doctor' ? '/doctor' : 
                       result.role === 'manager' ? '/manager' : '/patient';
        window.location.href = target;
      } else {
        error.value = 'Credenciales incorrectas.';
      }
    } 
    // 2. Lógica de REGISTRO (¡ESTO ES LO QUE FALTABA!)
    else {
      const success = await register(formData);
      if (success) {
        alert("¡Registro exitoso! Ahora puedes iniciar sesión.");
        isLogin.value = true; // Cambiamos a la vista de login automáticamente
      } else {
        error.value = 'El registro falló. Verifica los datos.';
      }
    }
  } catch (err) {
    console.error("Error crítico:", err);
    error.value = 'Error al conectar con el servidor';
  }
};
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50 flex items-center justify-center p-6">
    <div class="w-full max-w-md">
      <div class="text-center mb-8 transition-all duration-500">
        <img :src="logoImg" alt="AlertaRosa" class="w-48 h-auto mx-auto mb-4" />
        <p class="text-muted-foreground">Detección temprana, vida salvada</p>
      </div>

      <div class="bg-white rounded-2xl shadow-xl p-8">
        <div class="flex gap-2 mb-6 p-1 bg-muted rounded-lg">
          <button @click="isLogin = true" :class="['flex-1 py-2 px-4 rounded-md transition-all', isLogin ? 'bg-white shadow-sm font-medium' : 'text-muted-foreground']">
            Iniciar Sesión
          </button>
          <button @click="isLogin = false" :class="['flex-1 py-2 px-4 rounded-md transition-all', !isLogin ? 'bg-white shadow-sm font-medium' : 'text-muted-foreground']">
            Registro
          </button>
        </div>

        <form @submit="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm mb-2">Email</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input type="email" v-model="formData.email" class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500" required />
            </div>
          </div>

          <div v-if="!isLogin">
            <label class="block text-sm mb-2">Nombre Completo</label>
            <div class="relative">
              <User class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input type="text" v-model="formData.name" class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500" required />
            </div>
          </div>

          <div>
            <label class="block text-sm mb-2">Contraseña</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input type="password" v-model="formData.password" class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500" required />
            </div>
          </div>

          <div v-if="!isLogin">
            <label class="block text-sm mb-2">Tipo de Usuario</label>
            <select v-model="formData.role" class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500">
              <option value="patient">Paciente</option>
              <option value="doctor">Oncólogo/Especialista</option>
              <option value="manager">Gerente Médico</option>
            </select>
          </div>

          <div v-if="!isLogin && formData.role !== 'patient'">
            <label class="block text-sm mb-2">Registro Médico</label>
            <div class="relative">
              <FileText class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input type="text" v-model="formData.registro_medico" class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500" required />
            </div>
          </div>

          <div v-if="!isLogin && formData.role === 'doctor'">
            <label class="block text-sm mb-2">Especialidad</label>
            <div class="relative">
              <Stethoscope class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input type="text" v-model="formData.specialization" class="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500" required />
            </div>
          </div>

          <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-800">{{ error }}</p>
          </div>

          <button type="submit" class="w-full py-3 bg-gradient-to-r from-pink-600 to-purple-600 text-white rounded-lg hover:from-pink-700 hover:to-purple-700 transition-all font-medium">
            {{ isLogin ? 'Iniciar Sesión' : 'Crear Cuenta' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>