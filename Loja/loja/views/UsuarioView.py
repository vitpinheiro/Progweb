from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Usuario
from loja.forms.UserUsuarioForm import UserUsuarioForm, UserForm
def list_usuario_view(request, id=None):
# carrega somente usuarios, não inclui os admin
    usuarios = Usuario.objects.filter(perfil=2)
    context = {
    'usuarios': usuarios
    }
    return render(request, template_name='usuario/usuario.html', context=context,status=200)

# adicione o método de edição
def edit_usuario_view(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    usuarioForm = UserUsuarioForm(instance=usuario)
    # Crie uma instância da classe UserForm
    userForm = UserForm(instance=request.user)
    context = {
    'usuarioForm': usuarioForm,
    'userForm': userForm
    }
    return render(request, template_name='usuario/usuario-edit.html', context=context,status=200)