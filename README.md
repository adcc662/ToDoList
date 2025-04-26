# ToDo List API

API RESTful y GraphQL para gestión de tareas utilizando Django, Django Rest Framework y Strawberry GraphQL.

## Características

- CRUD completo para tareas usando REST API
- GraphQL API con Strawberry
- Documentación con Swagger/OpenAPI
- Contenerización con Docker
- Configuración ASGI para soporte asíncrono
- Pruebas unitarias con pytest
- Linting con flake8 y formateo con black

## Estructura del Proyecto

```
todo/                      # Proyecto principal de Django
├── todolist/              # Aplicación principal para las tareas
│   ├── models.py          # Modelo Task
│   ├── serializers.py     # Serializers para REST API
│   ├── views.py           # ViewSets y APIViews
│   ├── urls.py            # URLs para la API REST
│   ├── schema.py          # Definición del schema GraphQL
│   └── ...
├── todo/                  # Configuración principal
│   ├── settings.py        # Configuración del proyecto
│   ├── urls.py            # URLs principales
│   └── ...
└── ...
```

## Modelo de tarea

```json
{
  "id": integer,
  "title": string,
  "description": string,
  "completed": boolean
}
```

## Endpoints

- `/api/tasks/` (GET, POST)
- `/api/tasks/{id}/` (GET, PUT, PATCH, DELETE)
- `/graphql/` - API GraphQL
- `/swagger/` - Documentación Swagger
- `/redoc/` - Documentación ReDoc

## Requisitos

- Docker y Docker Compose

## Instalación y Ejecución

1. Clonar el repositorio:
```
git clone <repo-url>
cd todo
```

2. Crear archivo .env a partir de .env.example:
```
cp .env.example .env
```

3. Construir y levantar los contenedores:
```
docker-compose up -d --build
```

4. Ejecutar las migraciones:
```
docker-compose exec web python manage.py makemigrations todolist
docker-compose exec web python manage.py migrate
```

5. Crear un superusuario (opcional):
```
docker-compose exec web python manage.py createsuperuser
```

6. Acceder a la API:
   - API REST: http://localhost:8000/api/
   - API GraphQL: http://localhost:8000/graphql/
   - Documentación: http://localhost:8000/swagger/
   - Admin: http://localhost:8000/admin/

## Ejemplos de Uso

### REST API

#### Crear una tarea
```
POST /api/tasks/
{
    "title": "Completar proyecto",
    "description": "Terminar la implementación del API de tareas",
    "completed": false
}
```

#### Listar todas las tareas
```
GET /api/tasks/
```

#### Obtener una tarea específica
```
GET /api/tasks/1/
```

#### Actualizar una tarea
```
PUT /api/tasks/1/
{
    "title": "Completar proyecto",
    "description": "Terminar la implementación del API de tareas",
    "completed": true
}
```

#### Eliminar una tarea
```
DELETE /api/tasks/1/
```

### GraphQL API

#### Consultar todas las tareas
```graphql
query {
  tasks {
    id
    title
    description
    completed
  }
}
```

#### Consultar una tarea específica
```graphql
query {
  task(id: 1) {
    id
    title
    description
    completed
  }
}
```

#### Crear una tarea
```graphql
mutation {
  createTask(input: {
    title: "Completar proyecto",
    description: "Terminar la implementación del API de tareas",
    completed: false
  }) {
    id
    title
    description
    completed
  }
}
```

#### Actualizar una tarea
```graphql
mutation {
  updateTask(id: 1, input: {
    title: "Completar proyecto",
    description: "Terminar la implementación del API de tareas",
    completed: true
  }) {
    id
    title
    description
    completed
  }
}
```

#### Eliminar una tarea
```graphql
mutation {
  deleteTask(id: 1)
}
```

## Ejecutar pruebas

Para ejecutar las pruebas del proyecto:

```bash
# Ejecutar todos los tests
docker-compose exec web pytest

# Ejecutar tests con salida detallada
docker-compose exec web pytest -v

# Ejecutar tests específicos
docker-compose exec web pytest todolist/tests/test_models.py
docker-compose exec web pytest todolist/tests/test_api.py
docker-compose exec web pytest todolist/tests/test_graphql.py
```
