from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.postgres.models import Base
from features.task.domain.entities.task_entity import TaskEntity
from features.task.domain.entities.task_query_model import TaskReadModel
from features.user.infrastructure.models.user import User
from features.team.infrastructure.models.team import Team


class Task(Base):
    __tablename__ = 'tasks'

    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    team: Mapped[Team] = relationship("Team", foreign_keys=[team_id], lazy='joined')
    creator: Mapped[User] = relationship("User", foreign_keys=[creator_id], lazy='joined')
    assignee: Mapped[User | None] = relationship("User", foreign_keys=[assignee_id], lazy='joined')

    def to_entity(self) -> 'TaskEntity':
        return TaskEntity(
            id_=self.id,
            title=self.title,
            description=self.description,
            team_id=self.team_id,
            creator_id=self.creator_id,
            assignee_id=self.assignee_id,
            deadline=self.deadline,
            team=self.team.to_entity() if self.team else None,
            creator=self.creator.to_entity() if self.creator else None,
            assignee=self.assignee.to_entity() if self.assignee else None,
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'team_id': self.team_id,
            'creator_id': self.creator_id,
            'assignee_id': self.assignee_id,
            'deadline': self.deadline if self.deadline else None,
            'team': self.team.to_dict() if self.team else None,
            'creator': self.creator.to_dict() if self.creator else None,
            'assignee': self.assignee.to_dict() if self.assignee else None,
        }

    def to_read_model(self) -> 'TaskReadModel':
        return TaskReadModel(
            id=self.id,
            title=self.title,
            description=self.description,
            team_id=self.team_id,
            creator_id=self.creator_id,
            assignee_id=self.assignee_id,
            deadline=self.deadline,
            team=self.team.to_read_model() if self.team else None,
            creator=self.creator.to_read_model() if self.creator else None,
            assignee=self.assignee.to_read_model() if self.assignee else None,
        )

    @classmethod
    def from_entity(cls, task: 'TaskEntity') -> 'Task':
        # TODO: FIX CODE DUPLICATE
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            team_id=task.team_id,
            creator_id=task.creator_id,
            assignee_id=task.assignee_id,
            deadline=task.deadline,
            team=Team.from_entity(task.team) if task.team else None,
            creator=User.from_entity(task.creator) if task.creator else None,
            assignee=User.from_entity(task.assignee) if task.assignee else None,
        )
