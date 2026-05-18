<script setup lang="ts">
import { useAuth } from './app/composables/useAuth'
// We will import and display the appropriate view based on authentication later
// import Auth from './app/components/Auth.vue'
// import DoctorView from './app/components/DoctorView.vue'
// import PatientViewNew from './app/components/PatientViewNew.vue'
// import ManagerViewNew from './app/components/ManagerViewNew.vue'

const { user, loading } = useAuth()
</script>

<template>
  <div v-if="loading">Cargando...</div>
  <div v-else-if="!user">
    <!-- <Auth /> -->
    <p>Auth Component goes here</p>
  </div>
  <div v-else-if="user.role === 'patient'">
    <!-- <PatientViewNew /> -->
    <p>Patient View goes here</p>
  </div>
  <div v-else-if="user.role === 'manager'">
    <!-- <ManagerViewNew /> -->
    <p>Manager View goes here</p>
  </div>
  <div v-else>
    <!-- <DoctorView /> -->
    <p>Doctor View goes here</p>
  </div>
</template>
