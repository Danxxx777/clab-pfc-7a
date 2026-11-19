package com.clab.laboratorios;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LaboratoriosController {

    @GetMapping("/api/laboratorios/info")
    public InformacionServicio obtenerInformacion() {
        return new InformacionServicio("laboratorios", "Servicio de laboratorios de CLAB disponible");
    }

    public record InformacionServicio(String servicio, String mensaje) {
    }
}
