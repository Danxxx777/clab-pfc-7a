# ADR-001: migración gradual a servicios por dominio

- Estado: propuesto; pendiente de revisión y aceptación del equipo.
- Alcance: arquitectura objetivo de CLAB para E1–E4.
- Base de revisión: rama `main`, commit `81c75c4ee2eb00f812d9a0025379010bb4db4173`.
- Revisión de coherencia con los requisitos E1 y el borrador CAP/PACELC de JulianaEmanuel: `a2ecc7d14ceeca4587ea271f542b4c5eccd60dcb`.
- Revisión del protocolo de cierre y reapertura: `88f587d77865872a62cbc63b2b43a68a6ed6d4c8`. El protocolo forma parte de la propuesta; no acredita aceptación colectiva ni implementación.

## Contexto

CLAB gestiona laboratorios informáticos de la UTEQ. El documento previo describe reservas con conflictos de horario, inventario, incidencias y reportes. Es un antecedente de dominio, no un acta de levantamiento verificable para E1. En la revisión no se dispuso de acta firmada ni grabación consentida. Los requisitos y las prioridades deberán contrastarse con esa evidencia.

El legado conservado en `/legado/` tiene frontend Angular, backend Spring Boot y PostgreSQL. `ReservaRepository` invoca funciones y procedimientos del esquema `reservas`; por tanto, migrar controladores no basta para separar el dominio. El esqueleto de `/src/` contiene dos procesos Spring Boot: Reservas consulta a Laboratorios por REST/JSON y devuelve HTTP 503 ante una dependencia no disponible. No incorpora persistencia ni operaciones de negocio.

El plan académico exige evolucionar hasta un sistema distribuido y migrar el sistema completo durante el periodo. En la revisión E1 actual, RNF-01 concreta la meta de latencia: al menos el 95 % de las consultas válidas de disponibilidad correctas en menos de 2 segundos, durante 10 minutos de carga estable con 50 usuarios concurrentes; errores y tiempos agotados cuentan como incumplimientos. RNF-02 propone al menos el 99 % de comprobaciones correctas dentro de 5 segundos, con una sonda por minuto durante dos semanas de horario académico acordado. Son requisitos propuestos, no mediciones; su validación con usuarios y las pruebas siguen pendientes. No se ha demostrado que un monolito sea insuficiente por volumen o distribución geográfica.

RNF-03 exige no ejecutar confirmaciones, cancelaciones o bloqueos sin autorización verificable, incluida la revocación o pérdida de Identidad. RNF-06 exige confirmar y persistir diez reservas de prueba en franjas diferentes con Información y Avisos detenido y las dependencias de agenda operativas. RNF-07 exige auditoría local en todos los cambios exitosos del conjunto de prueba. Estos requisitos concretan las consecuencias de la agrupación propuesta sin demostrar todavía que se cumplan.

## Opciones consideradas

1. **Mantener un monolito modular.** Menor complejidad operativa y transacciones locales sencillas; puede satisfacer la demanda descrita, pero no ofrece despliegue independiente por dominio ni cumple el objetivo académico de migración a servicios.
2. **Crear un servicio por cada uno de los doce módulos.** Independencia fina, a costa de numerosas dependencias remotas, más procesos y transacciones distribuidas entre reservas, bloqueos y asistencia.
3. **Agrupar los doce módulos en cuatro servicios por dominio y migrarlos por etapas.** Mantiene juntas las invariantes de agenda y reduce las fronteras remotas sin conservar un backend único.

## Decisión propuesta

Adoptar la opción 3. Los cuatro servicios son desplegables independientes con API y almacenamiento de propiedad exclusiva. Un módulo no equivale automáticamente a un microservicio.

