from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Curso(models.Model):
    """
    Modelo de curso
    Nota: por padrão, não coloque hifens no nome do curso.
    """
    
    nome = models.CharField(max_length=32, help_text="Não coloque hifens no nome")
    resumo = models.CharField(max_length=320)
    
    data_inicio = models.DateField()
    data_fim = models.DateField()
    
    thumb = models.ImageField(upload_to="imagens/", blank=True, default="/imagens/default.png")
    
    def __str__(self):
        return(self.nome)
    
    def nome_pra_url(self):
        return self.nome.replace(" ", "-")
    
    def get_progresso_curso(self, user):
        """Calcula de imediato o progresso de um aluno no curso"""
        total_aulas = self.aulas.count()
        if total_aulas == 0:
            return 0
        
        aulas_concluidas_count = ProgressoAula.objects.filter(aluno=user, aula__curso=self, concluida=True).count()
        return round((aulas_concluidas_count / total_aulas) * 100)

class Aula(models.Model):
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="aulas")
    nome = models.CharField(max_length=32)
    num = models.IntegerField()
    data = models.DateField()
    
    resumo = models.CharField(max_length=320)
    
    # Nota: refactor da parte de vídeo
    video = models.CharField(max_length=100, blank=True, null=True)
    notas = models.FileField(upload_to="notas_de_aula/", null=True, blank=True)
    slides = models.FileField(upload_to="slides", null=True, blank=True)
    code = models.FileField(upload_to="codigos", null=True, blank=True)
    
    # porcentagem = 
    
    def __str__(self):
        return(f"{self.curso.nome}: Aula {self.num}-{self.nome}")
    
    def nome_pra_url(self):
        return self.nome.replace(" ", "-")
    
    def curso_pra_url(self):
        return self.curso.nome.replace(" ", "-")
    
## Matricula, progresso, exercicios, etc
class Matricula(models.Model):
    """
    Modelo que armazena a matrícula de um aluno e um curso
    """
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matriculas")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="matriculas")
    data_matricula = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('aluno', 'curso')
    
    def __str__(self):
        return f'{self.aluno.username} matriculado em {self.curso}'


## Classes de Exercícios e progressos de aula

class Questao(models.Model):
    """
    Modelo que armazena a questão e o enunciado
    """
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="questoes")
    pergunta = models.TextField()

    def __str__(self):
        return f'Questão para {self.aula.nome}'
    
class Alternativa(models.Model):
    """
    Modelo flexível que armazena as alternativas de uma questão
    """
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name="alternativas")
    texto = models.TextField(max_length=255)
    correta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

class RespostaQuestao(models.Model):
    """
    Modelo que armazena a resposta de um usuário/estudante a uma questão
    """
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="respostas")
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name="respostas")
    resposta = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    data_resposta = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Resposta de {self.aluno.username} para {self.questao.pergunta[:30]}...'

    def correta(self):
        """Checa se a resposta está correta"""
        return self.resposta.correta
    
class ProgressoAulaManager(models.Manager):
    """
    Método de gerenciamento para o progresso de uma aula
    Utilizamos um método lazy para atualizar e criar os ProgressoAula
    """
    def check_and_update(self, user, resposta_questao_obj):
        if not resposta_questao_obj.correta():
            return
        
        aula_atual = resposta_questao_obj.questao.aula

        progresso, created = self.get_or_create(aluno=user, aula=aula_atual, defaults={'concluida':False})
        if progresso.concluida:
            return
        
        total_questoes = aula_atual.questoes.count()
        respostas_corretas_count = RespostaQuestao.objects.filter(aluno=user, questao__aula=aula_atual, resposta__correta=True).values('questao').distinct().count()

        if respostas_corretas_count >= total_questoes:
            progresso.concluida = True
            progresso.data_conclusao = timezone.now()
            progresso.save()


class ProgressoAula(models.Model):
    """
    Modelo que armazena o progresso de uma aula (i.e se ela está completa ou não)
    """
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(null=True, blank=True)

    objects = ProgressoAulaManager()

    class Meta:
        unique_together = ('aluno', 'aula')

#---------------------------------------------------------------
# Modelos com relação aos usuários

class Perfil(models.Model):
    """
    Modelo customizável para o usuário, com bio, entre outras coisas
    Utilizamos signals.py para criação de um perfil quando um usuário cria uma conta
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    biografia = models.TextField(max_length=256, blank=True, null=True, default="Perfil de um usuário do CodeClass")
    # Outras coisas a adicionar aqui? (Foto de perfil, links, etc)

    def __str__(self):
        return f'Perfil associado à {self.user.username}'
