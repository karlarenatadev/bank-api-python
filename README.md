# 🏦 Bank API - Sistema Bancário 2.0

Este projeto representa a evolução técnica de um sistema bancário legado (baseado em terminal e listas em memória) para uma arquitetura moderna de **API RESTful**. Desenvolvido com **FastAPI** e **SQLAlchemy**, o sistema foca em persistência de dados real, validação rigorosa de esquemas e regras de negócio escaláveis.

## 🧠 Contexto e Evolução

O objetivo central desta nova versão foi aplicar padrões de **Engenharia de Dados** e **Desenvolvimento Backend** para garantir que a aplicação não apenas execute funções básicas (saque, depósito), mas que o faça de forma íntegra e auditável através de um banco de dados relacional (SQLite).

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI:** Framework moderno e de alto desempenho para construção de APIs.
* **SQLAlchemy:** ORM (Object-Relational Mapper) para comunicação e persistência em SQL.
* **Pydantic:** Validação de tipos e garantia da integridade dos dados (Schemas).
* **SQLite:** Banco de dados local para desenvolvimento ágil.
* **Uvicorn:** Servidor ASGI de produção.

## 📂 Estrutura do Projeto

A arquitetura foi dividida por responsabilidades para facilitar a manutenção e escalabilidade:

* `database.py`: Configuração da conexão e motor (engine) do banco de dados.
* `models.py`: Definição das tabelas e relacionamentos (Clientes ↔ Contas ↔ Transações).
* `schemas.py`: Contratos de entrada e saída de dados (Pydantic).
* `crud.py`: Lógica de negócio e operações diretas no banco de dados.
* `main.py`: Porta de entrada da aplicação e definição dos endpoints.

## ⚙️ Regras de Negócio Implementadas

Diferente da versão inicial, esta API impõe restrições diretamente na camada de serviço:

1. **Limite de Saque:** O valor máximo permitido por operação de saque é de **R$ 500,00**.
2. **Limite Diário:** Cada conta está restrita a, no máximo, **3 saques por dia**.
3. **Verificação de Saldo:** Operações de saque só são confirmadas se o saldo atual for suficiente.
4. **Integridade Transacional:** Toda movimentação (depósito ou saque) gera um registro automático na tabela de transações para auditoria futura.

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

- [ ] Integração com modelo de **Machine Learning** (Isolation Forest) para detecção automática de anomalias em transações.
- [ ] Implementação de autenticação JWT para acesso seguro às contas.
- [ ] Containerização da aplicação com **Docker**.

---

**Desenvolvido por:** Karla Renata