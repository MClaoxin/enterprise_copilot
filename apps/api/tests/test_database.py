from unittest.mock import Mock

import pytest

from app.db.unit_of_work import UnitOfWork
from app.models.user import User
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember


def test_user_email_has_a_named_unique_constraint():
    constraints = {item.name for item in User.__table__.constraints}
    assert "uq_users_email" in constraints


def test_workspace_has_slug_and_owner_indexes():
    indexes = {index.name: index for index in Workspace.__table__.indexes}
    constraints = {item.name for item in Workspace.__table__.constraints}
    assert "uq_workspaces_slug" in constraints
    assert "ix_workspaces_owner_id" in indexes


def test_workspace_member_constraints():
    indexes = {index.name: index for index in WorkspaceMember.__table__.indexes}
    constraints = {
        constraint.name: constraint
        for constraint in WorkspaceMember.__table__.constraints
        if constraint.name
    }
    assert "uq_workspace_member" in constraints
    assert "ix_workspace_members_user_id" in indexes
    assert "ck_workspace_member_role" in constraints
    assert {fk.ondelete for fk in WorkspaceMember.__table__.foreign_keys} == {"CASCADE"}


def test_unit_of_work_rolls_back_a_failed_commit():
    db = Mock()
    db.commit.side_effect = RuntimeError("commit failed")
    unit_of_work = UnitOfWork(db)

    with pytest.raises(RuntimeError, match="commit failed"):
        unit_of_work.commit()

    db.rollback.assert_called_once_with()
