<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { Users, Search, Mail, Phone, Trash2, Edit, Shield, LogOut, BarChart3, UserPlus, X } from 'lucide-vue-next';
import type { User, UserRole } from '../types';
import { useAuth } from '../composables/useAuth';
import Analytics from './Analytics.vue';
import logoImg from '../../imports/AlertaRosa.jpeg';
<<<<<<< HEAD
=======
import axios from 'axios';
>>>>>>> develop

type Tab = 'users' | 'analytics';

const { user, logout } = useAuth();

const activeTab = ref<Tab>('users');
const users = ref<User[]>([]);
const searchTerm = ref('');
const filterRole = ref<'all' | 'patient' | 'doctor'>('all');
const selectedUser = ref<User | null>(null);
const isEditMode = ref(false);
const isCreateMode = ref(false);

const formData = ref({
  name: '',
  email: '',
  phone: '',
  role: 'patient' as UserRole,
  specialization: '',
  password: '',
});

const tabs = [
  { id: 'users' as Tab, label: 'Gestión de Usuarios', icon: Users },
  { id: 'analytics' as Tab, label: 'Analíticas', icon: BarChart3 },
];

<<<<<<< HEAD
const loadUsers = () => {
  const usersData = localStorage.getItem('users');
  const allUsers: User[] = usersData ? JSON.parse(usersData) : [];
  users.value = allUsers.filter((u) => u.role !== 'manager');
=======
const loadUsers = async () => {
  try {
    const token = localStorage.getItem('token');
    
    // Llamada al backend
    const response = await axios.get('http://127.0.0.1:8000/api/admin/all-users', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    // Mapeo correcto de los datos que vienen de MongoDB a tu tipo 'User'
    users.value = response.data.map((u: any) => ({
      id: u.id,
      name: u.username, // Ajusta según el campo que llega del backend
      email: u.email,
      // Traducción de los roles de la base de datos a los que espera tu frontend
      role: u.role === 'Administrador' ? 'manager' : 
            u.role === 'Especialista' ? 'doctor' : 'patient',
      is_active: u.is_active
    }));
    
  } catch (error) {
    console.error("Error al cargar usuarios desde el servidor:", error);
    // Opcional: mostrar un aviso al usuario
    alert("No se pudieron cargar los usuarios. Revisa tu conexión.");
  }
>>>>>>> develop
};

onMounted(() => {
  loadUsers();
});

<<<<<<< HEAD
const deleteUser = (userId: string) => {
  if (confirm('¿Está seguro de eliminar este usuario?')) {
    const usersData = localStorage.getItem('users');
    const allUsers = usersData ? JSON.parse(usersData) : [];
    const updatedUsers = allUsers.filter((u: any) => u.id !== userId);
    localStorage.setItem('users', JSON.stringify(updatedUsers));
    loadUsers();
    selectedUser.value = null;
=======
const deleteUser = async (userId: string) => {
  if (confirm('¿Está seguro de eliminar este usuario de la base de datos?')) {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://127.0.0.1:8000/api/admin/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Si la petición tuvo éxito, recargamos la lista desde el servidor
      await loadUsers(); 
      selectedUser.value = null;
      alert("Usuario eliminado con éxito");
    } catch (error) {
      console.error("Error al eliminar usuario:", error);
      alert("No se pudo eliminar el usuario");
    }
>>>>>>> develop
  }
};

const handleEditUser = (userToEdit: User) => {
  formData.value = {
    name: userToEdit.name,
    email: userToEdit.email,
    phone: userToEdit.phone || '',
    role: userToEdit.role,
    specialization: userToEdit.specialization || '',
    password: '',
  };
  isEditMode.value = true;
  isCreateMode.value = false;
};

const handleCreateUser = () => {
  formData.value = {
    name: '', email: '', phone: '', role: 'patient', specialization: '', password: '',
  };
  isCreateMode.value = true;
  isEditMode.value = false;
  selectedUser.value = null;
};

<<<<<<< HEAD
const handleSaveUser = () => {
  const usersData = localStorage.getItem('users');
  const allUsers = usersData ? JSON.parse(usersData) : [];

  if (isEditMode.value && selectedUser.value) {
    const updatedUsers = allUsers.map((u: any) => {
      if (u.id === selectedUser.value?.id) {
        return {
          ...u,
          name: formData.value.name,
          email: formData.value.email,
          phone: formData.value.phone,
          role: formData.value.role,
          specialization: formData.value.specialization,
          ...(formData.value.password && { password: formData.value.password }),
        };
      }
      return u;
    });
    localStorage.setItem('users', JSON.stringify(updatedUsers));
    isEditMode.value = false;
    selectedUser.value = null;
  } else if (isCreateMode.value) {
    if (!formData.value.name || !formData.value.email || !formData.value.password) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }
    if (allUsers.some((u: any) => u.email === formData.value.email)) {
      alert('El email ya está registrado');
      return;
    }
    const newUser = {
      id: `U${Date.now()}`,
      ...formData.value,
      registrationDate: new Date().toISOString(),
    };
    allUsers.push(newUser);
    localStorage.setItem('users', JSON.stringify(allUsers));
    isCreateMode.value = false;
  }
  loadUsers();
=======
const handleSaveUser = async () => {
  if (!selectedUser.value) return;
  
  try {
    const token = localStorage.getItem('token');

    // Mapeo de valores de Frontend a Backend
    const roleMap: Record<string, string> = {
      'manager': 'Administrador',
      'doctor': 'Especialista',
      'patient': 'Paciente'
    };

    const payload = {
      username: formData.value.email, // Ajusta si necesitas enviar 'name'
      email: formData.value.email,
      role: roleMap[formData.value.role] || 'Paciente', // <--- AQUÍ ESTÁ LA MAGIA
      nombre_completo: formData.value.name,
      phone: formData.value.phone,
      especialidad: formData.value.specialization
    };

    await axios.put(
      `http://127.0.0.1:8000/api/admin/users/${selectedUser.value.id}`, 
      payload, 
      { headers: { Authorization: `Bearer ${token}` } }
    );
    
    alert("Usuario actualizado correctamente");
    isEditMode.value = false;
    await loadUsers();
  } catch (error: any) {
    console.error("Detalle del error:", JSON.stringify(error.response?.data, null, 2));
    alert("Error al actualizar. Revisa la consola.");
  }
>>>>>>> develop
};

const handleCancel = () => {
  isEditMode.value = false;
  isCreateMode.value = false;
  formData.value = { name: '', email: '', phone: '', role: 'patient', specialization: '', password: '' };
};

const filteredUsers = computed(() => {
  return users.value.filter((u) => {
    const matchesSearch =
      u.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      u.email.toLowerCase().includes(searchTerm.value.toLowerCase());
    const matchesFilter = filterRole.value === 'all' || u.role === filterRole.value;
    return matchesSearch && matchesFilter;
  });
});

const patientCount = computed(() => users.value.filter((u) => u.role === 'patient').length);
const doctorCount = computed(() => users.value.filter((u) => u.role === 'doctor').length);

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
};
</script>

<template>
  <div class="min-h-screen bg-background">
    <!-- Top Header -->
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
            <div class="text-right">
              <p class="text-sm font-medium">{{ user?.name }}</p>
              <p class="text-xs text-muted-foreground">
                {{ user?.role === 'manager' ? 'Gerente Médico' : 'Administrador' }}
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
          <div v-if="activeTab === tab.id" class="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500"></div>
        </button>
      </nav>
    </header>

    <main class="p-6">
      <transition name="fade" mode="out-in">
        <div :key="activeTab">
          <Analytics v-if="activeTab === 'analytics'" />
          
          <div v-else-if="activeTab === 'users'" class="space-y-6">
            <!-- Welcome Header -->
            <div class="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg p-6 text-white">
              <div class="flex items-start justify-between">
                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center">
                    <Shield class="w-6 h-6" />
                  </div>
                  <div>
                    <h2 class="text-2xl font-semibold mb-2">Gestión de Usuarios</h2>
                    <p class="text-indigo-100">Administración completa de pacientes y especialistas</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-white border border-border rounded-lg p-5">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm text-muted-foreground mb-1">Total Usuarios</p>
                    <p class="text-3xl font-semibold">{{ users.length }}</p>
                  </div>
                  <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
                    <Users class="w-6 h-6 text-white" />
                  </div>
                </div>
              </div>

              <div class="bg-white border border-border rounded-lg p-5">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm text-muted-foreground mb-1">Pacientes</p>
                    <p class="text-3xl font-semibold">{{ patientCount }}</p>
                  </div>
                  <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center">
                    <Users class="w-6 h-6 text-white" />
                  </div>
                </div>
              </div>

              <div class="bg-white border border-border rounded-lg p-5">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm text-muted-foreground mb-1">Especialistas</p>
                    <p class="text-3xl font-semibold">{{ doctorCount }}</p>
                  </div>
                  <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center">
                    <Users class="w-6 h-6 text-white" />
                  </div>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <!-- User List -->
              <div class="lg:col-span-1 space-y-4">
                <div class="bg-white border border-border rounded-lg p-4">
                  <!-- Search -->
                  <div class="relative flex-1 mb-4">
                    <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <input
                      type="text"
                      placeholder="Buscar usuario..."
                      v-model="searchTerm"
                      class="pl-10 pr-4 py-2 w-full bg-white border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors"
                    />
                  </div>

                  <!-- Filters -->
                  <div class="flex gap-2 mb-4">
                    <button
                      v-for="role in ['all', 'patient', 'doctor'] as const"
                      :key="role"
                      @click="filterRole = role"
                      :class="`px-3 py-1.5 text-xs rounded-lg transition-colors ${
                        filterRole === role
                          ? 'bg-indigo-600 text-white'
                          : 'bg-muted text-muted-foreground hover:bg-muted/80'
                      }`"
                    >
                      {{ role === 'all' ? 'Todos' : role === 'patient' ? 'Pacientes' : 'Especialistas' }}
                    </button>
                  </div>

                  <button
                    @click="handleCreateUser"
                    class="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all font-medium mb-4"
                  >
                    <UserPlus class="w-4 h-4" />
                    Crear Nuevo Usuario
                  </button>

                  <div class="text-sm text-muted-foreground mb-2">
                    {{ filteredUsers.length }} usuarios
                  </div>
                </div>

                <!-- User Cards -->
                <div class="space-y-2 max-h-[600px] overflow-y-auto">
                  <button
                    v-for="usr in filteredUsers"
                    :key="usr.id"
                    @click="selectedUser = usr; isEditMode = false; isCreateMode = false;"
                    :class="`w-full text-left p-4 rounded-lg border transition-all ${
                      selectedUser?.id === usr.id
                        ? 'bg-indigo-50 border-indigo-300 shadow-sm'
                        : 'bg-white border-border hover:border-indigo-200 hover:shadow-sm'
                    }`"
                  >
                    <div class="flex items-start justify-between mb-2">
                      <div>
                        <p class="font-medium">{{ usr.name }}</p>
                        <p class="text-xs text-muted-foreground">{{ usr.email }}</p>
                      </div>
                    </div>
                    <div class="flex items-center gap-2">
                      <span
                        :class="`px-2 py-0.5 text-xs rounded-full ${
                          usr.role === 'patient'
                            ? 'bg-pink-100 text-pink-700'
                            : 'bg-purple-100 text-purple-700'
                        }`"
                      >
                        {{ usr.role === 'patient' ? 'Paciente' : 'Especialista' }}
                      </span>
                      <span v-if="usr.specialization" class="text-xs text-muted-foreground">
                        {{ usr.specialization }}
                      </span>
                    </div>
                  </button>
                </div>
              </div>

              <!-- User Details / Edit Form -->
              <div class="lg:col-span-2">
                <div v-if="isEditMode || isCreateMode" class="bg-white border border-border rounded-lg p-6">
                  <div class="flex items-center justify-between mb-6">
                    <h3 class="text-xl font-semibold">
                      {{ isCreateMode ? 'Crear Nuevo Usuario' : 'Editar Usuario' }}
                    </h3>
                    <button @click="handleCancel" class="p-2 hover:bg-muted rounded-lg transition-colors">
                      <X class="w-5 h-5" />
                    </button>
                  </div>

                  <div class="space-y-4">
                    <div>
                      <label class="block text-sm mb-2">Nombre Completo *</label>
                      <input
                        type="text"
                        v-model="formData.name"
                        class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                        required
                      />
                    </div>
                    <div>
                      <label class="block text-sm mb-2">Email *</label>
                      <input
                        type="email"
                        v-model="formData.email"
                        class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                        required
                      />
                    </div>

                    <div v-if="isCreateMode">
                      <label class="block text-sm mb-2">Contraseña *</label>
                      <input
                        type="password"
                        v-model="formData.password"
                        class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                        required
                      />
                    </div>

                    <div v-if="isEditMode">
                      <label class="block text-sm mb-2">Nueva Contraseña (dejar vacío para no cambiar)</label>
                      <input
                        type="password"
                        v-model="formData.password"
                        class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label class="block text-sm mb-2">Teléfono</label>
                      <input
                        type="tel"
                        v-model="formData.phone"
                        class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label class="block text-sm mb-2">Rol *</label>
                      <select
                        v-model="formData.role"
                        class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                      >
                        <option value="patient">Paciente</option>
                        <option value="doctor">Especialista</option>
                      </select>
                    </div>

                    <div v-if="formData.role === 'doctor'">
                      <label class="block text-sm mb-2">Especialización</label>
                      <input
                        type="text"
                        v-model="formData.specialization"
                        class="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                        placeholder="Ej: Oncología Mamaria"
                      />
                    </div>

                    <div class="flex gap-3 pt-4">
                      <button
                        @click="handleSaveUser"
                        class="flex-1 px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all font-medium"
                      >
                        {{ isCreateMode ? 'Crear Usuario' : 'Guardar Cambios' }}
                      </button>
                      <button
                        @click="handleCancel"
                        class="flex-1 px-4 py-3 border border-border rounded-lg hover:bg-muted/50 transition-colors"
                      >
                        Cancelar
                      </button>
                    </div>
                  </div>
                </div>

                <div v-else-if="selectedUser" class="space-y-6">
                  <!-- Header -->
                  <div class="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg p-6 text-white">
                    <div class="flex items-start justify-between">
                      <div class="flex items-start gap-4">
                        <div class="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                          <Users class="w-8 h-8" />
                        </div>
                        <div>
                          <h2 class="text-2xl font-semibold mb-1">{{ selectedUser.name }}</h2>
                          <p class="text-indigo-100">ID: {{ selectedUser.id }}</p>
                        </div>
                      </div>
                      <span
                        :class="`px-3 py-1.5 rounded-lg text-sm font-medium border border-white/30 ${
                          selectedUser.role === 'patient' ? 'bg-pink-500/20' : 'bg-purple-500/20'
                        }`"
                      >
                        {{ selectedUser.role === 'patient' ? 'Paciente' : 'Especialista' }}
                      </span>
                    </div>
                  </div>

                  <!-- Contact Information -->
                  <div class="bg-white border border-border rounded-lg p-6">
                    <h3 class="font-semibold mb-4">Información de Contacto</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                          <Mail class="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                          <p class="text-xs text-muted-foreground">Email</p>
                          <p class="font-medium">{{ selectedUser.email }}</p>
                        </div>
                      </div>
                      <div v-if="selectedUser.phone" class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                          <Phone class="w-5 h-5 text-purple-600" />
                        </div>
                        <div>
                          <p class="text-xs text-muted-foreground">Teléfono</p>
                          <p class="font-medium">{{ selectedUser.phone }}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Additional Info -->
                  <div class="bg-white border border-border rounded-lg p-6">
                    <h3 class="font-semibold mb-4">Información Adicional</h3>
                    <div class="space-y-3">
                      <div>
                        <p class="text-sm text-muted-foreground mb-1">Fecha de Registro</p>
                        <p class="font-medium">{{ formatDate(selectedUser.registrationDate!) }}</p>
                      </div>
                      <div v-if="selectedUser.specialization">
                        <p class="text-sm text-muted-foreground mb-1">Especialización</p>
                        <p class="font-medium">{{ selectedUser.specialization }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Actions -->
                  <div class="flex gap-3">
                    <button
                      @click="handleEditUser(selectedUser)"
                      class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                    >
                      <Edit class="w-4 h-4" />
                      Editar Usuario
                    </button>
                    <button
                      @click="deleteUser(selectedUser.id)"
                      class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-red-50 border border-red-200 text-red-700 rounded-lg hover:bg-red-100 transition-colors"
                    >
                      <Trash2 class="w-4 h-4" />
                      Eliminar Usuario
                    </button>
                  </div>
                </div>

                <div v-else class="h-full flex items-center justify-center bg-white border border-border rounded-lg p-12">
                  <div class="text-center">
                    <div class="w-16 h-16 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
                      <Users class="w-8 h-8 text-muted-foreground" />
                    </div>
                    <p class="text-muted-foreground">Selecciona un usuario para ver sus detalles</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
