from classes import *
import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="supervelha"
)

class TurmaDAO:
    def __init__(self):
        pass

    def create_turma(self, codigo:int, nome, capacidade: int) -> Turma:
        turma = Turma(codigo, nome, capacidade, 0)
        cursor = connection.cursor()
        sql = "INSERT INTO turma (codigo, nome, capacidade, quantidade_alunos) VALUES (%s, %s, %s, %s)"
        data = (turma.codigo, turma.nome, turma.capacidade, turma.quantidade)
        cursor.execute(sql, data)
        connection.commit() 
        cursor.close()
        return turma

    def retrive_turma(self, codigo:int) -> Turma:
        cursor = connection.cursor()
        sql = "SELECT * FROM turma WHERE codigo = %s"
        cursor.execute(sql, codigo)
        result = cursor.fetchall()
        turma = Turma()
        cursor.close()
        return turma

    def update_turma(self, turma: Turma) -> bool:
        cursor = connection.cursor()
        sql = "UPDATE turma SET codigo = %s, nome = %s, capacidade = %s, quantidade_alunos = %s WHERE codigo = %s"
        data = (turma.codigo, turma.nome, turma.capacidade, turma.quantidade, turma.codigo)
        cursor.execute(sql, data)
        connection.commit() 
        cursor.close()
        return True

    def delete_turma(self, turma: Turma) -> bool:
        cursor = connection.cursor()
        sql = "DELETE FROM turma WHERE codigo = %s"
        data = ((turma.codigo,))
        cursor.execute(sql, data)
        connection.commit() 
        cursor.close()
        return True

    def query_turma():
        pass

def main():
    turmaDAO = TurmaDAO()
    turma = Turma(1, "turma bonita", 20, 1)
    print(turmaDAO.delete_turma(turma))

main()