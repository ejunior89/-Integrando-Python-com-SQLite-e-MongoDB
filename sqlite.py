from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

# Declaração das Classes para o Modelo ORM
Base = declarative_base()


class Client(Base):
    """
        classe que representa a tabela de clientes dentro do SQlite.
    """
    __tablename__ = "client"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    cpf = Column(String(9))
    address = Column(String(30))

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name}, address={self.address})"


class Account(Base):
    """
            Esta classe representa a tabela account dentro do SQlite.
        """
    __tablename__ = "account"
    # atributos
    id = Column(Integer, primary_key=True)
    tipo = Column(String(2))
    agency = Column(Integer)
    number = Column(Integer)
    balance = Column(Float)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)

    def __repr__(self):
        return f"Account(id={self.id}, tipo={self.tipo}, saldo={self.balance})"


# Realiza a conexão com o banco de dados
engine = create_engine("sqlite://")

# Cria as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Faz a persistência das Informações no Banco de Dados SQLite
with Session(engine) as session:
    endrick = Client(name='Endrick Felipe',
                     cpf='845.486.987.99',
                     address='Rua 1 de Roma, número 540'
                     )

    raphael = Client(name='Raphael Veiga',
                     cpf='101.203.406.23',
                     address='Rua do Pio, número 3'
                     )

    abel = Client(name='Abel Ferreira',
                  cpf='771.452.669.97',
                  address='Rua Boo Wong the Ha, número 73'
                  )

    account1 = Account(client_id='1',
                       tipo='cc',
                       agency=2800,
                       number=230803,
                       balance=18500
                       )
    account2 = Account(client_id='2',
                       tipo='cp',
                       agency=3001,
                       number=290110,
                       balance=87900
                       )
    account3 = Account(client_id='3',
                       tipo='cc',
                       agency=9003,
                       number=320457,
                       balance=4780
                       )

    # Envia as informações para o BD (persitência de dados)
    session.add_all([endrick, raphael, abel])
    session.add_all([account1, account2, account3])
    session.commit()

# Consulta as Informações Salvas no Banco de Dados SQLite

print('Recuperando clientes a partir de uma condição de filtragem:')
stmt_clients = select(Client).where(Client.name.in_(['Piangelo Diatore', 'Pietro de Lorenzo']))
for result in session.scalars(stmt_clients):
    print(result)

print("\nRecuperando clientes de maneira ordenada:")
stmt_order = select(Client).order_by(Client.name.desc())
for result in session.scalars(stmt_order):
    print(result)

print("\nRecuperando contas de maneira ordenada:")
stmt_accounts = select(Account).order_by(Account.tipo.desc())
for result in session.scalars(stmt_accounts):
    print(result)

print("\nRecuperando contas e clientes:")
stmt_join = select(Client.name, Account.tipo, Account.balance).join_from(Client, Account)
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
for result in results:
    print(result)

session.close()
