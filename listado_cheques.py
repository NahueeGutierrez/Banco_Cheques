import csv
import sys
from datetime import datetime

def cargar_datos(archivo):
    with open(archivo, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)


from datetime import datetime

def filtrar_cheques(cheques, cliente=None, estado=None, fecha_inicio=None, fecha_fin=None):
    resultados = []
    for cheque in cheques:
        
        if (
            (cliente is None or cheque.get('DNI') == cliente) and
            (estado is None or cheque.get('Estado') == estado) and
            (fecha_inicio is None or datetime.fromtimestamp(int(cheque.get('FechaPago'))) >= fecha_inicio) and
            (fecha_fin is None or datetime.fromtimestamp(int(cheque.get('FechaPago'))) <= fecha_fin)
        ):
            resultados.append(cheque)
    return resultados

def exportar_a_csv(cheques, archivo):
    with open(archivo, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=cheques[0].keys())
        writer.writeheader()
        writer.writerows(cheques)

if __name__ == '__main__':
    if len(sys.argv) < 6 :
        print("Para utilizar por favor complete los siguientes campos: python listado_cheques.py <archivo_csv> <DNI> <SALIDA> <TIPO_CHEQUE> [--estado <ESTADO>] [--fecha <FECHA_INICIO>, <FECHA_FIN>]")
        sys.exit(1)
  #FILTROS                     "EJEMPLO DE DNI" NO VA DENTRO DEL CODIGO , ES SOLO UN EJEMPLO
#PARA VER FECHA: python listado_cheques.py cheques.csv "EJEMPLO DE DNI" 55555555 PANTALLA DEPOSITADO --fecha 2021-09-12 2021-09-20
#PARA VER ESTADO APROBADO: python listado_cheques.py cheques.csv "EJEMPLO DE DNI" 55555555 PANTALLA EMITIDO --estado aprobado          
#PARA VER ESTADO RECHAZADO: python listado_cheques.py cheques.csv "EJEMPLO DE DNI" 55555555 PANTALLA EMITIDO --estado rechazado  

    archivo_csv = sys.argv[1]
    dni_cliente = sys.argv[2]
    tipo_salida = sys.argv[3]
    tipo_cheque = sys.argv[4]

    estado = None
    fecha_inicio = None
    fecha_fin = None

    i = 5
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--estado":
            i += 1
            estado = sys.argv[i]
        elif arg == "--fecha":
            i += 1
            fecha_inicio = datetime.fromisoformat(sys.argv[i])
            i += 1
            fecha_fin = datetime.fromisoformat(sys.argv[i])
        i += 1

    cheques = cargar_datos(archivo_csv)
    cheques_filtrados = filtrar_cheques(cheques, cliente=dni_cliente, estado=estado, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
#tipo_cheque=tipo_cheque
    if tipo_salida == "PANTALLA":
        for cheque in cheques_filtrados:
            print(f"NroCheque: {cheque['NroCheque']}, CodigoBanco: {cheque['CodigoBanco']}, CodigoScurusal: {cheque['CodigoScurusal']}, NumeroCuentaOrigen: {cheque['NumeroCuentaOrigen']}, NumeroCuentaDestino: {cheque['NumeroCuentaDestino']}, Valor: {cheque['Valor']}, FechaOrigen: {datetime.fromtimestamp(int(cheque['FechaOrigen']))}, FechaPago: {datetime.fromtimestamp(int(cheque['FechaPago']))}, DNI: {cheque['DNI']}, Estado: {cheque['Estado']}")
    elif tipo_salida == "CSV":
        timestamp_actual = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_csv = f"{dni_cliente}_{timestamp_actual}.csv"
        exportar_a_csv(cheques_filtrados, nombre_archivo_csv)
        print(f"Resultados exportados a '{nombre_archivo_csv}'")
    else:
        print("Tipo de salida no válido. Use 'PANTALLA' o 'CSV'.")
