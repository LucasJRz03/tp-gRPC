import grpc
import conversor_pb2
import conversor_pb2_grpc

IP_SERVIDOR = "127.0.0.1"
PUERTO = 50051

def run():

    destino = f"{IP_SERVIDOR}:{PUERTO}"

    with grpc.insecure_channel(destino) as canal:
        stub = conversor_pb2_grpc.ConversorStub(canal)
        try:
            celsius_input = float(input("Ingrese la temperatura en grados Celsius: "))
            solicitud = conversor_pb2.SolicitudTemperatura(celsius=celsius_input)
            respuesta = stub.CelsiusAFahrenheit(solicitud)
            print(f"Temperatura en Fahrenheit: {respuesta.fahrenheit:.2f} F°")
        except ValueError:
            print("Por favor, ingrese un número válido.")

if __name__ == '__main__':
    run()