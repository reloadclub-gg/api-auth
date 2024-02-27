up:
	docker-compose up -d

down:
	docker-compose down -v

halt:
	docker-compose down

reset:
	make down
	docker-compose up -d --build

logs:
	docker-compose logs api -f

refresh:
	make halt
	make up