| Servicio objetivo | Módulos del legado que incorpora | Datos e invariantes de su propiedad |
|---|---|---|
| Identidad y Académico | Usuarios, Académico, Estudiantes | Credenciales, roles, permisos, carreras, asignaturas, periodos, matrículas e inscripciones. |
| Laboratorios y Recursos | Laboratorios, Equipos, Reportes de Fallas | Catálogo, capacidad, equipos, incidencias e historial técnico. No decide la ocupación de intervalos. |
| Reservas y Agenda | Reservas, Bloqueos, Asistencia | Intervalos reservados, cancelaciones, bloqueos efectivos y asistencia. Es la única autoridad sobre ocupación. |
| Información y Avisos | Reportes de Uso, Notificaciones, vista central de Auditoría | Proyecciones de consulta, avisos internos y copia de auditoría. No confirma reservas ni modifica datos de origen. |

La auditoría fuente se registra transaccionalmente en cada servicio que modifica datos. Su vista central se actualiza después; una caída de Información y Avisos no debe borrar ni impedir el registro local de auditoría. Esta agrupación cubre los doce módulos sin prometer que ya estén migrados.

### Reglas de datos y comunicación

- Cada servicio escribe únicamente en su almacén. Se prohíben consultas SQL y claves foráneas entre almacenes de servicios distintos. Pueden alojarse en una misma instancia PostgreSQL al inicio, con bases y credenciales separadas; eso no elimina el punto único de fallo de la instancia.
- Reservas controla reservas y bloqueos dentro de una misma transacción. Se propone serializar todas las mutaciones de agenda por laboratorio mediante un bloqueo de fila estable y verificar solapamientos antes de confirmar. Todos los caminos de escritura, incluidas recurrencias, deben respetarlo; no basta un `SELECT` previo a un `INSERT`.
- El cierre de un laboratorio por mantenimiento se hace efectivo en la agenda al confirmar el bloqueo en Reservas. Un cambio de estado en el catálogo no equivale a un bloqueo confirmado. La interfaz debe mostrar el estado pendiente si no puede completar el trámite.
- Reservas consulta el catálogo de Laboratorios mediante REST antes de una nueva reserva. Si no puede validarlo, no confirma. Esa consulta no convierte dos bases en una transacción atómica: la ocupación se decide exclusivamente en Reservas y los metadatos consultados se conservan como instantánea.
- Para RF-P04, el cierre se hace efectivo al confirmar una barrera de nuevas reservas en Reservas. Solo después se publica `FUERA_DE_SERVICIO` en el catálogo. Consultar el catálogo antes de insertar no es la protección concurrente: toda confirmación vuelve a comprobar la barrera bajo el mismo bloqueo local por laboratorio. El protocolo siguiente precisa esta decisión sin prometer una transacción entre dos bases.
- La SPA obtiene credenciales de sesión en Identidad. Los otros tres servicios verifican sesión, usuario activo y permisos con Identidad por REST antes de autorizar solicitudes protegidas; ante fallo, deniegan la operación sin tratar el fallo como credenciales incorrectas. Es una dependencia central explícita, elegida para evitar permisos revocados aceptados desde una caché.
- Información y Avisos consulta incrementalmente registros de cambios durables de los otros tres servicios mediante REST en segundo plano. Cada origen escribe dato, auditoría y registro de cambio en la misma transacción; el consumidor conserva cursor y deduplica por origen e identificador. El registro de cambio no es una cola en memoria. La propagación es diferida, aunque cada petición HTTP de consulta es sincrónica.
- Los detalles de API, autenticación entre servicios, intervalos de consulta, retención, reintentos y tiempos de espera corresponden al modelo de comunicación y a ADR-002. REST/JSON es la base ya existente, no una comparación experimental ganadora: no se dispuso de resultados de PE-U1.

### Protocolo de cierre y reapertura de RF-P04

**Invariante objetivo:** mientras el catálogo publique `FUERA_DE_SERVICIO`, la barrera correspondiente en Reservas está activa. Una confirmación serializada después del cierre de esa barrera se rechaza, incluso si consultó un catálogo todavía activo antes del cierre. Una reserva que quedó confirmada antes de la barrera se conserva: cerrar no cancela automáticamente reservas existentes ni modifica sus resultados históricos. El responsable debe revisar las actividades afectadas; conservar el registro no autoriza el uso físico de un laboratorio cerrado.

