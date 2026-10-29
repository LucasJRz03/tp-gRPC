import grpc
import monitoreo_pb2
import monitoreo_pb2_grpc

IP_SERVIDOR = "127.0.0.1"
PUERTO = 50052

def run():

    destino = f"{IP_SERVIDOR}:{PUERTO}"

    input("Presione Enter para consultar el estado del servidor...")
    
    with grpc.insecure_channel(destino) as canal:
        stub = monitoreo_pb2_grpc.MonitorServidorStub(canal)
        solicitud = monitoreo_pb2.SolicitudVacia()    
        try:
            respuestas = stub.ConsultarEstado(solicitud)
            contador = 1
            for reporte in respuestas:
                print(f"\nReporte {contador}")
                print(f"CPU en uso: {reporte.cpu_uso_porcentaje:.1f} %")
                print(f"RAM disponible: {reporte.ram_disponible_mb:.0f} MB")
                print(f"Disco disponible: {reporte.disco_disponible_gb:.0f} GB")
                contador += 1
                
            print("\nMonitoreo finalizado.")
        except grpc.RpcError as e:
            print(f"Error gRPC: {e.details()}")

if __name__ == '__main__':
    run()