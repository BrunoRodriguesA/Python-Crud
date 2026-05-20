# Sistema de Gestão Comercial - Painel CRUD

Um aplicativo desktop completo desenvolvido em **Python** utilizando **Tkinter** para a interface gráfica e **MySQL** para o banco de dados. Este sistema possui autenticação segura de usuários e um painel administrativo para o gerenciamento de clientes através de operações CRUD (Create, Read, Update, Delete).

---

## Funcionalidades

* **Autenticação de Usuários:** Sistema de Login e Registro.
* **Segurança:** As senhas dos usuários são criptografadas utilizando hash **SHA-256** antes de serem salvas no banco de dados.
* **Segurança de Credenciais:** Uso de variáveis de ambiente (`.env`) para proteger as credenciais do banco de dados.
* **Gestão de Clientes (CRUD):**
    * **Criar (Create):** Adicionar novos clientes (Nome, Email e Telefone).
    * **Ler (Read):** Visualização dos dados em uma tabela (Treeview) interativa.
    * **Atualizar (Update):** Edição de dados de clientes já existentes.
    * **Deletar (Delete):** Exclusão de clientes com janela de confirmação para evitar acidentes.

---

## Capturas de Tela

Aqui está o fluxo de funcionamento do sistema:

1. Tela de Login
> *Interface inicial onde o usuário insere suas credenciais.*
![Tela de Login]<img width="838" height="565" alt="Captura de tela 2026-05-20 134157" src="https://github.com/user-attachments/assets/54c05efd-7042-4cef-9a4d-a2ea579ac11d" />

2. Tela de Criação de Conta
> *Área para registro de novos administradores.*
![Tela de Registro](<img width="840" height="570" alt="Captura de tela 2026-05-20 134209" src="https://github.com/user-attachments/assets/31fce87e-e28f-41cb-ad21-be13b8bb14bb" />)

3. Painel Administrativo (Vazio)
> *Visão geral do sistema CRUD antes da inserção de dados.*
![Painel CRUD Vazio](<img width="846" height="567" alt="Captura de tela 2026-05-20 134233" src="https://github.com/user-attachments/assets/cd628bc9-3a7d-40c3-9b74-565086449001" />)

4. Adicionando Cliente
> *Preenchimento dos campos para adicionar um novo cliente.*
![Adicionando Cliente](<img width="851" height="568" alt="Captura de tela 2026-05-20 134318" src="https://github.com/user-attachments/assets/83b50c42-5e31-496b-8c7e-628bcbf01c78" />)

5. Cliente Adicionado
> *Tabela atualizada após a primeira inserção.*
![Cliente Adicionado](<img width="846" height="578" alt="Captura de tela 2026-05-20 134342" src="https://github.com/user-attachments/assets/2b0074cd-ca64-4489-85ed-ca55d86f8606" />)

6. Múltiplos Registros
> *Visualização da tabela com vários clientes cadastrados.*
![Múltiplos Registros](<img width="841" height="567" alt="Captura de tela 2026-05-20 134422" src="https://github.com/user-attachments/assets/fec4b5cc-f8f8-4aa4-9f22-96feb7e8a7e9" />)

7. Confirmação de Exclusão
> *Pop-up de segurança exibido antes de deletar um registro.*
![Confirmação de Exclusão](<img width="840" height="566" alt="Captura de tela 2026-05-20 134430" src="https://github.com/user-attachments/assets/e5c9730d-6fa2-4214-8ec5-ed4c866a38a3" />)

**8. Painel Atualizado**
> *Resultado final após a exclusão de um registro.*
![Painel Atualizado](<img width="844" height="566" alt="Captura de tela 2026-05-20 134435" src="https://github.com/user-attachments/assets/f9a7943d-9c50-4a1e-b530-5997134239c2" />)

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Interface Gráfica:** Tkinter (`tkinter`, `ttk`, `messagebox`)
* **Banco de Dados:** MySQL
* **Bibliotecas de Terceiros:**
    * `mysql-connector-python` (Comunicação com o banco de dados)
    * `python-dotenv` (Leitura das variáveis de ambiente)
* **Segurança:** Módulo nativo `hashlib`

---

## Pré-requisitos e Instalação

Para rodar este projeto na sua máquina, siga os passos abaixo:

**1. Clone este repositório:**

git clone (https://github.com/BrunoRodriguesA/Python-Crud)
cd Python-Crud

2. Instale as dependências:
Crie um ambiente virtual (opcional, mas recomendado) e instale as bibliotecas necessárias:
Bash

pip install mysql-connector-python python-dotenv

3. Configure o Banco de Dados (MySQL):
Execute o seguinte script SQL no seu gerenciador de banco de dados (ex: phpMyAdmin, DBeaver, MySQL Workbench) para criar o banco e as tabelas:
SQL

CREATE DATABASE IF NOT EXISTS gestao_comercial;
USE gestao_comercial;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(256) NOT NULL
);

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20)
);

4. Configure as Variáveis de Ambiente:
Crie um arquivo chamado .env na raiz do projeto (mesmo local do script Python) e adicione suas credenciais do MySQL:
Code snippet

HOST=localhost
USER=seu_usuario_mysql
PASSWORD=sua_senha_mysql
DATABASE=gestao_comercial

5. Execute a aplicação:
Bash

python crud.py
