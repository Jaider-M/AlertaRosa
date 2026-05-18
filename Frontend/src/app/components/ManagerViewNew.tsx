import { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { Users, Search, Mail, Phone, Trash2, Edit, Shield, LogOut, BarChart3, UserPlus, X } from 'lucide-react';
import { User, UserRole } from '../types';
import { useAuth } from '../context/AuthContext';
import { Analytics } from './Analytics';
import logoImg from '../../imports/AlertaRosa.jpeg';

type Tab = 'users' | 'analytics';

export function ManagerViewNew() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState<Tab>('users');
  const [users, setUsers] = useState<User[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState<'all' | 'patient' | 'doctor'>('all');
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isEditMode, setIsEditMode] = useState(false);
  const [isCreateMode, setIsCreateMode] = useState(false);
  const [formData, setFormData] = useState({
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

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = () => {
    const usersData = localStorage.getItem('users');
    const allUsers: User[] = usersData ? JSON.parse(usersData) : [];
    const filteredUsers = allUsers.filter((u) => u.role !== 'manager');
    setUsers(filteredUsers);
  };

  const deleteUser = (userId: string) => {
    if (confirm('¿Está seguro de eliminar este usuario?')) {
      const usersData = localStorage.getItem('users');
      const allUsers = usersData ? JSON.parse(usersData) : [];
      const updatedUsers = allUsers.filter((u: any) => u.id !== userId);
      localStorage.setItem('users', JSON.stringify(updatedUsers));
      loadUsers();
      setSelectedUser(null);
    }
  };

  const handleEditUser = (userToEdit: User) => {
    setFormData({
      name: userToEdit.name,
      email: userToEdit.email,
      phone: userToEdit.phone || '',
      role: userToEdit.role,
      specialization: userToEdit.specialization || '',
      password: '',
    });
    setIsEditMode(true);
    setIsCreateMode(false);
  };

  const handleCreateUser = () => {
    setFormData({
      name: '',
      email: '',
      phone: '',
      role: 'patient',
      specialization: '',
      password: '',
    });
    setIsCreateMode(true);
    setIsEditMode(false);
    setSelectedUser(null);
  };

  const handleSaveUser = () => {
    const usersData = localStorage.getItem('users');
    const allUsers = usersData ? JSON.parse(usersData) : [];

    if (isEditMode && selectedUser) {
      const updatedUsers = allUsers.map((u: any) => {
        if (u.id === selectedUser.id) {
          return {
            ...u,
            name: formData.name,
            email: formData.email,
            phone: formData.phone,
            role: formData.role,
            specialization: formData.specialization,
            ...(formData.password && { password: formData.password }),
          };
        }
        return u;
      });
      localStorage.setItem('users', JSON.stringify(updatedUsers));
      setIsEditMode(false);
      setSelectedUser(null);
    } else if (isCreateMode) {
      if (!formData.name || !formData.email || !formData.password) {
        alert('Por favor complete todos los campos requeridos');
        return;
      }

      if (allUsers.some((u: any) => u.email === formData.email)) {
        alert('El email ya está registrado');
        return;
      }

      const newUser = {
        id: `U${Date.now()}`,
        ...formData,
        registrationDate: new Date().toISOString(),
      };

      allUsers.push(newUser);
      localStorage.setItem('users', JSON.stringify(allUsers));
      setIsCreateMode(false);
    }

    loadUsers();
  };

  const handleCancel = () => {
    setIsEditMode(false);
    setIsCreateMode(false);
    setFormData({
      name: '',
      email: '',
      phone: '',
      role: 'patient',
      specialization: '',
      password: '',
    });
  };

  const filteredUsers = users.filter((user) => {
    const matchesSearch =
      user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterRole === 'all' || user.role === filterRole;
    return matchesSearch && matchesFilter;
  });

  const patientCount = users.filter((u) => u.role === 'patient').length;
  const doctorCount = users.filter((u) => u.role === 'doctor').length;

  return (
    <div className="min-h-screen bg-background">
      {/* Top Header */}
      <header className="border-b border-border bg-white sticky top-0 z-50">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <img src={logoImg} alt="AlertaRosa" className="h-12 w-auto" />
              <div>
                <h1 className="text-xl font-semibold">AlertaRosa</h1>
                <p className="text-xs text-muted-foreground">
                  Detección temprana, vida salvada
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium">{user?.name}</p>
                <p className="text-xs text-muted-foreground">Gerente Médico</p>
              </div>
              <button
                onClick={logout}
                className="p-2 hover:bg-muted rounded-lg transition-colors"
                title="Cerrar sesión"
              >
                <LogOut className="w-5 h-5 text-muted-foreground" />
              </button>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="px-6 flex gap-1 border-t border-border">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className="relative px-4 py-3 text-sm font-medium transition-colors hover:text-foreground"
                style={{
                  color:
                    activeTab === tab.id
                      ? 'var(--foreground)'
                      : 'var(--muted-foreground)',
                }}
              >
                <div className="flex items-center gap-2">
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </div>
                {activeTab === tab.id && (
                  <motion.div
                    layoutId="activeTabManager"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500"
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                )}
              </button>
            );
          })}
        </nav>
      </header>

      <main className="p-6">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'analytics' && <Analytics />}

          {activeTab === 'users' && (
            <div className="space-y-6">
              {/* Welcome Header */}
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg p-6 text-white">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center">
                      <Shield className="w-6 h-6" />
                    </div>
                    <div>
                      <h2 className="text-2xl font-semibold mb-2">
                        Gestión de Usuarios
                      </h2>
                      <p className="text-indigo-100">
                        Administración completa de pacientes y especialistas
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white border border-border rounded-lg p-5">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">
                        Total Usuarios
                      </p>
                      <p className="text-3xl font-semibold">{users.length}</p>
                    </div>
                    <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
                      <Users className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </div>

                <div className="bg-white border border-border rounded-lg p-5">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">
                        Pacientes
                      </p>
                      <p className="text-3xl font-semibold">{patientCount}</p>
                    </div>
                    <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center">
                      <Users className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </div>

                <div className="bg-white border border-border rounded-lg p-5">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">
                        Especialistas
                      </p>
                      <p className="text-3xl font-semibold">{doctorCount}</p>
                    </div>
                    <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center">
                      <Users className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* User List */}
                <div className="lg:col-span-1 space-y-4">
                  <div className="bg-white border border-border rounded-lg p-4">
                    {/* Search */}
                    <div className="relative mb-4">
                      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                      <input
                        type="text"
                        placeholder="Buscar usuario..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full pl-9 pr-3 py-2 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    {/* Filters */}
                    <div className="flex gap-2 mb-4">
                      {(['all', 'patient', 'doctor'] as const).map((role) => (
                        <button
                          key={role}
                          onClick={() => setFilterRole(role)}
                          className={`px-3 py-1.5 text-xs rounded-lg transition-colors ${
                            filterRole === role
                              ? 'bg-indigo-600 text-white'
                              : 'bg-muted text-muted-foreground hover:bg-muted/80'
                          }`}
                        >
                          {role === 'all'
                            ? 'Todos'
                            : role === 'patient'
                            ? 'Pacientes'
                            : 'Especialistas'}
                        </button>
                      ))}
                    </div>

                    <button
                      onClick={handleCreateUser}
                      className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all font-medium mb-4"
                    >
                      <UserPlus className="w-4 h-4" />
                      Crear Nuevo Usuario
                    </button>

                    <div className="text-sm text-muted-foreground mb-2">
                      {filteredUsers.length} usuarios
                    </div>
                  </div>

                  {/* User Cards */}
                  <div className="space-y-2 max-h-[600px] overflow-y-auto">
                    {filteredUsers.map((usr) => (
                      <button
                        key={usr.id}
                        onClick={() => {
                          setSelectedUser(usr);
                          setIsEditMode(false);
                          setIsCreateMode(false);
                        }}
                        className={`w-full text-left p-4 rounded-lg border transition-all ${
                          selectedUser?.id === usr.id
                            ? 'bg-indigo-50 border-indigo-300 shadow-sm'
                            : 'bg-white border-border hover:border-indigo-200 hover:shadow-sm'
                        }`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <p className="font-medium">{usr.name}</p>
                            <p className="text-xs text-muted-foreground">
                              {usr.email}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2 py-0.5 text-xs rounded-full ${
                              usr.role === 'patient'
                                ? 'bg-pink-100 text-pink-700'
                                : 'bg-purple-100 text-purple-700'
                            }`}
                          >
                            {usr.role === 'patient' ? 'Paciente' : 'Especialista'}
                          </span>
                          {usr.specialization && (
                            <span className="text-xs text-muted-foreground">
                              {usr.specialization}
                            </span>
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* User Details / Edit Form */}
                <div className="lg:col-span-2">
                  {isEditMode || isCreateMode ? (
                    <div className="bg-white border border-border rounded-lg p-6">
                      <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-semibold">
                          {isCreateMode ? 'Crear Nuevo Usuario' : 'Editar Usuario'}
                        </h3>
                        <button
                          onClick={handleCancel}
                          className="p-2 hover:bg-muted rounded-lg transition-colors"
                        >
                          <X className="w-5 h-5" />
                        </button>
                      </div>

                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm mb-2">
                            Nombre Completo *
                          </label>
                          <input
                            type="text"
                            value={formData.name}
                            onChange={(e) =>
                              setFormData({ ...formData, name: e.target.value })
                            }
                            className="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                            required
                          />
                        </div>

                        <div>
                          <label className="block text-sm mb-2">Email *</label>
                          <input
                            type="email"
                            value={formData.email}
                            onChange={(e) =>
                              setFormData({ ...formData, email: e.target.value })
                            }
                            className="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                            required
                          />
                        </div>

                        {isCreateMode && (
                          <div>
                            <label className="block text-sm mb-2">
                              Contraseña *
                            </label>
                            <input
                              type="password"
                              value={formData.password}
                              onChange={(e) =>
                                setFormData({
                                  ...formData,
                                  password: e.target.value,
                                })
                              }
                              className="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                              required
                            />
                          </div>
                        )}

                        {isEditMode && (
                          <div>
                            <label className="block text-sm mb-2">
                              Nueva Contraseña (dejar vacío para no cambiar)
                            </label>
                            <input
                              type="password"
                              value={formData.password}
                              onChange={(e) =>
                                setFormData({
                                  ...formData,
                                  password: e.target.value,
                                })
                              }
                              className="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                            />
                          </div>
                        )}

                        <div>
                          <label className="block text-sm mb-2">Teléfono</label>
                          <input
                            type="tel"
                            value={formData.phone}
                            onChange={(e) =>
                              setFormData({ ...formData, phone: e.target.value })
                            }
                            className="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                          />
                        </div>

                        <div>
                          <label className="block text-sm mb-2">Rol *</label>
                          <select
                            value={formData.role}
                            onChange={(e) =>
                              setFormData({
                                ...formData,
                                role: e.target.value as UserRole,
                              })
                            }
                            className="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                          >
                            <option value="patient">Paciente</option>
                            <option value="doctor">Especialista</option>
                          </select>
                        </div>

                        {formData.role === 'doctor' && (
                          <div>
                            <label className="block text-sm mb-2">
                              Especialización
                            </label>
                            <input
                              type="text"
                              value={formData.specialization}
                              onChange={(e) =>
                                setFormData({
                                  ...formData,
                                  specialization: e.target.value,
                                })
                              }
                              className="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-indigo-500"
                              placeholder="Ej: Oncología Mamaria"
                            />
                          </div>
                        )}

                        <div className="flex gap-3 pt-4">
                          <button
                            onClick={handleSaveUser}
                            className="flex-1 px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all font-medium"
                          >
                            {isCreateMode ? 'Crear Usuario' : 'Guardar Cambios'}
                          </button>
                          <button
                            onClick={handleCancel}
                            className="flex-1 px-4 py-3 border border-border rounded-lg hover:bg-muted/50 transition-colors"
                          >
                            Cancelar
                          </button>
                        </div>
                      </div>
                    </div>
                  ) : selectedUser ? (
                    <div className="space-y-6">
                      {/* Header */}
                      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg p-6 text-white">
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-4">
                            <div className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                              <Users className="w-8 h-8" />
                            </div>
                            <div>
                              <h2 className="text-2xl font-semibold mb-1">
                                {selectedUser.name}
                              </h2>
                              <p className="text-indigo-100">
                                ID: {selectedUser.id}
                              </p>
                            </div>
                          </div>
                          <span
                            className={`px-3 py-1.5 rounded-lg text-sm font-medium border border-white/30 ${
                              selectedUser.role === 'patient'
                                ? 'bg-pink-500/20'
                                : 'bg-purple-500/20'
                            }`}
                          >
                            {selectedUser.role === 'patient'
                              ? 'Paciente'
                              : 'Especialista'}
                          </span>
                        </div>
                      </div>

                      {/* Contact Information */}
                      <div className="bg-white border border-border rounded-lg p-6">
                        <h3 className="font-semibold mb-4">
                          Información de Contacto
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                              <Mail className="w-5 h-5 text-blue-600" />
                            </div>
                            <div>
                              <p className="text-xs text-muted-foreground">
                                Email
                              </p>
                              <p className="font-medium">{selectedUser.email}</p>
                            </div>
                          </div>
                          {selectedUser.phone && (
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                                <Phone className="w-5 h-5 text-purple-600" />
                              </div>
                              <div>
                                <p className="text-xs text-muted-foreground">
                                  Teléfono
                                </p>
                                <p className="font-medium">{selectedUser.phone}</p>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Additional Info */}
                      <div className="bg-white border border-border rounded-lg p-6">
                        <h3 className="font-semibold mb-4">
                          Información Adicional
                        </h3>
                        <div className="space-y-3">
                          <div>
                            <p className="text-sm text-muted-foreground mb-1">
                              Fecha de Registro
                            </p>
                            <p className="font-medium">
                              {new Date(
                                selectedUser.registrationDate
                              ).toLocaleDateString('es-ES', {
                                day: 'numeric',
                                month: 'long',
                                year: 'numeric',
                              })}
                            </p>
                          </div>
                          {selectedUser.specialization && (
                            <div>
                              <p className="text-sm text-muted-foreground mb-1">
                                Especialización
                              </p>
                              <p className="font-medium">
                                {selectedUser.specialization}
                              </p>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex gap-3">
                        <button
                          onClick={() => handleEditUser(selectedUser)}
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                        >
                          <Edit className="w-4 h-4" />
                          Editar Usuario
                        </button>
                        <button
                          onClick={() => deleteUser(selectedUser.id)}
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-red-50 border border-red-200 text-red-700 rounded-lg hover:bg-red-100 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                          Eliminar Usuario
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="h-full flex items-center justify-center bg-white border border-border rounded-lg p-12">
                      <div className="text-center">
                        <div className="w-16 h-16 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
                          <Users className="w-8 h-8 text-muted-foreground" />
                        </div>
                        <p className="text-muted-foreground">
                          Selecciona un usuario para ver sus detalles
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </main>
    </div>
  );
}
