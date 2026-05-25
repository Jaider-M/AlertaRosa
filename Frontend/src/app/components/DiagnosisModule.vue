<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { Upload, CheckCircle2, FileDown } from 'lucide-vue-next';

// --- Estado ---
const fileInput = ref<HTMLInputElement | null>(null);
const loading = ref(false);
const uploadedImage = ref(false);
const fileName = ref('');

// --- Lógica de IA (Descarga de PDF) ---
const triggerUpload = () => {
  fileInput.value?.click();
};

const uploadDiagnostic = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (!target.files?.length) return;

  const file = target.files[0];
  fileName.value = file.name;
  const formData = new FormData();
  formData.append('file', file);

  loading.value = true;
  try {
    const token = localStorage.getItem('access_token');
    
    const baseUrl = import.meta.env.VITE_API_URL;

    const response = await axios.post(`${baseUrl}/api/diagnostics/upload-standalone`, formData, {
      headers: { 'Authorization': `Bearer ${token}` },
      responseType: 'blob'
    });

    // --- FORMA MÁS ROBUSTA DE DESCARGA ---
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Reporte_${new Date().getTime()}.pdf`;
    document.body.appendChild(link);
    link.click();
    
    // Limpieza
    window.URL.revokeObjectURL(url);
    link.remove();
    
    uploadedImage.value = true;
  } catch (error) {
    console.error("Error completo:", error);
    alert("No se pudo generar el PDF. Revisa la consola.");
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="max-w-4xl space-y-6">
    <div class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg p-6 text-white">
      <h2 class="text-2xl font-semibold mb-2">Análisis de IA Independiente</h2>
      <p class="text-pink-50">Sube una imagen y descarga tu reporte médico automático</p>
    </div>

    <div class="bg-white border border-border rounded-lg p-6">
      <input type="file" ref="fileInput" @change="uploadDiagnostic" class="hidden" accept="image/*" />

      <div class="border-2 border-dashed border-border rounded-lg p-8 text-center transition-all">
        <div v-if="!uploadedImage && !loading" class="space-y-4">
          <div class="w-16 h-16 rounded-full bg-pink-100 flex items-center justify-center mx-auto">
            <Upload class="w-8 h-8 text-pink-600" />
          </div>
          <button @click="triggerUpload" class="px-4 py-2 bg-pink-600 text-white rounded-lg hover:bg-pink-700">
            Subir Foto y Generar Reporte
          </button>
        </div>

        <div v-if="loading" class="py-10">
          <p class="animate-pulse font-medium text-pink-600">Procesando imagen con IA y generando PDF...</p>
        </div>

        <div v-if="uploadedImage && !loading" class="space-y-4">
          <CheckCircle2 class="w-12 h-12 text-green-600 mx-auto" />
          <p class="font-medium text-green-700">¡Reporte generado con éxito!</p>
          <button @click="uploadedImage = false" class="text-sm text-pink-600 hover:underline">Analizar otra imagen</button>
        </div>
      </div>
    </div>
  </div>
</template>