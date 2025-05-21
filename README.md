# Desafio Técnico Brasilprev - Backend

Esta aplicação simula uma API REST de previdência privada, desenvolvida em Python com Django REST Framework.

## Funcionalidades
- Cadastro de cliente
- Cadastro de produto
- Contratação de plano
- Aporte extra
- Resgate de plano

## Tecnologias
- Python 3
- Django
- Django REST Framework

## Como executar

```bash
# Instale as dependências
pip install -r requirements.txt

# Rode as migrações
python manage.py makemigrations
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```

## Para testar o aplicativo

Acesse via navegador ou Postman: http://localhost:8000/

## Observação
Este projeto utiliza bibliotecas Python padrão e não exige configuração adicional além de instalar dependências e rodar o servidor com `python manage.py runserver`.
