# ADR-002: HTTP REST/JSON como mecanismo principal

- Estado: propuesto; pendiente de aceptación del equipo.
- Alcance: comunicación de CLAB en E1 y contratos objetivo para E2–E4.
- Seguimiento: [issue #3](https://github.com/Danxxx777/clab-pfc-7a/issues/3).
- Base de revisión: `7e1b00cac5e4ca3f975b0359acd4bca8fd7d37bf`.

## Contexto y criterios

El esqueleto existente usa Java 25, Spring Boot 3.5.16 y dos procesos. Reservas
consulta a Laboratorios con `RestClient`; el cliente configura dos segundos de
conexión y dos segundos de lectura. La lógica de reservas, la autorización y la
persistencia todavía no están implementadas. La propuesta C4 contiene cuatro
servicios por dominio, definidos por ADR-001, cuya autoría se conserva.

Se requieren contratos inspeccionables, integración con la SPA, fallos acotados
por operación y un entorno reproducible para el equipo. Los resultados originales
de PE-U1 no están disponibles en el material revisado: no se atribuye a esta
decisión una victoria experimental ni cifras comparativas inexistentes.

## Alternativas

| Alternativa | Adecuación y coste |
|---|---|
| REST/JSON sobre HTTP | Compatible con la base existente y la SPA; se prueba con herramientas HTTP. JSON requiere validación explícita; las consultas sincrónicas acoplan disponibilidad y latencia. |
| gRPC/Protocol Buffers | Contrato tipado y generación de clientes; introduce gestión de esquemas y herramientas adicionales, y la SPA requiere adaptación. No se midió su rendimiento en CLAB. |
| Mensajería mediante broker | Desacopla temporalmente procesamiento y permite consumidores independientes; exige operación del broker, confirmaciones, retención y deduplicación. No reemplaza automáticamente las consultas ni garantiza entrega exactamente una vez. |

## Decisión propuesta

Conservar REST/JSON como mecanismo principal. En E1 el transporte real es HTTP
local; HTTPS y credenciales de servicio son requisitos del despliegue futuro,
no características ya demostradas. La comunicación de negocio no utiliza SQL
entre bases de servicios ni llamadas directas desde la SPA a esas bases.

1. **Peticiones interactivas:** solicitud/respuesta sincrónica. Cada servicio
   comprueba permisos; un botón oculto no es control de acceso. Las consultas a
   Identidad fallan de forma cerrada si no se puede verificar autorización.
2. **Agenda:** Reservas decide ocupación localmente. I09 consulta catálogo; no
   decide conflictos de horario. I13 coordina la barrera mediante comandos
   durables con ID estable y revisión. Se conserva el orden de ADR-001: cierre
   pendiente → barrera confirmada → fuera de servicio; reapertura pendiente →
   retiro de barrera operativa → activo. No se cancelan reservas previas.
3. **Sin llamadas circulares:** el manejador I13 no invoca I09. La validación de
   permisos no equivale a reconsultar el catálogo ni promete revertir operaciones
   confirmadas después de una revocación.
4. **Información y Avisos:** consulta periódica de cambios durables por REST,
   con procesamiento diferido respecto de la transacción de origen. Cada HTTP
   sigue siendo sincrónico; esto no significa que exista un broker.
5. **Fallo y reintento:** un timeout de escritura da resultado desconocido, no
   evidencia de rollback. Consultar el resultado por el mismo ID antes de
   reintentar; no generar IDs nuevos. No reintentar automáticamente 400/401/403
   ni conflictos de negocio. La deduplicación debe persistirse, no guardarse solo
   en memoria. Los GET podrán reintentarse con espera incremental y límite.

El [modelo por interacción](../desarrollo/modelo-comunicacion.md) precisa los
contratos propuestos. Los URI de negocio, valores de espera futuros, política de
retención y SLO necesitan aceptación y pruebas; no se modifican los dos endpoints
existentes por esta decisión documental.

## Consecuencias y validación

- Se reutiliza el esqueleto sin introducir infraestructura no justificada.
- Identidad y Laboratorios afectan la disponibilidad de operaciones dependientes;
  usar REST no elimina fallos parciales ni crea una transacción distribuida.
- Los reportes pueden quedar atrasados y deben mostrar su punto de actualización.
- La lectura periódica necesita paginación, cursores durables y control de carga;
  si se exceden los objetivos acordados se reconsiderará un broker en otro ADR.
- Los dos límites de dos segundos no constituyen un SLA total de cuatro segundos:
  resolución de nombres, procesamiento y otras fases pueden añadir tiempo.
- E1 se valida con `clean verify` y una prueba de procesos reales que observe
  200 → caída de Laboratorios → 503 → recuperación → 200. Eso no valida las
  garantías de cierre, bases privadas, autorización ni el sistema completo.
- Antes de aceptar este ADR: contrastar con los resultados auténticos de PE-U1,
  acordar los contratos y ensayar particiones, duplicados, concurrencia y reinicios
  en las operaciones implementadas de E2–E4. No se simula aprobación colectiva.

## Asistencia

Documento preparado para el bloque de Desarrollo con apoyo de OpenAI GPT-6.1 Sol.
La revisión del código y las ejecuciones automatizadas del asistente se distinguen
de la ejecución personal y de la aceptación que corresponde al equipo.
