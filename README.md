# Fiuba news bot

## Cómo usar
Es necesario un archivo .env con los siguientes campos:

```sh
BOT_TOKEN= # Token del bot
DEV_ID= # ID del desarrollador, para enviar stacktrace en caso de errores
ID_CANAL_NOTICIAS= # ID del canal de noticias en el cual se envian los mensaje automáticos
```

## Prerequisitos
- `pipenv` version 2022.10.25 o mayor
- `python` version 3.8 o mayor

## Preparación

Para instalar el entorno virtual con los paquetes:

```sh
pipenv --python 3.8
```

## Ejecución

```sh
pipenv run python3.8 main.py
```
