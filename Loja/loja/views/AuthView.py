from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from loja.forms.AuthForm import LoginForm, RegisterForm

def login_view(request):
    loginForm = LoginForm()
    message = None

    # Se o usuário já estiver autenticado, redireciona para a página inicial
    if request.user.is_authenticated:
        return redirect('/')

    # Se o método for POST, tenta autenticar o usuário
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                message = {'type': 'danger', 'text': 'Dados de usuário incorretos'}

    # Passa o formulário e a mensagem para o contexto
    context = {
        'form': loginForm,
        'message': message,
        'title': 'Login',
        'button_text': 'Entrar',
        'link_text': 'Registrar',
        'link_href': '/register'
    }

    # Renderiza a página de login
    return render(request, template_name='auth/auth.html', context=context, status=200)

def register_view(request):
    registerForm = RegisterForm()
    message = None

    # Se o usuário já estiver autenticado, redireciona para a página inicial
    if request.user.is_authenticated:
        return redirect('/')

    # Se o método for POST, tenta registrar o novo usuário
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        registerForm = RegisterForm(request.POST)

        if registerForm.is_valid():
            # Aqui verificamos se existe usuário ou e-mail com esse cadastro
            verifyUsername = User.objects.filter(username=username).first()
            verifyEmail = User.objects.filter(email=email).first()

            if verifyUsername is not None:
                message = {'type': 'danger', 'text': 'Já existe um usuário com este username!'}
            elif verifyEmail is not None:
                message = {'type': 'danger', 'text': 'Já existe um usuário com este e-mail!'}
            else:
                user = User.objects.create_user(username, email, password)
                if user is not None:
                    message = {'type': 'success', 'text': 'Conta criada com sucesso!'}
                else:
                    message = {'type': 'danger', 'text': 'Um erro ocorreu ao tentar criar o usuário.'}

    # Passa o formulário e a mensagem para o contexto
    context = {
        'form': registerForm,
        'message': message,
        'title': 'Registrar',
        'button_text': 'Registrar',
        'link_text': 'Login',
        'link_href': '/login'
    }

    # Renderiza a página de registro
    return render(request, template_name='auth/auth.html', context=context, status=200)
