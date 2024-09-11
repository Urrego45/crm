from rest_framework import generics
from rest_framework.views import APIView
import requests
import pprint

from .models import (
    Vulnerabilidad,
    SolucionVulnerabilidad,
    Descripcion,
    Metrica,
    DatoMetrica
)

from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count


class SincronizarVulnerabilidadesAPIView(APIView):

    def post(self, request):
        vulnerabilidad = []
        descripcion = []
        metrica = []
        datoMetrica = []

        url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'

        try:

            res = requests.get(url)
            datos = res.json()

            for vulnerabilidades in datos['vulnerabilities']:

                vulnerabilidad.append(self.armar_vulnerabilidad(vulnerabilidades['cve']))
            

            Vulnerabilidad.objects.bulk_create(vulnerabilidad, ignore_conflicts=True)

            for vulnerabilidades in datos['vulnerabilities']:

                descripcion.append(self.armar_descripcion(vulnerabilidades['cve']))

                metrica.append(self.armar_metrica(vulnerabilidades['cve']))

            lista_filtrada_descripcion = [x for x in descripcion if x is not None]
            lista_filtrada_metrica = [x for x in metrica if x is not None]

            
            if lista_filtrada_descripcion.count(None) != len(lista_filtrada_descripcion):
                Descripcion.objects.bulk_create(lista_filtrada_descripcion)

            if lista_filtrada_metrica.count(None) != len(lista_filtrada_metrica):

                Metrica.objects.bulk_create(lista_filtrada_metrica)


            for vulnerabilidades in datos['vulnerabilities']:

                datoMetrica.append(self.armar_datos_metrica(vulnerabilidades['cve']))
                


            lista_filtrada_dato_metrica = [x for x in datoMetrica if x is not None]

            if lista_filtrada_dato_metrica.count(None) != len(lista_filtrada_dato_metrica):

                DatoMetrica.objects.bulk_create(lista_filtrada_dato_metrica)
            
            return Response({'Mensaje': 'Vulnerabilidades sincronizadas'}, status=status.HTTP_200_OK)


        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

    def armar_vulnerabilidad(self, datos):
        return Vulnerabilidad(
            cve_id=datos['id'],
            source_identifier=datos['sourceIdentifier'],
            published=datos['published'],
            last_modified=datos['lastModified'],
            vuln_status=datos['vulnStatus'],
        )

    def armar_descripcion(self, datos):
        descripciones = []

        try:
            vulnerabilidad_instance = Vulnerabilidad.objects.get(cve_id=datos['id'])
        except Vulnerabilidad.DoesNotExist:
            return

        try:
            Descripcion.objects.get(vulnerabilidad__cve_id=datos['id'])
            return
        except Descripcion.DoesNotExist:

            return Descripcion(
                vulnerabilidad=vulnerabilidad_instance,
                lang=datos['descriptions'][0]['lang'],
                value=datos['descriptions'][0]['value'],
            )


    def armar_metrica(self, datos):

        if len(datos['metrics']) > 0:
            metricas = datos['metrics']['cvssMetricV2'][0]
        else:
            return

        try:
            vulnerabilidad_instance = Vulnerabilidad.objects.get(cve_id=datos['id'])
        except Vulnerabilidad.DoesNotExist:
            return
        
        try:
            Metrica.objects.get(vulnerabilidad__cve_id=datos['id'])
            return
        except Metrica.DoesNotExist:

            return Metrica(
                vulnerabilidad=vulnerabilidad_instance,
                source=metricas['source'],
                type=metricas['type'],
                base_severity=metricas['baseSeverity'],
                exploitability_score=metricas['exploitabilityScore'],
                impact_score=metricas['impactScore'],
            )


    def armar_datos_metrica(self, datos):

        if len(datos['metrics']) > 0:
            metricas = datos['metrics']['cvssMetricV2'][0]['cvssData']
        else:
            return
        
        # metricas = datos['metrics']['cvssMetricV2'][0]['cvssData']

        try:
            metrica_instance = Metrica.objects.get(vulnerabilidad__cve_id=datos['id'])
        except Metrica.DoesNotExist:
            return
        

        try:
            DatoMetrica.objects.get(metrica__vulnerabilidad__cve_id=datos['id'])
            return
        except DatoMetrica.DoesNotExist:

            return DatoMetrica(
                metrica=metrica_instance,
                version=metricas['version'],
                vector_string=metricas['vectorString'],
                access_vector=metricas['accessVector'],
                access_complexity=metricas['accessComplexity'],
                authentication=metricas['authentication'],
                confidentiality_impact=metricas['confidentialityImpact'],
                integrity_impact=metricas['integrityImpact'],
                availability_impact=metricas['availabilityImpact'],
                base_score=metricas['baseScore'],
            )


class VulnerabilidadesListAPIView(generics.ListAPIView):
    queryset = Vulnerabilidad.objects.all()
    serializer_class = serializers.VulnerabilidadListCreateSerializer


class DescripcionListAPIView(generics.ListAPIView):
    queryset = Descripcion.objects.all()
    serializer_class = serializers.DescripcionListSerializer


class MetricaListAPIView(generics.ListAPIView):
    queryset = Metrica.objects.all()
    serializer_class = serializers.MetricaListSerializer


class DatoMetricaListAPIView(generics.ListAPIView):
    queryset = DatoMetrica.objects.all()
    serializer_class = serializers.DatoMetricaListSerializer


class SolucionVulnerabilidadListCreateAPIView(generics.ListCreateAPIView):
    queryset = SolucionVulnerabilidad.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.SolucionVulnerabilidadCreateSerializer
        return serializers.SolucionVulnerabilidadListSerializer
    


class VulnerabilidadesSinSolucionListAPIView(generics.ListAPIView):
    queryset = Vulnerabilidad.objects.filter(soluciones_vulnerabilidades_vulnerabilidades__isnull=True)
    serializer_class = serializers.VulnerabilidadCompletaListCreateSerializer


class VulnerabilidadeSeveridadListAPIView(generics.ListAPIView):

    def get(self, request):
        conteo = (
            Metrica.objects.values('base_severity').annotate(cantidad=Count('uuid')).order_by('base_severity')
        )
        return Response(conteo)
