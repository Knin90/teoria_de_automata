"""Verificación por fuerza bruta de la Práctica de clase (10 problemas de AFD).

Para cada problema compara, sobre todas las cadenas de su alfabeto hasta
LONGITUD_MAX, tres descripciones del mismo lenguaje:
  1. el AFD (quíntupla),
  2. la expresión regular (notación de la práctica: | unión, * + ? cuantificadores),
  3. la definición del lenguaje en notación de conjuntos (predicado).
"""
import itertools
import re
import sys

LONGITUD_MAX = 12


def afd(sigma, finales, filas):
    """filas: {estado: (destino con sigma[0], destino con sigma[1])}; q0 es el inicial."""
    delta = {(q, s): d for q, ds in filas.items() for s, d in zip(sigma, ds)}
    return {"Q": set(filas), "sigma": sigma, "q0": "q0", "F": set(finales), "delta": delta}


def acepta(m, w):
    estado = m["q0"]
    for simbolo in w:
        estado = m["delta"][(estado, simbolo)]
    return estado in m["F"]


def alterna_desde_a(w):
    return len(w) >= 1 and all(c == "ab"[i % 2] for i, c in enumerate(w))


PROBLEMAS = [
    ("1. Terminan con 'b'",
     afd("ab", ["q1"], {"q0": ("q0", "q1"), "q1": ("q0", "q1")}),
     "(a|b)*b", lambda w: w.endswith("b")),
    ("2. Prefijo '0' opcional y uno o más '1'",
     afd("01", ["q2"], {"q0": ("q1", "q2"), "q1": ("q3", "q2"), "q2": ("q3", "q2"), "q3": ("q3", "q3")}),
     "0?1+", lambda w: (resto := w[1:] if w.startswith("0") else w) != "" and set(resto) == {"1"}),
    ("3. Al menos una 'a'",
     afd("ab", ["q1"], {"q0": ("q1", "q0"), "q1": ("q1", "q1")}),
     "b*a(a|b)*", lambda w: "a" in w),
    ("4. Comienzan y terminan con el mismo símbolo (longitud >= 1)",
     afd("01", ["q1", "q3"], {"q0": ("q1", "q3"), "q1": ("q1", "q2"), "q2": ("q1", "q2"),
                               "q3": ("q4", "q3"), "q4": ("q4", "q3")}),
     "0((0|1)*0)?|1((0|1)*1)?", lambda w: len(w) >= 1 and w[0] == w[-1]),
    ("5. Cero o más bloques 'ab'",
     afd("ab", ["q0"], {"q0": ("q1", "q2"), "q1": ("q2", "q0"), "q2": ("q2", "q2")}),
     "(ab)*", lambda w: len(w) % 2 == 0 and w == "ab" * (len(w) // 2)),
    ("6. x, y opcionales (una o más), x",
     afd("xy", ["q2"], {"q0": ("q1", "q3"), "q1": ("q2", "q1"), "q2": ("q3", "q3"), "q3": ("q3", "q3")}),
     "x(y+)?x", lambda w: len(w) >= 2 and w[0] == "x" and w[-1] == "x" and set(w[1:-1]) <= {"y"}),
    ("7. Contienen '00'",
     afd("01", ["q2"], {"q0": ("q1", "q0"), "q1": ("q2", "q0"), "q2": ("q2", "q2")}),
     "(0|1)*00(0|1)*", lambda w: "00" in w),
    ("8. Alternas comenzando con 'a'",
     afd("ab", ["q1", "q2"], {"q0": ("q1", "q3"), "q1": ("q3", "q2"), "q2": ("q1", "q3"), "q3": ("q3", "q3")}),
     "a(ba)*b?", alterna_desde_a),
    ("9. Uno o más dígitos y letra opcional",
     afd("dl", ["q1", "q2"], {"q0": ("q1", "q3"), "q1": ("q1", "q2"), "q2": ("q3", "q3"), "q3": ("q3", "q3")}),
     "d+l?", lambda w: len(w.rstrip("l")) >= 1 and set(w.rstrip("l")) == {"d"} and len(w) - len(w.rstrip("l")) <= 1),
    ("10. Número impar de '1'",
     afd("01", ["q1"], {"q0": ("q0", "q1"), "q1": ("q1", "q0")}),
     "0*1(0*10*1)*0*", lambda w: w.count("1") % 2 == 1),
]


def verificar(m, er, conjunto):
    er = re.compile(er)
    for n in range(LONGITUD_MAX + 1):
        for t in itertools.product(m["sigma"], repeat=n):
            w = "".join(t)
            r = (acepta(m, w), er.fullmatch(w) is not None, conjunto(w))
            if len(set(r)) > 1:
                return f"discrepancia en {w!r}: AFD={r[0]}, ER={r[1]}, conjunto={r[2]}"
    return None


def main():
    fallos = 0
    for nombre, m, er, conjunto in PROBLEMAS:
        error = verificar(m, er, conjunto)
        fallos += bool(error)
        print(f"FALLA  {nombre}: {error}" if error else f"OK     {nombre}")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
