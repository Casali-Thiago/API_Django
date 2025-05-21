from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date

class DesafioBrasilprevTests(APITestCase):
    def test_criar_cliente(self):
        data = {
            "nome": "Maria Teste",
            "cpf": "12345678900",
            "email": "maria@email.com",
            "dataDeNascimento": "1995-05-01",
            "sexo": "F",
            "rendaMensal": 4000.0
        }
        response = self.client.post("/clientes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_criar_produto(self):
        data = {
            "nome": "Plano Teste",
            "susep": "15414.999999/2024-00",
            "expiracaoDeVenda": "2026-12-31",
            "valorMinimoAporteInicial": 1000.0,
            "valorMinimoAporteExtra": 200.0,
            "idadeDeEntrada": 18,
            "idadeDeSaida": 65,
            "carenciaInicialDeResgate": 60,
            "carenciaEntreResgates": 30
        }
        response = self.client.post("/produtos/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_fluxo_contrato_e_resgate(self):
        # Criar cliente
        cliente = self.client.post("/clientes/", {
            "nome": "Carlos Fluxo",
            "cpf": "11122233344",
            "email": "carlos@fluxo.com",
            "dataDeNascimento": "1990-01-01",
            "sexo": "M",
            "rendaMensal": 5000.0
        }, format="json").data

        # Criar produto
        produto = self.client.post("/produtos/", {
            "nome": "Produto Fluxo",
            "susep": "12345.000000/2024-99",
            "expiracaoDeVenda": "2025-12-31",
            "valorMinimoAporteInicial": 1000.0,
            "valorMinimoAporteExtra": 100.0,
            "idadeDeEntrada": 18,
            "idadeDeSaida": 70,
            "carenciaInicialDeResgate": 0,
            "carenciaEntreResgates": 0
        }, format="json").data

        # Criar plano
        plano = self.client.post("/planos/", {
            "idCliente": cliente["id"],
            "idProduto": produto["id"],
            "aporte": 2000.0,
            "dataDaContratacao": str(date.today())
        }, format="json").data
        
        aporte = self.client.post("/aportes/", {
            "idPlano": plano["id"],
            "valorAporte": 50.0
        }, format="json")


        # Fazer resgate
        resgate = self.client.post("/resgates/", {
            "idPlano": plano["id"],
            "valorResgate": 1000.0
        }, format="json")

        self.assertEqual(resgate.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", resgate.data)
