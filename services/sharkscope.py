import abc
import logging

from pydantic import BaseModel

from services.proxy import ProxyService
import requests


class Statistic(BaseModel):
    tournaments_count: int
    tournaments_entries: int
    avg_profit: float
    avg_state: float
    avg_roi: float
    profit_usd: float
    total_roi: float


class SharkScopeSvc(abc.ABC):
    @abc.abstractmethod
    def get_statistic(self, username: str) -> Statistic:
        pass


class DefaultSharkScopeSvc(SharkScopeSvc):
    def __init__(self, proxy_svc: ProxyService | None = None):
        self.proxy_svc = proxy_svc if proxy_svc is not None else None

    def get_statistic(self, username: str) -> Statistic:
        url = f"https://ru.sharkscope.com/poker-statistics/networks/GGNetwork/players/{username}?&Currency=USD"

        payload = {}
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'search4=60.57006599889623; split=1; ShowDataSourcing=F',
            'Referer': 'https://ru.sharkscope.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'searchTag': 's60.57006599889623',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }
        if self.proxy_svc is not None:
            proxies = {
                "http": self.proxy_svc.get_proxy(),
                "https": self.proxy_svc.get_proxy(),
            }
        else:
            proxies = {}
        logging.log(logging.INFO, f"Requesting {url} with proxies {proxies}")
        response = requests.get(url, headers=headers, data=payload, proxies=proxies)
        statistic = response.json()["Response"]["PlayerResponse"]["PlayerView"]["Player"]["Statistics"]["Statistic"]
        return Statistic(
            tournaments_count=statistic[0]["$"],
            tournaments_entries=statistic[1]["$"],
            avg_profit=statistic[2]["$"],
            avg_state=statistic[3]["$"],
            avg_roi=statistic[4]["$"],
            profit_usd=statistic[5]["$"],
            total_roi=statistic[10]["$"],
        )
