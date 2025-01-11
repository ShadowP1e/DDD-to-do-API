from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

_T = TypeVar('_T')


class BaseQueryService(ABC, Generic[_T]):

    @abstractmethod
    async def fetch_all(self) -> Sequence[_T]:
        raise NotImplementedError()

    @abstractmethod
    async def fetch_by_id(self, id_: int) -> _T | None:
        raise NotImplementedError()
