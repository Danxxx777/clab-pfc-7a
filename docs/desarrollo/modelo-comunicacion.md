# Modelo de comunicación de CLAB

Responsabilidad: liderazgo de Desarrollo. Seguimiento: [issue #3](https://github.com/Danxxx777/clab-pfc-7a/issues/3).
Base: `7e1b00cac5e4ca3f975b0359acd4bca8fd7d37bf`. Decisión principal:
[ADR-002](../adr/ADR-002-mecanismo-comunicacion.md). Los identificadores conservan
la definición de los [C4 existentes](../diagramas/c4.md); no cambian sus autores.

## Inventario por interacción

La flecha indica quién inicia la petición; la respuesta vuelve en esa conexión.
Excepto el caso mínimo indicado abajo, las filas describen diseño objetivo.

| ID | Emisor → receptor | Datos y propósito | Mecanismo | Fallo / consistencia |
|---|---|---|---|---|
| I01 | Persona → SPA | Navegación e ingreso de solicitudes | HTTPS interactivo | Sin acceso al frontend no hay nuevas acciones desde esa sesión; no decide ocupación. |
| I02 | SPA → Identidad | Sesión, usuario, roles y datos académicos según permiso | REST/JSON, HTTPS, sincrónico | No exponer credenciales en respuestas o logs; rechazar credenciales inválidas. |
| I03 | SPA → Laboratorios | Catálogo, recursos, incidencias y trámite operativo | REST/JSON, HTTPS, sincrónico | Estado pendiente no equivale a cambio confirmado; registrar el resultado durable del trámite. |
| I04 | SPA → Reservas | Disponibilidad, solicitud, cancelación y bloqueos | REST/JSON, HTTPS, sincrónico | Confirmar bajo autoridad local de agenda, no desde una vista atrasada. ID de operación en escrituras. |
| I05 | SPA → Información | Reportes, auditoría proyectada y avisos | REST/JSON, HTTPS, sincrónico | Mostrar fecha/cursor de actualización; una vista atrasada no autoriza reservas. |
| I06 | Laboratorios → Identidad | Validar usuario activo y permiso de la operación | REST/JSON, HTTPS, sincrónico | No autorizar si no se pudo verificar; no registrar tokens. |
| I07 | Reservas → Identidad | Validar permiso antes de escritura protegida | REST/JSON, HTTPS, sincrónico | Fallo cerrado; definir con el equipo el alcance de revocaciones concurrentes. |
| I08 | Información → Identidad | Permisos para consultar datos o proyecciones | REST/JSON, HTTPS, sincrónico | No servir datos protegidos solo porque existe una copia local. |
| I09 | Reservas → Laboratorios | Consultar existencia y estado del laboratorio | REST/JSON, HTTPS, sincrónico | No confirmar si el catálogo requerido es inaccesible. La barrera se revalida localmente al confirmar. |
| I10 | Información → Identidad | Cambios académicos y de usuarios estrictamente necesarios | GET REST periódico sobre HTTPS | Cursor durable, lectura incremental; excluir hashes, claves y tokens. |
| I11 | Información → Laboratorios | Cambios de catálogo, recursos e incidencias | GET REST periódico sobre HTTPS | Proyección diferida e idempotente; no acceder a tablas ajenas. |
| I12 | Información → Reservas | Cambios de agenda para reportes y avisos | GET REST periódico sobre HTTPS | La reserva no espera a la proyección. Confirmar cursor solo después de aplicarla. |
| I13 | Laboratorios → Reservas | Comando activar/retirar barrera: laboratorio, ID, revisión y estado deseado | REST/JSON, HTTPS, sincrónico con conciliación | Persistir resultado y deduplicación. No invocar I09 desde el manejador. No aplicar revisiones antiguas. |
| D01–D04 | Cada servicio → su almacén | Persistencia exclusiva de su dominio | JDBC/SQL, TLS en red previsto | Transacción local; ninguna escritura directa en bases de otros servicios. |

HTTPS, autorización, bases privadas y cambios durables son objetivos futuros.
La lectura periódica es asincrónica respecto del productor, **no una llamada HTTP
que carezca de respuesta**. I13 tampoco crea una transacción atómica entre bases.

## Contrato real de E1

```text
Cliente → Reservas: GET http://127.0.0.1:8082/api/reservas/comunicacion
Reservas → Laboratorios: GET http://127.0.0.1:8081/api/laboratorios/info
Laboratorios → Reservas: 200 application/json
Reservas → Cliente: 200 application/json, respuesta anidada
```

Laboratorios responde:

```json
{"servicio":"laboratorios","mensaje":"Servicio de laboratorios de CLAB disponible"}
```

Reservas responde:

```json
{"servicio":"reservas","laboratorios":{"servicio":"laboratorios","mensaje":"Servicio de laboratorios de CLAB disponible"}}
```

Si falla la conexión, se recibe un error HTTP, no se puede decodificar el JSON o
el cuerpo está vacío, el controlador convierte el fallo en HTTP 503. Esto no
significa que todos esos casos estén cubiertos por las tres pruebas existentes:
estas simulan éxito, error de conexión y ausencia de contenido. El formato del
cuerpo de error lo genera Spring; no se fija aquí un contrato estable inexistente.

La URL base se configura con `LABORATORIOS_URL`. Los puertos se configuran con
`LABORATORIOS_PORT` y `RESERVAS_PORT`; `SERVER_ADDRESS` permite seleccionar la
interfaz. Los valores por defecto solo escuchan en `127.0.0.1`. Son dos procesos,
sin base de datos, autenticación ni creación de reservas. El intercambio mínimo
es un antecedente técnico de I09, no su implementación de negocio.

## Contratos objetivo que deben concretarse en E2

- Versionar los nuevos contratos de negocio, por ejemplo mediante prefijo `/api/v1`,
  sin romper los endpoints de diagnóstico de E1. Registrar OpenAPI y ejemplos.
- Definir DTO, campos obligatorios, tipos, estados permitidos y validación.
  Fechas de agenda con zona/offset acordado e intervalos semiabiertos `[inicio, fin)`.
- Propuesta de errores: 400 validación, 401 identidad inválida, 403 sin permiso,
  404 recurso inexistente, 409 conflicto/revisión incompatible y 503 dependencia
  indisponible. Acordar cuerpo con código, mensaje seguro e ID de correlación.
  Esta propuesta no sustituye el comportamiento actual del esqueleto.
- I13: ID estable, revisión creciente y resultado consultable. Mismo ID con
  contenido distinto se rechaza; un resultado histórico no reejecuta su efecto.
  No iniciar otro trámite por laboratorio hasta resolver el pendiente.
- I10–I12: evento con ID, origen, versión de esquema y carga mínima; cursor opaco,
  páginas acotadas y orden estable por origen. Aplicar evento y actualizar cursor
  en una transacción local. Si se pierde retención, reconstruir la proyección;
  no avanzar silenciosamente el cursor. No se requiere orden global entre fuentes.
- Reintentos propuestos: como máximo tres intentos totales para lecturas transitorias,
  con espera incremental y jitter; valores finales tras medir y acordar presupuesto.
  Para comandos, consultar resultado por ID; ningún reintento ciego con un ID nuevo.
  El esqueleto no incorpora estos reintentos ni circuit breaker.
- Autenticación de personas y de máquina separadas, permisos mínimos, secretos fuera
  de Git, HTTPS en red y propagación de correlación sin datos sensibles.

## Fallos que deben ensayarse

| Caso | Resultado exigido por el diseño |
|---|---|
| Identidad no responde | No ejecutar una operación protegida. |
| Catálogo no responde durante nueva reserva | No confirmar desde una copia vieja. |
| Se pierde el acuse de I13 | Conservar pendiente; recuperar el mismo resultado durable por ID. |
| Orden de cierre anterior a una reapertura | Rechazar una revisión nueva atrasada; no reaplicar resultados históricos. |
| Información se detiene | Continuar las transacciones locales y recuperar cambios después. |
| Reinicio del consumidor tras aplicar una página | No duplicar efectos; cursor y aplicación atómicos localmente. |

Estos son criterios futuros, no resultados de pruebas ejecutadas. El informe de
verificación del esqueleto se mantiene separado de las pruebas abstractas del
protocolo de cierre. No se recibieron resultados originales de PE-U1: su contraste
queda pendiente y no se reemplaza por cifras inventadas de REST, gRPC o mensajería.

Preparado con asistencia de OpenAI GPT-6.1 Sol; aceptación de contratos y defensa
personal pendientes de sus responsables.
