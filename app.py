import requests
from itertools import cycle
import traceback

def carregar_proxies(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    proxies = [linha.strip() for linha in linhas]
    return proxies

def solicitar_usando_proxy(url, proxy):
    try:
        resposta = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
        return resposta
    except Exception as e:
        traceback.print_exc()
        return None

if __name__ == "__main__":
    proxies = carregar_proxies("proxy.txt")
    pool_proxies = cycle(proxies)

    while True:
        proxy_atual = next(pool_proxies)
        print(f"Usando proxy: {proxy_atual}")
        url = "https://www.guaruja.sp.gov.br/"
        resultado = solicitar_usando_proxy(url, f"http://{proxy_atual}")
        if resultado:
            print(f"Resposta recebida: {resultado.status_code}")
        else:
            print("Falha na solicitação")