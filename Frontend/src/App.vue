<script setup lang="ts">
import { useAuth } from './app/composables/useAuth'

const { loading } = useAuth()
</script>

<template>
  <div v-if="loading" class="min-h-screen flex items-center justify-center">
    <p class="text-lg text-gray-500">Cargando aplicación...</p>
  </div>
  <router-view v-else />
</template>
