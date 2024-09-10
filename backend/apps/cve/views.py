from rest_framework import generics
from rest_framework.views import APIView
import requests
import pprint

# from .models import Tarea
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class ListarAPIView(APIView):

    def get(self, request):

        url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'

        try:

            res = requests.get(url)
            datos = res.json()

            pprint.pprint(datos['vulnerabilities'][0])



            # return Response(res.json(), status=status.HTTP_200_OK)

            return Response({'mensaje': 'funciona'}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

