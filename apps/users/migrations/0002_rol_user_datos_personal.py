# Generated manually to migrate the legacy text role into the Rol table.

from django.db import migrations, models
import django.db.models.deletion


def crear_roles_y_migrar_usuarios(apps, schema_editor):
    Rol = apps.get_model("users", "Rol")
    User = apps.get_model("users", "User")

    roles_base = {
        "BIOQUIMICO": "Bioquimico",
        "JEFE_UNIDAD": "Jefe de Unidad",
    }
    for nombre, descripcion in roles_base.items():
        Rol.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})

    legacy_map = {
        "BIOQUIMICO": "BIOQUIMICO",
        "JEFE_UNIDAD": "JEFE_UNIDAD",
    }
    for usuario in User.objects.all():
        legacy_role = getattr(usuario, "role", None) or "BIOQUIMICO"
        rol_nombre = legacy_map.get(legacy_role, legacy_role)
        rol, _ = Rol.objects.get_or_create(
            nombre=rol_nombre,
            defaults={"descripcion": roles_base.get(rol_nombre, rol_nombre)},
        )
        usuario.rol_id = rol.id
        usuario.save(update_fields=["rol"])


def restaurar_role_texto(apps, schema_editor):
    User = apps.get_model("users", "User")

    for usuario in User.objects.select_related("rol").all():
        if usuario.rol_id and usuario.rol.nombre == "JEFE_UNIDAD":
            usuario.role = "JEFE_UNIDAD"
        elif usuario.rol_id:
            usuario.role = usuario.rol.nombre
        else:
            usuario.role = "BIOQUIMICO"
        usuario.save(update_fields=["role"])


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rol",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("descripcion", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "permisos",
                    models.ManyToManyField(
                        blank=True,
                        related_name="roles_personalizados",
                        to="auth.permission",
                    ),
                ),
            ],
            options={
                "verbose_name": "Rol",
                "verbose_name_plural": "Roles",
                "ordering": ["nombre"],
            },
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=150, verbose_name="Nombre"),
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "Usuario", "verbose_name_plural": "Usuarios"},
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=150, verbose_name="Apellido paterno"),
        ),
        migrations.AddField(
            model_name="user",
            name="apellido_materno",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="telefono",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="rol",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="usuarios",
                to="users.rol",
            ),
        ),
        migrations.RunPython(crear_roles_y_migrar_usuarios, restaurar_role_texto),
        migrations.RemoveField(
            model_name="user",
            name="role",
        ),
    ]
