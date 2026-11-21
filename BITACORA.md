# Bitácora de CLAB

## 2026-11-19 - Actualización del runtime a Java 25

- Se actualizó la configuración Maven activa y el backend heredado a Java 25.
- Spring Boot se llevó de 3.2.1 a la versión compatible 3.5.16 en ambos módulos Maven.
- Se mantuvieron las pruebas existentes y el comportamiento de los servicios sin cambios en el código de aplicación.

## 2026-11-18 - Organización del código base y esqueleto de E1

- Participación registrada en esta sesión de chat de Codex. Byron Daniel Loor Mendoza solicitó preparar el esqueleto y guardar el código heredado en una carpeta para organizar la apertura del repositorio en el editor.
- Asistencia de OpenAI Codex. El asistente clonó la rama `main` de `clab-pfc-7a`, trasladó el código heredado a `legado/`, preparó el proyecto Maven con los servicios Laboratorios y Reservas, escribió las pruebas automatizadas y redactó las instrucciones de ejecución.
- Decisiones técnicas aplicadas. Se reutilizaron Java 17, Spring Boot 3.2.1 y el Maven Wrapper del backend original. Reservas consulta a Laboratorios mediante REST y JSON. El proyecto Maven de la raíz declara los dos servicios nuevos. La configuración de VS Code excluye `legado/` de la importación automática de proyectos Java.
- Problema abordado. La raíz contenía los proyectos de quinto semestre y sus archivos de configuración del editor. El traslado a `legado/` permite conservarlos como referencia y compilar el esqueleto desde el `pom.xml` de la raíz.
- Verificación técnica realizada por el asistente. Se compararon las huellas SHA-256 de los 466 archivos originales antes y después del traslado. La compilación con `mvnw.cmd verify` terminó correctamente y pasaron las tres pruebas de Reservas, que usan respuestas simuladas de Laboratorios para comprobar éxito, conexión fallida y respuesta vacía.
- Alcance de esta sesión. Se prepararon el código y sus instrucciones. Las capturas de los procesos comunicándose y el video corresponden a la ejecución posterior del equipo.

## Carlos Manotoa: 2026-11-18 - Búsqueda bibliográfica para los trabajos relacionados de E1

Se revisó de forma preliminar los artículos encontrados para el punto 5 de la guía. El tiempo estimado de la actividad fue de 1 hora.

Se reunieron cinco artículos de revistas indexadas en Scopus, publicados entre 2022 y 2025 y disponibles en texto completo de acceso abierto. Para la comparación con CLAB se seleccionaron los estudios de Gil Vera et al. sobre reservas de laboratorios, García-Granja et al. sobre disponibilidad de espacios universitarios y Müller, Rudová y Müllerová sobre restricciones de horario. Los trabajos de Rihm et al. y Oakley et al. quedaron como fuentes complementarias sobre inventario e implantación.

OpenAI Codex asistió con la búsqueda, el filtro de fuentes, y la preparación de la estructura nuevos archivos (.bib).

Queda pendiente redactar la comparación de los tres estudios y completar el mínimo de ocho referencias de la entrega.

## Carlos Manotoa: 2026-11-19 - Primera redacción de los trabajos relacionados de E1

Responsable de Calidad: Carlos Manotoa. Tiempo estimado de la actividad: 4 horas.

Se incorporó a [Carlos.tex](docs/Carlos.tex) un primer borrador del punto 5, sujeto a revisión y cambios. Se compararon STEM RRL, Biblio-Smart, el modelo de ITC 2019 y la propuesta de CLAB en nueve características, desde la consulta de disponibilidad y las reglas de reserva hasta la arquitectura y la evaluación.

El borrador identifica qué ideas puede aprovechar CLAB y distingue las funciones propuestas de la comunicación entre servicios que ya demuestra el esqueleto. Se comprobó la compilación del documento y la resolución de las citas.

## Carlos Manotoa — 2026-11-20 — Borrador de requisitos no funcionales de E1

Se incorporaron siete requisitos no funcionales en [Carlos.tex](docs/Carlos.tex) y se integraron en la sección de requisitos de [main.tex](docs/main.tex). Cada requisito indica la característica de ISO/IEC 25010:2023, la meta cuantitativa y cómo se comprobará. Las metas tomadas del informe anterior se identificaron por separado de los parámetros de prueba que siguen pendientes de validar con el levantamiento.

Se revisó manualmente las referencias. OpenAI Codex apoyó el filtrado y el cotejo bibliográfico. Se añadieron ocho artículos a [referencias.bib](docs/referencias.bib).

## 2026-11-20 - Análisis de riesgos técnicos de E1

Se incorporó el análisis de riesgos en [Carlos.tex](docs/Carlos.tex). Se documentaron cinco riesgos técnicos, tres derivados del caso de Amazon S3 analizado en FORM-AC-01 y dos de la arquitectura propuesta para CLAB. Para cada riesgo se definieron la probabilidad, el impacto, la medida de mitigación y una prueba propuesta. Se verificó la compilación del documento.

## 2026-11-20 - Propuesta inicial de requisitos funcionales

Se incorporaron en la sección de requisitos de `docs/main.tex` cuatro propuestas: consulta de disponibilidad (RF-P01), solicitud de reserva (RF-P02), cancelación de reserva propia (RF-P03) y actualización del catálogo de laboratorios (RF-P04). Cada propuesta identifica el actor, la operación y un criterio de aceptación.

Las propuestas se basan en los actores y flujos descritos en el contexto C4 y en la documentación actual de CLAB. Su aceptación por el equipo, las reglas de negocio y la ejecución de los criterios siguen pendientes.

Byron Daniel Loor Mendoza solicitó incorporar requisitos provisionales para revisarlos al final. OpenAI Codex (GPT-6) redactó las propuestas y esta entrada e integró el cambio en LaTeX. Esta intervención corresponde a asistencia de IA en documentación preliminar.

Se regeneró `docs/main.pdf` y se revisaron la compilación, la resolución de citas y la presentación de los requisitos.
