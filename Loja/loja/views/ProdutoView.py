from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from loja.models import Produto, Fabricante, Categoria
from datetime import timedelta, datetime
from django.utils import timezone
# inclua as bibliotecas FileSystemStorage


def list_produto_view(request, id=None):
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")
    produtos = Produto.objects.all()
    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days = int(dias))
        produtos = produtos.filter(criado_em__gte=now)
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)
    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
    if categoria is not None:
        produtos = produtos.filter(categoria__Categoria=categoria)
    if fabricante is not None:
        produtos = produtos.filter(fabricante__Fabricante=fabricante)
    if id is not None:
        produtos = produtos.filter(id=id)
    print(produtos)
    print(promocao)
    # Adicione para definir o contexto e carregar o template
    context = {
    'produtos': produtos
    }
    return render(request, template_name='produto/produto.html',context=context, status=200)
    # return HttpResponse('<h1>Produto de id %s!</h1>' % id)



def edit_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    context = {'produto': produto, 'fabricantes' : Fabricantes, 'categorias' : Categorias}
    return render(request, template_name='produto/produto-edit.html', context=context,status=200)




def edit_produto_postback(request, id=None):
    if request.method == 'POST':
        # Salva dados editados
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")
        print("postback")
        print(id)
        print(produto)
        print(destaque)
        print(promocao)
        print(msgPromocao)
        try:
            obj_produto = Produto.objects.filter(id=id).first()
            obj_produto.Produto = produto
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            #salve os objeto fabricante e categoria filtrados com base no id recebido na variavel categoria e fabricante
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante).first()
            obj_produto.categoria = Categoria.objects.filter(id=categoria).first()
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
            obj_produto.save()
            print("Produto %s salvo com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")

def details_produto_view(request, id=None):
    # Processa o evento GET gerado pela action
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    context = {'produto': produto, 'fabricantes' : Fabricantes, 'categorias' : Categorias}
    
    return render(request, template_name='produto/produto-details.html', context=context,
    status=200)

def delete_produto_view(request, id=None):
# Processa o evento GET gerado pela action
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    context = {'produto': produto, 'fabricantes' : Fabricantes, 'categorias' : Categorias}
    return render(request, template_name='produto/produto-delete.html', context=context, status=200)

# adicione a função que trata o postback da interface de exclusão
def delete_produto_postback(request, id=None):
    
# Processa o post back gerado pela action
    if request.method == 'POST':
# Salva dados editados
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        print("postback-delete")
        print(id)
        try:
            Produto.objects.filter(id=id).delete()
            print("Produto %s excluido com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")

def create_produto_view(request, id=None):
    if request.method == 'POST':
        produto_nome = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        preco = request.POST.get("preco")
        image = request.FILES.get("image")
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")

        print("postback-create")
        print(produto_nome)
        print(destaque)
        print(promocao)
        print(msgPromocao)
        print(preco)
        print(image)
        print(categoria_id)
        print(fabricante_id)

        try:
            obj_produto = Produto()
            obj_produto.Produto = produto_nome
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            if msgPromocao:
                obj_produto.msgPromocao = msgPromocao
            obj_produto.preco = float(preco) if preco else 0
            obj_produto.criado_em = timezone.now()
            obj_produto.alterado_em = obj_produto.criado_em

            # Se for anexado arquivo, salva na pasta e guarda nome no objeto
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                obj_produto.image = filename

            # Associa categoria e fabricante
            if categoria_id and categoria_id != "-1":
                obj_produto.categoria_id = categoria_id
            if fabricante_id and fabricante_id != "-1":
                obj_produto.fabricante_id = fabricante_id

            obj_produto.save()
            print(f"Produto {produto_nome} salvo com sucesso")
        except Exception as e:
            print(f"Erro inserindo produto: {e}")

        return redirect("/produto")

    else:
        # Preparar dados para o formulário de criação
        fabricantes = Fabricante.objects.all()
        categorias = Categoria.objects.all()
        context = {
            'fabricantes': fabricantes,
            'categorias': categorias
        }
        return render(request, 'produto/produto-create.html', context)