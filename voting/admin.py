from django.contrib import admin
from .models import VoterProfile

# Registramos el modelo para que aparezca en el panel de administración
admin.site.register(VoterProfile)