import subprocess
import string

def ejecutar_comando(comando):
    """Ejecuta un comando de shell y retorna la salida como texto."""
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    return resultado.stdout.strip()

def obtener_historial():
    """Obtiene la lista de hashes de los commits desde el más antiguo al más reciente."""
    salida = ejecutar_comando('git log --reverse --format="%H"')
    return salida.split('\n') if salida else []

def obtener_contenido_archivo(hash_commit):
    """Obtiene el contenido de nucleo.txt en un commit específico."""
    return ejecutar_comando(f'git show {hash_commit}:nucleo.txt')

def es_commit_merge(hash_commit):
    """Determina si un commit tiene más de un padre (es un merge)."""
    padres = ejecutar_comando(f'git log -1 --format="%P" {hash_commit}')
    return len(padres.split()) > 1

def aplicar_cifrado_cesar(caracter, desplazamiento):
    """Aplica un Cifrado César manteniendo letras."""
    if caracter.isalpha():
        base = ord('A') if caracter.isupper() else ord('a')
        return chr((ord(caracter) - base + desplazamiento) % 26 + base)
    return caracter

def descifrar():
    commits = obtener_historial()
    llave = "" # [cite: 26]

    for hash_commit in commits:
        if not hash_commit:
            continue
            
        # 1. Extracción [cite: 22]
        contenido = obtener_contenido_archivo(hash_commit)
        if not contenido:
            continue

        # 4. Mutación Final (Evaluada al inicio del ciclo sobre el commit actual) [cite: 31]
        if es_commit_merge(hash_commit):
            llave = llave[::-1]
            # La regla dice "antes de continuar con el siguiente commit", 
            # pero el merge en sí mismo también genera un hash que debe evaluarse.
            # Se aplica la inversión y se procesa el commit merge normalmente.

        # 2. Evaluación de Estado [cite: 23]
        primeros_6 = hash_commit[:6]
        valor_decimal = int(primeros_6, 16)
        
        # Conteo de entropía para la lógica de cifrado [cite: 27, 28]
        cant_numeros = sum(1 for c in hash_commit if c.isdigit())
        cant_letras = sum(1 for c in hash_commit if c in 'abcdef')

        # 3. Máquina de Estados (El Cifrado) [cite: 24, 25]
        if valor_decimal % 2 == 0:
            # Par [cite: 27]
            primer_caracter = contenido[0]
            nuevo_caracter = aplicar_cifrado_cesar(primer_caracter, cant_numeros)
            llave += nuevo_caracter # [cite: 30]
        else:
            # Impar [cite: 28, 29]
            ultimo_caracter = contenido[-1]
            nuevo_valor_ascii = ord(ultimo_caracter) + cant_letras
            llave += chr(nuevo_valor_ascii) # [cite: 30]

    # Entrega [cite: 32, 33]
    print(llave)

if __name__ == '__main__':
    descifrar()