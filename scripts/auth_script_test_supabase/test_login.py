import json
import os
import urllib.error
import urllib.request


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    supabase_url = _required_env("SUPABASE_URL").rstrip("/")
    anon_key = _required_env("SUPABASE_KEY")
    email = _required_env("SUPABASE_TEST_EMAIL")
    password = _required_env("SUPABASE_TEST_PASSWORD")

    payload = json.dumps({"email": email, "password": password}).encode("utf-8")
    request = urllib.request.Request(
        f"{supabase_url}/auth/v1/token?grant_type=password",
        data=payload,
        headers={
            "apikey": anon_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Login failed: HTTP {exc.code} {error_body}") from exc

    user = body.get("user") or {}
    print("Login succeeded.")
    print(f"User ID: {user.get('id')}")
    print(f"Email: {user.get('email')}")
    print(f"Expires in: {body.get('expires_in')} seconds")
    print("Access token is intentionally not printed. Use scripts/get_supabase_access_token.py when a local token is needed.")


if __name__ == "__main__":
    main()
