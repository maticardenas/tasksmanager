import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from tasks.enums import TaskStatus
from tasks.models import Task


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    # password = factory.Faker("password")


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    status = factory.Iterator([status.value for status in TaskStatus])
    creator = factory.SubFactory(UserFactory)

    owner = factory.Maybe(
        factory.Faker("pybool"),
        yes_declaration=factory.SubFactory(UserFactory),
        no_declaration=None,
    )
    version = factory.Sequence(lambda n: n)
