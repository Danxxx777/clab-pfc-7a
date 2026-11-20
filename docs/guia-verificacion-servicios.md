# Guía de verificación de los servicios CLAB

Esta guía complementa el [README principal](../README.md) y reúne pruebas manuales para el esqueleto E1 de Laboratorios y Reservas. **Los resultados descritos son expectativas de la implementación, no evidencias de una ejecución realizada para esta guía.**

## Preparación

Se necesita JDK 25, PowerShell y los puertos 8081 y 8082 disponibles. Desde la raíz:

```powershell
java -version
.\mvnw.cmd clean verify
```

El comando compila el proyecto y ejecuta las pruebas automatizadas configuradas. Si falla, conserva el error antes de intentar iniciar los servicios.

Inicia cada servicio en una terminal independiente:

**Terminal 1 — Laboratorios**
```powershell
java -jar src/servicio-laboratorios/target/servicio-laboratorios-0.0.1-SNAPSHOT.jar
```

**Terminal 2 — Reservas**
```powershell
java -jar src/servicio-reservas/target/servicio-reservas-0.0.1-SNAPSHOT.jar
```

## Casos de comprobación

En una tercera terminal:

| Caso | Acción | Comprobación esperada |
| --- | --- | --- |
| Laboratorios disponible | `Invoke-RestMethod http://127.0.0.1:8081/api/laboratorios/info` | JSON del servicio Laboratorios |
| Comunicación entre servicios | `Invoke-RestMethod http://127.0.0.1:8082/api/reservas/comunicacion | ConvertTo-Json -Depth 3` | Reservas incorpora la respuesta de Laboratorios |
| Dependencia no disponible | Detener Laboratorios con `Ctrl+C` y consultar Reservas | Reservas responde HTTP 503 si no consigue completar la consulta |
| Recuperación | Reiniciar Laboratorios y volver a consultar Reservas | La consulta vuelve a completarse |
| Reservas detenido | Detener Reservas y consultar su endpoint | Error de conexión al puerto 8082, no una respuesta HTTP 503 |

Para inspeccionar el estado HTTP aunque PowerShell trate las respuestas 5xx como errores, puedes usar:

```powershell
try {
    Invoke-WebRequest http://127.0.0.1:8082/api/reservas/comunicacion -ErrorAction Stop
} catch {
    Write-Host "Error observado:" $_.Exception.Message
    if ($_.Exception.Response) {
        Write-Host "Estado HTTP:" [int]$_.Exception.Response.StatusCode
    }
}
```

La recuperación consiste en iniciar nuevamente el proceso detenido y repetir la solicitud: el esqueleto no implica un mecanismo automático de reinicio, reintentos ni tolerancia a fallos.

## Diagnóstico básico

- **Puerto ocupado:** verifica qué proceso escucha en `8081` o `8082`, por ejemplo mediante `Get-NetTCPConnection -LocalPort 8081,8082 -ErrorAction SilentlyContinue`.
- **Versión incorrecta de Java:** confirma que `java -version` corresponde al JDK 25 requerido por este proyecto.
- **Laboratorios en otro puerto:** si cambias `LABORATORIOS_PORT`, ajusta también `LABORATORIOS_URL` al iniciar Reservas.
- **Error HTTP 503:** comprueba primero si Laboratorios está ejecutándose y si Reservas apunta a su dirección correcta. El servicio puede responder 503 por fallo o respuesta inválida de su dependencia.
- **Error de conexión al consultar Reservas:** comprueba si Reservas está iniciado y escucha en el puerto esperado.

## Registro de evidencias

Documenta únicamente pruebas ejecutadas realmente. Para contextualizar capturas, puedes mostrar:

```powershell
whoami
hostname
Get-Date -Format o
```

Guarda junto a cada evidencia el caso probado, el comando, el resultado observado y cualquier incidencia. Actualiza `BITACORA.md` con la fecha real de ejecución, integrantes presentes y alcance de las pruebas. No incluyas contraseñas, tokens, variables secretas ni datos personales en capturas públicas.
