from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil, Aula, Atividade

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Útil se adicionar mais campos no futuro
    if hasattr(instance, 'profile'):
        instance.perfil.save()

@receiver(post_save, sender=Aula)
def criar_atividade_padrao_para_aula(sender, instance, created, **kwargs):
    if created:
        if not Atividade.objects.filter(aula=instance).exists():
            Atividade.objects.create(
                aula=instance,
            )
            print(f"Atividade padrão criada para: {instance.nome}")