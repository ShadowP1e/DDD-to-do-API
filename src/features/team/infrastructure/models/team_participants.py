from sqlalchemy import Column, ForeignKey, Table

from core.models.postgres.models import Base

team_participants = Table(
    'team_participants',
    Base.metadata,
    Column('team_id', ForeignKey('teams.id', ondelete="CASCADE"), primary_key=True),
    Column('user_id', ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
)
