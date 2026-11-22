# Plan técnico y seguimiento E1–E4

Propuesta de liderazgo de Desarrollo. Seguimiento existente:
[issue #3](https://github.com/Danxxx777/clab-pfc-7a/issues/3).
El plan organiza trabajo; no convierte tareas propuestas en trabajo ejecutado.
Los responsables por rol se conservan según el README actual.

## Cronograma de las cuatro entregas

Solo se dispone de fecha oficial confirmada para E1: **29/11/2026, 23:55**.
Las fechas oficiales de E2, E3 y E4 no se recibieron. Sus ventanas son una
secuencia relativa propuesta, no fechas académicas confirmadas. Cada ventana
inicia después de la anterior; la duración se ajustará al calendario oficial y
a la capacidad que confirme el equipo. No se afirma un acuerdo colectivo.

| Entrega | Ventana propuesta | Desarrollo y dependencia | Verificación y salida |
|---|---|---|---|
| E1: base y diseño | Hasta 29/11/2026, 23:55 | Modelo de comunicación, ADR-002, ejecución del esqueleto y tablero E1/E2. Depende de C4/ADR-001 y resultados originales de PE-U1 para contrastar la decisión. | Compilación, pruebas y fallo/recuperación reproducibles; documentos e integración revisados; video real y enlace al tablero. |
| E2: API y despliegue inicial | S1: primera semana después de E1; S2: siguiente semana, ajustables a fecha oficial pendiente | S1: contratos versionados y pruebas de API; S2: contenerización de Reservas/Laboratorios e inicio de Identidad. Inventariar funciones SQL antes de migrar reglas. | Contratos y permisos acordados, dos servicios desplegables en entorno aislado, instrucciones y pruebas de contratos. No declarar terminado con solo el endpoint de diagnóstico. |
| E3: datos y consistencia | S3–S4, después de la base E2; fecha oficial pendiente | Separar almacenes, control de concurrencia de agenda y solicitudes durables de cierre/reapertura. Depende de contratos y del inventario de reglas SQL. | Pruebas de reservas incompatibles, idempotencia, pérdida de respuesta, órdenes atrasadas y reinicio. Validar I13 sin llamada circular. |
| E4: integración y validación final | S5–S6, después de E3; fecha oficial pendiente | Completar Información/Avisos, recuperación de proyecciones, seguridad e integración de módulos del periodo. Integrar SPA, pruebas y despliegue final. | Pruebas de extremo a extremo y fallos; métricas frente a RNF acordados, manuales, demostración y defensa. |

La migración objetivo comprende los cuatro servicios y los doce módulos de
ADR-001 durante el periodo; este cronograma no reduce ese alcance. Las duraciones
relativas requieren revisión si las fechas oficiales no permiten esas ventanas.
No se compromete integración con SGA sin contrato y aceptación específicos.

## Tareas para GitHub Projects

**Estado del tablero:** no se creó ni modificó un Project desde esta sesión.
Este archivo es un backlog preparado, no el enlace a un tablero existente.
La creación y asignación remotas corresponden al usuario con permisos.

Crear un Project de tipo **Board** llamado `CLAB — E1/E2`. Usar columnas
`Pendiente`, `En curso`, `En revisión` y `Hecho`; campos `Entrega` (E1/E2),
`Responsable` (assignee de la issue) y prioridad. Mantener los roles actuales.

Agregar las issues existentes #1–#4, sin duplicarlas ni cambiar sus autores.
En #3 mantener en revisión lo que solo está propuesto. Crear las tareas E2 de
la tabla como issues o borradores vinculados al Project, indicando dependencia
y criterios, sin marcar resultados aún no obtenidos. Convertir borradores a
issues cuando se requiera seguimiento y asignación en el repositorio.

| ID de planificación | Tarea y entrega | Responsable propuesto | Dependencia | Criterio para mover a Hecho |
|---|---|---|---|---|
| E1-DOC / #1 | Informe, levantamiento e integración E1 | Documentación | Aportes y respaldos del equipo | Informe compilado, fuentes y evidencias verificadas; limitaciones declaradas. |
| E1-ARQ / #2 | Coherencia C4, ADR-001 y evidencia de diseño | Arquitectura | Requisitos y revisión del diseño | Criterios reales de #2 satisfechos o aclarados formalmente. |
| E1-DEV / #3 | Comunicación, ADR-002 y demostración E1 | Desarrollo | C4, esqueleto y PE-U1 | Modelo revisado, ejecución personal, tablero y cronograma enlazados, video coordinado. |
| E1-QA / #4 | Calidad, referencias y evidencias E1 | Calidad | Informe integrado | Criterios de revisión y referencias comprobados por responsable. |
| E2-01 | Contratos OpenAPI de catálogo y agenda | Desarrollo, revisión Arquitectura | ADR-001/002 y requisitos | DTO, estados, validación y ejemplos de errores; contrato aprobado y versionado. |
| E2-02 | Entorno reproducible de dos servicios | Desarrollo | E2-01 y base E1 | Contenedores con puertos/configuración externos, healthchecks y guía; arranque desde entorno limpio. |
| E2-03 | Inventario de reglas SQL y plan de datos | Desarrollo, revisión Arquitectura | Fuente heredada identificada | Funciones y procedimientos mapeados a dominio y pruebas; sin acceso SQL cruzado. |
| E2-04 | Primera API de negocio de Laboratorios | Desarrollo | E2-01, E2-03 | Consulta por ID, validación, errores y pruebas; no solo mensaje fijo. |
| E2-05 | Primer flujo de Reservas y autorización | Desarrollo | E2-01, E2-03, E2-04 | Validación de laboratorio y permisos, control de agenda local y pruebas del alcance implementado. |
| E2-06 | Pruebas de contratos y fallos de E2 | Calidad con Desarrollo | E2-02, E2-04, E2-05 | Casos 2xx/4xx/5xx, dependencia caída, configuración reproducible y resultados reales. |
| E2-07 | Actualizar ejecución y evidencias de E2 | Documentación con Desarrollo | E2-02 y E2-06 | Instrucciones ejecutadas por otra persona, capturas y evidencia enlazadas sin secretos. |

Los identificadores E2-01–E2-07 son claves de este plan, **no números de issues
ya creadas**. Confirmar asignados concretos y fechas con el equipo; no imponer
asignaciones a compañeros desde esta propuesta.

## Dependencias, riesgos y control

- Ruta de trabajo: contratos → entorno/API → pruebas → documentación/evidencias.
- Trabajo paralelo: inventario de datos y contratos; integración documental y
  verificación bibliográfica de E1 pueden continuar sin alterar código.
- Riesgos de Desarrollo: reglas ocultas en SQL, reintentos de escrituras sin
  deduplicación, dependencia de Identidad y retraso del consumidor de cambios.
  Mitigar con inventario, pruebas por invariante, presupuestos de timeout y
  cursor durable. No se modifican los riesgos de Calidad ni se atribuyen
  resultados a FORM-AC-01 no disponible.
- Antes de cada entrega: revisar tareas bloqueadas, evidencia de cierre, alcance
  y fechas oficiales. Esto es una cadencia propuesta, no reuniones ya celebradas.
- Un archivo de backlog no sustituye el Project real. Después de crearlo, registrar
  su URL en #3 y pasar el enlace a Documentación para el informe; no inventar URL.

Preparado con asistencia de OpenAI GPT-6.1 Sol. No se realizaron operaciones de
escritura en GitHub ni se generaron actas, fechas oficiales o aprobaciones.
