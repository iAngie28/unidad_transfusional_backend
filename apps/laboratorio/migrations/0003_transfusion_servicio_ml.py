from django.db import migrations, models
import django.db.models.deletion


def migrate_servicio_to_fk(apps, schema_editor):
    Servicio = apps.get_model("admision", "Servicio")
    Transfusion = apps.get_model("laboratorio", "Transfusion")

    for transfusion in Transfusion.objects.all():
        nombre = (transfusion.servicio or "").strip() or "Sin servicio"
        servicio, _ = Servicio.objects.get_or_create(nombre=nombre)
        transfusion.servicio_ref = servicio
        transfusion.save(update_fields=["servicio_ref"])


class Migration(migrations.Migration):

    dependencies = [
        ("admision", "0008_citacion_servicio_choices"),
        ("laboratorio", "0002_alter_pruebapretransfusionalpac_resultado"),
    ]

    operations = [
        migrations.AddField(
            model_name="transfusion",
            name="ml",
            field=models.PositiveSmallIntegerField(default=1000),
        ),
        migrations.AddField(
            model_name="transfusion",
            name="servicio_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="transfusiones_migracion",
                to="admision.servicio",
            ),
        ),
        migrations.RunPython(migrate_servicio_to_fk, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="transfusion",
            name="servicio",
        ),
        migrations.RenameField(
            model_name="transfusion",
            old_name="servicio_ref",
            new_name="servicio",
        ),
        migrations.AlterField(
            model_name="transfusion",
            name="servicio",
            field=models.ForeignKey(
                db_column="id_servicio",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="transfusiones",
                to="admision.servicio",
            ),
        ),
        migrations.AlterField(
            model_name="transfusion",
            name="grupo_cabecera_h",
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
    ]
