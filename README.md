# CLAB - Proyecto Fin de Curso

CLAB gestiona los laboratorios y sus reservas. Esta base para E1 contiene dos servicios Java independientes que intercambian información mediante HTTP y JSON.

## Organización

```text
clab-pfc-7a/
  legado/                       Código heredado de CLAB
    backend/Clab-backend/        Backend Spring Boot original
    frontend/clab-frontend/      Frontend Angular original
    .idea/                      Configuración del editor del proyecto original
    package.json                Dependencias del proyecto original
    package-lock.json
  src/
    servicio-laboratorios/      Servicio que responde la consulta
    servicio-reservas/          Servicio que consulta a Laboratorios
  docs/
    adr/                        Registros de decisiones de arquitectura
    diagramas/                  Diagramas editables
  evidencias/                   Evidencias reales obtenidas por el equipo
  BITACORA.md                   Registro del trabajo realizado
  pom.xml                       Proyecto Maven con los dos servicios de E1
  mvnw
  mvnw.cmd
```

El código heredado procede de [Clab--Sistema](https://github.com/Danxxx777/Clab--Sistema), importado en este repositorio antes de E1. Se conserva en `legado/` para consultar y migrar sus componentes durante el PFC. La base de esta reorganización es el commit `5df22c945b82ff962541ebc33a2fa69984cd88b5`.

Abre la raíz del repositorio en el editor. En IntelliJ IDEA, importa el `pom.xml` de la raíz como proyecto Maven. Este archivo incluye los dos módulos de `/src/`. En VS Code, la configuración de `java.import.exclusions` excluye `legado/` de la importación automática de proyectos Java. Para trabajar directamente en el sistema heredado, abre la carpeta correspondiente dentro de `legado/` en otra ventana.

## Requisitos de ejecución

- JDK 17 o 21 con `java` disponible en la terminal. Compruébalo con `java -version`.
- Acceso a Internet durante la primera compilación para descargar Maven y sus dependencias.
- Puertos locales 8081 y 8082 disponibles.

El Maven Wrapper incluido permite compilar desde Windows, Linux y macOS. El código nuevo utiliza Spring Boot 3.2.1 y Java 17, las versiones declaradas por el backend original.

## Compilación

Desde la raíz del repositorio, en PowerShell ejecuta

```powershell
.\mvnw.cmd clean verify
```

En Linux o macOS usa `sh ./mvnw clean verify`.

El proceso compila los dos servicios, ejecuta las pruebas automatizadas de la consulta HTTP y genera un JAR ejecutable por servicio. Las pruebas usan una respuesta simulada de Laboratorios para comprobar la conversión de JSON y el tratamiento de conexión fallida o respuesta vacía.

## Arranque de los servicios

Abre dos terminales situadas en la raíz del repositorio.

En la primera ejecuta Laboratorios

```powershell
java -jar src/servicio-laboratorios/target/servicio-laboratorios-0.0.1-SNAPSHOT.jar
```

En la segunda ejecuta Reservas

```powershell
java -jar src/servicio-reservas/target/servicio-reservas-0.0.1-SNAPSHOT.jar
```

Ambos servicios se enlazan a `127.0.0.1`. La URL de Laboratorios que utiliza Reservas se configura con `LABORATORIOS_URL`. Los puertos pueden configurarse con `LABORATORIOS_PORT` y `RESERVAS_PORT`. Si cambias el puerto de Laboratorios, ajusta también `LABORATORIOS_URL` antes de iniciar Reservas.

## Consulta entre servicios

Desde una tercera terminal en PowerShell ejecuta

```powershell
Invoke-RestMethod http://127.0.0.1:8081/api/laboratorios/info | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8082/api/reservas/comunicacion | ConvertTo-Json -Depth 3
```

La segunda petición llega a Reservas. Ese servicio consulta a Laboratorios por HTTP, espera su respuesta y la incluye en el JSON que entrega al cliente. El resultado esperado es

```json
{
  "servicio": "reservas",
  "laboratorios": {
    "servicio": "laboratorios",
    "mensaje": "Servicio de laboratorios de CLAB disponible"
  }
}
```

La llamada es sincrónica y utiliza REST con JSON. Reservas tiene límites de conexión y lectura de dos segundos cada uno. Si Laboratorios está detenido, devuelve un error o entrega una respuesta vacía, Reservas responde HTTP 503. El endpoint realiza una consulta de comprobación de comunicación. Las operaciones de reserva y la persistencia se incorporarán al desarrollar la funcionalidad del PFC.

## Ejecución y evidencias del equipo

Para comprobar la dependencia entre procesos, ejecuta la consulta a Reservas, detén Laboratorios con `Ctrl+C`, repite la consulta y vuelve a iniciar Laboratorios. Repite la petición para observar la recuperación. Conserva los resultados que obtengas en tu ejecución.

Para mostrar tu usuario, equipo, fecha y hora en las capturas de terminal ejecuta

```powershell
whoami
hostname
Get-Date -Format o
```

Las capturas de ejecución, el video y la bitácora se elaboran a partir de las sesiones realizadas por los integrantes.

## Asistencia de IA

La reorganización en `legado/`, el esqueleto Java, sus pruebas automatizadas y estas instrucciones se prepararon con asistencia de OpenAI Codex. El asistente compiló los servicios y ejecutó las tres pruebas automatizadas con respuestas simuladas. Las evidencias de ejecución personal se obtienen en las sesiones de los integrantes.
