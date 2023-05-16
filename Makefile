start:
	docker-compose down -v && docker-compose build && docker-compose up -d

down:
	docker-compose down