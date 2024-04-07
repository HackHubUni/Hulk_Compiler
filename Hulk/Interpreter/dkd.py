from collections import OrderedDict

# Crear una lista con duplicados
lista = ['b', 'a', 'c', 'a', 'b', 'd']

# Usar OrderedDict para eliminar duplicados y mantener el orden
lista = list(OrderedDict.fromkeys(lista))

# Imprimir la lista
print(lista)  # Output: ['b', 'a', 'c', 'd']