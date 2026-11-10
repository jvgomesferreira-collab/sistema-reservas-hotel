from models import Cliente, Quarto, Suite, Reserva
import json 

lista_clientes = []
lista_quartos = []
lista_reservas = []

def salvar_dados():
    dados = {
        "clientes": [cliente.to_dict() for cliente in lista_clientes],
        "quartos": [quarto.to_dict() for quarto in lista_quartos],
        "reservas": [reserva.to_dict() for reserva in lista_reservas]
    }
    with open("dados_hotel.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)
        
def carregar_dados():
    global lista_clientes, lista_quartos, lista_reservas
    
    try:
        with open("dados_hotel.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            
        for c in dados["clientes"]:
            lista_clientes.append(Cliente(c["nome"], c["cpf"], c["telefone"], c["email"]))
            
        for q in dados["quartos"]:
            if q["tipo"] == "Suite":
                lista_quartos.append(Suite(q["numero"], q["capacidade"]))
            else:
                lista_quartos.append(Quarto(q["numero"], q["capacidade"]))
                
        for r in dados["reservas"]:
            cliente_real = next((c for c in lista_clientes if c.cpf == r["cliente"]["cpf"]), None)
            quarto_real = next((q for q in lista_quartos if q.numero == r["quarto"]["numero"]), None)
            
            # Se encontrou os dois, recria a reserva
            if cliente_real and quarto_real:
                nova_reserva = Reserva(
                    r["data_entrada"], 
                    r["data_saida"], 
                    quarto_real, 
                    cliente_real, 
                    r["status"], 
                    r["forma_pagamento"]
                )
                lista_reservas.append(nova_reserva)
                
        print("Dados carregados com sucesso!")
        
    except FileNotFoundError:
        # Se o arquivo não existir (primeira vez rodando), ignora e começa vazio
        pass 

def cadastrar_cliente():
    print("\n --- Cadastro de Cliente --- ")
    nome = input("Digite seu nome: ")
    cpf = input("Digite seu CPF: ")
    telefone = input("DIgite seu telefone: ")
    email = input("Digite seu email: ")
    
    novo_cliente = Cliente(nome, cpf, telefone, email)
    lista_clientes.append(novo_cliente)
    print("Cliente cadastrado com sucesso!")
    
def cadastrar_quarto():
    print("\n --- Cadastro de Quarto ---")
    tipo = input("Seu quarto é uma suíte(S) ou um quarto comum (C)? ").upper()
    numero = input("Qual o número do quarto?: ")
    capacidade = int(input("Digite a capacidade (número de pessoas): "))
    
    if tipo == "S":
        nova_suite = Suite(numero, capacidade)
        lista_quartos.append(nova_suite)
        print("Suíte cadastrada com sucesso!")
    else:
        novo_quarto = Quarto(numero, capacidade)
        lista_quartos.append(novo_quarto)
        print("Quarto comum cadastrado com sucesso!")
        
def cadastrar_reserva():
    global lista_reservas
    print("\n --- Cadastro de Reserva ---")
    
    cpf_busca = input("Digite o cpf do cliente: ")
    cliente_encontrado = None
    
    # 1. Busca o cliente
    for cliente in lista_clientes:
        if cliente.cpf == cpf_busca:
            cliente_encontrado = cliente
            break
            
    # 2. Se achou o cliente, continua a reserva
    if cliente_encontrado:
        numero_quarto = input("Digite o número do quarto desejado: ")
        
        # AQUI criamos a variável antes de usar
        quarto_encontrado = None 
        
        # 3. Busca o quarto
        for quarto in lista_quartos:
            if quarto.numero == numero_quarto:
                quarto_encontrado = quarto
                break
                
        # Print de debug para você ver se achou o quarto
        print(f"DEBUG: O quarto foi encontrado? {quarto_encontrado}")
        
        # 4. Se achou o quarto, pede as datas
        if quarto_encontrado:
            data_entrada = input("Digite a data de entrada (DD/MM/AAAA): ")
            data_saida = input("Digite a data de saída (DD/MM/AAAA): ")
            
            try:
                nova_reserva = Reserva(data_entrada, data_saida, quarto_encontrado, cliente_encontrado, "Ativa", "Cartão")
                lista_reservas.append(nova_reserva)
                print(f"Reserva realizada com sucesso! Valor total: R$ {nova_reserva.valor_total:.2f}")
            except ValueError:
                print("Erro: Data inválida! Use o formato DD/MM/AAAA.")
        else:
            print("Quarto não encontrado.")
            
    # 5. Se não achou o cliente, avisa (Este else fica alinhado com o if da linha 16)
    else:
        print("Erro: Cliente não encontrado. Cadastre o cliente primeiro.")
                
                
def listar_reservas():
        print("\n--- Lista de Reservas ---")
        if not lista_reservas:
           print("Nenhuma reserva cadastrada.")
        else:
            for reserva in lista_reservas:
                print(reserva)
         
def menu():
    while True:
        print("\n === SISTEMA DE RESERVAS ===")
        print("1. Cadastrar Cliente")
        print("2. Cadastrar Quarto")
        print("3. Realizar Reserva")
        print("4. Listar Reservas")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            cadastrar_quarto()
        elif opcao == "3":
            cadastrar_reserva()
        elif opcao == "4":
            listar_reservas()
        elif opcao == "5":
            salvar_dados()
            print("Saindo...")
            break
        else:
            print("Opção Inválida.")
    
if __name__ == "__main__":
    carregar_dados()
    menu()
        
        