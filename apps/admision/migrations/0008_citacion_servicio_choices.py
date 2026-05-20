from django.db import migrations, models
import django.db.models.deletion


def migrar_servicios_citacion(apps, schema_editor):
    Servicio = apps.get_model("admision", "Servicio")
    CitacionDonante = apps.get_model("admision", "CitacionDonante")

    for citacion in CitacionDonante.objects.all():
        nombre = (citacion.servicio or "Sin servicio").strip() or "Sin servicio"
        servicio, _ = Servicio.objects.get_or_create(
            nombre=nombre,
            defaults={"descripcion": f"Servicio de {nombre.lower()}"},
        )
        citacion.servicio_ref_id = servicio.id
        citacion.save(update_fields=["servicio_ref"])


def normalizar_datos_citacion(apps, schema_editor):
    CitacionDonante = apps.get_model("admision", "CitacionDonante")
    tipos_validos = {"SANGRE_TOTAL", "GLOBULOS_ROJOS", "PLASMA", "PLAQUETAS", "CRIOPRECIPITADO"}

    for citacion in CitacionDonante.objects.all():
        update_fields = []
        codigo_normalizado = "".join(char for char in citacion.codigo_donante if char.isalnum())
        if codigo_normalizado and codigo_normalizado != citacion.codigo_donante:
            if CitacionDonante.objects.filter(codigo_donante=codigo_normalizado).exclude(pk=citacion.pk).exists():
                codigo_normalizado = f"{codigo_normalizado}{citacion.pk}"
            citacion.codigo_donante = codigo_normalizado
            update_fields.append("codigo_donante")

        if citacion.sala_cama:
            sala_normalizada = "".join(char if char.isalnum() or char.isspace() else " " for char in citacion.sala_cama)
            sala_normalizada = " ".join(sala_normalizada.split())
            if sala_normalizada != citacion.sala_cama:
                citacion.sala_cama = sala_normalizada
                update_fields.append("sala_cama")

        if citacion.tipo not in tipos_validos:
            citacion.tipo = "SANGRE_TOTAL"
            update_fields.append("tipo")

        if update_fields:
            citacion.save(update_fields=update_fields)


class Migration(migrations.Migration):

    dependencies = [
        ("admision", "0007_servicio_consentimiento_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="citaciondonante",
            name="servicio_ref",
            field=models.ForeignKey(
                blank=True,
                db_column="id_servicio",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="citaciones_donante",
                to="admision.servicio",
            ),
        ),
        migrations.RunPython(migrar_servicios_citacion, migrations.RunPython.noop),
        migrations.RunPython(normalizar_datos_citacion, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="citaciondonante",
            name="servicio",
        ),
        migrations.RenameField(
            model_name="citaciondonante",
            old_name="servicio_ref",
            new_name="servicio",
        ),
        migrations.AlterField(
            model_name="citaciondonante",
            name="servicio",
            field=models.ForeignKey(
                db_column="id_servicio",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="citaciones_donante",
                to="admision.servicio",
            ),
        ),
        migrations.AlterField(
            model_name="citaciondonante",
            name="grupo_factor",
            field=models.CharField(
                choices=[
                    ("A+", "A+"),
                    ("A-", "A-"),
                    ("B+", "B+"),
                    ("B-", "B-"),
                    ("AB+", "AB+"),
                    ("AB-", "AB-"),
                    ("O+", "O+"),
                    ("O-", "O-"),
                ],
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="citaciondonante",
            name="tipo",
            field=models.CharField(
                choices=[
                    ("SANGRE_TOTAL", "Sangre total"),
                    ("GLOBULOS_ROJOS", "Globulos rojos"),
                    ("PLASMA", "Plasma"),
                    ("PLAQUETAS", "Plaquetas"),
                    ("CRIOPRECIPITADO", "Crioprecipitado"),
                ],
                max_length=30,
            ),
        ),
    ]
