
  <p align="center">
   <img src="https://github.com/user-attachments/assets/1cad89f4-4d36-4a79-afab-3da4d9efa789">
   </p>
<h1 align="center"> El rasca citas (célebres) </h1>

## Descripción del proyecto 

El rasca citas es un proyecto donde se "rascan" citas célebres de -en principio y a modo de muestra- dos sitios web.
Responde a la necesidad de la empresa XYZ Corp, que está pensando en utilizar una frase que se identifique con sus
valores y su misión.

## Funcionalidades

Después de sacar citas de dos sitios web, éstas se almacenan en una base de datos. Una vez almacenadas, se pueden buscar desde un fronted de las siguientes formas: 
- por una etiqueta: se muestran todas las citas que están asociadas a esa etiqueta
- por más de una etiqueta: se muestran todas las citas asociadas a la combinación de etiquetas seleccionadas
- por el autor de la cita
- por una combinación de etiqueta y autor

## Cómo se arranca

Variables de entorno (parar arrancar desde github o construir el docker compose: :

![variables de entorno](https://github.com/user-attachments/assets/714ea241-b061-463c-9572-1aad07efaada)

Comando para construir imagen de docker y ejecutarla: 

![imagen](https://github.com/user-attachments/assets/53841f41-3e96-48f4-bed1-b1b11b4bf9c4)


Para que el proyecto funciones tiene que tener en ejecución la base de datos scraping_quotes. 
A través de Visual Studio Code, habría que ejecutar el comando *streamlit run main.py * desde la carpeta src

![arrancar_vsc](https://github.com/user-attachments/assets/42697028-7c09-443d-8cf8-3da76a9d5311)

Otra forma sería desde Docker arrancar el contenedor *web_scraping_angel_sc*

![arrancar_desde_docker](https://github.com/user-attachments/assets/47bbc0b1-3e4d-4296-b05f-b2db0560a75e)

En un futuro también se desplegará desde Streamlite Cloud.

## Teconologías utilizadas

- Lenguaje de programación Python
- Base de datos MongoDB
- Test unitarios: Pytest
- Creación de fronted para que interaccione un usuario: Streamlite
- Creación de imagen y de contenedores de aplicación y base de datos: Docker
- Organizaciónd del trabajo: Trello
- Control de versiones: GitHub
  
![python-logo-master-v3-TM-flattened](https://github.com/user-attachments/assets/2e93137f-033a-4c03-bc18-22f829dd3a94)
![MongoDB_SpringGreen](https://github.com/user-attachments/assets/1ac19f43-c938-4577-9865-6eb8e6b2242c)
![pytest1](https://github.com/user-attachments/assets/1bdb7549-1d74-4e0c-b759-26c2b16e9576)
![streamlit-logo-primary-colormark-darktext](https://github.com/user-attachments/assets/1e0b7995-c482-4b7b-ad9e-77f15e8ac715)
![docker-mark-blue](https://github.com/user-attachments/assets/1fe34e27-5aa8-4c81-8f50-1428b7f9c599)
![trello_logo_icon_168452](https://github.com/user-attachments/assets/294b00bc-7503-46ca-a337-b1e296862a38)
![github](https://github.com/user-attachments/assets/1faaf580-7970-4d71-b306-1840cfa175a7)

## Posibles mejoras

- Despliegue en la web
- Rascado en más páginas de citas
- Mejora de búsqueda por etiqueta: que una etiqueta indique con qué otras etiquetas está relacionada al ser seleccionada...



## Autor del proyecto


Ángel Sanz Crespo
