def run(instrucciones):
    i = 0

    while i < len(instrucciones):
        tipo, valor = instrucciones[i]

        if tipo == "mostrar":
            print(valor)

        elif tipo == "repetir":
            for _ in range(valor):
                i += 1
                tipo2, valor2 = instrucciones[i]

                if tipo2 == "mostrar":
                    print(valor2)

        i += 1