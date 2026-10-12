# Teoría de Autómatas y Lenguajes Formales

Soluciones de prácticas del curso (Universidad de Panamá – FIEC, Departamento de Computación y Sistemas).

- [Práctica de clase (1-10-2026) – 10 problemas de AFD](practica_clase/Practica_Clase_AFD.md): quíntupla, diagrama, tabla de transición, expresión regular (con `*`, `+`, `?`) y lenguaje de cada problema, con un [script de verificación](practica_clase/verificar_afd.py).
- [Práctica N° 1 – Autómatas Finitos Deterministas (AFD)](practica1/Practica1_AFD.md): quíntupla, expresión regular y lenguaje regular de 5 problemas, con un [script de verificación](practica1/verificar_afd.py).
- [Visualizador interactivo](practica1/visualizador/index.html): construye cada AFD paso a paso (estados, aceptación, transiciones), simula cadenas símbolo por símbolo y deriva la expresión regular y el lenguaje. Incluye ambas prácticas. Ábrelo en el navegador.

## Despliegue en Vercel

El sitio muestra el visualizador en la raíz (`/`). `vercel.json` ejecuta `scripts/build.sh`, que genera `public/index.html` a partir de `practica1/visualizador/index.html` agregándole `<!doctype html>`, el charset y el viewport.
