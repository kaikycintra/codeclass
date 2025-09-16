from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

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


#---------------------------------------------------------------
# Modelos com relação à atividades

class Atividade(models.Model):
    """
    Modelo que armazena um tipo de atividade (CHECKBOX, TEXTO, etc)
    Modelo genérico que pode estender à diferentes tipos
    """
    class TipoAtividade(models.TextChoices):
        CHECKBOX = "CHECKBOX", "Confirmação Simples"
    
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="atividades")
    titulo = models.CharField(max_length=200, default=f"Confirmar Conclusão da Aula")
    tipo = models.CharField(max_length=10, choices=TipoAtividade.choices, default=TipoAtividade.CHECKBOX)
    enunciado = models.TextField(blank=True, null=True, default="Marque a caixa para concluir a aula")

    def __str__(self):
        return f'{self.titulo} ({self.aula.nome})'
    
class ProgressoAulaManager(models.Manager):
    """
    Gerencia a lógica de negócio para o progresso da aula.
    """
    def altera_status_conclusao(self, user, aula):
        """
        Método simples, que marca uma aula como concluída/não-concluída (como um toggle)
        """
        progresso, created = self.get_or_create(aluno=user, aula=aula)
        progresso.concluida = not progresso.concluida
        progresso.save()

        return progresso


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
    
    def save(self, *args, **kwargs):
        """ Define data de conclusão automaticamente """
        if self.concluida and not self.data_conclusao:
            self.data_conclusao = timezone.now()
        elif not self.concluida:
            self.data_conclusao = None
        super().save(*args, **kwargs)

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

class Comentario(models.Model):
    """
    Modelo de comentários, conectando com o usuário e a aula.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comentarios_feitos")
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="comentarios_aula")
    texto = models.TextField(max_length=256)
    data = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="respostas")

    # Podemos usar um campo Many-To-Many aqui. A ideia é que não precisamos de métodos extras, então um campo desse, por mais não-intuitivo que seja,
    # será o suficiente
    curtidas = models.ManyToManyField(User, related_name="comentarios_curtidos", blank=True)

    # Mostra comentários mais antigos primeiro
    class Meta:
        ordering = ['data']
    
    def __str__(self):
        if self.parent:
            return f'Resposta de {self.user.username} para {self.parent.user.username}'
        return f'Comentário de {self.user.username}'
    
    # Valida comentários para que possa ser até a primeira camada
    # Normalmente esse erro não irá ocorrer, mas se houver um bypass aí usamos essa validação também
    def save(self, *args, **kwargs):
        if self.parent:
            # Checa se o parent já possui um parent
            if self.parent.parent:
                raise ValidationError("Só é possível responder até a primeira camada")
        super().save(*args, **kwargs)
    
    @property
    def total_curtidas(self):
        return self.curtidas.count()