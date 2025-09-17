from django.contrib import admin
from .models import Aula, Curso, ProgressoAula, Perfil, Matricula

# Register your models here.

admin.site.register(Aula)
admin.site.register(Curso)
admin.site.register(Perfil)
admin.site.register(Matricula)

@admin.register(ProgressoAula)
class ProgressoAulaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'aula', 'concluida', 'data_conclusao')
    list_filter = ('concluida', 'aluno', 'aula__curso')
