from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admision", "0005_alter_paciente_sexo"),
    ]

    operations = [
        migrations.RenameField(
            model_name="paciente",
            old_name="edad",
            new_name="edad_valor",
        ),
        migrations.RenameField(
            model_name="solicitudtransfusion",
            old_name="edad_paciente",
            new_name="edad_valor",
        ),
        migrations.AddField(
            model_name="paciente",
            name="edad_unidad",
            field=models.CharField(
                choices=[("DIAS", "Dias"), ("MESES", "Meses"), ("ANOS", "Anos")],
                default="ANOS",
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name="paciente",
            name="fecha_nacimiento",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="solicitudtransfusion",
            name="edad_unidad",
            field=models.CharField(
                choices=[("DIAS", "Dias"), ("MESES", "Meses"), ("ANOS", "Anos")],
                default="ANOS",
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name="solicitudtransfusion",
            name="fecha_nacimiento",
            field=models.DateField(blank=True, null=True),
        ),
    ]
