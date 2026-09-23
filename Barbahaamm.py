import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Barbahaamm - Acesso")
janela.geometry("400x350")
janela.resizable(False, False)

clientes = []
barbearias = []
agendamentos = []

def mensagem(titulo, texto):
    messagebox.showinfo(titulo, texto)

def formatar_horarios(horarios):
    return "\n".join(
        f"{periodo}: {dados['Abertura']} as {dados['Fechamento']}"
        for periodo, dados in horarios.items()
    )


def voltar(janela_atual, anterior=None):
    janela_atual.destroy()
    if anterior:
        anterior.deiconify()


def tela_agendamentos(email):
    tela = ctk.CTkToplevel(janela)
    tela.title("Meus Agendamentos")
    tela.geometry("600x550")

    ctk.CTkLabel(
        tela, text="Meus Agendamentos",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    lista = ctk.CTkScrollableFrame(tela, width=520, height=380)
    lista.pack(fill="both", expand=True, padx=20, pady=10)

    meus = [
        item for item in agendamentos
        if item["Email"] == email
    ]

    def cancelar(item):
        if messagebox.askyesno(
            "Cancelar", "Deseja cancelar este agendamento?"
        ):
            agendamentos.remove(item)
            tela.destroy()
            tela_agendamentos(email)

    if not meus:
        ctk.CTkLabel(
            lista, text="Nenhum agendamento encontrado."
        ).pack(pady=30)

    for item in meus:
        cartao = ctk.CTkFrame(lista)
        cartao.pack(fill="x", pady=8, padx=5)

        texto = (
            f"{item['Barbearia']}\n"
            f"{item['Barbeiro']} - {item['Horario']}"
        )

        ctk.CTkLabel(
            cartao, text=texto, justify="left"
        ).pack(side="left", padx=15, pady=15)

        ctk.CTkButton(
            cartao, text="Cancelar",
            width=90, fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=lambda a=item: cancelar(a)
        ).pack(side="right", padx=15)


def tela_barbearia(principal, barbearia, email):
    principal.withdraw()

    tela = ctk.CTkToplevel(janela)
    tela.title(barbearia["nome"])
    tela.geometry("650x600")

    def fechar():
        tela.destroy()
        principal.deiconify()

    tela.protocol("WM_DELETE_WINDOW", fechar)

    conteudo = ctk.CTkScrollableFrame(tela, width=590, height=530)
    conteudo.pack(fill="both", expand=True, padx=15, pady=15)

    ctk.CTkLabel(
        conteudo, text=barbearia["nome"],
        font=("Arial", 24, "bold")
    ).pack(pady=10)

    ctk.CTkLabel(
        conteudo,
        text=f"Localização: {barbearia['bairro']}\n\n"
             f"{barbearia.get('informacoes', '')}",
        justify="left"
    ).pack(pady=10)

    ctk.CTkLabel(
        conteudo, text="Escolha o barbeiro",
        font=("Arial", 17, "bold")
    ).pack(pady=10)

    barbeiro = tk.StringVar(value="Barbeiro 1")

    for nome in ["Barbeiro 1", "Barbeiro 2", "Barbeiro 3"]:
        ctk.CTkButton(
            conteudo, text=nome,
            command=lambda valor=nome: barbeiro.set(valor)
        ).pack(pady=5)

    ctk.CTkLabel(
        conteudo, text="Escolha o horário",
        font=("Arial", 17, "bold")
    ).pack(pady=15)

    horario = tk.StringVar(value="")

    horarios = [
        "08:00 às 08:40", "08:50 às 09:30",
        "12:00 às 12:40", "12:50 às 13:30",
        "18:00 às 18:40", "18:50 às 19:30"
    ]

    for h in horarios:
        ctk.CTkButton(
            conteudo, text=h,
            command=lambda valor=h: horario.set(valor)
        ).pack(pady=4)

    ctk.CTkLabel(
        conteudo, textvariable=horario,
        text_color="#4DA3FF"
    ).pack(pady=10)

    def agendar():
        if not horario.get():
            messagebox.showwarning(
                "Atenção", "Escolha um horário."
            )
            return

        novo = {
            "Email": email,
            "Barbearia": barbearia["nome"],
            "Barbeiro": barbeiro.get(),
            "Horario": horario.get()
        }

        agendamentos.append(novo)

        mensagem(
            "Sucesso",
            "Agendamento realizado com sucesso!"
        )

        horario.set("")

    ctk.CTkButton(
        conteudo, text="Agendar",
        command=agendar
    ).pack(pady=15)

    ctk.CTkButton(
        conteudo, text="Meus Agendamentos",
        command=lambda: tela_agendamentos(email)
    ).pack(pady=5)


def tela_principal(email):
    janela.withdraw()

    tela = ctk.CTkToplevel(janela)
    tela.title("Barbahaamm")
    tela.geometry("700x600")

    def sair():
        tela.destroy()
        janela.destroy()

    tela.protocol("WM_DELETE_WINDOW", sair)

    topo = ctk.CTkFrame(tela)
    topo.pack(fill="x")

    ctk.CTkLabel(
        topo, text="Barbahaamm",
        font=("Arial", 25, "bold")
    ).pack(side="left", padx=20, pady=20)

    ctk.CTkButton(
        topo, text="Agendamentos",
        command=lambda: tela_agendamentos(email)
    ).pack(side="right", padx=10, pady=20)

    conteudo = ctk.CTkFrame(tela, fg_color="transparent")
    conteudo.pack(fill="both", expand=True, padx=25, pady=20)

    ctk.CTkLabel(
        conteudo, text="Encontre sua barbearia",
        font=("Arial", 22, "bold")
    ).pack(anchor="w", pady=10)

    lista = ctk.CTkScrollableFrame(
        conteudo, width=620, height=400
    )
    lista.pack(fill="both", expand=True)

    fixas = [
        {
            "nome": "Porva Barbearia",
            "bairro": "Guará II - QE 26",
            "horario": "06:00 às 19:30"
        },
        {
            "nome": "Barbearia Pente Fino",
            "bairro": "Jardim Botânico",
            "horario": "12:00 às 18:00"
        },
        {
            "nome": "Barba+",
            "bairro": "Samambaia Sul",
            "horario": "06:00 às 18:00"
        }
    ]

    todas = fixas + barbearias

    for barbearia in todas:
        cartao = ctk.CTkFrame(lista)
        cartao.pack(fill="x", pady=8, padx=5)

        informacoes = (
            f"{barbearia['nome']}\n"
            f"{barbearia['bairro']}\n"
            f"{barbearia['horario']}"
        )

        ctk.CTkLabel(
            cartao, text=informacoes,
            justify="left"
        ).pack(side="left", padx=15, pady=15)

        ctk.CTkButton(
            cartao, text="Ver", width=80,
            command=lambda b=barbearia:
            tela_barbearia(tela, b, email)
        ).pack(side="right", padx=15)

    ctk.CTkButton(
        conteudo, text="Sair",
        fg_color="#D32F2F",
        hover_color="#B71C1C",
        command=sair
    ).pack(fill="x", pady=15)


def cadastro_barbearia(anterior):
    anterior.destroy()

    tela = ctk.CTkToplevel(janela)
    tela.title("Cadastro de Barbearia")
    tela.geometry("500x850")

    campos = {}

    for nome in [
        "Nome da Barbearia", "Localização",
        "Email", "Telefone", "CNPJ"
    ]:
        ctk.CTkLabel(tela, text=nome).pack(pady=(8, 0))
        campos[nome] = ctk.CTkEntry(tela, width=320)
        campos[nome].pack(pady=4)

    ctk.CTkLabel(tela, text="Informações").pack(pady=8)

    informacoes = ctk.CTkTextbox(tela, width=320, height=60)
    informacoes.pack()

    ctk.CTkLabel(
        tela, text="Horários de Funcionamento",
        font=("Arial", 15, "bold")
    ).pack(pady=10)

    horarios = {}

    for periodo in ["Manhã", "Tarde", "Noite"]:
        ctk.CTkLabel(tela, text=periodo).pack()

        abertura = ctk.CTkEntry(
            tela, width=100, placeholder_text="08:00"
        )
        abertura.pack(pady=3)

        fechamento = ctk.CTkEntry(
            tela, width=100, placeholder_text="12:00"
        )
        fechamento.pack(pady=3)

        horarios[periodo] = {
            "Abertura": abertura,
            "Fechamento": fechamento
        }

    def salvar():
        dados = {
            nome: campo.get().strip()
            for nome, campo in campos.items()
        }

        if any(not valor for valor in dados.values()):
            messagebox.showwarning(
                "Atenção", "Preencha todos os campos."
            )
            return

        horarios_salvos = {}

        for periodo, campos_horario in horarios.items():
            abertura = campos_horario["Abertura"].get().strip()
            fechamento = campos_horario["Fechamento"].get().strip()

            if not abertura or not fechamento:
                messagebox.showwarning(
                    "Atenção",
                    f"Preencha o horário da {periodo.lower()}."
                )
                return

            horarios_salvos[periodo] = {
                "Abertura": abertura,
                "Fechamento": fechamento
            }

        nova = {
            "nome": dados["Nome da Barbearia"],
            "bairro": dados["Localização"],
            "horario": formatar_horarios(horarios_salvos),
            "informacoes": informacoes.get("1.0", "end").strip()
        }

        barbearias.append(nova)

        mensagem(
            "Sucesso",
            "Barbearia cadastrada com sucesso!"
        )

        tela.destroy()
        tela_principal(dados["Email"])

    ctk.CTkButton(
        tela, text="Enviar Solicitação",
        command=salvar
    ).pack(pady=15)


def cadastro_cliente(anterior):
    anterior.destroy()

    tela = ctk.CTkToplevel(janela)
    tela.title("Cadastro de Cliente")
    tela.geometry("400x650")

    campos = {}

    for nome in [
        "Nome", "Email", "Data de Nascimento",
        "Telefone", "Senha"
    ]:
        ctk.CTkLabel(tela, text=nome).pack(pady=(8, 0))

        campo = ctk.CTkEntry(
            tela, width=280,
            show="*" if nome == "Senha" else ""
        )

        campo.pack(pady=4)
        campos[nome] = campo

    def salvar():
        dados = {
            nome: campo.get().strip()
            for nome, campo in campos.items()
        }

        if any(not valor for valor in dados.values()):
            messagebox.showwarning(
                "Atenção", "Preencha todos os campos."
            )
            return

        clientes.append(dados)

        mensagem(
            "Sucesso",
            "Cliente cadastrado com sucesso!"
        )

        tela.destroy()

    ctk.CTkButton(
        tela, text="Cadastrar",
        command=salvar
    ).pack(pady=20)

    ctk.CTkButton(
        tela, text="Voltar",
        fg_color="#D32F2F",
        hover_color="#B71C1C",
        command=tela.destroy
    ).pack()


def cadastro():
    tela = ctk.CTkToplevel(janela)
    tela.title("Criar Conta")
    tela.geometry("400x350")

    ctk.CTkLabel(
        tela, text="Escolha o tipo de conta",
        font=("Arial", 20, "bold")
    ).pack(pady=30)

    ctk.CTkButton(
        tela, text="Conta Barbearia",
        command=lambda: cadastro_barbearia(tela)
    ).pack(pady=10)

    ctk.CTkButton(
        tela, text="Conta de Cliente",
        command=lambda: cadastro_cliente(tela)
    ).pack(pady=10)


def entrar():
    email = campo_email.get().strip().lower()
    senha = campo_senha.get().strip()

    if email == "admin@gmail.com" and senha == "1234":
        tela_principal(email)
        return

    for cliente in clientes:
        if (
            cliente["Email"].lower() == email
            and cliente["Senha"] == senha
        ):
            tela_principal(email)
            return

    messagebox.showerror(
        "Erro", "Email ou senha incorretos."
    )


# LOGIN

ctk.CTkLabel(
    janela, text="Barbahaamm",
    font=("Arial", 25, "bold")
).pack(pady=20)

ctk.CTkLabel(janela, text="Email").pack()

campo_email = ctk.CTkEntry(
    janela, width=250,
    placeholder_text="Digite seu email"
)
campo_email.pack(pady=5)

ctk.CTkLabel(janela, text="Senha").pack()

campo_senha = ctk.CTkEntry(
    janela, width=250,
    show="*",
    placeholder_text="Digite sua senha"
)
campo_senha.pack(pady=5)

ctk.CTkButton(
    janela, text="Entrar",
    command=entrar
).pack(pady=15)

ctk.CTkButton(
    janela, text="Criar Conta",
    command=cadastro
).pack()

janela.mainloop()