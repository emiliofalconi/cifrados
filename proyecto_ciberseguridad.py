# Proyecto Cifrado - Demostración de diferentes sistemas de cifrado
# Incluye César (número y texto), repetición y fuerza bruta para César

import time
from getpass import getpass

print("="*70)
print("          PROYECTO CIFRADO")
print("  Cifrado César (número y texto) + Repetición + Fuerza Bruta")
print("="*70)
print()


def cesar_cifrar(texto: str, desplazamiento: int) -> str:
    """Cifrado César clásico - desplazamiento numérico"""
    resultado = []
    desplazamiento = desplazamiento % 26
    
    for c in texto:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            nuevo = (ord(c) - base + desplazamiento) % 26 + base
            resultado.append(chr(nuevo))
        else:
            resultado.append(c)
    return ''.join(resultado)


def texto_a_desplazamiento(clave_texto: str) -> int:
    """Convierte una clave de texto en un número de desplazamiento (0-25)"""
    if not clave_texto:
        return 0
        
    total = 0
    for c in clave_texto.upper():
        if c.isalpha():
            total += ord(c) - ord('A')
    
    return total % 26


def cesar_descifrar(texto: str, desplazamiento: int) -> str:
    return cesar_cifrar(texto, -desplazamiento)


def fuerza_bruta_cesar(texto_cifrado: str, mostrar_todas=False):
    """Intenta todas las claves posibles (0-25) y muestra resultados"""
    print("\n" + "═"*60)
    print("       ATAQUE DE FUERZA BRUTA - CIFRADO CÉSAR")
    print("═"*60)
    print("Probando 26 posibles desplazamientos...\n")
    
    resultados = []
    
    for clave in range(26):
        intento = cesar_descifrar(texto_cifrado, clave)
        resultados.append((clave, intento))
        
        # Mostramos solo algunas para no saturar la pantalla
        if mostrar_todas or clave % 5 == 0 or clave == 25:
            print(f"clave {clave:2d} → {intento}")
    
    print("\n" + "═"*60)
    print("Todas las posibilidades (elige la que tenga sentido):")
    print("═"*60)
    
    for i, (clave, texto) in enumerate(resultados):
        print(f"[{clave:2d}] {texto}")
        if (i + 1) % 5 == 0:
            print("-" * 50)


def repeticion_cifrar(texto: str, clave: str) -> str:
    """Cifrado por repetición (XOR con clave repetida)"""
    resultado = []
    clave_bytes = clave.encode('utf-8')
    texto_bytes = texto.encode('utf-8')
    
    for i in range(len(texto_bytes)):
        c = texto_bytes[i]
        k = clave_bytes[i % len(clave_bytes)]
        resultado.append(c ^ k)
        
    return bytes(resultado).hex()


def repeticion_descifrar(hex_cifrado: str, clave: str) -> str:
    try:
        datos = bytes.fromhex(hex_cifrado)
    except:
        return "[Error: formato hexadecimal inválido]"
        
    clave_bytes = clave.encode('utf-8')
    resultado = []
    
    for i in range(len(datos)):
        c = datos[i]
        k = clave_bytes[i % len(clave_bytes)]
        resultado.append(c ^ k)
        
    try:
        return bytes(resultado).decode('utf-8')
    except:
        return "[No se pudo decodificar como UTF-8]"


# ----------------------------------------------------
#                    MENÚ PRINCIPAL
# ----------------------------------------------------

def main():
    while True:
        print("\nOpciones:")
        print("  1) Cifrar César - clave numérica")
        print("  2) Descifrar César - clave numérica")
        print("  3) Cifrar César - clave de texto")
        print("  4) Descifrar César - clave de texto")
        print("  5) Fuerza bruta César (cualquier mensaje cifrado)")
        print("  6) Cifrar con repetición (clave texto)")
        print("  7) Descifrar con repetición")
        print("  8) Salir")
        
        op = input("\n→ Elige (1-8): ").strip()
        
        if op == "8":
            print("\n¡Hasta luego!\n")
            break
            
        if op not in "1234567":
            print("Opción no válida\n")
            continue
            
        mensaje = input("Mensaje: ")
        if not mensaje.strip():
            print("El mensaje no puede estar vacío\n")
            continue
            
        # César numérico
        if op in ["1", "2"]:
            while True:
                try:
                    clave = int(input("Clave numérica (0-25): "))
                    if 0 <= clave <= 25:
                        break
                    print("La clave debe estar entre 0 y 25\n")
                except:
                    print("Debe ser un número\n")
                    
            if op == "1":
                print(f"\nCifrado César (desplazamiento {clave}):")
                print(cesar_cifrar(mensaje, clave))
            else:
                print(f"\nDescifrado César (desplazamiento {clave}):")
                print(cesar_descifrar(mensaje, clave))
                
        # César con clave de texto
        elif op in ["3", "4"]:
            clave = input("Clave de texto: ")
            if not clave.strip():
                print("La clave no puede estar vacía\n")
                continue
                
            desplazamiento = texto_a_desplazamiento(clave)
            print(f"→ Desplazamiento calculado: {desplazamiento}")
            
            if op == "3":
                print("\nCifrado César con clave de texto:")
                print(cesar_cifrar(mensaje, desplazamiento))
            else:
                print("\nDescifrado César con clave de texto:")
                print(cesar_descifrar(mensaje, desplazamiento))
                
        # Fuerza bruta
        elif op == "5":
            fuerza_bruta_cesar(mensaje, mostrar_todas=False)
            
        # Repetición
        else:
            clave = getpass("Clave de texto (se ocultará): ")
            if not clave:
                print("La clave no puede estar vacía\n")
                continue
                
            if op == "6":
                cifrado = repeticion_cifrar(mensaje, clave)
                print("\nCifrado por repetición (hex):")
                print(cifrado)
                print(f"\nGuarda esta clave: {clave}")
            else:
                print("\nDescifrado por repetición:")
                print(repeticion_descifrar(mensaje, clave))


if __name__ == "__main__":
    main()