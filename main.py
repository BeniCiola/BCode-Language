import sys
import parser
import interpreter

def main():
    if len(sys.argv) < 2:
        print("Uso: main.py archivo.bcode")
        return

    archivo = sys.argv[1]
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo: {archivo}")
        return

    instrucciones = parser.parse(codigo)
    interpreter.run(instrucciones)

if __name__ == "__main__":
    main()
