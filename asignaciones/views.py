
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Asignacion
from .serializers import AsignacionSerializer
from becagest.permisos import es_encargado


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lista_asignaciones(request):

    if request.method == 'GET':

        asignaciones = Asignacion.objects.all().order_by('id')

        if es_encargado(request.user):
            estado = request.query_params.get('estado')

            if estado:
                asignaciones = asignaciones.filter(estado=estado)
        else:
            asignaciones = asignaciones.filter(
                evaluacion__solicitud__estudiante__usuario=request.user
            )

        serializer = AsignacionSerializer(
            asignaciones,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    if not es_encargado(request.user):
        return Response(
            {'error': 'No tienes permiso para crear asignaciones.'},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = AsignacionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detalle_asignacion(request, pk):

    try:
        asignacion = Asignacion.objects.get(pk=pk)

    except Asignacion.DoesNotExist:
        return Response(
            {'error': 'Asignación no encontrada.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        if not es_encargado(request.user):
            if (
                asignacion.evaluacion.solicitud.estudiante.usuario_id
                != request.user.id
            ):
                return Response(
                    {'error': 'No tienes permiso para consultar esta asignación.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = AsignacionSerializer(asignacion)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    if not es_encargado(request.user):
        return Response(
            {'error': 'No tienes permiso para modificar asignaciones.'},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method in ['PUT', 'PATCH']:

        serializer = AsignacionSerializer(
            asignacion,
            data=request.data,
            partial=(request.method == 'PATCH')
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'DELETE':
        asignacion.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
