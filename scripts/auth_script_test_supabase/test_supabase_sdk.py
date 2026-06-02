import os

from supabase import Client, create_client


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    supabase_url = _required_env("SUPABASE_URL")
    anon_key = _required_env("SUPABASE_KEY")
    access_token = _required_env("SUPABASE_ACCESS_TOKEN")

    supabase: Client = create_client(supabase_url, anon_key)
    user_response = supabase.auth.get_user(access_token)
    user = user_response.user

    print("Supabase SDK auth check succeeded.")
    print(f"User ID: {user.id}")
    print(f"Email: {user.email}")


if __name__ == "__main__":
    main()
