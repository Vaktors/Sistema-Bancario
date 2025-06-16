import abc
from abc import ABC

# --- CLASSES DE TRANSAÇÃO E HISTÓRICO ---

class Transacao(ABC):
    """Classe abstrata para todas as transações."""
    @property
    @abc.abstractproperty
    def valor(self):
        pass

    @abc.abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    """Representa uma transação de saque."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f'Saque de R$ {self.valor:.2f}'

class Deposito(Transacao):
    """Representa uma transação de depósito."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f'Depósito de R$ {self.valor:.2f}'

class Historico:
    """Gerencia o histórico de transações de uma conta."""
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

# --- CLASSES DE CONTA ---

class Conta:
    """Classe base para contas bancárias."""
    def __init__(self, numero, cliente, senha):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        self._senha = senha # Mantido para não alterar a funcionalidade de login

    @classmethod
    def nova_conta(cls, cliente, numero, senha):
        return cls(numero, cliente, senha)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    @property
    def senha(self):
        return self._senha

    def sacar(self, valor):
        """Realiza o saque se houver saldo."""
        if valor > self.saldo:
            print("Operação falhou! Saldo insuficiente.")
            return False
        elif valor > 0:
            self._saldo -= valor
            #print("Saque realizado com sucesso!") # A mensagem agora é na função principal
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

    def depositar(self, valor):
        """Realiza o depósito de um valor positivo."""
        if valor > 0:
            self._saldo += valor
            #print("Depósito realizado com sucesso!") # A mensagem agora é na função principal
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

class ContaCorrente(Conta):
    """Representa uma conta corrente, com limites específicos."""
    def __init__(self, numero, cliente, senha, limite=500, limite_saques=3):
        super().__init__(numero, cliente, senha)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """Sobrescreve o método sacar para incluir regras da conta corrente."""
        saques_realizados = len(
            [transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)]
        )

        if valor > self._limite:
            print(f"Operação falhou! O valor do saque excede o limite (R$ {self._limite:.2f}).")
            return False
        elif saques_realizados >= self._limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False
        else:
            # Chama o método sacar da classe pai (Conta) para verificar o saldo
            return super().sacar(valor)
    
    @property
    def limite_saques_restantes(self):
        saques_realizados = len(
            [transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)]
        )
        return self._limite_saques - saques_realizados


# --- CLASSES DE CLIENTE ---

class Cliente:
    """Classe base para clientes do banco."""
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    """Representa um cliente do tipo Pessoa Física."""
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


# --- FUNÇÕES PRINCIPAIS DO SISTEMA (Interface com o Usuário) ---

