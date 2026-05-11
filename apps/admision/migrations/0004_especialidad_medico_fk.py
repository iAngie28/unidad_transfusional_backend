# Generated manually to convert Medico.especialidad from text to FK.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrar_especialidades(apps, schema_editor):
    Especialidad = apps.get_model("admision", "Especialidad")
    Medico = apps.get_model("admision", "Medico")

    for medico in Medico.objects.all():
        nombre = (medico.especialidad or "Sin especialidad").strip() or "Sin especialidad"
        especialidad, _ = Especialidad.objects.get_or_create(
            nombre=nombre,
            defaults={"descripcion": f"Especialidad de {nombre.lower()}"},
        )
        medico.especialidad_ref_id = especialidad.id
        medico.save(update_fields=["especialidad_ref"])


class Migration(migrations.Migration):

    dependencies = [
        ("admision", "0003_remove_pago_id_transfusion"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Especialidad",
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
                "verbose_name": "Especialidad",
                "verbose_name_plural": "Especialidades",
                "ordering": ["nombre"],
            },
        ),
        migrations.AddField(
            model_name="medico",
            name="especialidad_ref",
            field=models.ForeignKey(
                blank=True,
                db_column="id_especialidad",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="medicos",
                to="admision.especialidad",
            ),
        ),
        migrations.RunPython(migrar_especialidades, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="medico",
            name="especialidad",
        ),
        migrations.RenameField(
            model_name="medico",
            old_name="especialidad_ref",
            new_name="especialidad",
        ),
        migrations.AlterField(
            model_name="medico",
            name="especialidad",
            field=models.ForeignKey(
                db_column="id_especialidad",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="medicos",
                to="admision.especialidad",
            ),
        ),
    ]
