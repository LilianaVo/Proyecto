from django.db import models
# Importamos el modelo de usuario por defecto de Django
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- 1. MODELO DE PERFIL DE VOTANTE (VoterProfile) ---
class VoterProfile(models.Model):
    # Relación uno a uno con el usuario estándar de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campo para almacenar la llave pública RSA del votante.
    public_key = models.TextField(
        blank=True,         
        null=True,          
        help_text="Llave pública RSA del votante, usada para verificar la firma digital."
    )
    
    # Indica si el usuario ya emitió su voto (clave para el requisito de voto único)
    has_voted = models.BooleanField(default=False) 

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Señal para crear automáticamente un VoterProfile cuando se crea un nuevo User
# Usa el argumento 'created' para asegurar que solo se ejecuta la primera vez.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        VoterProfile.objects.create(user=instance)

# --- 2. MODELO DE VOTO (Vote) ---
class Vote(models.Model):
    # Relación con el perfil del votante (quién votó)
    voter = models.ForeignKey(
        'VoterProfile', 
        on_delete=models.CASCADE, 
        help_text="Perfil del votante que emitió este voto."
    )
    
    # La opción seleccionada (ej. "Partido Python", "Alianza Java")
    option = models.CharField(
        max_length=100,
        help_text="La opción seleccionada por el votante."
    )
    
    # La Firma Digital (el hash cifrado) - Prueba de No Repudio e Integridad.
    digital_signature = models.TextField(
        help_text="Firma digital (Hash RSA) del voto, prueba de no repudio."
    )
    
    # ¡CAMPO FALTANTE AÑADIDO! (Causa del error 'unexpected keyword argument')
    # Almacena el voto cifrado con AES, demostrando Confidencialidad.
    encrypted_vote = models.TextField(
        blank=True,
        null=True,
        help_text="Voto cifrado con AES-256 para demostrar confidencialidad."
    )
    
    # Marca de tiempo para el registro inmutable
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voto de {self.voter.user.username} por {self.option}"
