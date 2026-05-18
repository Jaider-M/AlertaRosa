import { BookOpen, Video, FileText, AlertCircle, CheckCircle2, Heart, Activity } from 'lucide-react';
import { motion } from 'motion/react';

const educationalResources = [
  {
    category: 'Prevención',
    icon: Heart,
    color: 'pink',
    items: [
      'Autoexamen mamario mensual',
      'Mamografías de detección periódicas',
      'Estilo de vida saludable',
      'Conocer su historial familiar',
    ],
  },
  {
    category: 'Factores de Riesgo',
    icon: AlertCircle,
    color: 'orange',
    items: [
      'Edad avanzada (>40 años)',
      'Antecedentes familiares',
      'Mutaciones genéticas BRCA1/BRCA2',
      'Tejido mamario denso',
      'Exposición hormonal prolongada',
    ],
  },
  {
    category: 'Signos de Alerta',
    icon: Activity,
    color: 'red',
    items: [
      'Bulto o masa en la mama',
      'Cambios en el tamaño o forma',
      'Secreción del pezón',
      'Cambios en la piel (hoyuelos, enrojecimiento)',
      'Dolor persistente en mama o axila',
    ],
  },
  {
    category: 'Detección Temprana',
    icon: CheckCircle2,
    color: 'green',
    items: [
      'Mamografía anual a partir de los 40',
      'Ecografía complementaria si es necesario',
      'Resonancia magnética en casos de alto riesgo',
      'Consultas regulares con especialista',
    ],
  },
];

const videoResources = [
  {
    title: 'Cómo realizar el autoexamen mamario',
    duration: '8:45',
    views: '1.2M',
    thumbnail: 'video1',
  },
  {
    title: 'Entendiendo la mamografía',
    duration: '12:30',
    views: '850K',
    thumbnail: 'video2',
  },
  {
    title: 'Factores de riesgo y prevención',
    duration: '15:20',
    views: '920K',
    thumbnail: 'video3',
  },
  {
    title: 'Opciones de tratamiento modernas',
    duration: '18:15',
    views: '680K',
    thumbnail: 'video4',
  },
];

const downloadableGuides = [
  {
    title: 'Guía Completa de Prevención',
    pages: 24,
    size: '2.3 MB',
    downloads: '45K',
  },
  {
    title: 'Manual de Autoexamen Paso a Paso',
    pages: 12,
    size: '1.8 MB',
    downloads: '62K',
  },
  {
    title: 'Comprensión de Resultados de Mamografía',
    pages: 18,
    size: '3.1 MB',
    downloads: '38K',
  },
  {
    title: 'Apoyo Emocional y Recursos',
    pages: 32,
    size: '4.2 MB',
    downloads: '29K',
  },
];

