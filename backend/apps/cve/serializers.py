from rest_framework import serializers
from .models import (
    Vulnerabilidad,
    SolucionVulnerabilidad,
    Descripcion,
    Metrica,
    DatoMetrica
)


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


class DescripcionSinSolucionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Descripcion
        fields = [
            'uuid',
            'lang',
            'value',
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

class MetricaSinSolucionListSerializer(serializers.ModelSerializer):
    metricas_datos_metricas = DatoMetricatSerializer(many=True)


    class Meta:
        model = Metrica
        fields = [
            'uuid',
            'source',
            'type',
            'base_severity',
            'exploitability_score',
            'impact_score',
            'metricas_datos_metricas'
        ]

class MetricaListSerializer(serializers.ModelSerializer):
    vulnerabilidad = VulnerabilidadListCreateSerializer()

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
    descripciones_vulnerabilidades = DescripcionSinSolucionListSerializer(many=True)
    metricas_vulnerabilidades = MetricaSinSolucionListSerializer(
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
