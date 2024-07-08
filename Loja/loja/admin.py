from django.contrib import admin
from .models import *  # Importa nossos models

admin.site.register(Fabricante) # Registra Fabricante com o FabricanteAdmin
admin.site.register(Categoria)
admin.site.register(Produto)