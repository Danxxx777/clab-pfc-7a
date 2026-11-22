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

## 2026-11-21 - Conservación del antecedente de CLAB

Byron Daniel Loor Mendoza proporcionó el informe original de CLAB de 54 páginas. OpenAI Codex (familia de modelos GPT-6) conservó una copia íntegra en `evidencias/antecedentes/CLAB-informe-original-2026.pdf` y comprobó que su SHA-256 coincide con el archivo recibido.

El documento contiene dieciséis requisitos en las páginas 14 y 15, diagnóstico en las páginas 19 y 20, un cuestionario en las páginas 45 y 46 y una fotografía de entrevista en la página 47. Se registró su referencia bibliográfica y su ubicación en el README. El acta con nombre, cargo, fecha y firma o el audio con consentimiento siguen pendientes de incorporación para completar la evidencia primaria exigida en E1.

## 2026-11-21 - Avance documental del bloque de Documentación

En la misma sesión de trabajo, Byron solicitó avanzar en su bloque de E1 a partir del informe original. Codex adaptó el resumen ejecutivo de 341 palabras y el contexto, documentó los interesados, propuso cinco objetivos específicos con indicadores y convirtió los dieciséis requisitos originales en historias de usuario con criterios de aceptación.

Estos textos reemplazan los cuatro requisitos preliminares y conservan la trazabilidad a los RF del informe original. La asistencia de IA se declaró en el documento. Se regeneró el PDF y se revisaron la compilación, la resolución de citas y la presentación. La validación con el registro primario del levantamiento y los datos completos de la portada continúan pendientes.

## 2026-11-21 - Integración de aportes disponibles de E1

Como parte de la misma sesión, Byron solicitó contrastar los aportes de Carlos Manotoa con el repositorio. Codex comprobó los seis commits comunicados por Carlos y la presencia de la comparación de tres estudios, siete requisitos no funcionales, cinco riesgos, tres capturas y su declaración de IA. Las capturas muestran la secuencia HTTP 200, HTTP 503 al detener Laboratorios y HTTP 200 después del reinicio, junto con usuario, equipo y fecha del sistema.

Se conectaron al documento principal los archivos existentes de justificación, C4 y CAP/PACELC, sus figuras y su bibliografía. Se incorporaron la tabla de aportes enlazada a commits, la declaración de asistencia de esta integración y las capturas de Carlos identificadas como tales. Se documentaron en el README la compilación con pdfLaTeX y Biber y las dependencias requeridas.

El problema de integración era que esos archivos de arquitectura estaban versionados, pero `docs/main.tex` no los incluía. Se regeneró `docs/main.pdf`, se comprobaron las citas y los enlaces de la tabla y se revisó la presentación de las figuras, capturas y texto. La consulta a GitHub no encontró issues en el repositorio al corte de esta revisión; su vinculación con la tabla sigue pendiente.

## 2026-11-21 - Portada y vinculación del seguimiento de E1

Se completó la portada con los datos de la asignatura, el proyecto, el periodo, la fecha prevista de entrega y la URL del repositorio. Para Roger se utilizó el nombre público de su registro ORCID enlazado desde GitHub; para Juliana, el nombre que figura en su repositorio académico. Los roles de Arquitectura y Liderazgo de Desarrollo se asignaron según los aportes y responsabilidades observados en el repositorio y requieren confirmación del equipo.

Se crearon las issues 1 a 4, asignadas respectivamente a Danxxx777, Esteiben, JulianaEmanuel y CarlosManotoa007. Las issues describen de forma explícita que los commits enlazados preceden a su creación y conservan abiertos los pendientes de cada rol. Sus enlaces se incorporaron a la tabla de aportes y al README.

Se reunieron en la sección de IA las declaraciones existentes y los registros de asistencia de Arquitectura y CAP/PACELC. El registro de CAP/PACELC no contiene la versión concreta del modelo ni una confirmación de revisión personal; esos datos siguen pendientes del responsable.

Byron indicó aplazar momentáneamente el acta o el audio del levantamiento. Se mantuvieron el informe original, su cuestionario y su fotografía como antecedentes identificados. El requisito del respaldo primario conserva su estado pendiente para la entrega final de E1.

