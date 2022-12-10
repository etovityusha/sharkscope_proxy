import abc
import datetime

from pymongo.database import Database

from services.sharkscope import Statistic


class StatisticEntity(Statistic):
    updated: datetime.datetime | None = None


class StatsRepo(abc.ABC):
    @abc.abstractmethod
    def get_statistic(self, username: str) -> StatisticEntity | None:
        pass

    @abc.abstractmethod
    def set_statistic(self, username: str, statistic: StatisticEntity) -> None:
        pass


class MongoStatsRepo(StatsRepo):

    def __init__(self, db: Database):
        self.db = db
        self.collection = db.stats

    def get_statistic(self, username: str) -> StatisticEntity | None:
        row = self.collection.find_one({"username": username})
        return None if row is None else StatisticEntity(**row["statistic"])

    def set_statistic(self, username: str, statistic: StatisticEntity) -> None:
        self.collection.update_one(
            {"username": username},
            {"$set": {"statistic": {**statistic.dict(), "updated": datetime.datetime.now()}}},
            upsert=True
        )
