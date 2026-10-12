#!/bin/sh
# Genera public/index.html para Vercel a partir del visualizador.
# El archivo fuente no trae <!doctype>, charset ni viewport (el visor de
# artifacts de claude.ai los agrega al publicarlo), así que aquí se anteponen.
set -e
mkdir -p public
{
  printf '%s\n' '<!doctype html>' '<html lang="es">' '<meta charset="utf-8">' \
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' \
    '<style>body{margin:0}[hidden]{display:none!important}</style>'
  cat practica1/visualizador/index.html
} > public/index.html
