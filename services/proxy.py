import abc
import random

import requests


class ProxyService(abc.ABC):
    @abc.abstractmethod
    def get_proxy(self) -> str:
        pass


class PyProxyService(ProxyService):
    def __init__(self, base_url: str, _top: int = 30):
        self.base_url = base_url
        self._top = _top

    def get_proxy(self) -> str:
        return self.get_serviceable_proxy()

    def get_serviceable_proxy(
            self) -> str:
        """
        Перебирает случайные прокси из списка, проверяя их на жизнеспособность методом proxy_health и возвращает
        первый найденный работоспособный прокси.
        """
        proxies = self._get_http_proxy_list(self._top)
        while True:
            proxy = random.choice(proxies)
            if self.proxy_health(proxy, url="https://google.com"):
                return proxy

    @classmethod
    def proxy_health(
            cls,
            proxy,
            timeout: int = 5,
            url: str = "https://sharkscope.com") -> bool:
        try:
            return requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=timeout).status_code == 200
        except:
            return False

    def _get_http_proxy_list(self, cnt: int) -> list[str]:
        """
        Возвращает список http прокси, получая их из сервиса proxy_py.
        """
        proxies_url = f'{self.base_url}/api/v1/'
        json_data = {
            "model": "proxy",
            "method": "get",
            "order_by": "response_time, uptime"
        }
        response = requests.post(proxies_url, json=json_data)
        if response.status_code == 200:
            return [f'{proxy["domain"]}:{proxy["port"]}' for proxy in response.json()['data'] if
                    proxy['protocol'] == 'http'][:cnt]
        else:
            raise ConnectionError
