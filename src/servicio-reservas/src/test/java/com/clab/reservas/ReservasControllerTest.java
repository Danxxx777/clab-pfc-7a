package com.clab.reservas;

import java.io.IOException;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.client.RestClient;

import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withException;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withNoContent;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class ReservasControllerTest {

    private MockRestServiceServer servidorLaboratorios;
    private MockMvc clienteReservas;

    @BeforeEach
    void prepararCliente() {
        RestClient.Builder builder = RestClient.builder().baseUrl("http://laboratorios.test");
        servidorLaboratorios = MockRestServiceServer.bindTo(builder).build();
        clienteReservas = MockMvcBuilders
                .standaloneSetup(new ReservasController(builder.build()))
                .build();
    }

    @Test
    void consultaLaboratoriosYDevuelveSuRespuesta() throws Exception {
        servidorLaboratorios.expect(requestTo("http://laboratorios.test/api/laboratorios/info"))
                .andRespond(withSuccess(
                        """
                        {"servicio":"laboratorios","mensaje":"Respuesta de prueba"}
                        """,
                        MediaType.APPLICATION_JSON));

        clienteReservas.perform(get("/api/reservas/comunicacion"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.servicio").value("reservas"))
                .andExpect(jsonPath("$.laboratorios.servicio").value("laboratorios"))
                .andExpect(jsonPath("$.laboratorios.mensaje").value("Respuesta de prueba"));
        servidorLaboratorios.verify();
    }

    @Test
    void devuelve503CuandoFallaLaConexion() throws Exception {
        servidorLaboratorios.expect(requestTo("http://laboratorios.test/api/laboratorios/info"))
                .andRespond(withException(new IOException("Conexión rechazada de prueba")));

        clienteReservas.perform(get("/api/reservas/comunicacion"))
                .andExpect(status().isServiceUnavailable());
        servidorLaboratorios.verify();
    }

    @Test
    void devuelve503CuandoLaboratoriosRespondeSinContenido() throws Exception {
        servidorLaboratorios.expect(requestTo("http://laboratorios.test/api/laboratorios/info"))
                .andRespond(withNoContent());

        clienteReservas.perform(get("/api/reservas/comunicacion"))
                .andExpect(status().isServiceUnavailable());
        servidorLaboratorios.verify();
    }
}
