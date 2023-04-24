# Ejercicio Web Scrapping

Este proyecto consiste en extraer información de los episodios de Los Simpsons del sitio https://simpsonizados.me/serie/los-simpson/ utilizando técnicas de web scraping.

## Descripción

El objetivo es extraer los siguientes datos de cada episodio:

- Número del capítulo
- Nombre del capítulo
- Resumen del capítulo
- Número de temporada
- Fecha de emisión
- URL del video

La información extraída se debe guardar en un archivo .json con una estructura adecuada que permita acceder fácilmente a la información mencionada anteriormente.

## Dependencias

El proyecto requiere las siguientes dependencias de Python:

- requests
- BeautifulSoup4

Estas dependencias se pueden instalar fácilmente con pip, por ejemplo:

```
pip install requests
pip install beautifulsoup4
```

## Ejecución

Para ejecutar el script de web scraping, simplemente se debe correr el archivo `scraping.py` con Python 3:

```
python3 scraping.py
```

Esto generará un archivo `simpsons.json` en el directorio raíz del proyecto, que contendrá toda la información de los episodios.

## Randomizer

Adicionalmente, se incluye un script `randomize.py` que selecciona un episodio aleatorio del archivo `simpsons.json` y lo imprime en la consola. Para ejecutarlo, simplemente se debe correr:

```
python3 randomize.py
```

Esto imprimirá un episodio aleatorio con el siguiente formato:

```
Capítulo 1x2: Sin blanca Navidad
Miralo en: https://simpsonizados.me/capitulo/los-simpson-1x2/
``` 

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulte el archivo LICENSE para obtener más información.