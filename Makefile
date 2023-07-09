build:
	docker compose up --build -d --remove-orphans
up:
	docker compose up -$(MAKEFLAGS)
down:
	docker compose down
logs:
	docker compose logs
superuser:
	docker-compose exec api bash echo "from apps.user.models import User; User.objects.create_superuser(email='administrator@mail.com', password='administrator')" | python3 manage.py shell