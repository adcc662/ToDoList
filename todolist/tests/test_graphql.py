import json
import pytest
from django.test import TestCase
from strawberry.django.test import GraphQLTestClient
from todo.urls import schema
from todolist.models import Task


class TaskGraphQLTests(TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.task1 = Task.objects.create(
            title="GraphQL Task 1", 
            description="First GraphQL test task", 
            completed=False
        )
        self.task2 = Task.objects.create(
            title="GraphQL Task 2", 
            description="Second GraphQL test task", 
            completed=True
        )
        self.client = GraphQLTestClient(schema)
    
    def test_query_all_tasks(self):
        """Test para obtener todas las tareas vía GraphQL"""
        query = """
        query {
            tasks {
                id
                title
                description
                completed
            }
        }
        """
        response = self.client.query(query)
        content = json.loads(response.content)
        
        self.assertIn("data", content)
        self.assertEqual(len(content["data"]["tasks"]), 2)
        
    def test_query_single_task(self):
        """Test para obtener una tarea específica vía GraphQL"""
        query = f"""
        query {{
            task(id: {self.task1.id}) {{
                id
                title
                description
                completed
            }}
        }}
        """
        response = self.client.query(query)
        content = json.loads(response.content)
        
        self.assertIn("data", content)
        self.assertEqual(content["data"]["task"]["title"], "GraphQL Task 1")
        
    def test_create_task_mutation(self):
        """Test para crear una tarea vía GraphQL"""
        mutation = """
        mutation {
            createTask(input: {
                title: "New GraphQL Task",
                description: "Created through GraphQL mutation",
                completed: false
            }) {
                id
                title
                description
                completed
            }
        }
        """
        response = self.client.query(mutation)
        content = json.loads(response.content)
        
        self.assertIn("data", content)
        self.assertEqual(content["data"]["createTask"]["title"], "New GraphQL Task")
        self.assertEqual(Task.objects.count(), 3)
        
    def test_update_task_mutation(self):
        """Test para actualizar una tarea vía GraphQL"""
        mutation = f"""
        mutation {{
            updateTask(id: {self.task1.id}, input: {{
                title: "Updated GraphQL Task",
                description: "Updated through GraphQL mutation",
                completed: true
            }}) {{
                id
                title
                description
                completed
            }}
        }}
        """
        response = self.client.query(mutation)
        content = json.loads(response.content)
        
        self.assertIn("data", content)
        self.assertEqual(content["data"]["updateTask"]["title"], "Updated GraphQL Task")
        self.assertEqual(content["data"]["updateTask"]["completed"], True)
        
        # Verificar que se actualizó en la base de datos
        updated_task = Task.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.title, "Updated GraphQL Task")
        
    def test_delete_task_mutation(self):
        """Test para eliminar una tarea vía GraphQL"""
        initial_count = Task.objects.count()
        mutation = f"""
        mutation {{
            deleteTask(id: {self.task1.id})
        }}
        """
        response = self.client.query(mutation)
        content = json.loads(response.content)
        
        self.assertIn("data", content)
        self.assertTrue(content["data"]["deleteTask"])
        self.assertEqual(Task.objects.count(), initial_count - 1)
        
        # Verificar que la tarea ya no existe
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task1.id)
