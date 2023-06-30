LIMITE_OPERACAO = 500
LIMITE_SAQUES = 3
MENU = """
Selecione uma operação:
cl - Cadastrar Cliente
co - Criar Conta
lc - Listar Contas
d  - Depósito
s  - Saque
e  - Extrato
q  - Sair

Operação: """

def buscar_cliente(cpf, clientes):
    existente = filter(lambda c: c["cpf"] == cpf, clientes)
    return list(existente)

def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF: ")

    if buscar_cliente(cpf, clientes):
        print("Já existe um cliente com este CPF!")

    else:
        nome = input("Informe o Nome: ")
        clientes.append({"nome": nome, "cpf": cpf})

def criar_conta(numero, clientes):
    cpf = input("Informe o CPF: ")
    cliente = buscar_cliente(cpf, clientes)

    if cliente:
        return {"conta": numero, "cliente": cliente[0]}

    else:
        print("Não existe cliente com o CPF informado!")

def listar_contas(contas):
    for conta in contas:
        print(f"Agência: 001, C/C: {conta['conta']}, Titular: {conta['cliente']['nome']}")

def obter_valor(tipo_valor):
    text = f"Valor de {tipo_valor}: "
    return float(input(text))

def depositar(saldo, deposito, extrato, /):
    saldo += deposito
    mensagem = f"Depositou R$ {deposito:.2f}\n"
    extrato += mensagem
    print(mensagem, end = "")
    return saldo, extrato

def sacar(*, saldo, saque, extrato, saques):
    if saques < LIMITE_SAQUES:
        if saque > LIMITE_OPERACAO:
            print("Seu limite é de R$ 500,00!")

        else:
            if saque > saldo:
                print("Saldo insuficiente!\n")

            else:
                saldo -= saque
                mensagem = f"Sacou R$ {saque:.2f}\n"
                extrato += mensagem
                print(mensagem, end = "")
                saques += 1
    else:
        print("Excedeu o limite de saques diários!\n")

    return saldo, extrato, saques

def exibir_extrato(saldo, /, *, extrato):
    print("\nEXTRATO")

    if extrato == "":
        print("Não houve operações no período!")
    else:
        print(extrato, end = "")
    
    print(f"Saldo de R$ {saldo:.2f}")

def selecionar_operacao():
    saldo, saques = 0, 0
    numero_conta = 1
    extrato, operacao = "", ""
    clientes, contas = [], []

    while operacao != "q":
        try:
            operacao = input(MENU).lower()

        except (KeyboardInterrupt):
            operacao = ""

        if operacao == "cl":
            cadastrar_cliente(clientes)

        elif operacao == "co":
            conta = criar_conta(numero_conta, clientes)

            if conta:
                contas.append(conta)
                numero_conta += 1

        elif operacao == "lc":
            listar_contas(contas)

        elif operacao == "d":
            try:
                deposito = obter_valor("Depósito")
                saldo, extrato = depositar(saldo, deposito, extrato)

            except ValueError or deposito <= 0:
                print("O valor do depósito deve ser positivo!")

        elif operacao == "s":
            saque = obter_valor("Saque")
            saldo, extrato, saques = sacar(
                saldo = saldo,
                saque = saque,
                extrato = extrato,
                saques = saques
            )

        elif operacao == "e":
            exibir_extrato(saldo, extrato=extrato)

        else:
            if operacao != "q":
                print("Informe uma operação válida!\n")

selecionar_operacao()