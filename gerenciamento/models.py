from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Motorista(models.Model):
    cpf_motorista = models.CharField(db_column='cpf_motorista',max_length=11,primary_key=True, null=False)
    registro_cnh = models.CharField(db_column='registro_cnh',max_length=11)
    nome = models.CharField(db_column='nome',max_length=50)
    telefone = models.CharField(db_column='telefone',max_length=11)
    endereco = models.CharField(db_column='endereco',max_length=50)
    data_admissao = models.DateField(db_column='data_admissao')

    class Meta:
        managed = False
        db_table = 'motorista'

    def __str__(self):
        return self.cpf_motorista

class Cartao(models.Model):
    codigo_cartao = models.CharField(db_column='codigo_cartao',max_length=10,primary_key=True, null=False)
    agencia = models.CharField(db_column='agencia',max_length=5)
    numero_conta = models.CharField(db_column='numero_conta',max_length=6)
    validade = models.DateField(db_column='validade')
    cpf_motorista = models.ForeignKey(Motorista,db_column='cpf_motorista', null=True,on_delete=models.SET_NULL,blank=True)

    class Meta:
        managed = False
        db_table = 'cartao'

    def __str__(self):
        return self.codigo_cartao
    
class Frete(models.Model):
    id_frete = models.IntegerField(db_column='id_frete',primary_key=True, null=False, unique=True)
    data_chegada = models.DateTimeField(db_column='data_chegada')
    data_saida = models.DateTimeField(db_column='data_saida')
    distancia_rodagem = models.SmallIntegerField(db_column='distancia_rodagem')
    valor_frete = models.DecimalField(db_column='valor_frete', max_digits=10, decimal_places=2)
    cpf_motorista = models.ForeignKey(Motorista,db_column='cpf_motorista',max_length=11, null=True,on_delete=models.SET_NULL,blank=True)  
    renavam = models.CharField(db_column='renavam',max_length=11) 


    class Meta:
        managed = False
        db_table = 'frete'

    def __str__(self):
        return self.id_frete

class MinhaGestaoUsuarios(BaseUserManager):
    def criar_usuario(self, nome_usuario, email, cpf_fiscal, password=None):
        if not cpf_fiscal:
            raise ValueError("Por favor informe um CPF")
        
        if not nome_usuario:
            raise ValueError("Por favor informe um nome")
        
        if not email:
            raise ValueError("Por favor informe um email")
        
        # Create the user object with necessary fields
        user = self.model(
            email=self.normalize_email(email),
            nome_usuario=nome_usuario,
            cpf_fiscal=cpf_fiscal,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def criar_superuser(self, nome_usuario, email, cpf_fiscal, password=None):
        user = self.criar_usuario(
            nome_usuario=nome_usuario,
            email=email,
            cpf_fiscal=cpf_fiscal,
            password=password
        )

        user.is_staff = True
        user.save(using=self._db)
        return user

# Custom model linked to 'fiscal' table
class Fiscal(AbstractBaseUser):
    cpf_fiscal = models.CharField(db_column='cpf_fiscal', primary_key=True, unique=True, max_length=11)
    nome_usuario = models.CharField(db_column='nome_usuario', max_length=50, unique=True)
    email = models.EmailField(db_column='email', max_length=55)
    is_active = models.BooleanField(db_column='ativo',default=True)     
    is_admin = models.BooleanField(db_column='staff',default=False) 

    objects = MinhaGestaoUsuarios()

    USERNAME_FIELD = 'nome_usuario'
    REQUIRED_FIELDS = ['email', 'cpf_fiscal']  

    class Meta:
        managed = False  
        db_table = 'fiscal'

    def __str__(self):
        return self.cpf_fiscal
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin