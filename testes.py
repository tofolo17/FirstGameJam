lista = [[1, 2, 3], [1, 2, 3]]
lines = 0
cont = 0
for line in lista:
    elements = 0
    for element in line:
        if element == 1:
            cont += 1
            if cont == 2:
                lista[lines][elements] = 2
        elements += 1
    lines += 1

print(lista)
