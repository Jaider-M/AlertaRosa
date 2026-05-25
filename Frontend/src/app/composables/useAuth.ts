import { ref, readonly } from 'vue';
import type { RegisterData } from '../types';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token && token !== 'null') {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

const user = ref<any | null>(null);

export function useAuth() {
  async function login(email: string, password: string): Promise<any | null> {
    try {
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);

      const response = await api.post('/auth/login', params);
      const token = response.data.access_token;

      const decoded: any = jwtDecode(token);
      const backendRole = decoded.role || 'Paciente';

      let frontendRole = 'patient';
      if (backendRole === 'Administrador') frontendRole = 'manager';
      else if (backendRole === 'Especialista') frontendRole = 'doctor';

      localStorage.setItem('access_token', token);
      localStorage.setItem('role', frontendRole);
      user.value = { email, role: frontendRole };

      return { access_token: token, role: frontendRole };
    } catch (error: any) {
      return null;
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
        full_name: userData.name || "Usuario",
        nombre_completo: userData.name || "Usuario",
        phone: userData.phone || "0000000000",
        especialidad: userData.specialization || "General",
        registro_medico: userData.registro_medico || "RM-000",
        medical_record_number: "HC-" + Date.now().toString().slice(-6),
        address: "Pendiente"
      };

      await api.post('/auth/register', payload);
      return true;
    } catch (error: any) {
      if (error.response && error.response.data) {
        console.error("DETALLE DEL ERROR 422:", JSON.stringify(error.response.data, null, 2));
      }
      return false;
    }
  }

  function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');

    localStorage.clear();

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