class WorkflowError(Exception):
    pass


class PermissionDenied(WorkflowError):
    pass


class InvalidStateTransition(WorkflowError):
    pass


class DrawingAlreadyClaimed(WorkflowError):
    pass


class NotOwner(WorkflowError):
    pass
