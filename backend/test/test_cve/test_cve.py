from rest_framework import status
from test.factories.cve.cve_factories import VulnerabilidadFactory
from test.test_setup import TestSetUp
from django.urls import reverse
from apps.cve.models import (
    Vulnerabilidad,
    Descripcion,
    SolucionVulnerabilidad,
    Metrica,
    DatoMetrica,
)

class VulnerabilidadTestCase(TestSetUp):   

    def test_list_vulnerabilidad(self):
        url = reverse('vulnerabilidad-api')

        Vulnerabilidad.objects.create(
            cve_id='CVE-1999-0095',
            source_identifier= 'cve@mitre.org',
            published= '1988-10-01T04:00:00.000',
            last_modified= '2019-06-11T20:29:00.263',
            vuln_status= 'Modified'
        )
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class DescripcionTestCase(TestSetUp):
    def test_list_descripcion(self):
        vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-1999-0095',
            source_identifier= 'cve@mitre.org',
            published= '1988-10-01T04:00:00.000',
            last_modified= '2019-06-11T20:29:00.263',
            vuln_status= 'Modified'
        )

        Descripcion.objects.create(
            vulnerabilidad= vulnerabilidad,
            lang= 'en',
            value= 'dato prueba',
        )

        url = reverse('descripcion-api')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class MetricaTestCase(TestSetUp):
    def test_list_metrica(self):
        vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-1999-0095',
            source_identifier= 'cve@mitre.org',
            published= '1988-10-01T04:00:00.000',
            last_modified= '2019-06-11T20:29:00.263',
            vuln_status= 'Modified'
        )

        Metrica.objects.create(
            vulnerabilidad=vulnerabilidad,
            source='dato prueba',
            type='prueba',
            base_severity='alto',
            exploitability_score=10.0,
            impact_score=12.0,
        )

        url = reverse('metrica-api')


        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class DatoMetricaTestCase(TestSetUp):
    def test_list_datos_metrica(self):
        vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-1999-0095',
            source_identifier= 'cve@mitre.org',
            published= '1988-10-01T04:00:00.000',
            last_modified= '2019-06-11T20:29:00.263',
            vuln_status= 'Modified'
        )

        metrica = Metrica.objects.create(
            vulnerabilidad=vulnerabilidad,
            source='dato prueba',
            type='prueba',
            base_severity='alto',
            exploitability_score=10.0,
            impact_score=12.0,
        )

        DatoMetrica.objects.create(
            metrica=metrica,
            version='dos',
            vector_string='prueba',
            access_vector='acceso',
            access_complexity='complejidad',
            authentication='prueba',
            confidentiality_impact='impacto',
            integrity_impact='integridad',
            availability_impact='disponibilidad',
            base_score=7.0,
        )
    

        url = reverse('dato-metrica-api')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class SolucionVulnerabilidadTestCase(TestSetUp):

    def test_create_solucion_vulnerabilidad(self):
        vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-1999-0095',
            source_identifier= 'cve@mitre.org',
            published= '1988-10-01T04:00:00.000',
            last_modified= '2019-06-11T20:29:00.263',
            vuln_status= 'Modified'
        )

        url = reverse('solucion-vulnerabilidad-api')

        data = {
            'vulnerabilidad':  vulnerabilidad.uuid
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SolucionVulnerabilidad.objects.count(), 1)
        solucion = SolucionVulnerabilidad.objects.get()
        self.assertEqual(solucion.vulnerabilidad, vulnerabilidad)



    def test_list_solucion_vulnerabilidad(self):
        vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-1999-0095',
            source_identifier= 'cve@mitre.org',
            published= '1988-10-01T04:00:00.000',
            last_modified= '2019-06-11T20:29:00.263',
            vuln_status= 'Modified'
        )

        SolucionVulnerabilidad.objects.create(
            vulnerabilidad = vulnerabilidad
        )

        url = reverse('solucion-vulnerabilidad-api')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)