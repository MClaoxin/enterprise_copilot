from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.core.exceptions import WorkspaceForbiddenError
from app.services.authorization import AuthorizationService


@pytest.mark.parametrize(
    ("actual", "required", "allowed"),
    [
        ("owner", "admin", True),
        ("admin", "member", True),
        ("member", "viewer", True),
        ("viewer", "member", False),
        (None, "viewer", False),
    ],
)
def test_workspace_role_hierarchy(actual, required, allowed):
    member = None if actual is None else SimpleNamespace(role=actual)
    service = AuthorizationService(SimpleNamespace(get=lambda *args: member))

    if allowed:
        service.require_role(uuid4(), uuid4(), required)
    else:
        with pytest.raises(WorkspaceForbiddenError):
            service.require_role(uuid4(), uuid4(), required)
