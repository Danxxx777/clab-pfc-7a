"""Prueba HTTP entre dos JAR reales; Python 3, sin paquetes externos.

No compila ni modifica el código. Solo detiene los procesos que ella inicia.
Los logs se conservan en un directorio temporal para diagnóstico.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import socket
import subprocess
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import build_opener, ProxyHandler


def puerto_libre():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def detener(proceso):
    if proceso is not None and proceso.poll() is None:
        proceso.terminate()
        try:
            proceso.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proceso.kill()
            proceso.wait(timeout=10)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raiz', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--java', default='java')
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    raiz = args.raiz.resolve()
    java = shutil.which(args.java)
    if java is None:
        parser.error('No se encuentra Java; usar --java con el ejecutable del JDK 25.')
    jars = {
        nombre: raiz / f'src/servicio-{nombre}/target/servicio-{nombre}-0.0.1-SNAPSHOT.jar'
        for nombre in ('laboratorios', 'reservas')
    }
    for jar in jars.values():
        if not jar.is_file():
            parser.error(f'Falta {jar}; ejecutar primero el Maven Wrapper con clean verify.')
    if args.salida.exists():
        parser.error('La salida ya existe; elegir un archivo nuevo para conservar resultados previos.')

    directorio_logs = Path(tempfile.mkdtemp(prefix='clab-http-'))
    puertos = {nombre: puerto_libre() for nombre in jars}
    while len(set(puertos.values())) != 2:
        puertos['reservas'] = puerto_libre()
    entorno = os.environ.copy()
    entorno.update({
        'SERVER_ADDRESS': '127.0.0.1',
        'LABORATORIOS_PORT': str(puertos['laboratorios']),
        'RESERVAS_PORT': str(puertos['reservas']),
        'LABORATORIOS_URL': f"http://127.0.0.1:{puertos['laboratorios']}",
    })
    # Sin proxy del usuario para estas peticiones estrictamente locales.
    http = build_opener(ProxyHandler({}))
    procesos, logs = {}, []
    resultado = {
        'inicio_utc': datetime.now(timezone.utc).isoformat(),
        'entorno': platform.system(),
        'java': subprocess.run([java, '-version'], capture_output=True, text=True, check=True).stderr.strip(),
        'alcance': 'Dos JAR reales, HTTP local; no prueba negocio, bases ni autorizacion.',
        'jars_sha256': {nombre: hashlib.sha256(jar.read_bytes()).hexdigest() for nombre, jar in jars.items()},
        'casos': [],
        'correcto': False,
    }

    def iniciar(nombre):
        log = (directorio_logs / f'{nombre}-{len(logs)}.log').open('wb')
        logs.append(log)
        procesos[nombre] = subprocess.Popen(
            [java, '-jar', str(jars[nombre]),
             '--server.address=127.0.0.1', f'--server.port={puertos[nombre]}',
             f"--clab.laboratorios.url={entorno['LABORATORIOS_URL']}"],
            cwd=raiz, env=entorno, stdout=log, stderr=subprocess.STDOUT,
        )

    def pedir(nombre, ruta):
        try:
            with http.open(f'http://127.0.0.1:{puertos[nombre]}{ruta}', timeout=8) as respuesta:
                return respuesta.status, respuesta.read().decode('utf-8')
        except HTTPError as error:
            return error.code, error.read().decode('utf-8')

    def esperar(nombre, ruta):
        limite = time.monotonic() + 60
        while time.monotonic() < limite:
            if procesos[nombre].poll() is not None:
                raise RuntimeError(f'{nombre} termino antes de estar disponible; revisar logs.')
            try:
                status, _ = pedir(nombre, ruta)
                if status == 200:
                    return
            except (URLError, TimeoutError, ConnectionError):
                pass
            time.sleep(0.25)
        raise TimeoutError(f'{nombre} no quedo listo en 60 segundos.')

    def registrar(nombre, servicio, ruta, esperado, validar=None):
        status, cuerpo = pedir(servicio, ruta)
        caso = {'nombre': nombre, 'estado_esperado': esperado, 'estado_observado': status}
        resultado['casos'].append(caso)
        caso['correcto'] = status == esperado
        if caso['correcto'] and validar is not None:
            caso['correcto'] = validar(json.loads(cuerpo))
        if not caso['correcto']:
            raise AssertionError(f'{nombre}: respuesta distinta de la esperada.')

    ruta = '/api/reservas/comunicacion'
    try:
        iniciar('laboratorios')
        esperar('laboratorios', '/api/laboratorios/info')
        registrar('consulta_directa', 'laboratorios', '/api/laboratorios/info', 200,
                  lambda body: body.get('servicio') == 'laboratorios')
        iniciar('reservas')
        esperar('reservas', ruta)

        def respuesta_valida(body):
            return (body.get('servicio') == 'reservas'
                    and body.get('laboratorios', {}).get('servicio') == 'laboratorios'
                    and body.get('laboratorios', {}).get('mensaje')
                    == 'Servicio de laboratorios de CLAB disponible')

        registrar('comunicacion_entre_procesos', 'reservas', ruta, 200, respuesta_valida)
        detener(procesos['laboratorios'])
        registrar('dependencia_detenida', 'reservas', ruta, 503)
        iniciar('laboratorios')
        esperar('laboratorios', '/api/laboratorios/info')
        registrar('recuperacion_sin_reiniciar_reservas', 'reservas', ruta, 200, respuesta_valida)
        resultado['correcto'] = True
    except Exception as error:
        resultado['error'] = f'{type(error).__name__}: {error}'
    finally:
        for proceso in procesos.values():
            detener(proceso)
        for log in logs:
            log.close()
        resultado['fin_utc'] = datetime.now(timezone.utc).isoformat()
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        print(f'Logs locales: {directorio_logs}')
    return 0 if resultado['correcto'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
