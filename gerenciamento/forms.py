from django import forms
from .models import Motorista, Cartao, Fiscal
from django.core.exceptions import ValidationError
from validate_docbr import CPF, CNH

class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = ['cpf_motorista','registro_cnh','nome', 'telefone','endereco', 'data_admissao']
        widgets = {
            'data_admissao': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        
    def clean_cpf_motorista(self):
        cpf = self.cleaned_data.get('cpf_motorista')
        validator = CPF()

        if not validator.validate(cpf):
            raise ValidationError("CPF inválido.")
        
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        if len(telefone) != 11 or not telefone.isdigit():
            raise ValidationError("Telefone inválido. Deve conter 11 dígitos.")
        
        return telefone
    
    def clean_registro_cnh(self):
        cnh = self.cleaned_data.get('registro_cnh')
        validator = CNH()

        if not validator.validate(cnh):
            raise ValidationError("CNH inválido.")
        
        return cnh
    
class CartaoForm(forms.ModelForm):
    class Meta:
        model = Cartao
        fields = ['codigo_cartao','cpf_motorista','agencia', 'numero_conta', 'validade']
        widgets = {
            'validade': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        
class RegistroFiscalForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = Fiscal
        fields = ['cpf_fiscal','nome_usuario','email', 'is_active', 'is_admin']
        
    def clean_cpf_fiscal(self):
        cpf = self.cleaned_data.get('cpf_fiscal')
        validator = CPF()

        if not validator.validate(cpf):
            raise ValidationError("CPF inválido.")
        
        return cpf
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("As senhas não correspondem")
        return cleaned_data