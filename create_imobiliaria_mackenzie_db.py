import sqlite3
import faker

def create_database():
    # Criar e conectar ao banco de dados SQLite
    conn = sqlite3.connect('imobiliaria_mackenzie.db')
    cursor = conn.cursor()

    # Criar a tabela imovel
    cursor.execute('''
    CREATE TABLE imovel (
        contrato TEXT,
        nome TEXT,
        endereco TEXT,
        metragem TEXT,
        comodos TEXT,
        garagem TEXT
    )
    ''')

    # Gerar dados fictícios
    fake = faker.Faker('pt_BR')
    insert_query = 'INSERT INTO imovel (contrato, nome, endereco, metragem, comodos, garagem) VALUES (?, ?, ?, ?, ?, ?)'

    for _ in range(50):
        contrato = fake.phone_number()
        nome = fake.first_name()
        endereco = fake.address()
        metragem = fake.floor_number()
        comodos = 3
        garagem = fake.boolean()
        cursor.execute(insert_query, (contrato, nome, endereco, metragem, comodos, garagem))

    # Commit e fechar a conexão
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()