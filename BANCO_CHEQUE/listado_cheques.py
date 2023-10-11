import csv
from datetime import datetime
#comento por aca porque no me acuerdo como comentar en un archivo.csv; en el archivo cheques.csv esta toda la data que importa
#este .py, todo lo que nosotros le deciamos que era como un bloc de notas
def cargar_datos(archivo):
    with open(archivo, 'r') as file:#esto es importante que lo aprendan en lo basico que hay en todos
        reader = csv.DictReader(file)
        return list(reader)#se abre como reader por eso el 'r' antes, la variable creada es reader y trae todo com archivo de lectura

def filtrar_cheques(cheques, cliente=None, estado=None, fecha_inicio=None, fecha_fin=None):
    resultados = []#en esta variable se guarda todo
    for cheque in cheques:
        if cliente and cheque['DNI'] != cliente:
            continue
        if estado and cheque['Estado'] != estado:
            continue
        if fecha_inicio and datetime.fromtimestamp(int(cheque['FechaPago'])) < fecha_inicio:
            continue
        if fecha_fin and datetime.fromtimestamp(int(cheque['FechaPago'])) > fecha_fin:
            continue
        resultados.append(cheque)
    return resultados#un bucle sencillo con varios if, no hay mucho que explicar, al final se hace un append que guarda todo en 'resultados'

def exportar_a_csv(cheques, archivo):
    with open(archivo, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=cheques[0].keys())
        writer.writeheader()
        writer.writerows(cheques)#y creo que en esto me esta fallando un poco el codigo, esto es en lo que me ayudo o me perjudico el chat
                                 #es para localizar exactamente lo que buscas con una key y se me hizo un quilombo, esto puede ser quesea la falla
if __name__ == '__main__':#esto importa y exporta todo, como lo que veiamos en el sprint pasado, yo lo tenia armado diferente pero el chat me lo puso con ese
                          #__name__ asique tambien puede ser que sea una falla 
    cheques = cargar_datos('cheques.csv')
    cheques_filtrados = filtrar_cheques(cheques, cliente='12345', estado='aprobado', fecha_inicio=datetime(2023, 1, 1), fecha_fin=datetime(2023, 12, 31))
    exportar_a_csv(cheques_filtrados, 'cheques_filtrados.csv')

#yo recomiendo que lo vean lo entiendan, no es muy complicado y tratemos de coordinar para juntarnos, lo resolvemos facil
#no hay css no hay nada es solo codigo q sale x terminal