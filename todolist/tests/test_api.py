import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from todolist.models import Task
from todolist.serializers import TaskSerializer


class TaskAPITests(APITestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.task1 = Task.objects.create(
            title="Task 1", 
            description="First test task", 
            completed=False
        )
        self.task2 = Task.objects.create(
            title="Task 2", 
            description="Second test task", 
            completed=True
        )
        self.tasks_url = '/api/tasks/'
        
    def test_get_all_tasks(self):
        """Test para obtener todas las tareas"""
        response = self.client.get(self.tasks_url)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)
        
    def test_create_task(self):
        """Test para crear una nueva tarea"""
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'completed': False
        }
        
        response = self.client.post(self.tasks_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.get(title='New Task').description, 'New task description')
        
    def test_get_single_task(self):
        """Test para obtener una tarea específica"""
        response = self.client.get(f'{self.tasks_url}{self.task1.id}/')
        serializer = TaskSerializer(self.task1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_update_task(self):
        """Test para actualizar una tarea"""
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'completed': True
        }
        
        response = self.client.put(f'{self.tasks_url}{self.task1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_task = Task.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.title, 'Updated Task')
        self.assertEqual(updated_task.description, 'Updated description')
        self.assertEqual(updated_task.completed, True)
        
    def test_delete_task(self):
        """Test para eliminar una tarea"""
        initial_count = Task.objects.count()
        response = self.client.delete(f'{self.tasks_url}{self.task1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), initial_count - 1)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task1.id)
