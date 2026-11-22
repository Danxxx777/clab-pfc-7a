# CLAB — Evidencias de revisión de arquitectura

Este directorio conserva un bosquejo y dos capturas de una videollamada de
revisión. Son evidencias de revisión del diseño propuesto, no de ejecución del
protocolo de negocio ni de aceptación formal de ADR-001.

## Archivos y procedencia

Los archivos fueron proporcionados por Roger y se conservan sin editar,
recortar ni convertir. Solo se cambia el nombre para organizar su destino.

| Archivo | Original recibido | Contenido observable |
|---|---|---|
| [bosquejo_revision.jpeg](bosquejo_revision.jpeg) | `bosquejo.jpeg` | Fotografía de un bosquejo manuscrito: actores, Angular SPA, cuatro dominios y una base propia por dominio. La fecha manuscrita se lee como 20/11/2026, 21:30. |
| [sesion_revision_01.png](sesion_revision_01.png) | `cap01.png` | Pantalla compartida del bosquejo en Pinta, anotaciones rojas sobre Identidad y cuatro cámaras visibles. No muestra una fecha independiente de la sesión; la fecha del papel pertenece al bosquejo. |
| [sesion_revision_02.jpeg](sesion_revision_02.jpeg) | `cap02.jpeg` | Interfaz de Discord, canal `SD-GRUPO-PFC`, pantalla compartida del bosquejo con un recuadro sobre Información y Avisos, y cuatro cámaras visibles. El escritorio muestra 21/11/2026, 21:08. |

La lista de conexión de la segunda captura muestra «Roger Ga…», «Byron Loor»,
«Carlos Manotoa» y «Juliana Emanuel». Estos son los rótulos observables; no se
atribuye cada rostro a un nombre ni se infieren intervenciones individuales.
La plataforma visible es Discord, aunque en la conversación previa se habló de
Meet. No se documentan dos reuniones distintas ni se deduce su duración.

## Fechas, revisión y límites

El autor informó que elaboró el bosquejo el día anterior y corrigió partes con
ayuda del esquema del asistente. No se recibió una versión anterior separada
ni la fecha precisa de cada corrección. La fecha escrita en el papel no demuestra
cuándo se realizaron todas las anotaciones ni fecha por sí sola la videollamada.
La fecha del escritorio se registra como información visible, no como una
verificación independiente del reloj o de la autenticidad temporal del archivo.

Las capturas permiten observar una revisión compartida con anotaciones distintas;
no contienen acta, audio ni detalle suficiente para afirmar qué acuerdos se
adoptaron, quién propuso cada cambio o que el equipo aceptó formalmente ADR-001.

Este material **no se presenta como primer bosquejo histórico anterior a los C4
publicados**. No resuelve automáticamente ese criterio de la guía o de la issue
[#2](https://github.com/Danxxx777/clab-pfc-7a/issues/2); la ausencia de ese original
debe declararse y consultarse con el docente.

## Lectura técnica del boceto

El boceto simplifica las relaciones: SPA → APIs es frontend/backend, no una
interacción entre dos servicios backend. Las palabras «permisos» y «leer cambios»
no detallan todos los emisores, destinatarios ni contratos. Las anotaciones de
pantalla no sustituyen los diagramas C4 ni acreditan una nueva decisión técnica.

La referencia formal está en [ADR-001](../../docs/adr/ADR-001-estilo-arquitectonico.md)
y en los [diagramas C4](../../docs/diagramas/c4.md): Reservas consulta el catálogo
de Laboratorios por I09; Laboratorios coordina la barrera en Reservas por I13.
El manejador de I13 no vuelve a consultar Laboratorios por I09. Las verificaciones
de permisos y la lectura periódica de cambios son parte del diseño objetivo.
El esqueleto de E1 solo demuestra la consulta HTTP Reservas → Laboratorios;
estas imágenes no prueban las otras interacciones, concurrencia ni persistencia.

## Asistencia y privacidad

Se utilizó OpenAI GPT-6.1 Sol como apoyo para el esquema y para organizar y
describir estas evidencias. El asistente no generó ni modificó las imágenes,
no asistió a la llamada ni certifica sus acuerdos o la aceptación del diseño.

Los archivos contienen rostros, nombres e información de la interfaz. El autor
debe confirmar el consentimiento de quienes aparecen antes de subirlos al
repositorio público. La recepción de los archivos no acredita ese consentimiento.
