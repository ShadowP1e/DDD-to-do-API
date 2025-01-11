from abc import ABC, abstractmethod
from typing import Generic, TypeVar

_T = TypeVar('_T')
_R = TypeVar('_R')


class BaseUseCase(ABC, Generic[_T, _R]):

    @abstractmethod
    async def execute(self, data: _T) -> _R:
        raise NotImplementedError()
