import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.admision.models import CitacionDonante
from apps.admision.serializers.citacion_donante_serializers import CitacionDonanteSerializer

try:
    c = CitacionDonante.objects.first()
    print("Primer citacion:", c)
    if c:
        ser = CitacionDonanteSerializer(c)
        print("Data:", ser.data)
except Exception as e:
    import traceback
    traceback.print_exc()
