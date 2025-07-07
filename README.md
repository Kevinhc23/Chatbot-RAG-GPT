# RAG Chat Application

Una aplicación de chat con Retrieval-Augmented Generation (RAG) que permite conversaciones inteligentes con soporte para multimedia y historial de chat.

## 🚀 Características

- **Chat inteligente**: Conversaciones potenciadas con RAG usando OpenAI
- **Soporte multimedia**: Renderizado selectivo de imágenes y videos relevantes
- **Historial de chat**: Persistencia de conversaciones con SQLite
- **Base de datos vectorial**: Almacenamiento de chunks con MongoDB
- **Autenticación**: Sistema de usuarios seguro
- **Frontend moderno**: Interfaz construida con Next.js y React

## 📋 Requisitos Previos

- **Python 3.11+**
- **Node.js 18+** y **npm/pnpm**
- **Docker** y **Docker Compose** (opcional)
- **MongoDB** (local o en la nube)
- **Clave API de OpenAI**

## ⚙️ Configuración de Variables de Entorno

### Backend (.env)

Crea un archivo `.env` en el directorio `backend/` con las siguientes variables:

```env
# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/rag_chat

# SQLite Database
DATABASE_URL=sqlite:///./chat_history.db

# Environment
ENVIRONMENT=development
```

### Descripción de Variables

| Variable         | Descripción                                             | Valor por Defecto                    | Requerido |
| ---------------- | ------------------------------------------------------- | ------------------------------------ | --------- |
| `OPENAI_API_KEY` | Tu clave API de OpenAI para el servicio de chat         | -                                    | ✅        |
| `MONGODB_URI`    | URI de conexión a MongoDB para almacenamiento de chunks | `mongodb://localhost:27017/rag_chat` | ✅        |
| `DATABASE_URL`   | Ruta de la base de datos SQLite para historial          | `sqlite:///./chat_history.db`        | ✅        |
| `ENVIRONMENT`    | Entorno de ejecución (development/production)           | `development`                        | ❌        |

### 🔑 Obtener Clave de OpenAI

1. Ve a [OpenAI Platform](https://platform.openai.com/)
2. Inicia sesión o crea una cuenta
3. Navega a **API Keys** en el dashboard
4. Crea una nueva clave API
5. Copia la clave y pégala en tu archivo `.env`

## 🛠️ Instalación

### Opción 1: Instalación Manual

#### Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install
# o con pnpm
pnpm install

# Ejecutar servidor de desarrollo
npm run dev
# o con pnpm
pnpm dev
```

### Opción 2: Docker Compose

```bash
# Desde el directorio raíz del proyecto
docker-compose up -d
```

## 🚦 Uso con VS Code Tasks

El proyecto incluye tareas predefinidas de VS Code para facilitar el desarrollo:

### Tareas Disponibles

- **🚀 Start Backend Server**: Inicia el servidor FastAPI
- **🌐 Start Frontend Server**: Inicia el servidor Next.js
- **🧪 Run Python Tests**: Ejecuta las pruebas del backend
- **📦 Install Backend Dependencies**: Instala dependencias de Python
- **📦 Install Frontend Dependencies**: Instala dependencias de Node.js
- **🐳 Docker Compose Up**: Levanta todos los servicios con Docker
- **🐳 Docker Compose Down**: Detiene todos los servicios Docker

### Ejecutar Tareas

1. Abre VS Code en el directorio del proyecto
2. Presiona `Ctrl+Shift+P` (o `Cmd+Shift+P` en Mac)
3. Escribe "Tasks: Run Task"
4. Selecciona la tarea que deseas ejecutar

## 📚 Estructura del Proyecto

```
rag-chat/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints de la API
│   │   ├── core/           # Configuración y dependencias
│   │   ├── models/         # Modelos Pydantic
│   │   ├── repositories/   # Acceso a datos
│   │   └── services/       # Lógica de negocio
│   ├── .env               # Variables de entorno
│   └── requirements.txt   # Dependencias Python
├── frontend/              # Aplicación Next.js
│   ├── src/
│   │   ├── app/          # App Router de Next.js
│   │   ├── components/   # Componentes React
│   │   └── contexts/     # Context Providers
│   └── package.json      # Dependencias Node.js
└── docker-compose.yml    # Configuración Docker
```

## 🔧 Funcionalidades Técnicas

### Sistema RAG

- **Retrieving**: Búsqueda semántica en chunks de MongoDB
- **Augmentation**: Enriquecimiento del contexto con chunks relevantes
- **Generation**: Generación de respuestas con OpenAI GPT

### Renderizado Multimedia Selectivo

El sistema incluye lógica avanzada para mostrar imágenes y videos:

- **Consultas normales**: Solo multimedia del chunk más relevante
- **Consultas visuales explícitas**: Hasta 2 chunks relevantes
- **Filtrado inteligente**: No renderiza arrays vacíos
- **Umbral de relevancia**: Solo chunks con alta puntuación de similitud

### Base de Datos

- **MongoDB**: Almacenamiento de chunks con embeddings vectoriales
- **SQLite**: Historial de chat y datos de usuarios
- **Persistencia**: Manejo automático de conexiones y transacciones

## 🧪 Testing

```bash
# Ejecutar tests del backend
cd backend
python -m pytest -v

# O usando la tarea de VS Code
# Tasks: Run Task -> 🧪 Run Python Tests
```

## 🐛 Troubleshooting

### Error: "OpenAI API Key not found"

- Verifica que `OPENAI_API_KEY` esté configurado en `.env`
- Asegúrate de que el archivo `.env` esté en `backend/`
- Reinicia el servidor después de cambiar variables de entorno

### Error de conexión a MongoDB

- Verifica que MongoDB esté ejecutándose
- Comprueba la URI en `MONGODB_URI`
- Para MongoDB local: `mongodb://localhost:27017/rag_chat`

### Puerto en uso

- Cambia los puertos en las configuraciones si hay conflictos:
  - Backend: puerto 8000
  - Frontend: puerto 3000

## 📝 API Endpoints

### Chat

- `POST /api/v1/chat` - Enviar mensaje de chat
- `GET /api/v1/chat/history` - Obtener historial

### Autenticación

- `POST /api/v1/auth/register` - Registro de usuario
- `POST /api/v1/auth/login` - Inicio de sesión

### Configuración

- `GET /api/v1/settings` - Obtener configuraciones
- `PUT /api/v1/settings` - Actualizar configuraciones

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la sección de **Troubleshooting**
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que las dependencias estén instaladas correctamente
4. Crea un issue en el repositorio con detalles del problema
