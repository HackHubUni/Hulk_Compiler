from collections import OrderedDict

# Crear una lista con duplicados
lista = ['b', 'a', 'c', 'a', 'b', 'd']

# Usar OrderedDict para eliminar duplicados y mantener el orden
lista = list(OrderedDict.fromkeys(lista))

# Imprimir la lista
print(lista)  # Output: ['b', 'a', 'c', 'd']



import enum

# Definir los tags como una lista de strings
tags = ['TAG1', 'TAG2', 'TAG3']

# Crear el enum dinámicamente
DynamicEnum = enum.Enum('DynamicEnum', tags)

# Obtener un tag dinámicamente
tag_name = 'TAG1'
tag = getattr(DynamicEnum, tag_name)
taf= getattr(DynamicEnum, 'TAG1')


print(tag==taf)



print(type(tag))
print(tag)  # Output: DynamicEnum.TAG1


a=4
print(-a)