def buscar_cliente(cpf, clientes):
    """Busca um cliente na lista pelo CPF."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def buscar_conta(numero_conta, contas):
    """Busca uma conta na lista pelo número."""
    contas_filtradas = [conta for conta in contas if conta.numero == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None

def cadastrar_usuario(clientes):
    """Cadastra um novo usuário (PessoaFisica)."""
    print('\n=== Cadastro de Usuário ===')
    cpf = input('CPF (apenas números): ')
    cliente = buscar_cliente(cpf, clientes)
    if cliente:
        print('Já existe um usuário cadastrado com esse CPF!')
        return

    nome = input('Nome: ')
    data_nascimento = input('Data de nascimento (DD/MM/AAAA): ')
    logradouro = input('Logradouro: ')
    numero = input('Número: ')
    bairro = input('Bairro: ')
    cidade = input('Cidade: ')
    estado = input('UF: ')
    endereco = f'{logradouro}, {numero} - {bairro} - {cidade}/{estado}'

    novo_cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(novo_cliente)
    print('Usuário cadastrado com sucesso!')

def criar_conta(contas, clientes, proximo_numero_conta):
    """Cria uma nova conta corrente para um cliente existente."""
    print('\n=== Criação de Conta Corrente ===')
    cpf = input('Informe o CPF do usuário: ')
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print('Usuário não encontrado. Cadastre o usuário primeiro.')
        return None, proximo_numero_conta
    
    senha = input('Defina uma senha para a conta: ')
    
    # Gera o número da conta e já o incrementa para a próxima chamada
    numero_conta = str(proximo_numero_conta)
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, senha=senha)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(f'Conta criada com sucesso! Agência: {conta.agencia} Conta: {conta.numero}')
    return conta, proximo_numero_conta + 1

def login(contas):
    """Realiza o login na conta."""
    print('\n=== Login ===')
    numero_conta = input('Número da conta: ')
    senha = input('Senha: ')
    
    conta = buscar_conta(numero_conta, contas)
    
    if conta and conta.senha == senha:
        print(f'Bem-vindo, {conta.cliente.nome}! Agência: {conta.agencia} Conta: {conta.numero}')
        return conta
    else:
        print('Conta ou senha inválidos!')
        return None

def operacao_depositar(conta):
    """Interface para a operação de depósito."""
    print('\nDepósito')
    print(f'Saldo: R$ {conta.saldo:.2f}')
    valor_str = input('Digite o valor do depósito: ')
    
    try:
        valor = float(valor_str.replace(',', '.'))
        if valor <= 0:
            print('Valor inválido! Por favor digite um valor positivo.')
        else:
            deposito = Deposito(valor)
            deposito.registrar(conta) # A classe Deposito chama o método conta.depositar()
            print('Depósito realizado com sucesso!')
    except ValueError:
        print("Valor inválido! Digite um número.")


def operacao_sacar(conta_logada):
    """Interface para a operação de saque."""
    print('\nSaque')
    print(f'Saldo: R$ {conta_logada.saldo:.2f}')
    
    # Verifica se a conta é uma ContaCorrente para mostrar os saques restantes
    if isinstance(conta_logada, ContaCorrente):
        print(f'Limite de saques restantes: {conta_logada.limite_saques_restantes}')

    valor_str = input('Digite o valor do saque: ')
    try:
        valor = float(valor_str.replace(',', '.'))
        saque = Saque(valor)
        # O método registrar da classe Saque contém toda a lógica de validação
        saque.registrar(conta_logada) 
        # A mensagem de sucesso/erro já é impressa dentro dos métodos de saque
    except ValueError:
        print("Valor inválido! Digite um número.")


def exibir_extrato(conta):
    """Exibe o extrato da conta."""
    print('\nExtrato')
    print(f"Cliente: {conta.cliente.nome}")
    print(f"Agência: {conta.agencia} | Conta: {conta.numero}")
    print("-" * 30)
    
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(transacao) # Usa o __str__ de Saque ou Deposito
            
    print("-" * 30)
    print(f'Saldo: R$ {conta.saldo:.2f}')
    if isinstance(conta, ContaCorrente):
         print(f'Saques restantes hoje: {conta.limite_saques_restantes}')
    print('Fim do extrato\n')


def saida():
    """Aguarda o usuário pressionar 'q' para continuar."""
    input('Pressione Enter para voltar ao menu...')


# --- BLOCO PRINCIPAL (EXECUÇÃO) ---

def main():
    clientes = []
    contas = []
    proximo_numero_conta = 1

    menu_principal = """
    === Sistema Bancário ===
    [u] Cadastrar usuário
    [n] Nova conta corrente
    [l] Login
    [q] Sair
    Escolha uma opção: """

    menu_conta = """
    ===================

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair da Conta

    ===================
    """

    while True:
        escolha = input(menu_principal)
        if escolha == 'u':
            cadastrar_usuario(clientes)
        elif escolha == 'n':
            _, proximo_numero_conta = criar_conta(contas, clientes, proximo_numero_conta)
        elif escolha == 'l':
            conta_logada = login(contas)
            if conta_logada:
                while True:
                    opcao = input(menu_conta)
                    if opcao == 'd':
                        operacao_depositar(conta_logada)
                        saida()
                    elif opcao == 's':
                        operacao_sacar(conta_logada)
                        saida()
                    elif opcao == 'e':
                        exibir_extrato(conta_logada)
                        saida()
                    elif opcao == 'q':
                        print('Saindo da conta...')
                        break
                    else:
                        print('Opção inválida!')
        elif escolha == 'q':
            print('Saindo do sistema...')
            break
        else:
            print('Opção inválida!')

if __name__ == "__main__":
    main()