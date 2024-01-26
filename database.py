import psycopg2
import os
from psycopg2 import Error
from dotenv import load_dotenv

class PostgresDB:
    def __init__(self):
        self.cursor = None
        self.connection = None

    def connect(self):
        try:
            load_dotenv()
            self.connection = psycopg2.connect(user=os.getenv('USER'),
                                               password=os.getenv('PASSWORD'),
                                               host=os.getenv('HOST'),
                                               port=os.getenv('PORT'),
                                               database=os.getenv('DATABASE')
                                               )

            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print("Ошибка при подключении", error)

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def InsertData(self, table, columns, data):
        print(table, columns, data)

        param = []
        param_insert = []
        for i in range(len(columns)):
            if 'id' in columns[i]:
                param.append(f'{columns[i]} = {data[i]}')
                param_insert.append(f"{data[i]}")
            else:
                param.append(f"{columns[i]} = '{data[i]}'")
                param_insert.append(f"'{data[i]}'")

        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM {table} WHERE {' AND '.join(param)});"
            print(str_exec)
            self.cursor.execute(str_exec)
            if self.cursor.fetchone()[0]:
                return 'Такие данные уже находятся в таблице'
            else:
                query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(param_insert)});"
                print(query)
                self.cursor.execute(query)
                self.connection.commit()
                return 'Данные добавлены'
        except (Exception, Error) as _:
            return 'Ошибка при вводе данных!'
        finally:
            self.close_connection()



    def DeleteData(self, table, columns, data):
        print(table, columns, data)
        param = []
        for i in range(len(columns)):
            if 'id' in columns[i]:
                param.append(f'{columns[i]} = {data[i]}')
            else:
                param.append(f'{columns[i]} = \'{data[i]}\'')

        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM {table} WHERE {' AND '.join(param)});"
            print(str_exec)
            self.cursor.execute(str_exec)
            if not self.cursor.fetchone()[0]:
                return 'Таких данных в таблице нет'
            else:
                query = f"DELETE FROM {table} WHERE {' AND '.join(param)};"
                print(query)
                self.cursor.execute(query)
                self.connection.commit()
                return 'Данные удалены'
        except (Exception, Error) as _:
            return 'Ошибка при вводе данных!'
        finally:
            self.close_connection()


    def UpdateData(self, table, columns, data):
        print(table, columns, data)
        pk_data = []
        change_data = []

        for index, column in enumerate(columns):
            if '!' in column:
                pk_column = column.replace('!', '')
                pk_data.append(
                    f"{pk_column} = {data[index]}" if 'id' in pk_column else f"{pk_column} = '{data[index]}'")
            else:
                change_column = column
                change_data.append(
                    f"{change_column} = {data[index]}" if 'id' in change_column else f"{change_column} = '{data[index]}'")


        print(change_data, pk_data)
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM {table} WHERE {' AND '.join(pk_data)});"
            print(str_exec)
            self.cursor.execute(str_exec)
            if not self.cursor.fetchone()[0]:
                return 'Таких данных в таблице нет'
            else:
                query = f"UPDATE {table} SET {', '.join(change_data)} WHERE {' AND '.join(pk_data)};"
                print(query)
                self.cursor.execute(query)
                self.connection.commit()
                return 'Данные изменены'
        except (Exception, Error) as _:
            return 'Ошибка при вводе данных!'
        finally:
            self.close_connection()


    def ShowTable(self, table):
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM {table});"
            print(str_exec)
            self.cursor.execute(str_exec)
            if not self.cursor.fetchone()[0]:
                return ('Таблица пуста', '')
            else:
                query = f"SELECT * FROM {table};"
                print(query)
                self.cursor.execute(query)
                data = self.cursor.fetchall()
                return (f'Вот следующие данные', data)
        except (Exception, Error) as error:
            return ('Ошибка при вводе данных!', '')
        finally:
            self.close_connection()