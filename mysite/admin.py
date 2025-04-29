from django.contrib import admin
from .models import Livro, Autor, Genero, Exemplar

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'disponivel')  # Usando a property

# Registrar os outros models...
admin.site.register([Autor, Genero, Exemplar])