# DESAFIO DIO - Integrando Python com SQLite e MongoDB

import pymongo
import pprint

print("Iniciando a conexão com o MongoDB")

# Cria a conexão com o MongoDB
connection = pymongo.MongoClient("link-para-o-mongo-db")

# Cria o banco de dados e a collection
db = connection.bank
collection = db.clients

# Define as informações que irão compor o documento
new_clients = [{
    "agency": 2800,
    "name": "Endrick Felipe",
    "cpf": "845.486.987.99",
    "address": "Rua 1 de Roma, número 540",
    "account": ["cc", "230803"],
    "balance": 18500
},
    {
        "agency": 3001,
        "name": "Raphael Veiga",
        "cpf": "778.159.687.12",
        "address": "Rua 20 Fox, número 10",
        "account": ["cp", "290110"],
        "balance": 87900
    },
    {
        "agency": 9003,
        "name": "Abel Ferreira",
        "cpf": "101.203.406.23",
        "address": "Rua do Pio, número 3",
        "account": ["cp", "320457"],
        "balance": 74570
    },
    {
        "agency": 9003,
        "name": "Eduardo Rodrigues",
        "cpf": "771.452.669.97",
        "address": "Rua Boo Wong the Ha, número 73",
        "account": ["cc", "120001"],
        "balance": 4780
    }]

print("Salvando as informações no MongoDB")
clients = db.clients
result = clients.insert_many(new_clients)
print(result.inserted_ids)

print("\n Recuperando as informações da cliente Stan:")
pprint.pprint(db.clients.find_one({"name": "Stan Lee"}))

print("\n Listagem dos clientes presentes na coleção clients:")
for client in clients.find():
    pprint.pprint(client)

print("\n Recuperando informação dos clientes de maneira ordenada pelo nome:")
for client in clients.find({}).sort("name"):
    pprint.pprint(client)

print("\n Clientes da agência 9003:")
for client in clients.find({"agency": 9003}):
    pprint.pprint(client)

print("\n Clientes com conta poupança:")
for client in clients.find({"account": "cp"}):
    pprint.pprint(client)

print("\n Clientes com conta corrente:")
for client in clients.find({"account": "cc"}):
    pprint.pprint(client)
