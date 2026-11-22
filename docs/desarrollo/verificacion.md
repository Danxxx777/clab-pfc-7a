# Verificación asistida del esqueleto E1

- Código base: `7e1b00cac5e4ca3f975b0359acd4bca8fd7d37bf`, rama `main` de CLAB.
- Ejecutor: asistente OpenAI GPT-6.1 Sol, entorno Linux de esta sesión.
- Fecha de ejecución HTTP: 22/11/2026, 02:54:57–02:55:04 UTC; corresponde al
  21/11/2026, 21:54:57–21:55:04 en UTC−05:00. No se altera la fecha de ejecución.
- Runtime de comprobación: Temurin OpenJDK 25.0.5.1+2; compilación `release 25`.
- Resultado HTTP detallado y hashes de los JAR:
  [verificacion-asistida.json](verificacion-asistida.json).

## Compilación y pruebas previas

En una copia de la revisión indicada se ejecutó el wrapper, sin modificar
fuentes, POM ni pruebas existentes:

```sh
sh ./mvnw clean verify
```

Resultado: **BUILD SUCCESS**, dos JAR generados. Las tres pruebas preexistentes
de `ReservasControllerTest` terminaron con 0 fallos, 0 errores y 0 omitidas:
consulta con JSON, conexión fallida y respuesta sin contenido. Usan una dependencia
simulada, no dos servicios desplegados. Laboratorios no tiene pruebas propias
en esa base. Se conserva la procedencia del esqueleto y sus pruebas.

## HTTP entre procesos reales

Después de compilar, se ejecutó el script entregado en
[`scripts/verificar_esqueleto.py`](../../scripts/verificar_esqueleto.py), con la
raíz de la copia y el ejecutable JDK 25 indicados mediante `--raiz` y `--java`.
El script eligió dos puertos locales disponibles y conservó la misma instancia
de Reservas durante la caída y recuperación de Laboratorios.

| Comprobación | Esperado | Observado |
|---|---|---|
| Consulta directa a Laboratorios | 200, servicio `laboratorios` | Correcto |
| Reservas consulta Laboratorios e incluye el mensaje | 200, JSON anidado | Correcto |
| Laboratorios detenido, Reservas sigue vivo | 503 | Correcto |
| Reinicio de Laboratorios, sin reiniciar Reservas | 200, mensaje recuperado | Correcto |

Al terminar se detuvieron únicamente los procesos iniciados por el script.
Los puertos efímeros evitan depender de 8081/8082, aunque una carrera externa
por esos puertos todavía puede hacer fallar el arranque y requiere repetir.

## Límites

Esta ejecución acredita el intercambio mínimo HTTP y su recuperación local,
no una medición comparativa de PE-U1 ni del rendimiento de REST frente a gRPC
o mensajería. No prueba Windows, Docker, HTTPS, autenticación, bases de datos,
concurrencia de reservas, fallos de red distribuidos ni el protocolo I13.

No es una fotografía de la ejecución personal de Roger ni demuestra su
participación en el video. Su verificación personal y defensa se documentarán
cuando las realice. No se generaron capturas ni reuniones artificiales.
