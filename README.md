# 🌸 AlertaRosa — Plataforma Inteligente para el Diagnóstico Temprano y Gestion integral de Cáncer de Mama

**AlertaRosa** es una plataforma web full-stack y de grado clínico diseñada para optimizar y asistir en el proceso de tamizaje y diagnóstico temprano de cáncer de mama. Combina una interfaz moderna e interactiva en **Vue 3** con un potente motor de inteligencia artificial en **FastAPI** construido sobre **PyTorch y MONAI** (DenseNet121) entrenado para clasificar mamografías y sugerir estadios preliminares BI-RADS.

---

## 🛠️ Arquitectura de la Plataforma

La aplicación está dividida en dos componentes principales perfectamente integrados:

### 1. 💻 Frontend (Vue 3 + Vite)
Una aplicación de una sola página (SPA) moderna, fluida y con micro-animaciones premium orientada al personal de la salud.
* **Tecnologías:** Vue 3 (Composition API), TypeScript, Vite, Tailwind CSS v4, Radix Vue, Motion y Lucide.
* **Visualizaciones:** Gráficos estadísticos dinámicos con Chart.js para el análisis demográfico e histórico de diagnósticos de las pacientes.
* **Características:** Carga interactiva de mamografías (Drag & Drop), panel de control intuitivo, historial clínico detallado de pacientes y visualización interactiva del BI-RADS sugerido.

### 2. ⚙️ Backend (FastAPI + MongoDB + AI)
Una API robusta, asíncrona y segura que gestiona los registros clínicos, la autenticación y ejecuta la inferencia de imágenes médicas.
* **Framework:** FastAPI con ciclo de vida asíncrono (`lifespan`).
* **Base de Datos:** MongoDB de alto rendimiento, integrado mediante la ODM asíncrona **Beanie** y el driver nativo **Motor**.
* **Motor de IA:** Red neuronal convolucional **DenseNet121** (2D, canal único en escala de grises, 2 clases de salida: Benigno/Maligno) implementada con **PyTorch y MONAI** (Medical Open Network for AI).
  * **Optimización Clínica:** Umbral de decisión ajustado de forma conservadora a **0.35** (en lugar del estándar 0.50) para maximizar la sensibilidad (Recall ~93.56%) y mitigar falsos negativos.
  * **Clasificación BI-RADS:** Mapeo de riesgo heurístico a estadios clínicos preliminares (BI-RADS 1 a 5).
* **Seguridad y Cumplimiento:** Autenticación JWT, contraseñas encriptadas mediante `bcrypt` y Middleware de Auditoría (`AuditMiddleware`) para registrar cada acceso a datos sensibles de pacientes (alineado con estándares de cumplimiento de salud).

---

## 📂 Estructura del Workspace

```text
AlertaRosa/
├── Backend/               # API FastAPI & Motor de Inferencia IA
│   ├── app/
│   │   ├── core/          # Configuraciones, seguridad y pesos del modelo
│   │   │   └── weights/   # Pesos entrenados: 'monai_mamografia_model.pth'
│   │   ├── db/            # Inicialización de MongoDB y Beanie
│   │   ├── models/        # Esquemas y modelos de datos (Beanie)
│   │   ├── routers/       # Endpoints de API (Auth, Pacientes, Diagnósticos)
│   │   └── services/      # Lógica de negocio y Motor de IA (ia_engine.py)
│   ├── uploads/           # Almacenamiento temporal de imágenes médicas cargadas
│   ├── requirements.txt   # Dependencias de Python (PyTorch, MONAI, FastAPI)
│   └── pyrefly.toml
│
├── Frontend/              # Interfaz de Usuario (Vue 3)
│   ├── src/               # Código fuente del Frontend
│   │   ├── components/    # Componentes modulares y visualizaciones
│   │   ├── views/         # Vistas de la aplicación (Dashboard, Patients, etc.)
│   │   └── main.ts
│   ├── package.json       # Dependencias de Node (Tailwind v4, Vue 3)
│   └── vite.config.ts     # Configuración de Vite
│
├── .gitignore             # Configuración de exclusiones de Git
└── README.md              # Documentación del proyecto (este archivo)
```

---

## 🚀 Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:
* **Node.js** (versión 18 o superior recomendada)
* **Python** (versión 3.10 o superior)
* **MongoDB** ejecutándose localmente (o una URI de conexión en la nube como MongoDB Atlas)

---

## 🔌 Configuración e Instalación

### Paso 1: Configurar el Backend

1. **Navega al directorio del backend:**
   ```bash
   cd Backend
   ```

2. **Crea y activa un entorno virtual de Python:**
   ```bash
   # En macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # En Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instala las dependencias necesarias:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Variables de Entorno (Opcional):**
   Puedes crear un archivo `.env` en la raíz de la carpeta `Backend/` si deseas anular los valores por defecto:
   ```env
   SECRET_KEY=tu_clave_secreta_super_segura
   MONGODB_URI=mongodb://localhost:27017
   DATABASE_NAME=alertarosa_db
   ```

5. **Pesos del Modelo de Inferencia:**
   Asegúrate de colocar los pesos entrenados del modelo en:
   `Backend/app/core/weights/monai_mamografia_model.pth`
   * *Nota: Si no se encuentra este archivo al iniciar, el sistema inicializará la red DenseNet121 con pesos aleatorios para permitir las pruebas de integración del pipeline.*

### Paso 2: Configurar el Frontend

1. **Abre otra pestaña de la terminal y navega al directorio del frontend:**
   ```bash
   cd Frontend
   ```

2. **Instala los módulos de Node.js:**
   ```bash
   npm install
   ```
   *(También puedes utilizar `pnpm install` o `yarn` si lo prefieres).*

---

## 🏃‍♂️ Ejecución del Proyecto

### 1. Iniciar la Base de Datos (MongoDB)
Asegúrate de que tu servidor de MongoDB esté en ejecución. En macOS, si usas Homebrew:
```bash
brew services start mongodb-community
```

### 2. Ejecutar el Backend (FastAPI)
Con tu entorno virtual activado dentro de la carpeta `Backend/`, inicia el servidor de desarrollo Uvicorn:
```bash
uvicorn app.main:app --reload --port 8000
```
* **API local:** El backend estará disponible en `http://127.0.0.1:8000`
* **Documentación interactiva (Swagger UI):** Accede a `http://127.0.0.1:8000/docs` para ver y probar todos los endpoints interactivos en tiempo real.

### 3. Ejecutar el Frontend (Vue 3 + Vite)
Dentro de la carpeta `Frontend/`, ejecuta el servidor de desarrollo Vite:
```bash
npm run dev
```
* **Interfaz local:** La aplicación se cargará en `http://localhost:5173` (o el puerto indicado por Vite en tu consola). Abre este enlace en tu navegador para ver la interfaz interactiva.

---

## 🔒 Buenas Prácticas y Seguridad Médica

AlertaRosa se ha construido bajo estándares profesionales de protección de datos:
1. **Ignorado de Datos Sensibles:** La carpeta `Backend/uploads/` y los archivos `.env` están configurados en `.gitignore` para prevenir cualquier filtración de información médica o claves criptográficas a repositorios públicos.
2. **Peticiones Seguras (CORS):** La API cuenta con middlewares de control de orígenes para mitigar riesgos de inyección y suplantación de identidad.
3. **Registro de Auditoría:** El backend mantiene una bitácora automática de accesos para rastrear operaciones sobre la base de datos de pacientes, fundamental en aplicaciones del sector salud.
