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


class SincronizarVulnerabilidadesAPIView(APIView):

    def post(self, request):
        vulnerabilidad = []
        descripcion = []
        descripcion_completa = []
        metrica = []
        datoMetrica = []

        c = 0
        a = 0
        b = 0

        url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'

        try:

            res = requests.get(url)
            datos = res.json()

            for vulnerabilidades in datos['vulnerabilities']:

                vulnerabilidad.append(self.armar_vulnerabilidad(vulnerabilidades['cve']))
                c += 1

                if c == 5:
                    break
            

            Vulnerabilidad.objects.bulk_create(vulnerabilidad, ignore_conflicts=True)

            for vulnerabilidades in datos['vulnerabilities']:
                if a == 5:
                    break

                descripcion.append(self.armar_descripcion(vulnerabilidades['cve']))

                metrica.append(self.armar_metrica(vulnerabilidades['cve']))

                a += 1

            if not None in descripcion: 
                Descripcion.objects.bulk_create(descripcion)

            if not None in metrica:
                Metrica.objects.bulk_create(metrica)



            for vulnerabilidades in datos['vulnerabilities']:
                if b == 5:
                    break

                datoMetrica.append(self.armar_datos_metrica(vulnerabilidades['cve']))
                

                b += 1

            if not None in datoMetrica:
                DatoMetrica.objects.bulk_create(datoMetrica)
            
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
            # for descripcion in datos['descriptions']:
            #     descripciones.append(
            #     )

            return descripciones

    def armar_metrica(self, datos):

        metricas = datos['metrics']['cvssMetricV2'][0]

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
        metricas = datos['metrics']['cvssMetricV2'][0]['cvssData']

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

        # return DatoMetrica(
            
        # )



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
        serializer = serializers.VulnerabilidadSeveridadListSerializer
        conteo = serializer.get_conteo()
        return Response(conteo)