**Propiedad:** Laboratorios conserva el estado operativo visible y la solicitud durable del trámite. Reservas conserva la barrera de admisión y su revisión aplicada. Ambos conservan su auditoría local; no acceden a tablas ajenas. El nuevo enlace C4 **I13** va de Laboratorios a Reservas mediante REST/JSON sincrónico. Reservas autoriza el comando recibido y lo ejecuta localmente; este manejador no vuelve a consultar Laboratorios por I09, para evitar una dependencia circular dentro del trámite. I09 sigue siendo la validación de catálogo de una nueva reserva.

#### Cierre

1. Laboratorios verifica permisos y persiste una solicitud con estado `CIERRE_PENDIENTE`, identificador estable y revisión creciente por laboratorio. Este estado no afirma que el cierre esté confirmado. Solo puede haber un trámite operativo en curso por laboratorio.
2. Por I13 solicita a Reservas activar la barrera. Reservas verifica autorización, adquiere el bloqueo estable por laboratorio que también usa la confirmación de reservas y persiste barrera, revisión, resultado idempotente, auditoría y registro de cambio en la misma transacción local.
3. Tras recibir o consultar una confirmación durable de esa revisión, Laboratorios persiste `FUERA_DE_SERVICIO` con su auditoría local. Si la respuesta se pierde o hay una partición, muestra cierre pendiente y consulta/reintenta la misma solicitud: no presupone que haya fallado ni emite otro trámite con distinto identificador.

Si Reservas confirmó la barrera pero falla la actualización del catálogo, la barrera permanece activa: se pierde disponibilidad, no se reabre el laboratorio para compensar el fallo. La recuperación continúa hasta reconciliar el catálogo con el resultado durable. No se declara un cierre completado sin evidencia de confirmación de la barrera.

#### Reapertura

1. Tras la verificación operativa y de permisos, Laboratorios abandona `FUERA_DE_SERVICIO` y persiste `APERTURA_PENDIENTE` con una revisión posterior. La interfaz no lo anuncia todavía como reservable; la barrera sigue activa.
2. Solicita por I13 retirar únicamente la barrera operativa de esa revisión, bajo el mismo bloqueo de Reservas. No elimina bloqueos académicos, de mantenimiento programado u otras restricciones de agenda.
3. Después de confirmar la revisión aplicada, Laboratorios persiste `ACTIVO`. Si se pierde la respuesta, conserva apertura pendiente y reconcilia la solicitud; no regresa a `FUERA_DE_SERVICIO` mientras la barrera pudiera estar retirada. La validación de catálogo puede seguir rechazando solicitudes durante el estado pendiente, aunque Reservas ya haya retirado la barrera.

Este orden evita dejar el catálogo fuera de servicio con la agenda abierta. La reapertura no garantiza que una franja esté libre: todavía deben comprobarse reservas y bloqueos de intervalo.

#### Reintentos, orden y fallos

- Cada comando lleva laboratorio, identificador de solicitud, revisión y estado deseado. Repetir el mismo identificador y contenido devuelve su resultado sin duplicar efectos; reutilizarlo con contenido diferente se rechaza.
- Reservas no aplica revisiones anteriores a la última aceptada: un comando nuevo con revisión anterior o repetida se rechaza. Reconsultar un identificador ya procesado puede devolver su resultado histórico, pero nunca vuelve a ejecutarlo. Una respuesta atrasada solo puede finalizar el trámite que coincida con la revisión pendiente en Laboratorios. Así una orden de cierre vieja no deshace una reapertura posterior, ni un acuse viejo cambia el catálogo actual.
- No se inicia otro trámite mientras el anterior siga pendiente de resolución. Identificadores, revisiones, barrera y resultados deben sobrevivir a reinicios; su retención debe acordarse en los contratos, no darse por garantizada por una caché en memoria.
- Ante permisos insuficientes o Identidad inaccesible, no se ejecuta un cambio de barrera. Un trámite pendiente puede seguir visible sin anunciar un efecto confirmado. La autorización de una petición no promete deshacer transacciones ya confirmadas por revocaciones posteriores.
- La garantía depende de que **todas** las confirmaciones, incluidas recurrencias y operaciones administrativas, respeten la misma barrera y serialización. Una ruta que la omita invalida el protocolo. Esta propiedad todavía requiere implementación y pruebas de integración.

