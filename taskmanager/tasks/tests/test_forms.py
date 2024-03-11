import uuid

from tasks.forms import TaskFormWithRedis


def test_task_form_with_redis_is_valid_fails_second_time(uuid: str):
    uuid1 = uuid

    form_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "UNASSIGNED",
        "watchers": "watcher1@example.com, watcher2@example.com",
        "uuid": uuid1,
    }

    form = TaskFormWithRedis(data=form_data)
    assert form.is_valid(), f"Form should be valid: {form.errors}"

    form = TaskFormWithRedis(data=form_data)
    assert not form.is_valid()
    assert form.errors == {"uuid": ["Form already submitted"]}
