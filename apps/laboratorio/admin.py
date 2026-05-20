from django.contrib import admin

from apps.laboratorio.models import (
    PruebaPretransfusionalPAC,
    PruebasPretransfHema,
    Reaccion,
    Transfusion,
)


@admin.register(PruebaPretransfusionalPAC)
class PruebaPretransfusionalPACAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha_hora", "paciente", "solicitud", "user", "resultado")
    search_fields = ("paciente__ci", "paciente__nombre", "solicitud__nro", "user__username", "resultado")
    list_filter = ("resultado", "fecha_hora")
    autocomplete_fields = ("paciente", "solicitud", "user")


@admin.register(PruebasPretransfHema)
class PruebasPretransfHemaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "hemocomponente", "solicitud", "user", "cruzada_mayor", "cruzada_menor")
    search_fields = ("hemocomponente__nro_bolsa", "solicitud__nro", "user__username")
    list_filter = ("fecha",)
    autocomplete_fields = ("hemocomponente", "solicitud", "user")


@admin.register(Transfusion)
class TransfusionAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "hemocomponente", "user", "servicio", "hora_inicio", "hora_fin", "fraccionado", "ml")
    search_fields = ("paciente__ci", "paciente__nombre", "hemocomponente__nro_bolsa", "user__username", "servicio__nombre")
    list_filter = ("servicio", "fraccionado", "hora_inicio")
    autocomplete_fields = ("paciente", "hemocomponente", "user", "servicio")


@admin.register(Reaccion)
class ReaccionAdmin(admin.ModelAdmin):
    list_display = ("id", "transfusion", "fecha_hora")
    search_fields = ("=transfusion__id", "transfusion__paciente__ci", "descripcion")
    list_filter = ("fecha_hora",)
    autocomplete_fields = ("transfusion",)
