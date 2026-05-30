login_get_AT: 
	uv run python -m scripts.auth_script_test_supabase.test_login

get_supabase_user: 
	uv run python -m scripts.auth_script_test_supabase.test_supabase_sdk

clean: 
	./clean.sh

t1:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

t2:
	uv run celery -A app.core.celery_app.celery_app worker -Q document -l info --pool=solo --concurrency 1

t3:
	uv run celery -A app.core.celery_app.celery_app worker -Q notification,maintenance -l info --pool=solo --concurrency 1

t4:
	uv run celery -A app.core.celery_app.celery_app beat -l info

t5:
	uv run python -m app.services.agent_voice_gpt_realtime start

gat:
	uv run python scripts/get_supabase_access_token.py