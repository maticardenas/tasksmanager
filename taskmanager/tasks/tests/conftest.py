import pytest
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from ninja.testing import TestClient
from tasks.api.tasks import api_router
from tasks.enums import TaskStatus
from tasks.models import Task
from tasks.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def client():
    return TestClient(api_router)


@pytest.fixture
def user():
    user = UserFactory()
    user.save()

    return user


@pytest.fixture
def user_with_permissions(user: User):
    from django.contrib.auth.models import Permission

    content_type = ContentType.objects.get_for_model(Task)

    change_task_permission = Permission.objects.get(codename="change_task", content_type=content_type)
    add_task_permission = Permission.objects.get(codename="add_task", content_type=content_type)

    user.user_permissions.add(change_task_permission)
    user.user_permissions.add(add_task_permission)

    return user


@pytest.fixture
def jwt_auth_token(user):
    from accounts.services.auth import issue_jwt_token

    token = issue_jwt_token(user)
    return token


@pytest.fixture
def auth_headers(jwt_auth_token: str) -> dict:
    return {"Authorization": f"Bearer {jwt_auth_token}"}


@pytest.fixture
def task(user) -> Task:
    task = Task.objects.create(title="Test Task", description="Test Description", creator=user)
    return task


@pytest.fixture
def archived_task(user) -> Task:
    task = Task.objects.create(
        title="Test Task", description="Test Description", creator=user, status=TaskStatus.ARCHIVED.value
    )
    task.created_at = "2024-12-31"
    task.save()
    return task


@pytest.fixture
def uuid() -> str:
    import uuid

    return str(uuid.uuid4())
