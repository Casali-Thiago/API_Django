from django.db import models

class Cliente(models.Model):
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    dataDeNascimento = models.DateField()
    sexo = models.CharField(max_length=1)
    rendaMensal = models.FloatField()

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    susep = models.CharField(max_length=50)
    expiracaoDeVenda = models.DateField()
    valorMinimoAporteInicial = models.FloatField()
    valorMinimoAporteExtra = models.FloatField()
    idadeDeEntrada = models.IntegerField()
    idadeDeSaida = models.IntegerField()
    carenciaInicialDeResgate = models.IntegerField()
    carenciaEntreResgates = models.IntegerField()

class Plano(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    aporte_inicial = models.FloatField()
    data_contratacao = models.DateField()
    saldo = models.FloatField(default=0)
    #ultima_data_resgate = models.DateField(null=True, blank=True)

class Aporte(models.Model):
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    valor = models.FloatField()
    data = models.DateField(auto_now_add=True)

class Resgate(models.Model):
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    valor = models.FloatField()
    data = models.DateField(auto_now_add=True)
