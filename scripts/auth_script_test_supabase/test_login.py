import requests

res = requests.post(
    "https://drlbwntplyteqvrpnmdi.supabase.co/auth/v1/token?grant_type=password",
    headers={"apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRybGJ3bnRwbHl0ZXF2cnBubWRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA1Mzk1MzQsImV4cCI6MjA4NjExNTUzNH0.9GxV8X3iSls_0JQrzVIbRvgR6YOSW2jWMCJmiCGrdM0"},
    json={"email": "khoalmht0@gmail.com", "password": "123456"}
)
print(res.json().get("access_token"))
