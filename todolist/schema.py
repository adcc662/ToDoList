import strawberry
from typing import List, Optional
from .models import Task

@strawberry.type
class TaskType:
    id: int
    title: str
    description: str
    completed: bool

@strawberry.type
class Query:
    @strawberry.field
    def tasks(self) -> List[TaskType]:
        return Task.objects.all()

    @strawberry.field
    def task(self, id: int) -> Optional[TaskType]:
        try:
            return Task.objects.get(pk=id)
        except Task.DoesNotExist:
            return None

@strawberry.input
class TaskInput:
    title: str
    description: str
    completed: bool = False

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(self, input: TaskInput) -> TaskType:
        task = Task.objects.create(
            title=input.title,
            description=input.description,
            completed=input.completed
        )
        return task

    @strawberry.mutation
    def update_task(self, id: int, input: TaskInput) -> Optional[TaskType]:
        try:
            task = Task.objects.get(pk=id)
            task.title = input.title
            task.description = input.description
            task.completed = input.completed
            task.save()
            return task
        except Task.DoesNotExist:
            return None

    @strawberry.mutation
    def delete_task(self, id: int) -> bool:
        try:
            Task.objects.get(pk=id).delete()
            return True
        except Task.DoesNotExist:
            return False

schema = strawberry.Schema(query=Query, mutation=Mutation)
