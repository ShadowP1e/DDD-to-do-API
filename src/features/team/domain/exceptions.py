class TeamDoesNotExistError(Exception):
    ...


class NotTeamOwnerError(Exception):
    ...


class NotTeamParticipantError(Exception):
    ...


class CanNotRemoveOwnerError(Exception):
    ...
