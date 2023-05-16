start:
	docker-compose down -v && docker-compose build && docker-compose up -d

down:
	docker-compose down

test:
	cd tests/ && docker-compose down && docker-compose build && docker-compose up tests