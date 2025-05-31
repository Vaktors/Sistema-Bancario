menu = '''
===================

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

===================
'''

usuarios = {}  # chave: cpf, valor: dados do usuário
contas = {}    # chave: numero da conta, valor: dados da conta
cpfs_cadastrados = set()
proximo_numero_conta = 1  # começa em 1

def gerar_numero_conta():
    global proximo_numero_conta
    numero = str(proximo_numero_conta)  # sem zeros à esquerda
    proximo_numero_conta += 1
    return numero

def cadastrar_usuario():
    print('\n=== Cadastro de Usuário ===')
    nome = input('Nome: ')
    data_nascimento = input('Data de nascimento (DD/MM/AAAA): ')
    cpf = input('CPF (apenas números): ')
    if cpf in cpfs_cadastrados:
        print('Já existe um usuário cadastrado com esse CPF!')
        return False
    logradouro = input('Logradouro: ')
    numero = input('Número: ')
    bairro = input('Bairro: ')
    cidade = input('Cidade: ')
    estado = input('UF: ')
    endereco = f'{logradouro}, {numero} - {bairro} - {cidade}/{estado}'
    usuarios[cpf] = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    cpfs_cadastrados.add(cpf)
    print('Usuário cadastrado com sucesso!')
    return True

def criar_conta():
    print('\n=== Criação de Conta Corrente ===')
    cpf = input('Informe o CPF do usuário: ')
    if cpf not in usuarios:
        print('Usuário não encontrado. Cadastre o usuário primeiro.')
        return False
    senha = input('Defina uma senha para a conta: ')
    numero_conta = gerar_numero_conta()
    contas[numero_conta] = {
        'agencia': '0001',
        'numero_conta': numero_conta,
        'cpf': cpf,
        'senha': senha,
        'saldo': 0,
        'extrato': [],
        'limiteSaques': 3
    }
    print(f'Conta criada com sucesso! Agência: 0001 Conta: {numero_conta}')
    return True

def login():
    print('\n=== Login ===')
    numero_conta = input('Número da conta: ')
    senha = input('Senha: ')
    conta = contas.get(numero_conta)
    if conta and conta['senha'] == senha:
        usuario = usuarios[conta['cpf']]
        print(f'Bem-vindo, {usuario["nome"]}! Agência: {conta["agencia"]} Conta: {conta["numero_conta"]}')
        return numero_conta
    else:
        print('Conta ou senha inválidos!')
        return None

def depositar(conta):
    print('\nDepósito')
    print(f'Saldo: R$ {conta["saldo"]:.2f}')
    while True:
        valor = input('Digite o valor do depósito: ')
        if float(valor.replace(',', '.')) <= 0:
            print('Valor inválido! Por favor digite um valor positivo.')
        else:
            conta['saldo'] += float(valor.replace(',', '.'))
            conta['extrato'].append(f'Depósito de R$ {float(valor.replace(",", ".")):.2f}')
            print('Depósito realizado com sucesso!')
            break

def sacar(conta):
    print('\nSaque')
    print(f'Saldo: R$ {conta["saldo"]:.2f}')
    print(f'Limite de saques restantes: {conta["limiteSaques"]}')
    if conta['limiteSaques'] == 0:
        print('Limite de saques diário atingido!')
    elif conta['saldo'] == 0:
        print('Saldo insuficiente!')
    else:
        valor = input('Digite o valor do saque: ')
        valor_float = float(valor.replace(',', '.'))
        if conta['saldo'] >= valor_float and 0 < valor_float <= 500:
            conta['saldo'] -= valor_float
            conta['extrato'].append(f'Saque de R$ {valor_float:.2f}')
            conta['limiteSaques'] -= 1
            print('Saque realizado com sucesso!')
        else:
            print('Saldo insuficiente ou fora do limite (R$500.00)!')

def exibir_extrato(conta):
    print('\nExtrato')
    print(f'Saldo: R$ {conta["saldo"]:.2f}')
    print(f'Saques disponíveis: {conta["limiteSaques"]}')
    print('Extrato:')
    for operacao in conta['extrato']:
        print(operacao)
    print('Fim do extrato\n\n')

def saida():
    saida = input('Digite "q" para voltar ao menu...')
    return saida == 'q'

# Menu principal
while True:
    print('\n=== Sistema Bancário ===')
    print('[u] Cadastrar usuário')
    print('[n] Nova conta corrente')
    print('[l] Login')
    print('[q] Sair')
    escolha = input('Escolha uma opção: ')
    if escolha == 'u':
        cadastrar_usuario()
    elif escolha == 'n':
        criar_conta()
    elif escolha == 'l':
        numero_conta_logada = login()
        if numero_conta_logada:
            conta = contas[numero_conta_logada]
            while True:
                opcao = input(menu)
                if opcao == 'd':
                    depositar(conta)
                    if saida():
                        continue  # volta para o menu da conta logada
                elif opcao == 's':
                    sacar(conta)
                    if saida():
                        continue
                elif opcao == 'e':
                    exibir_extrato(conta)
                    if saida():
                        continue
                elif opcao == 'q':
                    print('Saindo da conta...')
                    break  # volta para o menu principal
                else:
                    print('Opção inválida!')
    elif escolha == 'q':
        print('Saindo do sistema...')
        break
    else:
        print('Opção inválida!')