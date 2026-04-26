# Guía de Instalación — Emergencias Viales

Sistema de asistencia vial: backend FastAPI + frontend Angular 21.

---

## Requisitos previos

Antes de empezar, asegurate de tener instalado:

| Herramienta | Versión mínima | Verificar con |
|---|---|---|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Angular CLI | 21.x | `ng version` |
| PostgreSQL | 13+ | `psql --version` |
| Git | cualquiera | `git --version` |

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/AlexRV7766/PrimerParcial.git
cd PrimerParcial
```

---

## 2. Base de datos (PostgreSQL)

Abrí pgAdmin o la terminal de PostgreSQL y ejecutá:

```sql
CREATE DATABASE "Emergencias";
```

> Si tu usuario, contraseña o puerto son distintos a los predeterminados, anotálos — los vas a usar en el paso 4.

---

## 3. Backend (FastAPI)

### 3.1 Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python -m venv venv
source venv/bin/activate
```

### 3.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3.3 Configurar variables de entorno

Creá un archivo `.env` en la raíz del proyecto (al lado de `main.py`):

```env
DB_NAME=Emergencias
DB_USER=postgres
DB_PASSWORD=12345678
DB_HOST=localhost
DB_PORT=5432
```

> Cambiá los valores si tu PostgreSQL tiene credenciales distintas.

### 3.4 Crear las tablas

Ejecutá esto una sola vez para crear todas las tablas en la base de datos:

```bash
python -c "from app.core.database import Base, engine; from app.models import *; Base.metadata.create_all(bind=engine)"
```

### 3.5 Iniciar el backend

```bash
uvicorn main:app --reload --reload-dir app
```

El backend queda disponible en: **http://localhost:8000**

Documentación interactiva (Swagger): **http://localhost:8000/docs**

---

## 4. Frontend (Angular 21)

Abrí una **nueva terminal** (dejá el backend corriendo en la anterior).

### 4.1 Instalar Angular CLI (si no lo tenés)

```bash
npm install -g @angular/cli@21
```

### 4.2 Instalar dependencias del frontend

```bash
cd frontend
npm install
```

> La primera vez puede demorar unos minutos.

### 4.3 Iniciar el frontend

```bash
ng serve
```

El frontend queda disponible en: **http://localhost:4200**

---

## 5. Verificar que todo funciona

1. Abrí **http://localhost:4200** en el navegador
2. Registrá un usuario nuevo desde la pantalla de registro
3. Iniciá sesión con ese usuario
4. Deberías ver el dashboard con el hero en negro

---

## Estructura del proyecto

```
PrimerParcial/
├── main.py                  # Entrada del backend FastAPI
├── requirements.txt         # Dependencias Python
├── .env                     # Variables de entorno (creás vos)
├── app/
│   ├── core/
│   │   └── database.py      # Conexión a PostgreSQL
│   ├── models/              # Modelos SQLAlchemy
│   ├── routes/              # Endpoints de la API
│   ├── schemas/             # Schemas Pydantic
│   └── services/            # Lógica de negocio
└── frontend/
    ├── package.json
    └── src/
        ├── styles.css        # Sistema de diseño global
        └── app/
            ├── features/     # Páginas (auth, dashboard, emergencias, vehículos, talleres)
            ├── core/         # Guards, interceptors, servicios, modelos
            └── shared/       # Navbar
```

---

## Solución de problemas frecuentes

### Puerto 4200 ocupado

```bash
# Windows PowerShell
Get-NetTCPConnection -LocalPort 4200 | Select-Object OwningProcess
Stop-Process -Id <PID>

# Linux / Mac
lsof -ti:4200 | xargs kill
```

### Puerto 8000 ocupado

```bash
# Windows PowerShell
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
Stop-Process -Id <PID>

# Linux / Mac
lsof -ti:8000 | xargs kill
```

### Error de conexión a la base de datos

- Verificá que PostgreSQL esté corriendo
- Confirmá que la base de datos `Emergencias` existe
- Revisá las credenciales en el archivo `.env`

### Error CORS en el navegador

Verificá que el backend esté corriendo en `http://localhost:8000` y el frontend en `http://localhost:4200`. Si usás otro puerto para el frontend, cambiá `allow_origins` en `main.py`.

### `ng: command not found`

```bash
npm install -g @angular/cli@21
```

### Módulos de Python no encontrados

Asegurate de tener el entorno virtual activado:
```bash
# Windows
venv\Scripts\activate
```

---

## Credenciales de prueba

No hay usuarios precargados. Registrá uno desde **http://localhost:4200/register**.
