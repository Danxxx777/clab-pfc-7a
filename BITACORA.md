# Bitácora de CLAB

## 2026-11-18 - Organización del código base y esqueleto de E1

- Participación registrada en esta sesión de chat de Codex. Byron Daniel Loor Mendoza solicitó preparar el esqueleto y guardar el código heredado en una carpeta para organizar la apertura del repositorio en el editor.
- Asistencia de OpenAI Codex. El asistente clonó la rama `main` de `clab-pfc-7a`, trasladó el código heredado a `legado/`, preparó el proyecto Maven con los servicios Laboratorios y Reservas, escribió las pruebas automatizadas y redactó las instrucciones de ejecución.
- Decisiones técnicas aplicadas. Se reutilizaron Java 17, Spring Boot 3.2.1 y el Maven Wrapper del backend original. Reservas consulta a Laboratorios mediante REST y JSON. El proyecto Maven de la raíz declara los dos servicios nuevos. La configuración de VS Code excluye `legado/` de la importación automática de proyectos Java.
- Problema abordado. La raíz contenía los proyectos de quinto semestre y sus archivos de configuración del editor. El traslado a `legado/` permite conservarlos como referencia y compilar el esqueleto desde el `pom.xml` de la raíz.
- Verificación técnica realizada por el asistente. Se compararon las huellas SHA-256 de los 466 archivos originales antes y después del traslado. La compilación con `mvnw.cmd verify` terminó correctamente y pasaron las tres pruebas de Reservas, que usan respuestas simuladas de Laboratorios para comprobar éxito, conexión fallida y respuesta vacía.
- Alcance de esta sesión. Se prepararon el código y sus instrucciones. Las capturas de los procesos comunicándose y el video corresponden a la ejecución posterior del equipo.
