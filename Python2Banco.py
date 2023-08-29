import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    |  [d]\tDepositar                    |
    |  [s]\tSacar                        |
    |  [e]\tExtrato                      |
    |  [nc]\tNova conta                   |
    |  [lc]\tListar contas                |
    |  [nu]\tNovo usuário                 |
    |  [q]\tSair                         |
    |  [p]\tPIX Transferência            |
    =>>>>> """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\nFalha no depósito! é necessário um valor maior que 0!!")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nFalha ao sacar! Você não tem saldo suficiente para a realização do saque!!")

    elif excedeu_limite:
        print("\nFalha ao sacar! O valor do saque excede o limite!!")

    elif excedeu_saques:
        print("\nFalha ao sacar!! Excedeu o número máximo de saques diário!!")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\nFalha na operação! O valor informado é inválido.")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n=============== EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF *somente número: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nCPF já existente!!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário cadastrado com sucesso!! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break
        
        elif opcao == "p":
            chave = input("Informe a chave PIX (celular ou CPF): ")
            valor = float(input("Informe o valor da transferência PIX: "))
            
            saldo, extrato = pix_transfer(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                chave=chave,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
    )

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

def pix_transfer(*, saldo, valor, extrato, chave, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nFalha na transferência PIX! Você não tem saldo suficiente para realizar a transferência.")

    elif excedeu_limite:
        print("\nFalha na transferência PIX! O valor da transferência excede o limite permitido.")

    elif excedeu_saques:
        print("\nFalha na transferência PIX! Excedeu o número máximo de transferências diárias.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Transferência PIX:\tR$ {valor:.2f} para a chave {chave}\n"
        numero_saques += 1
        print("\n=== Transferência PIX realizada com sucesso! ===")

    else:
        print("\nfalha na operação! O valor informado não é valido!!")
    
    return saldo, extrato

main()