import os
import sys
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, CENTER
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


def carregar_variaveis_de_ambiente():
    """
    Descobre onde o programa está rodando para encontrar o arquivo .env
    Isso é vital para não deixarmos senhas expostas diretamente no código.
    """
    if getattr(sys, 'frozen', False):
        
        diretorio_base = os.path.dirname(sys.executable)
    else:
       
        diretorio_base = os.path.dirname(os.path.abspath(__file__))

    caminho_env = os.path.join(diretorio_base, '.env')
    load_dotenv(caminho_env)


carregar_variaveis_de_ambiente()


def obter_conexao():
    """
    Tenta abrir a 'porta' de comunicação com o MySQL.
    Retorna a conexão aberta se der certo, ou None se falhar.
    """
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        return conexao
    except Error as e:
        messagebox.showerror("Erro de Conexão", f"Ocorreu um erro ao conectar:\n{e}")
        return None

def codificar_senha(senha):
    """
    Transforma a senha em um código embaralhado (Hash SHA-256).
    Isso impede que alguém leia a senha original se invadir o banco.
    """
    return hashlib.sha256(senha.encode()).hexdigest()

# MOTOR DA INTERFACE GRÁFICA (A Janela Principal)

class Application(tk.Tk):
    """
    Esta é a janela principal (a moldura do quadro). 
    Ela não mostra conteúdo próprio, apenas gerencia qual 'Tela' 
    deve aparecer no momento (Login, Registro ou CRUD).
    """
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão Comercial")
        self.geometry("850x550")
        self.resizable(False, False)
            
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for Tela in (TelaLogin, TelaRegistro, TelaCRUD):
            frame = Tela(parent=self.container, controller=self)
            self.frames[Tela] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            

        self.mudar_tela(TelaLogin)

    def mudar_tela(self, classe_tela):
        """Traz a tela desejada para a frente, escondendo as outras."""
        frame = self.frames[classe_tela]
        

        if classe_tela == TelaCRUD:
            frame.atualizar_tabela() 
            
        frame.tkraise()

# TELAS DO SISTEMA

class TelaLogin(tk.Frame):
    """Tela responsável por receber o usuário e senha e verificar no banco."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Login do Sistema", font=("Arial", 20, "bold"), fg="#2c3e50").pack(pady=90),
        
        frame_campos = tk.Frame(self)
        frame_campos.pack(pady=(1,1), anchor=CENTER)
        
        tk.Label(frame_campos, text="Usuário:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_usuario = tk.Entry(frame_campos, font=("Arial", 11), width=30)
        self.ent_usuario.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame_campos, text="Senha:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.ent_senha = tk.Entry(frame_campos, font=("Arial", 11), width=30, show="*")
        self.ent_senha.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Button(self, text="Entrar", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", width=15, command=self.autenticar).pack(pady=20)
        tk.Button(self, text="Não tem conta? Registre-se aqui", font=("Arial", 9, "underline"), fg="#3498db", bd=0, cursor="hand2", command=lambda: controller.mudar_tela(TelaRegistro)).pack()


    def autenticar(self):
        """Lógica executada ao clicar no botão 'Entrar'"""
        usuario = self.ent_usuario.get().strip()
        senha = self.ent_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()

                cursor.execute("SELECT senha FROM usuarios WHERE usuario = %s", (usuario,))
                resultado = cursor.fetchone()
                
                if resultado and resultado[0] == codificar_senha(senha):
                    self.ent_usuario.delete(0, tk.END)
                    self.ent_senha.delete(0, tk.END)
                    self.controller.mudar_tela(TelaCRUD)
                else:
                    messagebox.showerror("Erro", "Usuário ou senha incorretos.")
            except Error as e:
                messagebox.showerror("Erro", f"Erro no banco: {e}")
            finally:
                cursor.close()
                conexao.close()

class TelaRegistro(tk.Frame):
    """Tela responsável por cadastrar um novo usuário de acesso."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Criar Nova Conta", font=("Arial", 20, "bold"), fg="#2c3e50").pack(pady=40)
        
        frame_campos = tk.Frame(self)
        frame_campos.pack(pady=10)
        
        tk.Label(frame_campos, text="Escolha um Usuário:").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_usuario = tk.Entry(frame_campos, font=("Arial", 11), width=30)
        self.ent_usuario.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame_campos, text="Escolha uma Senha:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_senha = tk.Entry(frame_campos, font=("Arial", 11), width=30, show="*")
        self.ent_senha.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Button(self, text="Registrar Conta", font=("Arial", 11, "bold"), bg="#3498db", fg="white", width=15, command=self.registrar).pack(pady=20)
        tk.Button(self, text="Voltar para o Login", font=("Arial", 9, "underline"), fg="#2c3e50", bd=0, cursor="hand2", command=lambda: controller.mudar_tela(TelaLogin)).pack()

    def registrar(self):
        """Lógica executada ao clicar em 'Registrar Conta'"""
        usuario = self.ent_usuario.get().strip()
        senha = self.ent_senha.get().strip()
        
        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
            
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                senha_hash = codificar_senha(senha)

                cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", (usuario, senha_hash))
                conexao.commit()
                
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.ent_usuario.delete(0, tk.END)
                self.ent_senha.delete(0, tk.END)
                self.controller.mudar_tela(TelaLogin)
                
            except Error as e:
                if e.errno == 1062: 
                    messagebox.showerror("Erro", "Este nome de usuário já existe.")
                else:
                    messagebox.showerror("Erro", f"Erro ao registrar: {e}")
            finally:
                cursor.close()
                conexao.close()

