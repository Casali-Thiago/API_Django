from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CadastrarClienteViewSet,
    CadastrarProdutoViewSet,
    ContratarPlanoViewSet,
    AporteExtraViewSet,
    ResgateViewSet
)

router = DefaultRouter()
router.register('CadastrarClientes', CadastrarClienteViewSet, basename='Cadastrarclientes')
router.register('CadastrarProdutos', CadastrarProdutoViewSet, basename='CadastrarProdutos')
router.register('ContratarPlanos', ContratarPlanoViewSet, basename='ContratarPlano')
router.register('aportes', AporteExtraViewSet, basename='aporte')
router.register('resgates', ResgateViewSet, basename='resgate')

urlpatterns = [
    path('', include(router.urls)),
]
