import re

def traducir_booleans(expresion):
    expr = expresion.lower()
    expr = re.sub(r'\bverdadero\b', 'True', expr)
    expr = re.sub(r'\bfalso\b', 'False', expr)
    return expr

def calcular_expresion(expresion, variables, modo_condicional=False):
    expresion = expresion.strip()
    expresion = traducir_booleans(expresion)
    try:
        return eval(expresion, {}, variables)
    except ZeroDivisionError:
        if modo_condicional:
            raise
        return "A ver la recalcada concha de tu madre, ¿Cómo que querés dividir por cero?"
    except NameError as e:
        if modo_condicional:
            raise
        return f"Idiota, no ves que: {str(e)}"
    except Exception as e:
        if modo_condicional:
            raise
        return f"No se que es esto, te toca adivinar: {str(e)}"


def parsear_variable(linea, variables):
    partes = linea.split("=", 1)
    nombre = partes[0].replace("variable", "").strip()
    valor = partes[1].strip() if len(partes) > 1 else None

    if valor and valor.startswith('"') and valor.endswith('"'):
        valor = valor[1:-1]
    elif valor:
        # Aquí interpretamos los booleanos en español:
        if valor.lower() == "verdadero":
            valor = True
        elif valor.lower() == "falso":
            valor = False
        else:
            valor = calcular_expresion(valor, variables)

    return nombre, valor

def parse(codigo):
    lineas = codigo.splitlines()
    variables = {}
    instrucciones = []

    ignorar_bloque = False
    nivel_bloque = 0
    si_se_ejecuto = None

    for i, linea in enumerate(lineas):
        linea = linea.strip()

        if ignorar_bloque:
            if "{" in linea:
                nivel_bloque += 1
            if "}" in linea:
                nivel_bloque -= 1
                if nivel_bloque == 0:
                    ignorar_bloque = False
            continue

        if linea.startswith("si"):
            condicion = linea[2:].strip().rstrip("{").strip()
            try:
                resultado = calcular_expresion(condicion, variables, modo_condicional=True)
                si_se_ejecuto = bool(resultado)
            except:
                si_se_ejecuto = False

            if not si_se_ejecuto:
                ignorar_bloque = True
                nivel_bloque = 1
            continue

        if linea.startswith("sino"):
            if si_se_ejecuto is True:
                ignorar_bloque = True
                nivel_bloque = 1
            else:
                ignorar_bloque = False
            si_se_ejecuto = None
            continue

        if linea.startswith("mostrar"):
            parte = linea.split("mostrar", 1)[1].strip()
            if parte.startswith('"') and parte.endswith('"'):
                texto = parte[1:-1]
                instrucciones.append(("mostrar", texto))
            else:
                match = re.match(r'^(\w+)\[(\d+)\]$', parte)
                if match:
                    nombre_var = match.group(1)
                    indice = int(match.group(2))
                    if nombre_var in variables:
                        valor_var = variables[nombre_var]
                        try:
                            valor = valor_var[indice]
                            # Conversión a español si es booleano
                            if isinstance(valor, bool):
                                valor = "verdadero" if valor else "falso"
                            instrucciones.append(("mostrar", valor))
                        except Exception as e:
                            instrucciones.append(("mostrar", f"Error: {str(e)}"))
                    else:
                        instrucciones.append(("mostrar", f"Error: variable '{nombre_var}' no encontrada"))
                else:
                    resultado = calcular_expresion(parte, variables)
                    # Conversión a español si es booleano
                    if isinstance(resultado, bool):
                        resultado = "verdadero" if resultado else "falso"
                    instrucciones.append(("mostrar", resultado))

        elif linea.startswith("repetir"):
            cantidad = int(linea.split()[1])
            instrucciones.append(("repetir", cantidad))

        elif linea.startswith("variable"):
            variable, contenido = parsear_variable(linea, variables)
            variables[variable] = contenido

    return instrucciones