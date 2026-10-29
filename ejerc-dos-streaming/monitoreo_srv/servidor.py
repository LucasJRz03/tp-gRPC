import grpc
import time
import psutil
from concurrent import futures
import monitoreo_pb2
import monitoreo_pb2_grpc

class MonitorServidorServicer(monitoreo_pb2_grpc.MonitorServidorServicer):
    def ConsultarEstado(self, request, context):
        for _ in range(5):
            # Obtener métricas reales de la máquina donde corre el servidor
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().available / (1024 * 1024) # Convertir a MB
            disco = psutil.disk_usage('/').free / (1024 * 1024 * 1024) # Convertir a GB
            
            yield monitoreo_pb2.ReporteEstado(
                cpu_uso_porcentaje=cpu,
                ram_disponible_mb=ram,
                disco_disponible_gb=disco
            )
            time.sleep(2) # Pausa de 2 segundos entre envíos

def serve():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    monitoreo_pb2_grpc.add_MonitorServidorServicer_to_server(MonitorServidorServicer(), servidor)
    servidor.add_insecure_port('127.0.0.1:50052')
    print("Servidor de monitoreo ejecutándose en el puerto 50052...")
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    serve()       