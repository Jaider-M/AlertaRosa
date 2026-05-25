import { createRouter, createWebHistory } from 'vue-router'
import Auth from '../app/components/Auth.vue'
import DoctorView from '../app/components/DoctorView.vue'
import PatientViewNew from '../app/components/PatientViewNew.vue'
import ManagerViewNew from '../app/components/ManagerViewNew.vue'
import Dashboard from '../app/components/Dashboard.vue'

const routes = [
  { path: '/', redirect: '/auth' },
  { path: '/auth', name: 'Auth', component: Auth, meta: { requiresAuth: false } },
  { path: '/doctor', name: 'DoctorView', component: DoctorView, meta: { requiresAuth: true, role: 'doctor' } },
  { path: '/patient', name: 'PatientView', component: PatientViewNew, meta: { requiresAuth: true, role: 'patient' } },
  { path: '/manager', name: 'ManagerView', component: ManagerViewNew, meta: { requiresAuth: true, role: 'manager' } },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  // CORRECCIÓN: Cambiamos 'token' por 'access_token'
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('role')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth === true)

  if (requiresAuth && !token) return { name: 'Auth' }

  if (to.name === 'Auth' && token) {
    if (role === 'patient') return { name: 'PatientView' }
    if (role === 'manager') return { name: 'ManagerView' }
    return { name: 'DoctorView' }
  }
})

export default router