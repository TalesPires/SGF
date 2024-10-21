"""Define os URL patterns de gerenciamento."""

from django.urls import path
from . import views
from gerenciamento.views import ResetPasswordView
from django.contrib.auth import views as auth_views

app_name = 'gerenciamento'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Home page admin
    path('iadmin/', views.indexadmin, name='indexadmin'),
    # Pagina de cadastro dos motoristas
    path('cadastrarm/', views.cadastrarm, name='cadastrarm'),
    # Pagina de sucesso
    path('sucesso/', views.sucesso, name='sucesso'),
    # Pagina de sucesso
    path('pesquisarm/', views.pesquisarm, name='pesquisarm'),
    # Pagina de edição dos motoristas
    path('editarm/', views.editarm, name='editarm'),
    # Pagina inserção dos dados da edição dos motoristas
    path('formeditarm/<str:cpf_motorista>/', views.formeditarm, name='formeditarm'),
    # Pagina de edição dos motoristas
    path('excluirm/', views.excluirm, name='excluirm'),
    # Pagina inserção dos dados da edição dos motoristas
    path('excluirm/<str:cpf_motorista>/', views.formexcluirm, name='formexcluirm'),
    
    path('cadastraru/', views.cadastraru, name='cadastraru'),
    
    path('login/', views.login_view, name='login'),
    
    path('logout/', views.logout_view, name='logout'),
    
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    
    path('password-reset-confirm/<str:email>/', views.custom_password_reset_confirm,
        name='redefinir_senha'),
    
    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='gerenciamento/password_reset_complete.html'),
    name='password_reset_complete'),
]