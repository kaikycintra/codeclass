from django.db import models

# Create your models here.

class Curso(models.Model):
    
    nome = models.CharField(max_length=32)
    resumo = models.CharField(max_length=320)
    
    data_inicio = models.DateField()
    data_fim = models.DateField()
    
    thumb = models.ImageField(upload_to="imagens/", blank=True, default="/imagens/default.png")
    
    # porcentagem = 
    
    def __str__(self):
        return(self.nome)
    
    def nome_pra_url(self):
        return self.nome.replace(" ", "-")

class Aula(models.Model):
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="aulas")
    nome = models.CharField(max_length=32)
    num = models.IntegerField()
    data = models.DateField()
    
    resumo = models.CharField(max_length=320)
    
    video = models.CharField(max_length=100)
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
    
    # questoes = N sei o q fazer aq
    # comentarios = Aq tmb n
    
# class Comment(models.model):
#     pass

# class User(models.model):
#     pass