export function Education() {
  return (
    <div className="max-w-7xl space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-pink-500 to-rose-600 rounded-lg p-6 text-white">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-lg bg-white/20 backdrop-blur-sm flex items-center justify-center flex-shrink-0">
            <BookOpen className="w-6 h-6" />
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-semibold mb-2">Recursos Educativos</h2>
            <p className="text-pink-50">
              Información completa y actualizada sobre prevención, detección y tratamiento del cáncer de mama
            </p>
          </div>
        </div>
      </div>

      {/* Key Information Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {educationalResources.map((resource, index) => {
          const Icon = resource.icon;
          const colorClasses = {
            pink: { bg: 'bg-pink-100', text: 'text-pink-600', border: 'border-pink-200' },
            orange: { bg: 'bg-orange-100', text: 'text-orange-600', border: 'border-orange-200' },
            red: { bg: 'bg-red-100', text: 'text-red-600', border: 'border-red-200' },
            green: { bg: 'bg-green-100', text: 'text-green-600', border: 'border-green-200' },
          };
          const colors = colorClasses[resource.color as keyof typeof colorClasses];

          return (
            <motion.div
              key={resource.category}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`bg-white border ${colors.border} rounded-lg p-5 hover:shadow-md transition-shadow`}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className={`w-10 h-10 rounded-lg ${colors.bg} flex items-center justify-center`}>
                  <Icon className={`w-5 h-5 ${colors.text}`} />
                </div>
                <h3 className="font-semibold">{resource.category}</h3>
              </div>
              <ul className="space-y-2">
                {resource.items.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <CheckCircle2 className={`w-4 h-4 ${colors.text} flex-shrink-0 mt-0.5`} />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
          );
        })}
      </div>

      {/* Video Resources */}
      <div className="bg-white border border-border rounded-lg p-6">
        <div className="flex items-center gap-2 mb-6">
          <Video className="w-5 h-5 text-pink-600" />
          <h3 className="font-semibold">Videos Educativos</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {videoResources.map((video, index) => (
            <div
              key={index}
              className="group cursor-pointer"
            >
              <div className="relative mb-3 rounded-lg overflow-hidden bg-gradient-to-br from-pink-100 to-purple-100 aspect-video flex items-center justify-center hover:from-pink-200 hover:to-purple-200 transition-all">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-12 h-12 rounded-full bg-white/90 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <div className="w-0 h-0 border-l-8 border-l-pink-600 border-t-6 border-t-transparent border-b-6 border-b-transparent ml-1" />
                  </div>
                </div>
                <div className="absolute bottom-2 right-2 px-2 py-0.5 bg-black/70 text-white text-xs rounded">
                  {video.duration}
                </div>
              </div>
              <h4 className="font-medium text-sm mb-1 group-hover:text-pink-600 transition-colors">
                {video.title}
              </h4>
              <p className="text-xs text-muted-foreground">{video.views} visualizaciones</p>
            </div>
          ))}
        </div>
      </div>

      {/* Downloadable Guides */}
      <div className="bg-white border border-border rounded-lg p-6">
        <div className="flex items-center gap-2 mb-6">
          <FileText className="w-5 h-5 text-pink-600" />
          <h3 className="font-semibold">Guías Descargables</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {downloadableGuides.map((guide, index) => (
            <div
              key={index}
              className="flex items-center gap-4 p-4 border border-border rounded-lg hover:border-pink-300 hover:bg-pink-50/50 transition-all cursor-pointer"
            >
              <div className="w-12 h-16 rounded bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <div className="flex-1">
                <h4 className="font-medium mb-1">{guide.title}</h4>
                <div className="flex items-center gap-3 text-xs text-muted-foreground">
                  <span>{guide.pages} páginas</span>
                  <span>·</span>
                  <span>{guide.size}</span>
                  <span>·</span>
                  <span>{guide.downloads} descargas</span>
                </div>
              </div>
              <button className="px-4 py-2 bg-pink-600 text-white text-sm rounded-lg hover:bg-pink-700 transition-colors">
                Descargar
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Self-Examination Guide */}
      <div className="bg-gradient-to-br from-pink-50 to-purple-50 border border-pink-200 rounded-lg p-6">
        <div className="max-w-3xl">
          <h3 className="font-semibold mb-4 text-lg">Guía Rápida: Autoexamen Mamario</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white rounded-lg p-4 border border-pink-200">
              <div className="w-8 h-8 rounded-full bg-pink-600 text-white flex items-center justify-center font-semibold mb-3">
                1
              </div>
              <p className="text-sm font-medium mb-2">Inspección Visual</p>
              <p className="text-xs text-muted-foreground">
                Observe frente al espejo con los brazos a los lados, luego levantados, buscando cambios en forma, tamaño o piel
              </p>
            </div>
            <div className="bg-white rounded-lg p-4 border border-pink-200">
              <div className="w-8 h-8 rounded-full bg-pink-600 text-white flex items-center justify-center font-semibold mb-3">
                2
              </div>
              <p className="text-sm font-medium mb-2">Palpación Acostada</p>
              <p className="text-xs text-muted-foreground">
                Acostada, use movimientos circulares firmes con las yemas de los dedos, cubriendo toda la mama
              </p>
            </div>
            <div className="bg-white rounded-lg p-4 border border-pink-200">
              <div className="w-8 h-8 rounded-full bg-pink-600 text-white flex items-center justify-center font-semibold mb-3">
                3
              </div>
              <p className="text-sm font-medium mb-2">Palpación en la Ducha</p>
              <p className="text-xs text-muted-foreground">
                Con la piel húmeda, es más fácil detectar cambios. Repita los movimientos circulares
              </p>
            </div>
          </div>
          <div className="mt-4 p-4 bg-pink-100 border border-pink-300 rounded-lg">
            <p className="text-sm text-pink-900">
              <strong>Importante:</strong> El autoexamen complementa, pero no reemplaza, las mamografías regulares y consultas médicas.
              Realícelo mensualmente, preferiblemente una semana después de la menstruación.
            </p>
          </div>
        </div>
      </div>

      {/* Support Resources */}
      <div className="bg-white border border-border rounded-lg p-6">
        <h3 className="font-semibold mb-4">Recursos de Apoyo</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="font-medium mb-2 text-blue-900">Línea de Ayuda</h4>
            <p className="text-sm text-blue-800 mb-3">Atención 24/7 por profesionales capacitados</p>
            <p className="font-semibold text-blue-900">900 123 456</p>
          </div>
          <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
            <h4 className="font-medium mb-2 text-purple-900">Grupos de Apoyo</h4>
            <p className="text-sm text-purple-800 mb-3">Comunidades de pacientes y sobrevivientes</p>
            <button className="text-sm text-purple-700 font-medium hover:underline">
              Encontrar un grupo →
            </button>
          </div>
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <h4 className="font-medium mb-2 text-green-900">Asesoramiento</h4>
            <p className="text-sm text-green-800 mb-3">Apoyo psicológico y orientación</p>
            <button className="text-sm text-green-700 font-medium hover:underline">
              Solicitar cita →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
