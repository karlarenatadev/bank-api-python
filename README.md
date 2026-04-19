# 🏦 Bank API - Sistema Bancário 2.0

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)

Este projeto evoluiu de um sistema legado em memória para uma **API RESTful moderna**. O foco principal foi aplicar padrões de **Engenharia de Software** para garantir persistência, segurança e, acima de tudo, **precisão financeira**.

## 🚀 Diferenciais Técnicos

* **Precisão Financeira:** Utilização do tipo `Decimal` (via `Annotated` e `Field`) em vez de `float`, garantindo que não existam erros de arredondamento em transações monetárias.
* **Segurança Baseada em JWT:** Implementação de autenticação assíncrona com **JSON Web Tokens**, garantindo acesso seguro e isolado aos dados de cada usuário.
* **Arquitetura em Camadas:** Organização modular entre Controllers, Services e Models para facilitar a manutenção e escalabilidade do código.

## ⚙️ Regras de Negócio Implementadas

A camada de serviço (`TransactionService`) impõe restrições rigorosas para auditoria e controle:

1. **Limite de Saque:** O valor máximo permitido por operação de saque é de **R$ 500,00**.
2. **Limite Diário:** Cada conta está restrita a, no máximo, **3 saques por dia**.
3. **Validação de Saldo:** Saques são processados apenas se houver saldo suficiente disponível.
4. **Isolamento de Contas:** Um usuário autenticado só pode realizar transações ou visualizar extratos de contas que pertencem ao seu ID.

## 📂 Estrutura do Projeto

```text
src/
├── controllers/  # Endpoints da API e injeção de dependências
├── services/     # Core da aplicação (Regras de negócio)
├── models/       # Tabelas e relacionamentos do banco de dados
├── schemas/      # Contratos de entrada/saída e validações Pydantic
├── config.py     # Gestão de variáveis de ambiente (.env)
├── database.py   # Configuração do motor de banco de dados
└── security.py   # Lógica de criptografia, JWT e proteção de rotas
```

## 🚀 Como Executar

1. Clone o repositório:

   ```bash
   git clone [https://github.com/karlarenatadev/bank-api-python.git](https://github.com/karlarenatadev/bank-api-python.git)
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd bank-api-python
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o servidor:

   ```bash
   uvicorn main:app --reload
   ```

5. Acesse a documentação interativa da API (Swagger UI) em:

   ```bash
   http://127.0.0.1:8000/docs
   ```

---

## 🔭 Próximos Passos

- [ ] Implementação de **Testes Unitários com Pytest**.
- [ ] Containerização da aplicação com **Docker**.
- [ ] Integração com modelo de **Machine Learning** para detecção de anomalias.

---

**Desenvolvido por:** Karla Renata