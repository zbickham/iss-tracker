#NAME ?= zbickham

all: build run push

images:
	docker images | grep zbickham

ps:
	docker ps -a | grep zbickham

build:
	docker build -t zbickham/iss_tracker_flask:latest .

run:
	docker run --name "iss_flask" -d -p 5003:5000 --rm -v \:/app zbickham/iss_tracker_flask:latest

push:
	docker push zbickham/iss_tracker_flask:latest
