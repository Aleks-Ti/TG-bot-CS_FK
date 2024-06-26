ifeq (revision,$(firstword $(MAKECMDGOALS)))
	# use the rest as arguments for run
	RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
	# ... and turn them into do-nothing targets
	$(eval $(RUN_ARGS):;@:)
endif

.PHONY: start revision migrate

start:
	python src/main.py

revision:
	alembic revision --autogenerate -m "fix game dificulty"

migrate:
	alembic upgrade head

st:
	ruff . --fix

startd:
	docker compose down && docker compose up -d
