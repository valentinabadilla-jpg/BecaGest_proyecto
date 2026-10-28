
from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase

from .models import Asignacion
from .serializers import AsignacionSerializer


class PruebasAsignaciones(TestCase):

    def test_monto_negativo(self):
        serializer = AsignacionSerializer(
            data={'monto_mensual': -100}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            'monto_mensual',
            serializer.errors
        )


class PruebasAPIAsignaciones(APITestCase):

    def setUp(self):
        self.encargado = User.objects.create_user(
            username='encargado_prueba',
            password='Clave12345!'
        )

        self.estudiante = User.objects.create_user(
            username='estudiante_prueba',
            password='Clave12345!'
        )

        grupo_encargado, _ = Group.objects.get_or_create(
            name='Encargado'
        )

        grupo_estudiante, _ = Group.objects.get_or_create(
            name='Estudiante'
        )

        self.encargado.groups.add(grupo_encargado)
        self.estudiante.groups.add(grupo_estudiante)

    def test_sin_token(self):
        respuesta = self.client.get(
            '/api/asignaciones/'
        )

        self.assertEqual(
            respuesta.status_code,
            401
        )

    def test_estudiante_no_puede_crear(self):
        self.client.force_authenticate(
            user=self.estudiante
        )

        respuesta = self.client.post(
            '/api/asignaciones/',
            {},
            format='json'
        )

        self.assertEqual(
            respuesta.status_code,
            403
        )

    def test_encargado_puede_consultar(self):
        self.client.force_authenticate(
            user=self.encargado
        )

        respuesta = self.client.get(
            '/api/asignaciones/'
        )

        self.assertEqual(
            respuesta.status_code,
            200
        )
