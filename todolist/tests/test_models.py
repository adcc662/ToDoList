import pytest
from django.test import TestCase
from todolist.models import Task


class TaskModelTests(TestCase):
    def test_task_creation(self):
        """Test que verifica la creación correcta de una tarea"""
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            completed=False
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.completed, False)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

    def test_task_string_representation(self):
        """Test que verifica la representación string de una tarea"""
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            completed=False
        )
        self.assertEqual(str(task), "Test Task")
