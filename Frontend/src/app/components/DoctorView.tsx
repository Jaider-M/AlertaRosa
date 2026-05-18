import { useState } from 'react';
import { motion } from 'motion/react';
import { Users, Brain, BarChart3, LogOut, Bell } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Dashboard } from './Dashboard';
import { DiagnosisModule } from './DiagnosisModule';
import { PatientManagement } from './PatientManagement';
import { Analytics } from './Analytics';
import { PatientAlerts } from './PatientAlerts';
import logoImg from '../../imports/AlertaRosa.jpeg';

type Tab = 'dashboard' | 'diagnosis' | 'patients' | 'analytics' | 'alerts';

export function DoctorView() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState<Tab>('dashboard');

  const tabs = [
    { id: 'dashboard' as Tab, label: 'Dashboard', icon: BarChart3 },
    { id: 'diagnosis' as Tab, label: 'Diagnóstico', icon: Brain },
    { id: 'patients' as Tab, label: 'Pacientes', icon: Users },
    { id: 'analytics' as Tab, label: 'Analíticas', icon: BarChart3 },
    { id: 'alerts' as Tab, label: 'Alertas', icon: Bell },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-white sticky top-0 z-50">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <img
                src={logoImg}
                alt="AlertaRosa"
                className="h-12 w-auto"
              />
              <div>
                <h1 className="text-xl font-semibold">AlertaRosa</h1>
                <p className="text-xs text-muted-foreground">
                  Detección temprana, vida salvada
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-50 border border-green-200">
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <span className="text-sm text-green-700">Sistema Activo</span>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium">{user?.name}</p>
                <p className="text-xs text-muted-foreground">
                  {user?.specialization || 'Oncología'}
                </p>
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
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-pink-500"
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                )}
              </button>
            );
          })}
        </nav>
      </header>

      {/* Main Content */}
      <main className="p-6">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'diagnosis' && <DiagnosisModule />}
          {activeTab === 'patients' && <PatientManagement />}
          {activeTab === 'analytics' && <Analytics />}
          {activeTab === 'alerts' && <PatientAlerts />}
        </motion.div>
      </main>
    </div>
  );
}
