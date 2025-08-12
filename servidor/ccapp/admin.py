from django.contrib import admin
from .models import Aula, Curso, Questao, Alternativa, RespostaQuestao, ProgressoAula, Perfil, Comentario

# Register your models here.

class AlternativaInline(admin.TabularInline):
    model = Alternativa
    extra = 4

class QuestaoAdmin(admin.ModelAdmin):
    list_display= ('pergunta', 'aula')
    inlines = [AlternativaInline]

admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Alternativa)
admin.site.register(Aula)
admin.site.register(Curso)
admin.site.register(Perfil)
admin.site.register(Comentario)

@admin.register(RespostaQuestao)
class RespostaQuestaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'questao', 'resposta', 'data_resposta')
    list_filter = ('aluno', 'questao__aula__curso', 'questao__aula')
    readonly_fields = ('aluno', 'questao', 'resposta', 'data_resposta')

@admin.register(ProgressoAula)
class ProgressoAulaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'aula', 'concluida', 'data_conclusao')
    list_filter = ('concluida', 'aluno', 'aula__curso')
