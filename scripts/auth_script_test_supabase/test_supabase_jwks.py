import requests

url1 = "https://drlbwntplyteqvrpnmdi.supabase.co/auth/v1/jwks"
url2 = "https://drlbwntplyteqvrpnmdi.supabase.co/rest/v1/jwks"
url3 = "https://drlbwntplyteqvrpnmdi.supabase.co/auth/v1/settings"

for u in [url1, url2, url3]:
    res = requests.get(u)
    print(f"{u} no header -> {res.status_code}")

header = {'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRybGJ3bnRwbHl0ZXF2cnBubWRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA1Mzk1MzQsImV4cCI6MjA4NjExNTUzNH0.9GxV8X3iSls_0JQrzVIbRvgR6YOSW2jWMCJmiCGrdM0'}
for u in [url1, url2, url3]:
    res = requests.get(u, headers=header)
    print(f"{u} with anon -> {res.status_code}")
    if res.status_code == 200:
        print(res.text[:100])
