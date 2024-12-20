# Generated by Django 4.2.16 on 2024-10-29 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('codigo_cartao', models.CharField(db_column='codigo_cartao', max_length=10, primary_key=True, serialize=False)),
                ('agencia', models.CharField(db_column='agencia', max_length=5)),
                ('numero_conta', models.CharField(db_column='numero_conta', max_length=6)),
                ('validade', models.DateField(db_column='validade')),
            ],
            options={
                'db_table': 'cartao',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Frete',
            fields=[
                ('id_frete', models.IntegerField(db_column='id_frete', primary_key=True, serialize=False, unique=True)),
                ('data_chegada', models.DateTimeField(db_column='data_chegada')),
                ('data_saida', models.DateTimeField(db_column='data_saida')),
                ('distancia_rodagem', models.SmallIntegerField(db_column='distancia_rodagem')),
                ('valor_frete', models.DecimalField(db_column='valor_frete', decimal_places=2, max_digits=10)),
                ('renavam', models.CharField(db_column='renavam', max_length=11)),
            ],
            options={
                'db_table': 'frete',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Motorista',
            fields=[
                ('cpf_motorista', models.CharField(db_column='cpf_motorista', max_length=11, primary_key=True, serialize=False)),
                ('registro_cnh', models.CharField(db_column='registro_cnh', max_length=11)),
                ('nome', models.CharField(db_column='nome', max_length=50)),
                ('telefone', models.CharField(db_column='telefone', max_length=11)),
                ('endereco', models.CharField(db_column='endereco', max_length=50)),
                ('data_admissao', models.DateField(db_column='data_admissao')),
            ],
            options={
                'db_table': 'motorista',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Fiscal',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('cpf_fiscal', models.CharField(db_column='cpf_fiscal', max_length=11, primary_key=True, serialize=False, unique=True)),
                ('nome_usuario', models.CharField(db_column='nome_usuario', max_length=50, unique=True)),
                ('email', models.EmailField(db_column='email', max_length=55)),
                ('is_active', models.BooleanField(db_column='ativo', default=True)),
                ('is_admin', models.BooleanField(db_column='staff', default=False)),
            ],
            options={
                'db_table': 'fiscal',
                'managed': True,
            },
        ),
    ]
