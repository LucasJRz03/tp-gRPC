import grpc
from concurrent import futures
import conversor_pb2
import conversor_pb2_grpc

class ConversorServicer(conversor_pb2_grpc.ConversorServicer):
    def CelsiusAFahrenheit(self, request, context):
        # Conversión: F = C * 1.8 + 32
        fahrenheit = request.celsius * 1.8 + 32
        return conversor_pb2.RespuestaTemperatura(fahrenheit=fahrenheit)

def serve():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    conversor_pb2_grpc.add_ConversorServicer_to_server(ConversorServicer(), servidor)
    servidor.add_insecure_port('127.0.0.1:50051')
    servidor.start()
    
    print("Servidor de conversión ejecutándose en el puerto 50051...")
    servidor.wait_for_termination()

if __name__ == '__main__':
    serve()