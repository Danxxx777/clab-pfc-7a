# CLAB - Proyecto Fin de Curso

CLAB es la aplicación web de gestión de laboratorios y reservas desarrollada en semestres anteriores, con un backend centralizado. El PFC de Aplicaciones Distribuidas propone evolucionarla hacia una arquitectura distribuida. Esta base para E1 contiene dos servicios Java mínimos que intercambian información mediante HTTP y JSON; ese esqueleto no equivale a la migración del sistema de negocio.

## Integrantes y responsabilidades de E1

- Byron Daniel Loor Mendoza, Responsable de Documentación. [Seguimiento del bloque](https://github.com/Danxxx777/clab-pfc-7a/issues/1).
- Roger Garcia (`Esteiben`), Líder de Desarrollo. [Comunicación, esqueleto y plan técnico](https://github.com/Danxxx777/clab-pfc-7a/issues/3).
- Juliana Emanuel Pino (`JulianaEmanuel`), Arquitecta. [Arquitectura y ADR-001](https://github.com/Danxxx777/clab-pfc-7a/issues/2).
- Carlos Manotoa (`CarlosManotoa007`), Responsable de Calidad. [Calidad y evidencias](https://github.com/Danxxx777/clab-pfc-7a/issues/4).

Las issues se abrieron el 21 de noviembre de 2026 para vincular los aportes
existentes y seguir los pendientes reales de cada bloque.

El borrador del informe reúne las declaraciones de Carlos y Byron y los
registros de asistencia presentes en los archivos de Arquitectura y Desarrollo.
En el registro de CAP/PACELC queda por confirmar la versión concreta del modelo
y la revisión personal de su responsable.

## Organización

```text
clab-pfc-7a/
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

El código de semestres anteriores se consulta en [Clab--Sistema](https://github.com/Danxxx777/Clab--Sistema). Esta copia conserva el trabajo del equipo de PFC desde noviembre de 2026; el código heredado se retiró de sus archivos y del historial de `main`. Se mantiene la procedencia del proyecto.

El [informe original de CLAB](evidencias/antecedentes/CLAB-informe-original-2026.pdf)
se conserva como antecedente documental. Sus páginas 14 y 15 contienen los
dieciséis requisitos de origen, las páginas 19 y 20 describen el diagnóstico
y las páginas 45 a 47 incluyen la guía de entrevistas y una fotografía.
Las historias de E1 remiten a esos requisitos. El acta firmada o el audio
consentido que exige la guía vigente siguen pendientes de incorporación.

Abre la raíz del repositorio en el editor. En IntelliJ IDEA, importa el `pom.xml` de la raíz como proyecto Maven. Este archivo incluye los dos módulos de `/src/`.

## Requisitos de ejecución

- JDK 25 con `java` disponible en la terminal. Compruébalo con `java -version`.
- Acceso a Internet durante la primera compilación para descargar Maven y sus dependencias.
- Puertos locales 8081 y 8082 disponibles.

El Maven Wrapper incluido permite compilar desde Windows, Linux y macOS. El proyecto utiliza Spring Boot 3.5.16 y Java 25.

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

### Video de E1

[Ver presentación y demostración de CLAB] https://youtu.be/whyKD8NsjFg

## Compilación del documento de E1

El archivo principal es `docs/main.tex`. Se compila con pdfLaTeX y Biber
desde la carpeta `docs`. El resultado es `docs/main.pdf`.

```powershell
Set-Location docs
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

El informe utiliza la clase `article`, en una columna compacta, conserva la
portada académica y coloca las figuras y tablas dentro de su sección.
La distribución TeX debe incluir `fontenc`, `geometry`, `babel` con español, `csquotes`,
`graphicx`, `float`, `array`, `microtype`, `enumitem`, las fuentes Times y Courier de `psnfss`, `biblatex` con el estilo
`ieee`, `xurl` e `hyperref`. Las bibliografías son `docs/referencias.bib` y
`docs/arquitectura/fuentes-arquitectura.bib`. Las figuras C4 se incluyen desde
`docs/figuras` y las capturas desde `evidencias`.

El informe integra los aportes disponibles de arquitectura, requisitos y
calidad, la tabla de aportes y las capturas. La aprobación de las propuestas
y la integración de los apartados restantes de E1 siguen pendientes.

## Asistencia de IA

La reorganización en `legado/`, el esqueleto Java, sus pruebas automatizadas y estas instrucciones se prepararon con asistencia de OpenAI Codex. El asistente compiló los servicios y ejecutó las tres pruebas automatizadas con respuestas simuladas. Las evidencias de ejecución personal se obtienen en las sesiones de los integrantes.
