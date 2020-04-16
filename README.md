# MsDocker
### Microservicio Docker
Servicio capaz de hacer funciones sobre docker.

#### Implementaion
Se ha implementado usando el SDK para python para controlar los servicios del DockerD de la máquina host.

#### Conexion
##### RabbitMQ RPC
Este servicio escucha en una cola de rabbitmq definida internamente y devuelve las respuestas por otra cola 
con el mismo correlationId.

Los mensajes del protocolo llevan en el cuerpo la informacion necesaria como el metodo y sus argumentos en formato JSON.

##### API REST
Implementa una API Rest implementado con Flask con los siguientes endpoints:
- /build
- /push
- /pull
- /list
- /docker-compose

Todos estos endpoints reciben peticiones POST y la información necesaria estará en el cuerpo del mensaje.

##### Componentes
Cuenta con archivos de configuracion para la ejecución del proyecto.