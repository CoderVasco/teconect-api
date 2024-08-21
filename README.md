
# TeconectAPI

TeconectAPI é uma API robusta para autenticação e gerenciamento de usuários, projetada para ser facilmente integrada em sistemas que requerem autenticação segura e eficiente. Nossa missão é proporcionar uma solução segura e escalável para desenvolvedores, permitindo a construção de sistemas que valorizam a segurança e o controle de acesso.

## Visão Geral

TeconectAPI é uma API RESTful que centraliza as funcionalidades de autenticação, gerenciamento de usuários e controle de acesso, oferecendo uma solução moderna para desenvolvedores que buscam uma API confiável para integrar em seus sistemas.

### Funcionalidades Principais

- **Autenticação de Usuários:** Utilizando JSON Web Tokens (JWT) para autenticação.
- **Gerenciamento de Usuários:** Registro, login, atualização de perfil, e exclusão de usuários.
- **Controle de Acesso:** Baseado em funções (admin, root, usuário).
- **Segurança:** Implementação de criptografia para senhas e uso de tokens JWT para sessões seguras.

## Requisitos

Para rodar o projeto, certifique-se de que as seguintes dependências estão instaladas:

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite (ou outro banco de dados de sua escolha)
- JWT (JSON Web Tokens)
- Passlib
- Python-Jose
- Loguru
- Pydantic
- Email-Validator
- Bcrypt
- SlowAPI

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/CoderVasco/teconect-api.git
```

2. Entre no diretório do projeto:

```bash
cd teconect-api
```

3. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv env
source env/bin/activate  # No Windows, use `env\Scripts\activate`
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente necessárias (como `SECRET_KEY`, `DATABASE_URL` etc.).

5. Execute a aplicação:

```bash
uvicorn main:app --reload
```

## Estrutura do Projeto

```
/api
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── admin.py
│   └── services/
│       ├── __init__.py
│       └── auth_service.py
├── main.py
├── config.py
└── requirements.txt
```

## Contribua com o Projeto

Se você deseja contribuir com o projeto, entre em contato através dos canais abaixo. Estamos sempre abertos a novas ideias e colaborações para melhorar a TeconectAPI e apoiar nossa comunidade.

## Contatos

**Co-Fundador**  
**Vasco Pinto**  
- **Facebook:** [vasco.gouveiapinto](https://www.facebook.com/vasco.gouveiapinto)  
- **Email:** [me@vascopinto.site](mailto:me@vascopinto.site)  
- **Website:** [vascopinto.site](http://vascopinto.site)  
- **Telefone:** +244 946 210 892  
- **Email Alternativo:** [imarca.ao@gmail.com](mailto:imarca.ao@gmail.com)  
- **Email comunitário:** [add@teconectapi.it.ao](mailto:add@teconectapi.it.ao)  
- **Website do projeto:** [teconectapi.it.ao](http://teconectapi.it.ao)

## Contribuintes

1. **Vasco Pinto** - Co-Fundador & Desenvolvedor Fullstack

## Patrocinador Oficial

1. **Tecnideia - Ideias Tecnológicas**  
   - **Email:** [geral@tecnideia.ao](mailto:geral@tecnideia.ao)  
   - **Website:** [tecnideia.ao](http://tecnideia.ao)
