import pyodbc
def tratarResultado(ob):
    lista = []
    for row in ob:
        lista.append(str(row))
        lista = [col.replace(',', '') for col in lista]
        lista = [col.replace('(', '') for col in lista]
        lista = [col.replace(')', '') for col in lista]
        lista = [col.replace('\'', '') for col in lista]
        lista = [col.replace('\'', '') for col in lista]

    return lista
class Exceptn(Exception):
    def __init__(self,campo):
        self.campo = campo

    def __str__(self):
        print(type(self.campo))
        return repr(self.campo)


def isNumber(valor):
    try:
        int(valor)
    except:
        raise ValueError



