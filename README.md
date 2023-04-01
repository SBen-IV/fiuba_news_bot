# Fiuba news bot

## Cómo usar
Es necesario un archivo .env con los siguientes campos:

```sh
BOT_TOKEN= # Token del bot
DEV_ID= # ID del desarrollador, para enviar stacktrace en caso de errores
ID_CANAL_NOTICIAS= # ID del canal de noticias en el cual se envian los mensaje automáticos
ID_GRUPO_NOTICIAS= # ID del grupo de noticias en el cual se maneja al bot
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

## TODOs

- [x] Ver cómo cambiar las noticias automáticas para hacer menos pegadas a la página (método que reciba una fecha y devuelva sólo noticias posteriores).
- [ ] Agregar método para convertir una url de una noticia.
- [ ] Agregar archivo config para variables como delay, intervalo entre mensajes, etc.
- [ ] Agregar script para correr en "dev" y "prod".
- [ ] Agregar comando /status, /estado o /info que devuelva el estado del bot
- [ ] Agregar /version (?)
- [ ] Agregar tests