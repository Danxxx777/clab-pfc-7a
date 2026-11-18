# CLAB | Sistema distribuido de gestión de laboratorios

CLAB permite gestionar las reservas y los horarios de uso de laboratorios. El Proyecto Fin de Curso (PFC) adapta el sistema desarrollado en quinto nivel para incorporar arquitectura distribuida, persistencia distribuida y prácticas de calidad de software.

**Aplicaciones Distribuidas · 7.º nivel, paralelo A · Universidad Técnica Estatal de Quevedo**

Ingeniería de Software · Período académico 2026-2027 SPA

## Entregas del PFC

- [ ] **Entrega 1 - Propuesta y análisis.** Documentar el problema, el alcance, los requisitos y los componentes que se distribuirán a partir del sistema base.
- [ ] **Entrega 2 - Arquitectura y API.** Diseñar los microservicios, documentar la API REST con OpenAPI y preparar el despliegue con Docker Compose, autenticación JWT y un API Gateway con Nginx.
- [ ] **Entrega 3 - Datos y procesamiento distribuido.** Integrar una base de datos distribuida, documentar la estrategia de fragmentación y replicación e incorporar el componente de procesamiento.
- [ ] **Entrega final - Calidad y despliegue.** Documentar el despliegue, ejecutar pruebas automatizadas unitarias, de integración y de carga, configurar CI/CD con GitHub Actions y reunir evidencia de observabilidad y de evaluación según ISO/IEC 25010:2023.

## Código base

El historial de CLAB parte del trabajo del equipo de quinto nivel. El código base tiene un [backend](backend/Clab-backend) y un [frontend](frontend). [Repositorio original del equipo](https://github.com/Danxxx777/Clab--Sistema).

## Colaboración

Usa una rama por tarea y abre un pull request hacia `main`. En cada pull request, indica la entrega a la que aporta el cambio y cómo se verificó.
