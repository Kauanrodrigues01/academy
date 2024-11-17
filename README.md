# Academia - Projeto Django

## Passos para Rodar o Projeto

### 1. Clonar o Repositório

Clone o repositório do projeto para seu diretório local:

```bash
git clone https://link-do-repositorio.git
cd nome-do-repositorio
```

### 2. Criar e Ativar um Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

Ative o ambiente virtual:

- Windows:
```bash
venv\Scripts\activate
```

- Linux/macOS:
```bash
source venv/bin/activate
```

### 3. Instalar as Dependências

Instale as dependências do projeto com o comando:

```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto e preencha as variáveis de ambiente necessárias para a configuração do banco de dados e do superusuário. Exemplo de como configurar o arquivo .env:

```bash
# Configuração do email, USE ESTE MESMO, pois é apenas um email de teste
EMAIL_HOST_PASSWORD = 'yzuy uyju jxpo faxf'

# Configurações do superusuário (serão usadas para criar o superusuário automaticamente após a migração)
DJANGO_SUPERUSER_CPF = 'seu cpf'
DJANGO_SUPERUSER_EMAIL = 'seu email'
DJANGO_SUPERUSER_PASSWORD = 'sua senha'

```

### 5. Aplicar as Migrações

Rode as migrações para criar as tabelas do banco de dados. Isso também criará automaticamente o superusuário, se ele não existir, utilizando as variáveis de ambiente configuradas no .env:

```bash
python manage.py migrate
```

### 6. Rodar o Servidor Local e Celery

Agora você pode rodar o servidor de desenvolvimento do Django e iniciar as tarefas assíncronas com Celery:

#### Rodar o Servidor Django

Para rodar o servidor local do Django, use o comando:

```bash
python manage.py runserver
```

#### Redis Container

O Celery usa o Redis como o broker de mensagens. Portanto, é necessário ter um container Redis rodando para o Celery funcionar corretamente.

Caso você esteja utilizando Docker, você pode rodar um container Redis com o seguinte comando:

```bash
docker run --name redis -p 6379:6379 -d redis
```

#### Rodar a Celery

O Celery é responsável por rodar tarefas assíncronas em segundo plano, e o Celery Beat gerencia a execução periódica dessas tarefas.

Em um **terminal separado**, certifique-se de que esteja com o ambiente virtual(venv) ativo. Execute:

```bash
celery -A project worker --loglevel=info --pool=solo
```

#### Rodar a Celery Beat

**Em outro terminal separado**, certifique-se de que esteja com o ambiente virtual(venv) ativo. Execute:

```bash
celery -A project beat --loglevel=info
```

