# Desarrollo — Ejecución, validación y demostración

Complemento del [README de la raíz](../../README.md), que conserva los aportes
existentes. No cambia el runtime ni la implementación de los compañeros.

## Preparación y compilación

Requisitos: JDK 25, puertos disponibles y acceso a dependencias Maven durante la
primera compilación. El wrapper está incluido; no hace falta instalar Maven.
Desde la raíz del repositorio:

```powershell
java -version
.\mvnw.cmd clean verify
```

Linux/macOS:

```sh
java -version
sh ./mvnw clean verify
```

Se generan los JAR de `src/servicio-laboratorios/target/` y
`src/servicio-reservas/target/`. Las tres pruebas existentes usan una dependencia
simulada; no se atribuyen al nuevo script ni se confunden con dos procesos reales.

## Demostración manual: tres terminales

Terminal A, desde la raíz:

```sh
java -jar src/servicio-laboratorios/target/servicio-laboratorios-0.0.1-SNAPSHOT.jar
```

Terminal B:

```sh
java -jar src/servicio-reservas/target/servicio-reservas-0.0.1-SNAPSHOT.jar
```

Terminal C, PowerShell:

```powershell
whoami
hostname
Get-Date -Format o
Invoke-RestMethod http://127.0.0.1:8081/api/laboratorios/info | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8082/api/reservas/comunicacion | ConvertTo-Json -Depth 3
```

En Linux/macOS, las consultas equivalentes son:

```sh
whoami
hostname
date -Iseconds
curl -i http://127.0.0.1:8081/api/laboratorios/info
curl -i http://127.0.0.1:8082/api/reservas/comunicacion
```

Con los dos procesos activos, ambas consultas deben responder 200 y la segunda
incluye el mensaje de Laboratorios. Detener **solo Laboratorios** con Ctrl+C en
A. Repetir la consulta a Reservas: debe responder 503; el proceso de Reservas
sigue vivo. Reiniciar Laboratorios y repetir: debe recuperarse a 200 sin
reiniciar Reservas. No se crea ninguna reserva ni se escribe una base de datos.

PowerShell puede lanzar una excepción con el 503. Para ver el estado con una
salida equivalente a Linux, usar `curl.exe -i` (no el alias `curl` de versiones
antiguas de PowerShell):

```powershell
curl.exe -i http://127.0.0.1:8082/api/reservas/comunicacion
```

## Configuración

| Variable | Valor predeterminado | Consideración |
|---|---|---|
| `LABORATORIOS_PORT` | `8081` | Cambiar también la URL que usa Reservas si se modifica este puerto. |
| `RESERVAS_PORT` | `8082` | Puerto HTTP de Reservas. |
| `LABORATORIOS_URL` | `http://127.0.0.1:8081` | URL base; no añadir `/api/laboratorios/info` porque el cliente añade la ruta. |
| `SERVER_ADDRESS` | `127.0.0.1` | No exponer en una red pública el esqueleto sin autenticación. |

Por ejemplo, antes de arrancar los procesos, si se usa 9081 para Laboratorios:

```powershell
$env:LABORATORIOS_PORT = '9081'
$env:LABORATORIOS_URL = 'http://127.0.0.1:9081'
```

Definir cada variable en la terminal del proceso que la necesita. En Linux/macOS
se usa `export LABORATORIOS_PORT=9081` y
`export LABORATORIOS_URL=http://127.0.0.1:9081`.

## Prueba automatizada con procesos reales

Requisito adicional opcional: Python 3, sin paquetes externos. Después de compilar:

```powershell
python scripts/verificar_esqueleto.py --salida verificacion-local.json
```

En Linux/macOS usar `python3`. Si Python o Java no están en PATH, invocar el
ejecutable correspondiente; `--java` permite seleccionar la ruta del JDK 25.
El script escoge puertos locales libres, inicia sus propios dos JAR, comprueba
consulta directa, comunicación anidada, caída y recuperación; finalmente detiene
solo sus procesos. No compila ni modifica código ni detiene servicios ajenos.
Una carrera al asignar puertos puede hacer fallar el arranque: revisar logs y
reintentar, no atribuir ese fallo a una confirmación del comportamiento esperado.

El resultado JSON registra estados HTTP, versión Java, fechas UTC y SHA-256 de
los JAR; los logs quedan en un directorio temporal indicado al terminar. El
script no sobrescribe un resultado existente. `verificacion-local.json` es
salida local: no subir automáticamente logs, `target/`, credenciales o archivos
del entorno. Revisar el resultado antes de incorporarlo como evidencia propia.

El [resultado asistido](verificacion-asistida.json) corresponde a la ejecución
automatizada del asistente descrita en [su alcance](verificacion.md); **no
acredita ejecución personal del integrante ni participación en el video**.

## Diagnóstico breve

- `release version 25 not supported`: seleccionar JDK 25 y comprobar JAVA_HOME.
- Puerto ocupado: detener solo el proceso propio o cambiar puerto y URL de forma
  coherente. No finalizar procesos ajenos indiscriminadamente.
- 503 con ambos procesos: consultar directamente Laboratorios, revisar URL,
  puertos y logs; no asumir que el endpoint creó o rechazó una reserva.
- Descarga Maven fallida: revisar conectividad y repetir `clean verify`; no
  presentar una compilación interrumpida como correcta.

## Verificación automatizada con procesos reales

Después de `clean verify`, se puede ejecutar el script opcional con Python 3
(solo biblioteca estándar). No sustituye los pasos manuales del video.

PowerShell:

```powershell
py -3 scripts/verificar_esqueleto.py --salida resultados-http-personal.json
```

Linux/macOS:

```sh
python3 scripts/verificar_esqueleto.py --salida resultados-http-personal.json
```

El script elige dos puertos locales libres, arranca los JAR y verifica cuatro
casos: consulta directa, respuesta anidada, dependencia detenida y recuperación.
Solo finaliza procesos que inició. Usa `--java` si el ejecutable JDK 25 no está
en PATH. No sobreescribe resultados existentes; usar otro nombre al repetir.
Las salidas contienen fecha real y resultados; revisar privacidad antes de
publicarlas. Los logs quedan en una carpeta temporal local y no se suben por
defecto. El informe incluido como `verificacion-asistida.json` corresponde al
asistente, no a la ejecución personal del integrante.

## Video y seguimiento

Guion propuesto, no grabación ya realizada: mostrar rostro y rol; explicar los
dos procesos y REST/JSON; mostrar arranque y petición anidada; detener la
dependencia, observar 503, recuperarla y observar 200; cerrar con los límites de
E1. El miembro debe ejecutar y explicar su demostración, no atribuirse la prueba
del asistente. Coordinar duración con el video del equipo y no mostrar secretos.

En [#3](https://github.com/Danxxx777/clab-pfc-7a/issues/3), enlazar los aportes
publicados y la ejecución personal cuando exista. El [plan](plan-entregas.md)
incluye las tareas que se deben trasladar a un Project real; los resultados de
PE-U1, su contraste y el enlace del tablero siguen requiriendo incorporación.

Preparado con asistencia de OpenAI GPT-6.1 Sol. El código base y las tres pruebas
previas conservan la procedencia declarada en el README raíz y la bitácora.
