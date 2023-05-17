start:
	docker-compose down -v && docker-compose build && docker-compose up -d

down:
	docker-compose down

test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml down && \
	docker-compose -f docker-compose.yml -f docker-compose.test.yml build && \
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up