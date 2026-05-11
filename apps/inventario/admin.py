from django.contrib import admin

from apps.inventario.models import Descarte, Hemocomponente, Trazabilidad


@admin.register(Hemocomponente)
class HemocomponenteAdmin(admin.ModelAdmin):
    list_display = (
        "nro_bolsa",
        "nro_tubuladura",
        "tipo",
        "grupo_sanguineo",
        "estado",
        "fecha_ingreso",
        "fecha_vencimiento",
        "devuelto",
    )
    search_fields = ("nro_bolsa", "nro_tubuladura", "tipo", "grupo_sanguineo", "estado")
    list_filter = ("tipo", "grupo_sanguineo", "estado", "devuelto")


@admin.register(Trazabilidad)
class TrazabilidadAdmin(admin.ModelAdmin):
    list_display = ("id", "hemocomponente", "evento", "encargado", "fecha_hora")
    search_fields = ("hemocomponente__nro_bolsa", "evento", "encargado__username")
    list_filter = ("evento", "fecha_hora")
    autocomplete_fields = ("hemocomponente", "encargado")


@admin.register(Descarte)
class DescarteAdmin(admin.ModelAdmin):
    list_display = ("id", "hemocomponente", "tipo_accion", "fecha_hora")
    search_fields = ("hemocomponente__nro_bolsa", "tipo_accion", "motivo")
    list_filter = ("tipo_accion", "fecha_hora")
    autocomplete_fields = ("hemocomponente",)
