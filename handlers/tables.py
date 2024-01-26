from aiogram import Router

router = Router()

# Необходимо, чтобы знать какие поля есть в бд, как обращаться к пользователю
# и для хранения передаваемых значений в бд
# "!" - ключ в таблице

class Table:
    def __init__(self, db_columns=[], ru_columns=[]):
        self.__db_columns = db_columns      # Как называются поля в БД
        self.__ru_columns = ru_columns      # Для обращения к пользователю
        self.__transfer_columns = []        # В какие поля бд передаем данные
        self.__transfer_data = []           # Что передаем в бд
        self.__size = len(db_columns)       # Количество полей в таблице

    def clear_transfer_columns(self):
        self.__transfer_columns.clear()

    def clear_transfer_data(self):
        self.__transfer_data.clear()

    def get_size(self):
        return self.__size

    def get_db_columns(self):
        return self.__db_columns

    def get_ru_columns(self):
        return self.__ru_columns

    def get_transfer_columns(self):
        return self.__transfer_columns

    def get_transfer_data(self):
        return self.__transfer_data

    def add_transfer_columns(self, element):
        self.__transfer_columns.append(element)

    def add_transfer_data(self, element):
        self.__transfer_data.append(element)



class Tables:
    def __init__(self):
        self.__tables = {
            'owners': Table(['!full_name', 'date_of_birth'],
                            ['ФИО', 'дату рождения']),

            'author': Table(['!full_name', 'date_of_birth'],
                            ['ФИО', 'дату рождения']),

            'printery': Table(['!id_printery', 'name_of_printery', 'address_of_printery', 'pages_per_day', 'owners_name'],
                              ['id типографии', 'название типографии', 'адрес типографии', 'количество страниц в день', 'имя владельца']),

            'publishing_office': Table(['!id_pub_office', 'name_of_office', 'address_of_office', 'printing_price_per_page', 'owners_name'],
                                       ['id издательства', 'название издательства', 'адрес издательства', 'стоимость печати страницы', 'имя владельца']),

            'book': Table(['!id_book', 'name_of_book', 'year_of_book', 'author_name'],
                          ['id книги', 'название книги', 'год издания книги', 'имя автора']),

            'printing': Table(['!id_print', 'number_of_books_in_print', 'printery_id', 'pub_office_id', 'book_id'],
                              ['id печати', 'число книг в печати', 'id типографии', 'id издательства', 'id книги']),

            'work': Table(['!id_work', 'work_name', 'work_year', 'number_of_pages', 'book_id'],
                          ['id произведения', 'название произведения', 'год написания произведения', 'число страниц', 'id книги'])
        }

    def add_transfer_columns(self, current_table, element):
        self.__tables[current_table].add_transfer_columns(element)

    def add_transfer_data(self, current_table, element):
        self.__tables[current_table].add_transfer_data(element)

    def clear_transfer_columns(self, current_table):
        self.__tables[current_table].clear_transfer_columns()

    def clear_transfer_data(self, current_table):
        self.__tables[current_table].clear_transfer_data()

    def get_size(self, current_table):
        return self.__tables[current_table].get_size()

    def get_db_columns(self, current_table):
        return self.__tables[current_table].get_db_columns()

    def get_ru_columns(self, current_table):
        return self.__tables[current_table].get_ru_columns()

    def get_transfer_columns(self, current_table):
        return self.__tables[current_table].get_transfer_columns()

    def get_transfer_data(self, current_table):
        return self.__tables[current_table].get_transfer_data()

tables = Tables()

