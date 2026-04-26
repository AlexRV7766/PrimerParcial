# Guía de Base de Datos — Emergencias Viales

---

## 1. Instalar PostgreSQL

Descargá el instalador oficial desde:

**https://www.postgresql.org/download/windows/**

Durante la instalación:
- Puerto: `5432` (dejarlo por defecto)
- Usuario: `postgres`
- Contraseña: anotá bien la que ponés, la vas a necesitar
- Dejá marcado **pgAdmin 4** para tener interfaz gráfica

---

## 2. Crear la base de datos

### Opción A — pgAdmin (interfaz gráfica)

1. Abrí **pgAdmin 4**
2. Conectate al servidor con tu contraseña
3. Click derecho en **Databases** → **Create** → **Database...**
4. En el campo **Database** escribí: `Emergencias`
5. Click **Save**

### Opción B — psql (terminal)

```bash
psql -U postgres
```

```sql
CREATE DATABASE "Emergencias";
\q
```

---

## 3. Crear las tablas

Con el entorno virtual activado y el `.env` configurado (ver `INSTALACION.md`), ejecutá desde la raíz del proyecto:

```bash
python -c "from app.core.database import Base, engine; from app.models import *; Base.metadata.create_all(bind=engine)"
```

Si todo salió bien, no aparece ningún error. Las 15 tablas quedan creadas automáticamente.

### Verificar que las tablas se crearon

En psql o pgAdmin ejecutá:

```sql
\c "Emergencias"
\dt
```

Deberías ver:

```
 Schema |       Name        | Type  |  Owner
--------+-------------------+-------+----------
 public | analisis_ia       | table | postgres
 public | asignaciones      | table | postgres
 public | comisiones        | table | postgres
 public | dispositivos      | table | postgres
 public | emergencia        | table | postgres
 public | evidencia         | table | postgres
 public | historial_estados | table | postgres
 public | metricas          | table | postgres
 public | notificaciones    | table | postgres
 public | pago              | table | postgres
 public | taller            | table | postgres
 public | tecnico           | table | postgres
 public | ubicaciones       | table | postgres
 public | usuario           | table | postgres
 public | vehiculo          | table | postgres
```

---

## 4. Diagrama de tablas

```
usuario
├── id, nombre, email, password, telefono, rol, activo, creado_en
│
├──< vehiculo
│    └── id, usuario_id, marca, modelo, placa, anio
│
└──< emergencia
     ├── id, usuario_id, vehiculo_id, descripcion
     ├── latitud, longitud, tipo, prioridad, estado, creado_en
     │
     ├──< evidencia          (imágenes, audio, texto de la emergencia)
     ├──< historial_estados  (registro de cambios de estado)
     ├──< ubicaciones        (rastro GPS de la emergencia)
     ├──< analisis_ia        (análisis automático)
     └──< asignaciones ──> taller ──< tecnico
          │
          └──< pago ──< comisiones

notificaciones  (usuario_id + taller_id)
dispositivos    (tokens push por usuario)
metricas        (estadísticas del sistema)
```

---

## 5. Descripción de cada tabla

| Tabla | Descripción |
|---|---|
| `usuario` | Clientes y administradores del sistema |
| `vehiculo` | Vehículos registrados por cada usuario |
| `emergencia` | Solicitudes de asistencia vial |
| `evidencia` | Archivos adjuntos a una emergencia (foto, audio) |
| `historial_estados` | Cada cambio de estado de una emergencia |
| `taller` | Talleres mecánicos disponibles |
| `tecnico` | Técnicos que trabajan en un taller |
| `asignaciones` | Qué taller/técnico atiende cada emergencia |
| `analisis_ia` | Resultado del análisis automático de la emergencia |
| `ubicaciones` | Historial de ubicaciones GPS de una emergencia |
| `pago` | Registro de pagos por servicio |
| `comisiones` | Comisión del 10% por cada pago |
| `metricas` | Estadísticas generales del sistema |
| `notificaciones` | Notificaciones enviadas a usuarios y talleres |
| `dispositivos` | Tokens para notificaciones push (móvil) |

