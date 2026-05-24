import { ref, readonly } from 'vue';
<<<<<<< HEAD
import type { User, RegisterData } from '../types';
import { initializeDemoUsers } from '../utils/initDemoUsers';
=======
import type { RegisterData } from '../types';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
>>>>>>> develop

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api'
});

const user = ref<any | null>(null);

<<<<<<< HEAD
export function initAuth() {
  if (loading.value) {
    initializeDemoUsers();
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
      user.value = JSON.parse(storedUser);
    }
    loading.value = false;
  }
}

export function useAuth() {
  // Ensure it's initialized when used in components if not done by router yet
  initAuth();
=======
export function useAuth() {
>>>>>>> develop

  async function login(email: string, password: string): Promise<boolean> {
    try {
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);

      const response = await api.post('/auth/login', params);
      const token = response.data.access_token;

      // En tu useAuth.ts dentro del login
      const decoded: any = jwtDecode(token);
      // Ahora decoded.role EXISTIRÁ gracias a los cambios en el backend
      const backendRole = decoded.role || 'Paciente';

      let frontendRole = 'patient';
      if (backendRole === 'Administrador') frontendRole = 'manager';
      else if (backendRole === 'Especialista') frontendRole = 'doctor';
      else frontendRole = 'patient';

      localStorage.setItem('token', token);
      localStorage.setItem('role', frontendRole);
      user.value = { email, role: frontendRole };

      return true;
    } catch (error: any) {
      console.error("Error de login:", error);
      return false;
    }
  }

  async function register(userData: RegisterData): Promise<boolean> {
    try {
      const roleMap: Record<string, string> = {
        'patient': 'Paciente',
        'doctor': 'Especialista',
        'manager': 'Administrador'
      };

      const payload: any = {
        username: userData.email,
        email: userData.email,
        password: userData.password,
        role: roleMap[userData.role] || 'Paciente',
        full_name: userData.name,
        nombre_completo: userData.name,
        phone: userData.phone || null
      };

      if (userData.role === 'doctor' || userData.role === 'manager') {
        payload.registro_medico = userData.registro_medico || "000000";
        payload.especialidad = userData.specialization || "General";
      }

      await api.post('/auth/register', payload);
      return true;
    } catch (error: any) {
      if (error.response && error.response.data) {
        console.error("Error 422:", JSON.stringify(error.response.data, null, 2));
      }
      return false;
    }
  }

  function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    user.value = null;
    window.location.href = '/auth';
  }

  return {
    user: readonly(user),
    login,
    register,
    logout
  };
}