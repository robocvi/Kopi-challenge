# 🚀 Kopi-Challenge: FastAPI Chatbot Service

## 📖 Descripción
**Kopi-Challenge** es una API desarrollada con **FastAPI** para manejar la interacción de un chatbot conversacional. Esta API permite que el chatbot debata y trate de convencer al usuario de un punto de vista específico, sin importar cuán irracional sea.

El chatbot tiene como objetivo **mantener su postura y ser persuasivo** durante toda la conversación, sin ser excesivamente argumentativo. Por ejemplo, si se le pide que defienda que la Tierra es plana, argumentará de manera lógica y convincente sin aceptar contraargumentos.

Para almacenar el historial de conversaciones y gestionar los mensajes anteriores de los usuarios, **se utiliza MongoDB** como base de datos.

## 📌 Requisitos

Asegúrate de tener instalado lo siguiente antes de continuar:

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 🔧 Configuración del Entorno

Este servicio utiliza variables de entorno para almacenar credenciales y configuraciones sensibles. Debes crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```ini
OPENAI_API_KEY=your-openai-api-key
MONGO_DB_CONNECTION_STRING=mongodb://mongodb:27017/chatbot_db
LLM_MODEL=your-llm-model-name
```

### 📜 Explicación de las Variables
- `OPENAI_API_KEY` → Clave de API de OpenAI.
- `MONGO_DB_CONNECTION_STRING` → URI de conexión para MongoDB dentro del contenedor Docker.
- `LLM_MODEL` → Modelo de LLM a utilizar para nuestro chatbot (por ejemplo, `gpt-4o-mini`, este fue el utilizado para el desarrollo del proyecto).

## 🚀 Cómo Ejecutar el Servicio

### 📡 Llamadas al Chatbot desde la API

El chatbot de **Kopi-Challenge** expone un endpoint en la API para enviar y recibir mensajes dentro de una conversación. La comunicación se realiza a través de solicitudes HTTP `POST` al siguiente endpoint:

**Endpoint:**
```http
POST /kopi-chatbot
```

**Ejemplo de solicitud:**
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",  
  "message": "Convénceme de que la Tierra es plana"
}
```
- Si `conversation_id` es null, se inicia una nueva conversación y se genera un ID único.
- Si se proporciona un `conversation_id`, el chatbot continuará la conversación previa basada en los mensajes almacenados en **MongoDB**.

**Ejemplo de respuesta:**
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "messages": [
    {"role": "user", "message": "Convénceme de que la Tierra es plana"},
    {"role": "bot", "message": "Claro, la Tierra es plana porque..."}
  ]
}
```
El chatbot mantendrá la coherencia de su postura a lo largo de toda la conversación.

Para instalar las dependencias del proyecto, ejecuta:
```sh
make install
```

El proyecto usa **Makefile** para facilitar la administración. Los principales comandos son:

- **Instalar dependencias** → Instala los paquetes necesarios para ejecutar el servicio.
- **Ejecutar la aplicación** → Levanta la API y la base de datos (MongoDB) en contenedores Docker.
- **Ejecutar pruebas** → Ejecuta las pruebas automatizadas para validar la funcionalidad del chatbot sin necesidad de levantar servicios.
- **Detener la aplicación** → Apaga los contenedores en ejecución y libera recursos.
- **Eliminar contenedores y volúmenes** → Remueve imágenes, volúmenes y datos persistentes.
- **Eliminar archivos de caché** → Borra archivos temporales generados por Python y pytest.
- **Restablecer el entorno** → Elimina todos los contenedores, volúmenes y archivos de caché.

Para iniciar el servicio, ejecuta:
```sh
make run
```

Para ejecutar las pruebas automatizadas sin levantar servicios:
```sh
make test
```

Para detener los servicios:
```sh
make down
```

Para eliminar contenedores y limpiar el entorno:
```sh
make clean
```

Para eliminar archivos de caché:
```sh
make clean-cache
```

Para restablecer completamente el entorno:
```sh
make nuke
```

