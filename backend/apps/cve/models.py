from django_extensions.db.models import TimeStampedModel
from django.db import models
import uuid


class Vulnerabilidad(TimeStampedModel):

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    cve_id = models.CharField(
        verbose_name="ID CVE",
        max_length=50
    )

    source_identifier = models.CharField(
        verbose_name="Identificador",
        max_length=50
    )

    published = models.CharField(
        verbose_name="Publicación",
        max_length=50
    )

    last_modified = models.CharField(
        verbose_name="Última modificación",
        max_length=50
    )

    vuln_status = models.CharField(
        verbose_name="Status",
        max_length=50
    )


    class Meta:
        verbose_name = "Vulnerabilidad"
        verbose_name_plural = "Vulnerabilidades"


class SolucionVulnerabilidad(TimeStampedModel):

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    vulnerabilidad = models.ForeignKey(
        Vulnerabilidad,
        on_delete=models.CASCADE,
        related_name='solucion_vulnerabilidad_vulnerabilidad',
        verbose_name="vulnerabilidad",
    )

    fecha_solucion = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        verbose_name = "Vulnerabilidad solucionada"
        verbose_name_plural = "Vulnerabilidades solucionadas"


class Descripcion(TimeStampedModel):

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    vulnerabilidad = models.ForeignKey(
        Vulnerabilidad,
        on_delete=models.CASCADE,
        related_name='descripcion_vulnerabilidad',
        verbose_name="vulnerabilidad",
    )

    lang = models.CharField(
        verbose_name="Lenguaje",
        max_length=5
    )

    value = models.TextField(
        verbose_name="Descripción"
    )

    class Meta:
        verbose_name = "Descripción"
        verbose_name_plural = "Descripciones"


class Metrica(TimeStampedModel):

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    vulnerabilidad = models.ForeignKey(
        Vulnerabilidad,
        on_delete=models.CASCADE,
        related_name='metrica_vulnerabilidad',
        verbose_name="vulnerabilidad",
    )

    source = models.CharField(
        verbose_name="Fuente",
        max_length=30
    )

    type = models.CharField(
        verbose_name="Tipo de metrica",
        max_length=15
    )

    base_severity = models.CharField(
        verbose_name="Severidad",
        max_length=50
    )

    exploitability_score = models.PositiveSmallIntegerField(
        verbose_name="Puntos de exploit",
    )

    impact_score = models.PositiveSmallIntegerField(
        verbose_name="Puntos de impacto",
    )

    class Meta:
        verbose_name = "Metrica"
        verbose_name_plural = "Metricas"


class DatoMetrica(TimeStampedModel):

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    metrica = models.ForeignKey(
        Metrica,
        on_delete=models.CASCADE,
        related_name='metrica_datos_metrica',
        verbose_name="metrica",
    )

    version = models.CharField(
        verbose_name="Versión",
        max_length=10
    )

    vector_string = models.TextField(
        verbose_name="Vector",
    )

    access_vector = models.CharField(
        verbose_name="Acceso al vector",
        max_length=30
    )

    access_complexity = models.CharField(
        verbose_name="Complejidad del acceso",
        max_length=15
    )

    authentication = models.CharField(
        verbose_name="Autenticación",
        max_length=20
    )

    confidentiality_impact = models.CharField(
        verbose_name="Confidencialidad del impacto",
        max_length=30
    )

    integrity_impact = models.CharField(
        verbose_name="Integridad del impacto",
        max_length=30
    )

    availability_impact = models.CharField(
        verbose_name="Disponibilidad del impacto",
        max_length=30
    )

    base_score = models.SmallIntegerField(
        verbose_name="Puntuacion base",
    )

    class Meta:
        verbose_name = "Dato de la metrica"
        verbose_name_plural = "Datos de las metricas"
