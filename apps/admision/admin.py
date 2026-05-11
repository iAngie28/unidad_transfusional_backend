from django.contrib import admin

from apps.admision.models import (
    CitacionDonante,
    ConsentimientoInformado,
    Medico,
    Paciente,
    Pago,
    SolicitudTransfusion,
)


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = (
        "ci",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "edad",
        "sexo",
        "historia_clinica",
        "grupo_sanguineo",
    )
    search_fields = ("ci", "nombre", "apellido_paterno", "apellido_materno", "historia_clinica")
    list_filter = ("sexo", "grupo_sanguineo")


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
    search_fields = ("nombre", "apellido_paterno", "apellido_materno", "especialidad", "matricula_profesional")
    list_filter = ("especialidad",)


@admin.register(SolicitudTransfusion)
class SolicitudTransfusionAdmin(admin.ModelAdmin):
    list_display = (
        "nro",
        "fecha",
        "hora",
        "paciente",
        "medico",
        "user",
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
    search_fields = ("solicitud__nro", "servicio", "nombre_familiar", "apellido_paterno_familiar", "ci")
    list_filter = ("fecha", "servicio")
    autocomplete_fields = ("solicitud",)


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
    search_fields = ("solicitud__nro", "codigo_donante", "servicio", "grupo_factor", "tipo")
    list_filter = ("fecha", "servicio", "grupo_factor", "tipo")
    autocomplete_fields = ("solicitud", "user")


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "estado", "es_sus", "citacion", "transfusion", "created_at")
    search_fields = ("citacion__codigo_donante", "citacion__solicitud__nro", "estado")
    list_filter = ("estado", "es_sus")
    autocomplete_fields = ("citacion", "transfusion")
