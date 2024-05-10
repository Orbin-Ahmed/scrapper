import requests
import random

def get_random_proxy():
    url = "https://proxylist.geonode.com/api/proxy-list"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            proxies = data["data"]
            random_proxy = random.choice(proxies)
            ip = random_proxy["ip"]
            port = random_proxy["port"]
            protocol = random_proxy["protocols"][0]
            return {protocol: f"{protocol}://{ip}:{port}"}
        else:
            print("Failed to fetch proxies. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred while fetching proxies:", e)
        return None

p = get_random_proxy();
print(p)