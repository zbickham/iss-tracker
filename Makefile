#NAME ?= zbickham

all: build run push

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

build:
	docker build -t ${NAME}/iss_tracker_flask:latest .

run:
	docker run --name "iss_flask" -d -p 5003:5000 ${NAME}/iss_tracker_flask:latest

push:
	docker push ${NAME}/iss_tracker_flask:latest
