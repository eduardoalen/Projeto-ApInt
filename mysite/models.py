from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# 1º MODEL: Livro (Exemplo de Meta Class e Properties)
class Livro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey('Autor', on_delete=models.CASCADE)  # 1ª Relação
    genero = models.ManyToManyField('Genero')  # 2ª Relação
    paginas = models.IntegerField()
    avaliacao = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    # 1ª Property
    @property
    def disponivel(self):
        return self.exemplares.filter(emprestado=False).exists()

    class Meta:  # 1ª Meta Class
        verbose_name = "Livro"
        ordering = ['titulo']

# 2º MODEL: Autor
class Autor(models.Model):
    nome = models.CharField(max_length=50)
    pais = models.CharField(max_length=30)
    data_nascimento = models.DateField()
    falecido = models.BooleanField(default=False)
    biografia = models.TextField()

    # 2ª Property
    @property
    def livros_publicados(self):
        return self.livro_set.count()

    class Meta:  # 2ª Meta Class
        verbose_name_plural = "Autores"

# 3º MODEL: Genero
class Genero(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    século_origem = models.IntegerField()
    popularidade = models.CharField(max_length=10, choices=[
        ('A', 'Alta'), 
        ('M', 'Média'), 
        ('B', 'Baixa')
    ])
    subgenero = models.CharField(max_length=30, blank=True)

    # 3ª Property
    @property
    def livros_disponiveis(self):
        return Livro.objects.filter(genero=self, exemplares__emprestado=False).distinct()

    class Meta:  # 3ª Meta Class
        constraints = [
            models.UniqueConstraint(fields=['nome'], name='genero_unico')
        ]

# 4º MODEL: Exemplar (3ª Relação)
class Exemplar(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='exemplares')
    codigo = models.CharField(max_length=20, unique=True)
    data_aquisicao = models.DateField(auto_now_add=True)
    emprestado = models.BooleanField(default=False)
    localizacao = models.CharField(max_length=10)

    # 4ª Property
    @property
    def status(self):
        return "Emprestado" if self.emprestado else "Disponível"

    class Meta:  # 4ª Meta Class
        verbose_name = "Exemplar"
        verbose_name_plural = "Exemplares"