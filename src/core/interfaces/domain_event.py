from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseDomainEvent(ABC):
    @staticmethod
    @abstractmethod
    def get_event_name() -> str:
        pass
