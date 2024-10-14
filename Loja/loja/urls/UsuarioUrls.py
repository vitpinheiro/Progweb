from django.urls import path
from loja.views.UsuarioView import list_usuario_view
from loja.views.UsuarioView import edit_usuario_view

urlpatterns = [
    path("", list_usuario_view, name='usuario'),
    # Adicione a linha a seguir
    path("edit", edit_usuario_view, name='edit_usuario'),
]