---

## 6. Datos de prueba (opcional)

Para probar la app con talleres ya cargados, ejecutá esto en psql o pgAdmin:

```sql
\c "Emergencias"

INSERT INTO taller (nombre, email, telefono, direccion, latitud, longitud, activo)
VALUES
  ('Taller El Mecánico', 'mecanico@gmail.com', '+591 76543210',
   'Av. Cañoto #450, Santa Cruz', -17.783300, -63.182100, true),

  ('Taller Central Motors', 'central@motors.com', '+591 77654321',
   'Radial 17 y medio #820, Santa Cruz', -17.796400, -63.165300, true),

  ('Taller Rápido 24h', 'rapido24@gmail.com', '+591 78765432',
   'Av. Banzer Km 5, Santa Cruz', -17.751200, -63.201400, true);
```

Para agregar técnicos a esos talleres:

```sql
INSERT INTO tecnico (taller_id, nombre, telefono, disponible)
VALUES
  (1, 'Carlos Ríos', '+591 71234567', true),
  (1, 'Marcos Vidal', '+591 72345678', true),
  (2, 'Juan Peña', '+591 73456789', true),
  (3, 'Rodrigo Lara', '+591 74567890', true);
```

---

## 7. Valores posibles (Enums)

### `emergencia.tipo`
| Valor | Significado |
|---|---|
| `bateria` | Problema de batería |
| `llanta` | Llanta pinchada o reventada |
| `choque` | Accidente de tránsito |
| `motor` | Falla de motor |
| `otro` | Otro tipo de emergencia |

### `emergencia.estado` / `historial_estados.estado`
| Valor | Significado |
|---|---|
| `pendiente` | Recién creada, sin atender |
| `en_proceso` | Taller asignado, en camino |
| `atendido` | Emergencia resuelta |
| `cancelado` | Cancelada por el usuario |

### `emergencia.prioridad`
| Valor | Significado |
|---|---|
| `baja` | Sin urgencia inmediata |
| `media` | Urgencia moderada |
| `alta` | Requiere atención inmediata |

### `asignaciones.estado`
| Valor | Significado |
|---|---|
| `asignado` | Taller notificado |
| `aceptado` | Taller confirmó la asistencia |
| `rechazado` | Taller rechazó la solicitud |

### `pago.estado`
| Valor | Significado |
|---|---|
| `pendiente` | Pago no realizado aún |
| `pagado` | Pago confirmado |
| `fallido` | Pago fallido |

---

## 8. Comandos útiles en psql

```sql
-- Conectarse a la base de datos
\c "Emergencias"

-- Ver todas las tablas
\dt

-- Ver la estructura de una tabla
\d usuario
\d emergencia

-- Ver todos los usuarios registrados
SELECT id, nombre, email, rol, creado_en FROM usuario;

-- Ver emergencias con su estado
SELECT e.id, u.nombre, e.descripcion, e.estado, e.creado_en
FROM emergencia e
JOIN usuario u ON u.id = e.usuario_id
ORDER BY e.creado_en DESC;

-- Ver talleres activos
SELECT id, nombre, direccion, activo FROM taller;

-- Borrar todos los datos de prueba (respeta el orden por FK)
TRUNCATE TABLE comisiones, pago, analisis_ia, ubicaciones,
  historial_estados, evidencia, asignaciones, notificaciones,
  emergencia, vehiculo, dispositivos, tecnico, taller,
  metricas, usuario RESTART IDENTITY CASCADE;
```

---

## 9. Resetear la base de datos

Si necesitás empezar desde cero:

```sql
\c "Emergencias"

-- Elimina y vuelve a crear todas las tablas
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

Luego volvé a correr el comando Python del paso 3 para recrear las tablas.