class TelaCRUD(tk.Frame):
    """Tela Principal onde acontece a listagem e edição dos dados dos clientes."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.id_selecionado = None

        frame_topo = tk.Frame(self, bg="#2c3e50", height=60)
        frame_topo.pack(fill="x", side="top")
        frame_topo.pack_propagate(False)
        
        tk.Label(frame_topo, text="Painel Administrativo - CRUD", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50").pack(side="left", padx=20)
        tk.Button(frame_topo, text="Sair / Logout", bg="#e74c3c", fg="white", bd=0, padx=10, font=("Arial", 10, "bold"), command=lambda: controller.mudar_tela(TelaLogin)).pack(side="right", padx=20)
        
        frame_lateral = tk.LabelFrame(self, text=" Dados do Cliente ", font=("Arial", 10, "bold"), padx=15, pady=15)
        frame_lateral.pack(side="left", fill="y", padx=20, pady=20)
        
        tk.Label(frame_lateral, text="Nome:").pack(anchor="w", pady=2)
        self.ent_nome = tk.Entry(frame_lateral, width=25)
        self.ent_nome.pack(pady=5)
        
        tk.Label(frame_lateral, text="Email:").pack(anchor="w", pady=2)
        self.ent_email = tk.Entry(frame_lateral, width=25)
        self.ent_email.pack(pady=5)
        
        tk.Label(frame_lateral, text="Telefone:").pack(anchor="w", pady=2)
        self.ent_tel = tk.Entry(frame_lateral, width=25)
        self.ent_tel.pack(pady=5)
        
        tk.Button(frame_lateral, text="Adicionar Novo", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=20, command=self.inserir_dados).pack(pady=15)
        tk.Button(frame_lateral, text="Salvar Alterações", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), width=20, command=self.atualizar_dados).pack(pady=5)
        tk.Button(frame_lateral, text="Excluir Selecionado", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=20, command=self.deletar_dados).pack(pady=5)
        tk.Button(frame_lateral, text="Limpar Campos", bg="#7f8c8d", fg="white", width=20, command=self.limpar_campos).pack(pady=5)

        frame_tabela = tk.Frame(self)
        frame_tabela.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.tabela = ttk.Treeview(frame_tabela, columns=("id", "nome", "email", "telefone"), show="headings")
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("email", text="Email")
        self.tabela.heading("telefone", text="Telefone")
        
        self.tabela.column("id", width=40, anchor="center")
        self.tabela.column("nome", width=150)
        self.tabela.column("email", width=150)
        self.tabela.column("telefone", width=100)
        
        self.tabela.pack(fill="both", expand=True)
        self.tabela.bind("<<TreeviewSelect>>", self.pegar_linha_selecionada)

    #  LÓGICAS DO CRUD
    
    def atualizar_tabela(self):
        """READ: Busca os clientes no banco e exibe na interface visual."""
        for i in self.tabela.get_children():
            self.tabela.delete(i)
            
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT id, nome, email, telefone FROM clientes")

                for linha in cursor.fetchall():
                    self.tabela.insert("", "end", values=linha)
            except Error as e:
                print(f"Erro ao listar: {e}")
            finally:
                cursor.close()
                conexao.close()

    def inserir_dados(self):
        """CREATE: Insere um novo cliente no banco de dados."""
        nome, email, tel = self.ent_nome.get().strip(), self.ent_email.get().strip(), self.ent_tel.get().strip()
        
        if not nome or not email:
            messagebox.showwarning("Aviso", "Nome e Email são obrigatórios!")
            return
            
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)", (nome, email, tel))
                conexao.commit()
                
                self.limpar_campos()
                self.atualizar_tabela()
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao inserir: {e}")
            finally:
                cursor.close()
                conexao.close()

    def pegar_linha_selecionada(self, event):
        """Evento acionado quando o usuário clica em uma linha da tabela."""
        item_selecionado = self.tabela.selection()
        if item_selecionado:

            valores = self.tabela.item(item_selecionado, "values")
             
            self.limpar_campos()
            
            self.id_selecionado = valores[0]

            self.ent_nome.insert(0, valores[1])
            self.ent_email.insert(0, valores[2])
            self.ent_tel.insert(0, valores[3])

    def atualizar_dados(self):
        """UPDATE: Atualiza um cliente existente baseado no ID selecionado."""
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela primeiro!")
            return
            
        nome, email, tel = self.ent_nome.get().strip(), self.ent_email.get().strip(), self.ent_tel.get().strip()
        
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("UPDATE clientes SET nome=%s, email=%s, telefone=%s WHERE id=%s", (nome, email, tel, self.id_selecionado))
                conexao.commit()
                
                messagebox.showinfo("Sucesso", "Dados alterados com sucesso!")
                self.limpar_campos()
                self.atualizar_tabela()
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao alterar: {e}")
            finally:
                cursor.close()
                conexao.close()

    def deletar_dados(self):
        """DELETE: Remove o cliente selecionado do banco."""
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela primeiro!")
            return

        if messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este cliente?"):
            conexao = obter_conexao()
            if conexao:
                try:
                    cursor = conexao.cursor()
                    cursor.execute("DELETE FROM clientes WHERE id=%s", (self.id_selecionado,))
                    conexao.commit()
                    
                    self.limpar_campos()
                    self.atualizar_tabela()
                except Error as e:
                    messagebox.showerror("Erro", f"Erro ao deletar: {e}")
                finally:
                    cursor.close()
                    conexao.close()

    def limpar_campos(self):
        """Remove todo o texto das caixas de entrada e solta a seleção do ID."""
        self.ent_nome.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.ent_tel.delete(0, tk.END)
        self.id_selecionado = None

# INICIALIZAÇÃO

if __name__ == "__main__":
    app = Application()
    app.mainloop()