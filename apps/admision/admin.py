from django.contrib import admin

from apps.admision.models import (
    CitacionDonante,
    ConsentimientoInformado,
    Especialidad,
    Medico,
    Paciente,
    Pago,
    Servicio,
    SolicitudTransfusion,
)


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre", "descripcion")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre", "descripcion")


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = (
        "ci",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "edad_valor",
        "edad_unidad",
        "fecha_nacimiento",
        "sexo",
        "historia_clinica",
        "grupo_sanguineo",
    )
    search_fields = ("ci", "nombre", "apellido_paterno", "apellido_materno", "historia_clinica")
    list_filter = ("edad_unidad", "sexo", "grupo_sanguineo")


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "especialidad",
        "matricula_profesional",
    )
    search_fields = (
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "especialidad__nombre",
        "matricula_profesional",
    )
    list_filter = ("especialidad",)
    autocomplete_fields = ("especialidad",)


@admin.register(SolicitudTransfusion)
class SolicitudTransfusionAdmin(admin.ModelAdmin):
    list_display = (
        "nro",
        "fecha",
        "hora",
        "paciente",
        "medico",
        "user",
        "edad_valor",
        "edad_unidad",
        "hemocomponente",
        "cantidad",
        "tipo_urgencia",
    )
    search_fields = ("nro", "paciente__ci", "paciente__nombre", "medico__nombre", "diagnostico")
    list_filter = ("fecha", "hemocomponente", "tipo_urgencia", "grupo")
    autocomplete_fields = ("paciente", "medico", "user")


@admin.register(ConsentimientoInformado)
class ConsentimientoInformadoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "solicitud",
        "fecha",
        "servicio",
        "nombre_familiar",
        "apellido_paterno_familiar",
        "telefono",
        "ci",
    )
    search_fields = ("solicitud__nro", "servicio__nombre", "nombre_familiar", "apellido_paterno_familiar", "ci")
    list_filter = ("fecha", "servicio")
    autocomplete_fields = ("solicitud", "servicio")


@admin.register(CitacionDonante)
class CitacionDonanteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "solicitud",
        "codigo_donante",
        "fecha",
        "hora",
        "servicio",
        "cantidad",
        "grupo_factor",
        "tipo",
        "user",
    )
    list_filter = ("fecha", "servicio", "grupo_factor", "tipo")
    search_fields = ("solicitud__nro", "codigo_donante", "servicio__nombre", "grupo_factor", "tipo")
    autocomplete_fields = ("solicitud", "servicio", "user")


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "estado", "es_sus", "citacion", "transfusion", "created_at")
    search_fields = ("citacion__codigo_donante", "citacion__solicitud__nro", "estado")
    list_filter = ("estado", "es_sus")
    autocomplete_fields = ("citacion", "transfusion")
