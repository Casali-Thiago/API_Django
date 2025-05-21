from rest_framework import viewsets, status
from rest_framework.response import Response
from datetime import date
from .models import Cliente, Produto, Plano, Aporte, Resgate
#from .serializers import *


class CadastrarClienteViewSet(viewsets.ViewSet):
    def create(self, request):
        nome = request.data.get("nome")
        cpf = request.data.get("cpf")
        email = request.data.get("email")
        data_nascimento = request.data.get("dataDeNascimento")
        sexo = request.data.get("sexo")
        renda = request.data.get("rendaMensal")

        if not all([nome, cpf, email, data_nascimento, sexo, renda]):
            return Response({"erro": "Campos obrigatórios ausentes"}, status=400)

        cliente = Cliente.objects.create(
            nome=nome,
            cpf=cpf,
            email=email,
            dataDeNascimento=data_nascimento,
            sexo=sexo,
            rendaMensal=renda,
        )
        return Response({"id": str(cliente.id)}, status=201)

class CadastrarProdutoViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            produto = Produto.objects.create(
                nome=request.data["nome"],
                susep=request.data["susep"],
                expiracaoDeVenda=request.data["expiracaoDeVenda"],
                valorMinimoAporteInicial=request.data["valorMinimoAporteInicial"],
                valorMinimoAporteExtra=request.data["valorMinimoAporteExtra"],
                idadeDeEntrada=request.data["idadeDeEntrada"],
                idadeDeSaida=request.data["idadeDeSaida"],
                carenciaInicialDeResgate=request.data["carenciaInicialDeResgate"],
                carenciaEntreResgates=request.data["carenciaEntreResgates"]
            )
        except KeyError:
            return Response({"erro": "Campos obrigatórios ausentes"}, status=400)

        return Response({"id": str(produto.id)}, status=201)

class ContratarPlanoViewSet(viewsets.ViewSet):
    def create(self, request):
        id_cliente = request.data.get("idCliente")
        id_produto = request.data.get("idProduto")
        aporte = request.data.get("aporte")
        data_contratacao = request.data.get("dataDaContratacao")

        if not all([id_cliente, id_produto, aporte, data_contratacao]):
            return Response({"erro": "Campos obrigatórios ausentes"}, status=400)

        try:
            cliente = Cliente.objects.get(id=id_cliente)
            produto = Produto.objects.get(id=id_produto)
            aporte = float(aporte)
        except (Cliente.DoesNotExist, Produto.DoesNotExist):
            return Response({"erro": "Cliente ou Produto não encontrado"}, status=404)
        except ValueError:
            return Response({"erro": "Valor de aporte inválido"}, status=400)

        idade_cliente = (date.fromisoformat(data_contratacao) - cliente.dataDeNascimento).days // 365

        if idade_cliente < produto.idadeDeEntrada or idade_cliente > produto.idadeDeSaida:
            return Response({"erro": "Cliente fora da faixa etária permitida"}, status=400)

        if date.fromisoformat(data_contratacao) > produto.expiracaoDeVenda:
            return Response({"erro": "Produto com venda expirada"}, status=400)

        if aporte < produto.valorMinimoAporteInicial:
            return Response({"erro": "Valor abaixo do aporte inicial mínimo"}, status=400)

        plano = Plano.objects.create(
            cliente=cliente,
            produto=produto,
            aporte_inicial=aporte,
            data_contratacao=data_contratacao,
            saldo=aporte
        )
        return Response({"id": str(plano.id)}, status=201)

class AporteExtraViewSet(viewsets.ViewSet):
    def create(self, request):
        plano_id = request.data.get("idPlano")
        valor_aporte = request.data.get("valorAporte")

        if not plano_id or valor_aporte is None:
            return Response({"erro": "Campos obrigatórios ausentes"}, status=400)

        try:
            valor_aporte = float(valor_aporte)
            plano = Plano.objects.get(id=plano_id)
        except ValueError:
            return Response({"erro": "valorAporte inválido"}, status=400)
        except Plano.DoesNotExist:
            return Response({"erro": "Plano não encontrado"}, status=404)

        produto = plano.produto
        if valor_aporte < produto.valorMinimoAporteExtra:
            return Response({"erro": "Valor abaixo do aporte extra mínimo"}, status=400)

        plano.saldo += valor_aporte
        plano.save()

        aporte = Aporte.objects.create(plano=plano, valor=valor_aporte)
        return Response({"id": str(aporte.id)}, status=201)

class ResgateViewSet(viewsets.ViewSet):
    def create(self, request):
        plano_id = request.data.get('idPlano')
        valor_resgate = request.data.get('valorResgate')

        if plano_id is None:
            return Response({'erro': 'Campo "idPlano" é obrigatório'}, status=400)
        if valor_resgate is None:
            return Response({'erro': 'Campo "valorResgate" é obrigatório'}, status=400)

        try:
            valor_resgate = float(valor_resgate)
            plano = Plano.objects.get(id=plano_id)
        except ValueError:
            return Response({'erro': '"valorResgate" deve ser numérico'}, status=400)
        except Plano.DoesNotExist:
            return Response({'erro': 'Plano não encontrado'}, status=404)

        produto = plano.produto
        hoje = date.today()
        dias_ativos = (hoje - plano.data_contratacao).days

        if dias_ativos < produto.carenciaInicialDeResgate:
            return Response({'erro': 'Carência inicial não cumprida'}, status=400)

        if plano.saldo < valor_resgate:
            return Response({'erro': 'Saldo insuficiente'}, status=400)

        plano.saldo -= valor_resgate
        plano.save()

        resgate = Resgate.objects.create(plano=plano, valor=valor_resgate)
        return Response({'id': str(resgate.id)}, status=201)
