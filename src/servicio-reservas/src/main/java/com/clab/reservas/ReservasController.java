package com.clab.reservas;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;
import org.springframework.web.server.ResponseStatusException;

@RestController
public class ReservasController {

    private final RestClient laboratoriosClient;

    public ReservasController(RestClient laboratoriosClient) {
        this.laboratoriosClient = laboratoriosClient;
    }

    @GetMapping("/api/reservas/comunicacion")
    public ComunicacionRespuesta comprobarComunicacion() {
        try {
            InformacionLaboratorios respuesta = laboratoriosClient.get()
                    .uri("/api/laboratorios/info")
                    .retrieve()
                    .body(InformacionLaboratorios.class);

            if (respuesta == null) {
                throw new ResponseStatusException(
                        HttpStatus.SERVICE_UNAVAILABLE,
                        "El servicio de laboratorios devolvió una respuesta vacía");
            }

            return new ComunicacionRespuesta("reservas", respuesta);
        } catch (RestClientException error) {
            throw new ResponseStatusException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo consultar el servicio de laboratorios",
                    error);
        }
    }

    public record InformacionLaboratorios(String servicio, String mensaje) {
    }

    public record ComunicacionRespuesta(String servicio, InformacionLaboratorios laboratorios) {
    }
}
