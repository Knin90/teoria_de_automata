"""Verificación por fuerza bruta de la Práctica N° 1 (AFD).

Para cada problema compara, sobre todas las cadenas de {a,b} hasta
LONGITUD_MAX, tres descripciones del mismo lenguaje:
  1. el AFD (quíntupla),
  2. la expresión regular,
  3. la definición del lenguaje en notación de conjuntos (predicado).
"""
import itertools
import re
import sys

SIGMA = "ab"
LONGITUD_MAX = 12


def acepta(afd, w):
    estado = afd["q0"]
    for simbolo in w:
        estado = afd["delta"][(estado, simbolo)]
    return estado in afd["F"]


PROBLEMAS = [
    {
        "nombre": "1. Cadenas que terminan en 'ab'",
        "afd": {
            "Q": {"q0", "q1", "q2"},
            "q0": "q0",
            "F": {"q2"},
            "delta": {
                ("q0", "a"): "q1", ("q0", "b"): "q0",
                ("q1", "a"): "q1", ("q1", "b"): "q2",
                ("q2", "a"): "q1", ("q2", "b"): "q0",
            },
        },
        "er": "(a|b)*ab",
        "conjunto": lambda w: w.endswith("ab"),
    },
    {
        "nombre": "2. Número par de 'a'",
        "afd": {
            "Q": {"q0", "q1"},
            "q0": "q0",
            "F": {"q0"},
            "delta": {
                ("q0", "a"): "q1", ("q0", "b"): "q0",
                ("q1", "a"): "q0", ("q1", "b"): "q1",
            },
        },
        "er": "b*(ab*ab*)*",
        "conjunto": lambda w: w.count("a") % 2 == 0,
    },
    {
        "nombre": "3. Empiezan y terminan con el mismo símbolo",
        "afd": {
            "Q": {"q0", "q1", "q2", "q3", "q4"},
            "q0": "q0",
            "F": {"q3", "q4"},
            "delta": {
                ("q0", "a"): "q1", ("q0", "b"): "q2",
                ("q1", "a"): "q3", ("q1", "b"): "q1",
                ("q2", "a"): "q2", ("q2", "b"): "q4",
                ("q3", "a"): "q3", ("q3", "b"): "q1",
                ("q4", "a"): "q2", ("q4", "b"): "q4",
            },
        },
        "er": "a(a|b)*a|b(a|b)*b",
        "conjunto": lambda w: len(w) >= 2 and w[0] == w[-1],
    },
    {
        "nombre": "4. Número de 'b' múltiplo de 3",
        "afd": {
            "Q": {"q0", "q1", "q2"},
            "q0": "q0",
            "F": {"q0"},
            "delta": {
                ("q0", "a"): "q0", ("q0", "b"): "q1",
                ("q1", "a"): "q1", ("q1", "b"): "q2",
                ("q2", "a"): "q2", ("q2", "b"): "q0",
            },
        },
        "er": "a*(ba*ba*ba*)*",
        "conjunto": lambda w: w.count("b") % 3 == 0,
    },
    {
        "nombre": "5. No contienen la subcadena 'bb'",
        "afd": {
            "Q": {"q0", "q1", "q2"},
            "q0": "q0",
            "F": {"q0", "q1"},
            "delta": {
                ("q0", "a"): "q0", ("q0", "b"): "q1",
                ("q1", "a"): "q0", ("q1", "b"): "q2",
                ("q2", "a"): "q2", ("q2", "b"): "q2",
            },
        },
        "er": "(a|ba)*b?",
        "conjunto": lambda w: "bb" not in w,
    },
]


def cadenas(longitud_max):
    for n in range(longitud_max + 1):
        for t in itertools.product(SIGMA, repeat=n):
            yield "".join(t)


def verificar(problema):
    afd = problema["afd"]
    # La función de transición debe ser total: δ: Q × Σ → Q
    for q in afd["Q"]:
        for s in SIGMA:
            if afd["delta"].get((q, s)) not in afd["Q"]:
                return f"δ({q}, {s}) no está definida"
    er = re.compile(problema["er"])
    for w in cadenas(LONGITUD_MAX):
        r_afd = acepta(afd, w)
        r_er = er.fullmatch(w) is not None
        r_conj = problema["conjunto"](w)
        if not (r_afd == r_er == r_conj):
            return f"discrepancia en {w!r}: AFD={r_afd}, ER={r_er}, conjunto={r_conj}"
    return None


def main():
    fallos = 0
    for p in PROBLEMAS:
        error = verificar(p)
        if error:
            fallos += 1
            print(f"FALLA  {p['nombre']}: {error}")
        else:
            print(f"OK     {p['nombre']}")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
