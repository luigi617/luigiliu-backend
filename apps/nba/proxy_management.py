import requests
from bs4 import BeautifulSoup

valid_proxies = set()

def check_proxy_ssl(proxy):
    
    proxies = {"https": f"http://{proxy}"}
    test_url = "https://httpbin.org/ip"
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except:
        return False

def get_free_ssl_proxy():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find("table")
    for row in table.tbody.find_all("tr"):
        tds = row.find_all("td")
        if tds[6].text == "yes" and check_proxy_ssl(f"{tds[0].text}:{tds[1].text}"):
            return f"{tds[0].text}:{tds[1].text}"            
    return None

def get_next_proxy():
    if valid_proxies:
        proxy = valid_proxies.pop()
        valid_proxies.add(proxy)
    else:
        proxy = get_free_ssl_proxy()
    return proxy

def add_valid_proxy(proxy):
    valid_proxies.add(proxy)

def remove_valid_proxy(proxy):
    if proxy in valid_proxies:
        valid_proxies.remove(proxy)

def call_function_with_proxy(func, max_trial=5):
    for _ in range(max_trial):
        proxy = get_next_proxy()
        try:
            res = func(proxy)
            add_valid_proxy(proxy)
            return res
        except:
            remove_valid_proxy(proxy)
    return None

