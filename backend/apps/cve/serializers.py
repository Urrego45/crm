from rest_framework import serializers
from .models import (
    Vulnerabilidad,
    SolucionVulnerabilidad,
    Descripcion,
    Metrica,
    DatoMetrica
)
from django.db.models import Count


class VulnerabilidadListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Vulnerabilidad
        fields = [
            'uuid',
            'cve_id',
            'source_identifier',
            'published',
            'last_modified',
            'vuln_status',
        ]


class SolucionVulnerabilidadCreateSerializer(serializers.ModelSerializer):
    vulnerabilidad = serializers.SlugRelatedField(queryset=Vulnerabilidad.objects.all(), slug_field='uuid')
    class Meta:
        model= SolucionVulnerabilidad
        fields = [
            'vulnerabilidad',
        ]



class SolucionVulnerabilidadListSerializer(serializers.ModelSerializer):
    vulnerabilidad = VulnerabilidadListCreateSerializer()
    class Meta:
        model= SolucionVulnerabilidad
        fields = [
            'uuid',
            'vulnerabilidad',
            'fecha_solucion'
        ]


class DescripcionListSerializer(serializers.ModelSerializer):
    vulnerabilidad = VulnerabilidadListCreateSerializer()

    class Meta:
        model = Descripcion
        fields = [
            'uuid',
            'vulnerabilidad',
            'lang',
            'value',
        ]


class DatoMetricatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatoMetrica
        fields = [
            'uuid',
            'version',
            'vector_string',
            'access_vector',
            'access_complexity',
            'authentication',
            'confidentiality_impact',
            'integrity_impact',
            'availability_impact',
            'base_score',
        ]

class MetricaListSerializer(serializers.ModelSerializer):
    vulnerabilidad = VulnerabilidadListCreateSerializer()
    metricas_datos_metricas = DatoMetricatSerializer(many=True)


    class Meta:
        model = Metrica
        fields = [
            'uuid',
            'vulnerabilidad',
            'source',
            'type',
            'base_severity',
            'exploitability_score',
            'impact_score',
            'metricas_datos_metricas'
        ]

class DatoMetricaListSerializer(serializers.ModelSerializer):
    metrica = MetricaListSerializer()
    class Meta:
        model = DatoMetrica
        fields = [
            'uuid',
            'metrica',
            'version',
            'vector_string',
            'access_vector',
            'access_complexity',
            'authentication',
            'confidentiality_impact',
            'integrity_impact',
            'availability_impact',
            'base_score',
        ]


class VulnerabilidadCompletaListCreateSerializer(serializers.ModelSerializer):
    descripciones_vulnerabilidades = DescripcionListSerializer(many=True)
    metricas_vulnerabilidades = MetricaListSerializer(
        DatoMetricaListSerializer(),
        many=True
    )

    class Meta:
        model= Vulnerabilidad
        fields = [
            'uuid',
            'cve_id',
            'source_identifier',
            'published',
            'last_modified',
            'vuln_status',
            'descripciones_vulnerabilidades',
            'metricas_vulnerabilidades',
        ]

class VulnerabilidadSeveridadListSerializer(serializers.ModelSerializer):
    def get_conteo():

        return (
            Metrica.objects.values('base_severity').annotate(cantidad=Count('uuid')).order_by('base_severity')
        )