"""
Módulo: rsa_demo.py
RSA demostrativo — cifrado asimétrico de clave pública.

ADVERTENCIA: esta implementación usa números pequeños para que el proceso
sea legible y verificable a mano. NO es segura para uso real. RSA seguro
requiere primos de al menos 2048 bits.

Fundamento matemático:
  1. Se eligen dos primos p y q.
  2. n = p * q  (módulo público)
  3. phi(n) = (p-1) * (q-1)  (función de Euler)
  4. Se elige e tal que 1 < e < phi(n) y mcd(e, phi(n)) = 1  (exponente público)
  5. Se calcula d = e^{-1} mod phi(n)  (exponente privado, usando Euclides extendido)
  6. Clave pública: (e, n)  — se puede compartir libremente.
     Clave privada: (d, n)  — debe mantenerse secreta.
  7. Cifrar:   c = m^e mod n
     Descifrar: m = c^d mod n

La seguridad de RSA depende de la dificultad de factorizar n = p*q cuando
p y q son primos grandes (problema NP-duro sin algoritmo eficiente conocido).

Aplicación al sistema: un nodo podría firmar digitalmente sus eventos con su
clave privada; el receptor verifica con la clave pública, garantizando que el
evento no fue alterado en tránsito.
"""
from math import gcd
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Algoritmo de Euclides extendido
# ---------------------------------------------------------------------------

def _euclides_extendido(a: int, b: int) -> Tuple[int, int, int]:
    """
    Calcula mcd(a, b) y los coeficientes de Bezout (x, y) tal que a*x + b*y = mcd(a,b).

    Complexity: O(log(min(a,b))).
    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = _euclides_extendido(b, a % b)
    return g, y1, x1 - (a // b) * y1


def _inverso_modular(e: int, phi: int) -> int:
    """
    Calcula e^{-1} mod phi usando el algoritmo de Euclides extendido.

    Raises:
        ValueError: si e y phi no son coprimos (no existe inverso).
    """
    g, x, _ = _euclides_extendido(e, phi)
    if g != 1:
        raise ValueError(f"{e} no tiene inverso modular respecto a {phi} (mcd={g})")
    return x % phi


def _es_primo(n: int) -> bool:
    """Verificación de primalidad por divisores hasta sqrt(n). Solo para n pequeños."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

class RSADemo:
    """
    Implementación demostrativa de RSA con primos pequeños.

    Attributes:
        p (int): Primer primo.
        q (int): Segundo primo.
        n (int): Módulo público (p * q).
        e (int): Exponente público.
        d (int): Exponente privado.
        clave_publica (Tuple[int,int]): (e, n)
        clave_privada (Tuple[int,int]): (d, n)
    """

    def __init__(self, p: int, q: int, e: int = None):
        """
        Genera un par de claves RSA a partir de dos primos p y q.

        Args:
            p: Primer número primo.
            q: Segundo número primo (distinto de p).
            e: Exponente público. Si no se provee, se elige el menor valor
               mayor a 1 que sea coprimo con phi(n).

        Raises:
            ValueError: si p o q no son primos, o si son iguales.
        """
        if not _es_primo(p) or not _es_primo(q):
            raise ValueError(f"p={p} y q={q} deben ser numeros primos")
        if p == q:
            raise ValueError("p y q deben ser distintos")

        self.p = p
        self.q = q
        self.n = p * q
        phi = (p - 1) * (q - 1)

        if e is None:
            e = 2
            while e < phi and gcd(e, phi) != 1:
                e += 1
        else:
            if gcd(e, phi) != 1:
                raise ValueError(f"e={e} no es coprimo con phi(n)={phi}")

        self.e = e
        self.d = _inverso_modular(e, phi)
        self.clave_publica  = (self.e, self.n)
        self.clave_privada  = (self.d, self.n)

    def cifrar(self, mensaje: int) -> int:
        """
        Cifra un número entero con la clave pública.

        Args:
            mensaje: Número entero m tal que 0 <= m < n.

        Returns:
            Texto cifrado c = m^e mod n.

        Raises:
            ValueError: si el mensaje es mayor o igual que n.
        """
        if mensaje >= self.n:
            raise ValueError(f"El mensaje ({mensaje}) debe ser menor que n={self.n}")
        return pow(mensaje, self.e, self.n)

    def descifrar(self, cifrado: int) -> int:
        """
        Descifra un número entero con la clave privada.

        Args:
            cifrado: Texto cifrado c.

        Returns:
            Mensaje original m = c^d mod n.
        """
        return pow(cifrado, self.d, self.n)

    def cifrar_texto(self, texto: str) -> List[int]:
        """
        Cifra cada carácter de un string usando su valor ASCII.

        Limitación: cada carácter debe tener valor ASCII < n.

        Args:
            texto: Cadena a cifrar.

        Returns:
            Lista de enteros cifrados, uno por carácter.
        """
        return [self.cifrar(ord(c)) for c in texto]

    def descifrar_texto(self, cifrados: List[int]) -> str:
        """
        Descifra una lista de enteros y reconstruye el string original.

        Args:
            cifrados: Lista producida por cifrar_texto.

        Returns:
            Texto original.
        """
        return "".join(chr(self.descifrar(c)) for c in cifrados)

    def __repr__(self) -> str:
        return (f"RSADemo(p={self.p}, q={self.q}, n={self.n}, "
                f"e={self.e}, d={self.d})")