### Etapas

| Entrega | Incremento previsto y criterio de salida |
|---|---|
| E1 | Definir límites y políticas; mantener los dos servicios mínimos comunicándose. No exigir migración funcional completa en esta entrega. |
| E2 | Incorporar APIs y contenedores, consolidar Reservas y Laboratorios e iniciar Identidad. Inventariar y probar las funciones SQL antes de trasladar su lógica. |
| E3 | Completar los cuatro almacenes y los módulos restantes; incorporar proyecciones y propagación durable. Diseñar y probar la distribución o replicación de datos requerida por E3. |
| E4 | Completar integración de los doce módulos, pruebas de concurrencia, seguridad, recuperación y defensa. Retirar el uso operativo del backend legado únicamente tras validar equivalencia y recuperación. |

No habrá doble escritura entre el backend legado y un servicio nuevo para una misma entidad. Cada corte de migración debe definir fuente de verdad, copia verificable de datos, ventana de cambio y procedimiento de reversión, sin eliminar la copia de consulta del legado.

## Consecuencias

**Beneficios esperados:** despliegue independiente; informes desacoplados del camino de confirmación; escalado selectivo de consultas; invariantes de agenda locales; evolución sin migrar doce servicios a la vez.

**Costes y límites:** más procesos y fallos parciales; contratos versionados; coordinación de identificadores; retraso de avisos; autenticación como dependencia compartida; necesidad de probar migración SQL, cursores y deduplicación. Cuatro servicios en un mismo equipo no constituyen alta disponibilidad. La meta del 99 % no queda garantizada por esta decisión.

**Alternativa de reconsideración:** si las pruebas o la capacidad operativa no justifican cuatro servicios, revisar la agrupación mediante otro ADR; no afirmar que los microservicios siempre mejoran rendimiento o disponibilidad.

## Validación pendiente de la propuesta

- Trazar requisitos hasta el levantamiento real y validar los umbrales propuestos por Calidad. Ya se dispone de percentil, carga y duración en RNF-01, y de sonda y ventana de observación en RNF-02; falta ejecutar y registrar esas pruebas, no volver a definirlos como si no existieran.
- Alinear esta propuesta con ADR-002 y con los resultados reales de PE-U1.
- Revisar colectivamente el protocolo propuesto de RF-P04 y comprobar el invariante catálogo fuera de servicio implica barrera activa, incluidos pérdida de respuesta, reinicios, reintentos y comandos atrasados.
- Probar que dos solicitudes simultáneas para el mismo intervalo no se confirman ambas.
- Probar carreras entre reserva, bloqueo, cancelación y reserva recurrente.
- Detener Información y Avisos: la reserva debe persistir y su auditoría local también; al volver, la proyección debe recuperar los cambios sin duplicarlos.
- Cortar acceso a Identidad: no deben aceptarse operaciones protegidas sin autorización verificable.
- Validar cobertura funcional de los doce módulos y datos migrados antes de retirar el legado.
- Comprobar RNF-01, RNF-02, RNF-03, RNF-06 y RNF-07 contra sus escenarios y conjuntos de prueba E1. RNF-04 y RNF-05 mantienen como restricciones la interfaz adaptable y el despliegue institucional sin nube pública, sin introducir servicios externos obligatorios en este ADR.

## Fuentes técnicas

- Simon Brown, modelo C4, diagramas de contenedores: https://c4model.com/diagrams/container
- PostgreSQL, restricciones: https://www.postgresql.org/docs/current/ddl-constraints.html
- Gilbert y Lynch, fundamento de CAP: https://doi.org/10.1145/564585.564601
- Daniel Abadi, explicación original de PACELC: https://dbmsmusings.blogspot.com/2010/04/problems-with-cap-and-yahoos-little.html

## Declaración de asistencia

Propuesta preparada con asistencia de IA (OpenAI, GPT-6.1 Sol), a partir del documento previo de CLAB y del código consultado. No acredita aceptación del equipo, levantamiento con usuarios ni ejecución experimental de la arquitectura objetivo.