## 2026-11-21 - Limpieza del código e historial heredados

Por solicitud de Byron, Codex retiró el código heredado del repositorio del PFC y preparó el historial de `main` desde noviembre de 2026. Se conservaron los 24 commits existentes del equipo actual, incluidos los dos últimos aportes de Roger, con sus autores, fechas y mensajes originales. La reescritura cambió sus identificadores y se actualizaron las referencias documentales. El esqueleto de E1 en `src/` se conservó sin cambios.

Antes de la limpieza se guardaron un respaldo completo del historial y una copia de los cambios locales pendientes, incluido su estado de preparación para commits. La procedencia de CLAB se mantiene mediante el enlace al repositorio original y el informe antecedente. Las entradas anteriores de esta bitácora describen el estado que existía en cada sesión.

## 2026-11-21 - Ajuste de la presentación del informe

Por solicitud de Byron, Codex cambió el cuerpo del documento a la clase IEEEtran de dos columnas y conservó la portada académica. Se ajustaron las listas, la tabla de aportes, las figuras y las capturas para retirar los saltos forzados y aprovechar el ancho disponible, sin modificar sus datos ni los archivos de evidencia. Se actualizaron las dependencias de compilación en el README.

Antes de guardar esta versión se incorporó el commit `6aaa159` de Carlos, que actualiza su declaración de IA. Se recompiló con pdfLaTeX y Biber y se revisó el PDF renderizado. El documento pasó de 31 a 14 páginas; se comprobaron las dieciséis historias, los cinco objetivos específicos, las diecisiete referencias y la ausencia de citas indefinidas y desbordes.

## 2026-11-21 - Corrección del orden de lectura del informe

Byron señaló que la distribución anterior mezclaba elementos de distintas secciones. Codex corrigió la colocación automática de tablas y figuras y dejó el informe en una columna compacta. La consigna exige un único documento LaTeX y referencias IEEE, sin imponer dos columnas. Los diagramas permanecen en Arquitectura; las capturas del esqueleto preceden a la tabla de aportes, las declaraciones de IA y las referencias finales.

Se recompiló con pdfLaTeX y Biber y se revisaron las páginas renderizadas. El PDF resultante tiene 18 páginas, conserva las dieciséis historias, los cinco objetivos específicos y las diecisiete referencias, y no presenta desbordes ni citas indefinidas. Los archivos originales de evidencia, los diagramas editables y los servicios no se modificaron.

## 2026-11-21 - Revisión de portada, asistencia de IA y cobertura de aportes

Por solicitud de Byron, Codex sustituyó la tabla de integrantes de la portada por nombres y responsabilidades en líneas independientes y fijó la fecha de entrega del documento en el 21 de noviembre de 2026. La tabla de aportes se conservó porque forma parte de los entregables de E1.

Se revisaron la corrección de la declaración personal del punto 4 de SGRA y la sección 6.1 del encuadre. La declaración de Byron se pasó a primera persona, conservando el alcance real de la asistencia en organización, textos técnicos, integración, código inicial, pruebas automatizadas y comprobaciones del documento. No se trasladaron a CLAB las ejecuciones personales de la otra actividad ni se atribuyeron a Byron las capturas de Carlos.

Se contrastó la copia de trabajo con main remoto y se comprobó que todos los archivos LaTeX y los cuatro bloques de Carlos están incluidos en el documento principal. Se añadieron a la tabla los enlaces a la ampliación CAP/PACELC y al protocolo de cierre y reapertura de Roger, la última declaración de Carlos y los commits de integración documental. El registro de IA de CAP/PACELC distingue el borrador de Juliana de la ampliación de Roger y mantiene identificados los datos personales que no constan en el borrador.

El PDF se recompiló y se revisó visualmente, conservando 18 páginas, las historias, los objetivos, las referencias y el orden de sus elementos. Esta integración recoge lo disponible en el repositorio; no acredita que ya estén entregados ADR-002, el plan y cronograma con el enlace al tablero de E1/E2, el video ni los respaldos primarios aplazados.
