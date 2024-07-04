abrir mongodb atlas a todo el trafico

crear ec2 t2.large
añadir al security group: regla inbound	Todo el tráfico	Todo	Todo	0.0.0.0/0	–
conectar con ssh desde la consola de aws
ejecutar:
- sudo apt-get update
- sudo snap install docker
- navegar a usr/local/bin y ejecutar:
    - curl -SL https://github.com/docker/compose/releases/download/v2.28.1/docker-compose-linux-x86_64 -o docker-compose
    - sudo chmod +x docker-compose
- sudo systemctl start docker
- sudo docker run hello-world

crear el .env y el docker-compose.yaml

ejecutar docker-compose up

navegar a ECR y crear los repositorios:

drones_simulator
drones_ingester
drones_api
trips_api
trips_manager

abrir cloud9, pegar el directorio completo de src

ejecutar: aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 804314932290.dkr.ecr.us-east-1.amazonaws.com

navegar a cada directorio de app y ejecutar:
# Drones Simulator
docker build -t drones_simulator .
docker tag drones_simulator:latest 804314932290.dkr.ecr.us-east-1.amazonaws.com/drones_simulator:latest
docker push 804314932290.dkr.ecr.us-east-1.amazonaws.com/drones_simulator:latest

# Drones Ingester
docker build -t drones_ingester .
docker tag drones_ingester:latest 804314932290.dkr.ecr.us-east-1.amazonaws.com/drones_ingester:latest
docker push 804314932290.dkr.ecr.us-east-1.amazonaws.com/drones_ingester:latest

# Drones API
docker build -t drones_api .
docker tag drones_api:latest 804314932290.dkr.ecr.us-east-1.amazonaws.com/drones_api:latest
docker push 804314932290.dkr.ecr.us-east-1.amazonaws.com/drones_api:latest

# Trips API
docker build -t trips_api .
docker tag trips_api:latest 804314932290.dkr.ecr.us-east-1.amazonaws.com/trips_api:latest
docker push 804314932290.dkr.ecr.us-east-1.amazonaws.com/trips_api:latest

# Trips Manager
docker build -t trips_manager .
docker tag trips_manager:latest 804314932290.dkr.ecr.us-east-1.amazonaws.com/trips_manager:latest
docker push 804314932290.dkr.ecr.us-east-1.amazonaws.com/trips_manager:latest

navegar a ECS, crear un cluster, en el security group o usamos el mismo de la ec2 o tenemos q ir al default y abrir trafico a todo

navegar a definicion de tareas, crear una tarea para cada servicio, en las tareas definir las variables de entorno y poner en los dos roles que hay: labrole

desde cada tarea le damos a implementar servicio de tipo fargate

ir a api gateway, crear una de tipo rest con nombre cabifly

crear los registros de tipo http: http://18.208.232.169:5000/drones