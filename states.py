from aiogram.fsm.state import StatesGroup, State

class BotAction(StatesGroup):
    table = State()
    action = State()
    dataCollect = State()

#   Логика КА
#
#   +-------------------+                       +--------------------------+
#   |                   |---------------------->|                          |-------+
#   |   Выбор таблицы   |                       |___  Действие с таблицей  |       |
#   |                   |<----------------------| DC|                      |<------+
#   +-------------------+                       +--------------------------+
#
#                                       dataCollect - находится внутри действий с таблицей
#                                       и нужен ради сбора и подготовки данных для работы с бд