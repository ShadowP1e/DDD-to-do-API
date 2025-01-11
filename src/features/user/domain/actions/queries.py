from dataclasses import dataclass

from core.actions.base import BaseAction


@dataclass
class GetUserQuery(BaseAction):
    id: int
