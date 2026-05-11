from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.admision.models import (
    CitacionDonante,
    ConsentimientoInformado,
    Medico,
    Paciente,
    Pago,
    SolicitudTransfusion,
)
from apps.inventario.models import Descarte, Hemocomponente, Trazabilidad
from apps.laboratorio.models import (
    PruebaPretransfusionalPAC,
    PruebasPretransfHema,
    Reaccion,
    Transfusion,
)
from apps.users.models import Rol

User = get_user_model()


class Command(BaseCommand):
    help = "Carga datos iniciales de prueba para la Unidad Transfusional"

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando carga de datos...")

        roles = self.crear_roles()
        usuarios = self.crear_usuarios(roles)
        admision = self.crear_admision(usuarios)
        inventario = self.crear_inventario(usuarios)
        laboratorio = self.crear_laboratorio(usuarios, admision, inventario)
        self.crear_pagos(usuarios, admision, laboratorio)

        self.stdout.write(self.style.SUCCESS("Seeder ejecutado con exito."))

    def crear_roles(self):
        self.stdout.write("- Creando roles...")
        roles_data = {
            "BIOQUIMICO": "Bioquimico",
            "JEFE_UNIDAD": "Jefe de Unidad",
        }
        roles = {}
        for nombre, descripcion in roles_data.items():
            rol, _ = Rol.objects.update_or_create(
                nombre=nombre,
                defaults={"descripcion": descripcion},
            )
            roles[nombre] = rol

        User.objects.filter(rol__nombre="ADMINISTRADOR").update(rol=roles["JEFE_UNIDAD"])
        User.objects.filter(rol__nombre="TECNICO").update(rol=roles["BIOQUIMICO"])
        Rol.objects.filter(nombre__in=["ADMINISTRADOR", "TECNICO"]).delete()

        return roles

    def crear_usuarios(self, roles):
        self.stdout.write("- Creando usuarios...")
        usuarios_data = [
            {
                "username": "bio01",
                "password": "password123",
                "first_name": "Juan",
                "last_name": "Bioquimico",
                "apellido_materno": "Mendez",
                "email": "bio01@example.com",
                "telefono": "70000001",
                "rol": roles["BIOQUIMICO"],
                "is_staff": True,
            },
            {
                "username": "jefe01",
                "password": "password123",
                "first_name": "Ana",
                "last_name": "Jefa",
                "apellido_materno": "Paredes",
                "email": "jefe01@example.com",
                "telefono": "70000003",
                "rol": roles["JEFE_UNIDAD"],
                "is_staff": True,
            },
        ]

        usuarios = {}
        for data in usuarios_data:
            password = data.pop("password")
            username = data.pop("username")
            user, _ = User.objects.update_or_create(
                username=username,
                defaults={**data, "is_active": True},
            )
            user.set_password(password)
            user.save()
            usuarios[username] = user
        return usuarios

    def crear_admision(self, usuarios):
        self.stdout.write("- Creando datos de admision...")
        bio = usuarios["bio01"]
        now = timezone.localtime()
        hora_actual = now.time().replace(tzinfo=None)
        hora_menos_1 = (now - timedelta(hours=1)).time().replace(tzinfo=None)
        hora_menos_2 = (now - timedelta(hours=2)).time().replace(tzinfo=None)

        pacientes_data = [
            {
                "ci": "12345678",
                "nombre": "Carlos",
                "apellido_paterno": "Gomez",
                "apellido_materno": "Vargas",
                "edad": 36,
                "sexo": "M",
                "historia_clinica": "HC-001",
                "grupo_sanguineo": "A+",
            },
            {
                "ci": "87654321",
                "nombre": "Maria",
                "apellido_paterno": "Rodriguez",
                "apellido_materno": "Lopez",
                "edad": 29,
                "sexo": "F",
                "historia_clinica": "HC-002",
                "grupo_sanguineo": "O-",
            },
            {
                "ci": "11223344",
                "nombre": "Pedro",
                "apellido_paterno": "Suarez",
                "apellido_materno": "Molina",
                "edad": 58,
                "sexo": "M",
                "historia_clinica": "HC-003",
                "grupo_sanguineo": "B+",
            },
        ]

        pacientes = {}
        for data in pacientes_data:
            paciente, _ = Paciente.objects.update_or_create(
                ci=data["ci"],
                defaults={**data, "created_by": bio},
            )
            pacientes[paciente.ci] = paciente

        medicos_data = [
            {
                "matricula_profesional": "MP-001",
                "nombre": "Elena",
                "apellido_paterno": "Paredes",
                "apellido_materno": "Rojas",
                "especialidad": "Medicina Interna",
            },
            {
                "matricula_profesional": "MP-002",
                "nombre": "Marco",
                "apellido_paterno": "Rivera",
                "apellido_materno": "Soto",
                "especialidad": "Cirugia",
            },
        ]

        medicos = {}
        for data in medicos_data:
            medico, _ = Medico.objects.update_or_create(
                matricula_profesional=data["matricula_profesional"],
                defaults={**data, "created_by": bio},
            )
            medicos[medico.matricula_profesional] = medico

        solicitudes_data = [
            {
                "nro": "SOL-001",
                "fecha": now.date(),
                "hora": hora_actual,
                "edad_paciente": 36,
                "hto": 28.5,
                "hb": 8.7,
                "grupo": "A+",
                "hemocomponente": "GLOBULOS_ROJOS",
                "cantidad": 2,
                "tipo_urgencia": "URGENTE",
                "diagnostico": "Anemia severa",
                "user": bio,
                "paciente": pacientes["12345678"],
                "medico": medicos["MP-001"],
            },
            {
                "nro": "SOL-002",
                "fecha": (now - timedelta(days=1)).date(),
                "hora": hora_menos_2,
                "edad_paciente": 29,
                "hto": 31.2,
                "hb": 9.4,
                "grupo": "O-",
                "hemocomponente": "PLASMA",
                "cantidad": 1,
                "tipo_urgencia": "RUTINA",
                "diagnostico": "Preparacion preoperatoria",
                "user": bio,
                "paciente": pacientes["87654321"],
                "medico": medicos["MP-002"],
            },
        ]

        solicitudes = {}
        for data in solicitudes_data:
            solicitud, _ = SolicitudTransfusion.objects.update_or_create(
                nro=data["nro"],
                defaults={**data, "created_by": bio},
            )
            solicitudes[solicitud.nro] = solicitud

        ConsentimientoInformado.objects.update_or_create(
            solicitud=solicitudes["SOL-001"],
            ci="99887766",
            defaults={
                "fecha": now.date(),
                "servicio": "Medicina Interna",
                "nombre_familiar": "Rosa",
                "apellido_paterno_familiar": "Gomez",
                "apellido_materno_familiar": "Vargas",
                "telefono": "71000001",
                "created_by": bio,
            },
        )
        ConsentimientoInformado.objects.update_or_create(
            solicitud=solicitudes["SOL-002"],
            ci="88776655",
            defaults={
                "fecha": (now - timedelta(days=1)).date(),
                "servicio": "Cirugia",
                "nombre_familiar": "Andres",
                "apellido_paterno_familiar": "Rodriguez",
                "apellido_materno_familiar": "Lopez",
                "telefono": "71000002",
                "created_by": bio,
            },
        )

        citaciones = {}
        citaciones_data = [
            {
                "codigo_donante": "DON-001",
                "solicitud": solicitudes["SOL-001"],
                "user": bio,
                "fecha": now.date(),
                "servicio": "Medicina Interna",
                "sala_cama": "Sala 2 - Cama 4",
                "cantidad": 2,
                "hora": hora_actual,
                "grupo_factor": "A+",
                "tipo": "Reposicion",
            },
            {
                "codigo_donante": "DON-002",
                "solicitud": solicitudes["SOL-002"],
                "user": bio,
                "fecha": (now - timedelta(days=1)).date(),
                "servicio": "Cirugia",
                "sala_cama": "Sala 1 - Cama 8",
                "cantidad": 1,
                "hora": hora_menos_1,
                "grupo_factor": "O-",
                "tipo": "Programada",
            },
        ]
        for data in citaciones_data:
            citacion, _ = CitacionDonante.objects.update_or_create(
                codigo_donante=data["codigo_donante"],
                defaults={**data, "created_by": bio},
            )
            citaciones[citacion.codigo_donante] = citacion

        return {
            "pacientes": pacientes,
            "medicos": medicos,
            "solicitudes": solicitudes,
            "citaciones": citaciones,
        }

    def crear_inventario(self, usuarios):
        self.stdout.write("- Creando datos de inventario...")
        bio = usuarios["bio01"]
        jefe = usuarios["jefe01"]
        now = timezone.localtime()

        bolsas_data = [
            {
                "nro_bolsa": "BOL-001",
                "nro_tubuladura": "TUB-001",
                "tipo": "GLOBULOS_ROJOS",
                "grupo_sanguineo": "A+",
                "estado": "TRANSFUNDIDO",
                "fecha_ingreso": now - timedelta(days=3),
                "fecha_vencimiento": now + timedelta(days=32),
                "devuelto": False,
            },
            {
                "nro_bolsa": "BOL-002",
                "nro_tubuladura": "TUB-002",
                "tipo": "PLASMA",
                "grupo_sanguineo": "O-",
                "estado": "DISPONIBLE",
                "fecha_ingreso": now - timedelta(days=2),
                "fecha_vencimiento": now + timedelta(days=180),
                "devuelto": False,
            },
            {
                "nro_bolsa": "BOL-003",
                "nro_tubuladura": "TUB-003",
                "tipo": "PLAQUETAS",
                "grupo_sanguineo": "B+",
                "estado": "DESCARTADO",
                "fecha_ingreso": now - timedelta(days=7),
                "fecha_vencimiento": now - timedelta(days=1),
                "devuelto": False,
            },
        ]

        bolsas = {}
        for data in bolsas_data:
            bolsa, _ = Hemocomponente.objects.update_or_create(
                nro_bolsa=data["nro_bolsa"],
                defaults={**data, "created_by": bio},
            )
            bolsas[bolsa.nro_bolsa] = bolsa

        trazas_data = [
            ("BOL-001", "INGRESO", bio, now - timedelta(days=3)),
            ("BOL-001", "DESPACHO", bio, now - timedelta(hours=4)),
            ("BOL-002", "INGRESO", bio, now - timedelta(days=2)),
            ("BOL-003", "INGRESO", bio, now - timedelta(days=7)),
            ("BOL-003", "DESCARTE", jefe, now - timedelta(hours=6)),
        ]
        for nro_bolsa, evento, encargado, fecha_hora in trazas_data:
            Trazabilidad.objects.update_or_create(
                hemocomponente=bolsas[nro_bolsa],
                evento=evento,
                defaults={
                    "encargado": encargado,
                    "fecha_hora": fecha_hora,
                    "created_by": encargado,
                },
            )

        Descarte.objects.update_or_create(
            hemocomponente=bolsas["BOL-003"],
            defaults={
                "tipo_accion": "VENCIMIENTO",
                "motivo": "Bolsa vencida durante control de stock.",
                "fecha_hora": now - timedelta(hours=6),
                "created_by": bio,
            },
        )

        return {"bolsas": bolsas}

    def crear_laboratorio(self, usuarios, admision, inventario):
        self.stdout.write("- Creando datos de laboratorio...")
        bio = usuarios["bio01"]
        now = timezone.localtime()
        pacientes = admision["pacientes"]
        solicitudes = admision["solicitudes"]
        bolsas = inventario["bolsas"]

        PruebaPretransfusionalPAC.objects.update_or_create(
            solicitud=solicitudes["SOL-001"],
            paciente=pacientes["12345678"],
            defaults={
                "fecha_hora": now - timedelta(hours=5),
                "user": bio,
                "anti_a": "POSITIVO",
                "anti_b": "NEGATIVO",
                "anti_ab": "POSITIVO",
                "anti_d": "POSITIVO",
                "control_rhesus": "Valido",
                "alfa": "Negativo",
                "beta": "Positivo",
                "o": "Negativo",
                "fenotipo": "A Rh+",
                "hto": 28.5,
                "hb": 8.7,
                "coombs_directo": "Negativo",
                "resultado": "APTO",
                "created_by": bio,
            },
        )
        PruebaPretransfusionalPAC.objects.update_or_create(
            solicitud=solicitudes["SOL-002"],
            paciente=pacientes["87654321"],
            defaults={
                "fecha_hora": now - timedelta(hours=3),
                "user": bio,
                "anti_a": "NEGATIVO",
                "anti_b": "NEGATIVO",
                "anti_ab": "NEGATIVO",
                "anti_d": "NEGATIVO",
                "control_rhesus": "Valido",
                "alfa": "Positivo",
                "beta": "Positivo",
                "o": "Negativo",
                "fenotipo": "O Rh-",
                "hto": 31.2,
                "hb": 9.4,
                "coombs_directo": "Negativo",
                "resultado": "PENDIENTE",
                "created_by": bio,
            },
        )

        PruebasPretransfHema.objects.update_or_create(
            solicitud=solicitudes["SOL-001"],
            hemocomponente=bolsas["BOL-001"],
            defaults={
                "fecha": now - timedelta(hours=4),
                "salina": "Compatible",
                "albumina": "Compatible",
                "liss": "Compatible",
                "coombs": "Negativo",
                "cruzada_mayor": "Compatible",
                "cruzada_menor": "Compatible",
                "hemolisis": "No",
                "anti_a": "POSITIVO",
                "anti_b": "NEGATIVO",
                "anti_ab": "POSITIVO",
                "anti_d": "POSITIVO",
                "celula_a": "Negativo",
                "celula_b": "Positivo",
                "celula_o": "Negativo",
                "fenotipo": "A Rh+",
                "user": bio,
                "created_by": bio,
            },
        )
        PruebasPretransfHema.objects.update_or_create(
            solicitud=solicitudes["SOL-002"],
            hemocomponente=bolsas["BOL-002"],
            defaults={
                "fecha": now - timedelta(hours=2),
                "salina": "Pendiente",
                "albumina": "Pendiente",
                "liss": "Pendiente",
                "coombs": "No realizado",
                "cruzada_mayor": "Pendiente",
                "cruzada_menor": "Pendiente",
                "hemolisis": "No realizado",
                "anti_a": "NO_REALIZADO",
                "anti_b": "NO_REALIZADO",
                "anti_ab": "NO_REALIZADO",
                "anti_d": "NO_REALIZADO",
                "celula_a": "No realizado",
                "celula_b": "No realizado",
                "celula_o": "No realizado",
                "fenotipo": "Pendiente",
                "user": bio,
                "created_by": bio,
            },
        )

        transfusion, _ = Transfusion.objects.update_or_create(
            hemocomponente=bolsas["BOL-001"],
            paciente=pacientes["12345678"],
            defaults={
                "servicio": "Medicina Interna",
                "diagnostico": "Anemia severa",
                "ate_trans_alerg": False,
                "grupo_cabecera_h": "A+",
                "hora_inicio": now - timedelta(hours=3),
                "hora_fin": now - timedelta(hours=1),
                "fraccionado": False,
                "user": bio,
                "created_by": bio,
            },
        )

        Reaccion.objects.update_or_create(
            transfusion=transfusion,
            defaults={
                "descripcion": "Sin reaccion adversa reportada durante observacion.",
                "fecha_hora": now - timedelta(minutes=45),
                "created_by": bio,
            },
        )

        return {"transfusion": transfusion}

    def crear_pagos(self, usuarios, admision, laboratorio):
        self.stdout.write("- Creando pagos...")
        bio = usuarios["bio01"]
        citaciones = admision["citaciones"]
        transfusion = laboratorio["transfusion"]

        Pago.objects.update_or_create(
            citacion=citaciones["DON-001"],
            defaults={
                "estado": "EXENTO",
                "es_sus": True,
                "transfusion": transfusion,
                "created_by": bio,
            },
        )
        Pago.objects.update_or_create(
            citacion=citaciones["DON-002"],
            defaults={
                "estado": "PENDIENTE",
                "es_sus": False,
                "transfusion": None,
                "created_by": bio,
            },
        )
