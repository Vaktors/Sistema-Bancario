menu = '''
===================

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

===================
'''
saldo = 0
limite = 500
extrato = []
limiteSaques = 3

while True:
    opcao = input(menu)
    if opcao == 'd': # Sistema de deposito
        while True:
            print('\nDepósito')
            print(f'Saldo: R$ {saldo:.2f}')
            valor = input('Digite o valor do depósito ou "q" para sair: ')
            if valor == 'q':
                break
            if float(valor.replace(',', '.'))<0: # Checagem de valor negativo
                print('Valor inválido! Por favor digite um valor positivo.')
            else: 
                saldo += float(valor.replace(',', '.'))
                extrato.append(f'Depósito de R$ {float(valor.replace(',', '.')):.2f}')
                print('Depósito realizado com sucesso!')
                saida = input('Digite "q" para voltar ao menu...')
            if saida == 'q':
                saida = ''
                break
    elif opcao == 's': # Sistema de saque
        while True:
            print('\nSaque')
            print(f'Saldo: R$ {saldo:.2f}')
            print(f'Limite de saques restantes: {limiteSaques}')
            if limiteSaques == 0:#Checagem de limite de saques diario
                print('Limite de saques diario atingido!')
                saida = input('Digite "q" para voltar ao menu...')
            if saida == 'q':
                saida = ''
                break
            if saldo == 0: #Checagem de saldo
                print('Saldo insuficiente!')
                saida = input('Digite "q" para voltar ao menu...')
            if saida == 'q':
                saida = ''
                break
            valor = input('Digite o valor do saque ou "q" para sair: ')
            if valor == 'q':
                break
            if saldo >= float(valor.replace(',', '.')) and float(valor.replace(',', '.')) > 0 and float(valor.replace(',', '.')) <= 500: #  Checagem de saldo e limite
                saldo -= float(valor.replace(',', '.'))
                extrato.append(f'Saque de R$ {float(valor.replace(',', '.')):.2f}')
                limiteSaques -= 1
                print('Saque realizado com sucesso!')
                saida = input('Digite "q" para voltar ao menu...')
            if saida == 'q':
                saida = ''
                break
            else:
                print('Saldo insuficiente ou fora do limite (R$500.00)!')
    elif opcao == 'e':
        while True:
            print('\nExtrato')
            print(f'Saldo: R$ {saldo:.2f}')
            print(f'Limite: R$ {limite}')
            print(f'Saques disponiveis: {limiteSaques}')
            print('Extrato:')
            for operacao in extrato: #print de cada saque ou deposito feito
                print(operacao)
            print('Fim do extrato\n\n')
            saida = input('Digite "q" para voltar ao menu...')
            if saida == 'q':
                saida = ''	
                break
    elif opcao == 'q':
        print('Saindo...')
        break
    else:
        print('Opção inválida!')
