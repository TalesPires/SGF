from django import forms
from .models import Motorista, Cartao, Fiscal, Tipo, Veiculo
from django.core.exceptions import ValidationError
from validate_docbr import CPF, CNH, RENAVAM

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
        fields = ['cpf_motorista','agencia', 'numero_conta', 'validade']
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
    
class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['id_tipo','nome_tipo', 'capacidade_peso', 'quantidade_eixos']
    
    def clean_capacidade_peso(self):
        capacidade_peso = self.cleaned_data.get(capacidade_peso)
        quantidade_eixos = self.cleaned_data.get(quantidade_eixos)
        
        if capacidade_peso < 0:
            raise ValidationError('Capacidade de peso deve ser maior que zero')
        
        if quantidade_eixos < 0:
            raise ValidationError('Quantidade de eixos deve ser maior que zero')

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['renavam','id_tipo', 'placa', 'marca','modelo', 'cor', 'ano']
        
    def clean_renavam(self):
        renavam = self.cleaned_data.get('renavam')
        validator = RENAVAM()

        if not validator.validate(renavam):
            raise ValidationError("Renavam inválido.")
        
        return renavam