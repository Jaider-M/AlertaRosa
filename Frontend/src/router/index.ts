import { createRouter, createWebHistory } from 'vue-router'
import { useAuth, initAuth } from '../app/composables/useAuth'

import Auth from '../app/components/Auth.vue'
import DoctorView from '../app/components/DoctorView.vue'
import PatientViewNew from '../app/components/PatientViewNew.vue'
import ManagerViewNew from '../app/components/ManagerViewNew.vue'
import Dashboard from '../app/components/Dashboard.vue'
import Analytics from '../app/components/Analytics.vue'
import DiagnosisModule from '../app/components/DiagnosisModule.vue'
import Education from '../app/components/Education.vue'
import PatientAlerts from '../app/components/PatientAlerts.vue'
import PatientManagement from '../app/components/PatientManagement.vue'
import SymptomTriage from '../app/components/SymptomTriage.vue'

const routes = [
  { path: '/', redirect: '/auth' },
  { path: '/auth', name: 'Auth', component: Auth, meta: { requiresAuth: false } },
  { path: '/doctor', name: 'DoctorView', component: DoctorView, meta: { requiresAuth: true, role: 'doctor' } },
  { path: '/patient', name: 'PatientView', component: PatientViewNew, meta: { requiresAuth: true, role: 'patient' } },
  { path: '/manager', name: 'ManagerView', component: ManagerViewNew, meta: { requiresAuth: true, role: 'manager' } },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/analytics', name: 'Analytics', component: Analytics, meta: { requiresAuth: true } },
  { path: '/diagnosis', name: 'DiagnosisModule', component: DiagnosisModule, meta: { requiresAuth: true } },
  { path: '/education', name: 'Education', component: Education, meta: { requiresAuth: true } },
  { path: '/patient-alerts', name: 'PatientAlerts', component: PatientAlerts, meta: { requiresAuth: true } },
  { path: '/patient-management', name: 'PatientManagement', component: PatientManagement, meta: { requiresAuth: true } },
  { path: '/symptom-triage', name: 'SymptomTriage', component: SymptomTriage, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // Ensure authentication state is initialized before checking routes
  initAuth()
  const { user } = useAuth()

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)
  const isAuthenticated = !!user.value

  if (requiresAuth && !isAuthenticated) {
    next('/auth')
  } else if (to.path === '/auth' && isAuthenticated) {
    // Redirect to default view based on role
    const role = user.value?.role
    if (role === 'patient') next('/patient')
    else if (role === 'manager') next('/manager')
    else next('/doctor')
  } else {
    next()
  }
})

export default router
