from django.shortcuts import render, redirect
from .forms import MotoristaForm, CartaoForm, RegistroFiscalForm
from .models import Motorista, Cartao, Frete
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


@login_required
def index(request):
    """A pagina inicial dos fiscais"""
    return render(request, 'gerenciamento/index.html')

@staff_member_required
def indexadmin(request):
    """A pagina inicial do administrador"""
    return render(request, 'gerenciamento/indexadmin.html')

@login_required
def cadastrarm(request):
    if request.method != 'POST':
        form = MotoristaForm()
    else:
        form = MotoristaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciamento:sucesso')  
    
    context = {'form': form}
    return render(request, 'gerenciamento/cadastrarm.html', context)

@login_required
def sucesso(request):
    return render(request, 'gerenciamento/sucesso.html')

@login_required
def pesquisarm(request):
    motoristas = Motorista.objects.all()
    
    context = {
        'motoristas': motoristas
    }
    return render(request, 'gerenciamento/pesquisarm.html', context)

@login_required
def editarm(request):
    motoristas = Motorista.objects.all()
    
    context = {
        'motoristas': motoristas
    }
    return render(request, 'gerenciamento/editarm.html', context)

@login_required
def formeditarm(request, cpf_motorista):
    motoristas = Motorista.objects.get(cpf_motorista=cpf_motorista)
    
    form = MotoristaForm(request.POST or None,instance=motoristas)
    
    if form.is_valid():
        form.save()
        return redirect('gerenciamento:sucesso')  
    
    context = {'form': form, 'motoristas': motoristas}
    return render(request, 'gerenciamento/formeditarm.html', context)

@login_required
def excluirm(request):
    motoristas = Motorista.objects.all()
    
    context = {
        'motoristas': motoristas
    }
    return render(request, 'gerenciamento/excluirm.html', context)

@login_required
def formexcluirm(request,cpf_motorista):

    motoristas = Motorista.objects.get(cpf_motorista=cpf_motorista)
    
    Cartao.objects.filter(cpf_motorista=cpf_motorista).update(cpf_motorista=None)
    
    Frete.objects.filter(cpf_motorista=cpf_motorista).update(cpf_motorista=None)

    motoristas.delete()
    
    return render(request,'gerenciamento/sucesso.html')
    
@staff_member_required
def cadastraru(request):
    if request.method != 'POST':
        form = RegistroFiscalForm()
    else:
        form = RegistroFiscalForm(request.POST)
        if form.is_valid():
            # Create the user but don't save to the database yet
            user = form.save(commit=False)
            # Set the hashed password and save the user
            user.set_password(form.cleaned_data['password'])
            
            user.is_active = True
            user.is_admin = False
            
            user.save()
            return redirect('gerenciamento:indexadmin')  

    return render(request, 'gerenciamento/cadastraru.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        nome_usuario = request.POST.get('nome_usuario')
        password = request.POST.get('password')

        user = authenticate(request, nome_usuario=nome_usuario, password=password)

        if user is not None:
            login(request, user)
            user.last_login = timezone.now()  # Update last_login
            user.save()  # Save the user to update the last_login
            
            if user.is_staff:
                return redirect('gerenciamento:indexadmin')  # Redirect to homepage after login
            else:
                return redirect('gerenciamento:index')  # Redirect to homepage after login
            
            
        else:
            messages.error(request, "Nome de usuario ou senha inválidos, Tente novamente.")  # Update message to reflect changes

    return render(request, 'gerenciamento/login.html')

def logout_view(request):
    logout(request)
    return redirect('gerenciamento:login')  # Redirect to the login page after logging out