import { useState } from 'react';
import { motion } from 'motion/react';
import { User, Lock, Mail, Phone, Stethoscope } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { UserRole } from '../types';
import logoImg from '../../imports/AlertaRosa.jpeg';

export function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    role: 'patient' as UserRole,
    phone: '',
    specialization: '',
  });
  const [error, setError] = useState('');
  const { login, register } = useAuth();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (isLogin) {
      const success = login(formData.email, formData.password);
      if (!success) {
        setError('Credenciales incorrectas');
      }
    } else {
      if (!formData.email || !formData.password || !formData.name) {
        setError('Por favor complete todos los campos requeridos');
        return;
      }
      const success = register(formData);
      if (!success) {
        setError('El email ya está registrado');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50 flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        {/* Logo */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <img
            src={logoImg}
            alt="AlertaRosa"
            className="w-48 h-auto mx-auto mb-4"
          />
          <p className="text-muted-foreground">
            Detección temprana, vida salvada
          </p>
        </motion.div>

        {/* Form Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl shadow-xl p-8"
        >
          {/* Tabs */}
          <div className="flex gap-2 mb-6 p-1 bg-muted rounded-lg">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-2 px-4 rounded-md transition-all ${
                isLogin
                  ? 'bg-white shadow-sm font-medium'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Iniciar Sesión
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-2 px-4 rounded-md transition-all ${
                !isLogin
                  ? 'bg-white shadow-sm font-medium'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Registro
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label className="block text-sm mb-2">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  className="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                  placeholder="correo@ejemplo.com"
                  required
                />
              </div>
            </div>

            {/* Name (register only) */}
            {!isLogin && (
              <div>
                <label className="block text-sm mb-2">Nombre Completo</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) =>
                      setFormData({ ...formData, name: e.target.value })
                    }
                    className="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                    placeholder="Juan Pérez"
                    required
                  />
                </div>
              </div>
            )}

            {/* Password */}
            <div>
              <label className="block text-sm mb-2">Contraseña</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({ ...formData, password: e.target.value })
                  }
                  className="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            {/* Role (register only) */}
            {!isLogin && (
              <>
                <div>
                  <label className="block text-sm mb-2">Tipo de Usuario</label>
                  <select
                    value={formData.role}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        role: e.target.value as UserRole,
                      })
                    }
                    className="w-full px-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                  >
                    <option value="patient">Paciente</option>
                    <option value="doctor">Oncólogo/Especialista</option>
                    <option value="manager">Gerente Médico</option>
                  </select>
                </div>

                {/* Phone */}
                <div>
                  <label className="block text-sm mb-2">
                    Teléfono (opcional)
                  </label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                    <input
                      type="tel"
                      value={formData.phone}
                      onChange={(e) =>
                        setFormData({ ...formData, phone: e.target.value })
                      }
                      className="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                      placeholder="+34 600 000 000"
                    />
                  </div>
                </div>

                {/* Specialization (doctors only) */}
                {formData.role === 'doctor' && (
                  <div>
                    <label className="block text-sm mb-2">
                      Especialización
                    </label>
                    <div className="relative">
                      <Stethoscope className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                      <input
                        type="text"
                        value={formData.specialization}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            specialization: e.target.value,
                          })
                        }
                        className="w-full pl-10 pr-4 py-2.5 bg-muted rounded-lg border-0 focus:ring-2 focus:ring-pink-500"
                        placeholder="Ej: Oncología Mamaria"
                      />
                    </div>
                  </div>
                )}
              </>
            )}

            {/* Error Message */}
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-pink-600 to-purple-600 text-white rounded-lg hover:from-pink-700 hover:to-purple-700 transition-all font-medium"
            >
              {isLogin ? 'Iniciar Sesión' : 'Crear Cuenta'}
            </button>
          </form>

          {/* Demo Credentials */}
          {isLogin && (
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-xs font-medium text-blue-900 mb-2">
                Credenciales de demostración:
              </p>
              <div className="space-y-1 text-xs text-blue-800">
                <p>
                  <strong>Gerente:</strong> gerente@alertarosa.com / admin123
                </p>
                <p>
                  <strong>Especialista:</strong> doctor@alertarosa.com / doctor123
                </p>
                <p>
                  <strong>Paciente:</strong> paciente@alertarosa.com /
                  paciente123
                </p>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
