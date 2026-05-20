from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrar_servicios(apps, schema_editor):
    Servicio = apps.get_model("admision", "Servicio")
    ConsentimientoInformado = apps.get_model("admision", "ConsentimientoInformado")

    for consentimiento in ConsentimientoInformado.objects.all():
        nombre = (consentimiento.servicio or "Sin servicio").strip() or "Sin servicio"
        servicio, _ = Servicio.objects.get_or_create(
            nombre=nombre,
            defaults={"descripcion": f"Servicio de {nombre.lower()}"},
        )
        consentimiento.servicio_ref_id = servicio.id
        consentimiento.save(update_fields=["servicio_ref"])


class Migration(migrations.Migration):

    dependencies = [
        ("admision", "0006_edad_valor_unidad_fecha_nacimiento"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Servicio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("nombre", models.CharField(max_length=120, unique=True)),
                ("descripcion", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Servicio",
                "verbose_name_plural": "Servicios",
                "ordering": ["nombre"],
            },
        ),
        migrations.AddField(
            model_name="consentimientoinformado",
            name="servicio_ref",
            field=models.ForeignKey(
                blank=True,
                db_column="id_servicio",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="consentimientos",
                to="admision.servicio",
            ),
        ),
        migrations.RunPython(migrar_servicios, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="consentimientoinformado",
            name="servicio",
        ),
        migrations.RenameField(
            model_name="consentimientoinformado",
            old_name="servicio_ref",
            new_name="servicio",
        ),
        migrations.AlterField(
            model_name="consentimientoinformado",
            name="servicio",
            field=models.ForeignKey(
                db_column="id_servicio",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="consentimientos",
                to="admision.servicio",
            ),
        ),
    ]
