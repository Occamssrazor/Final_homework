# Задача 1. Стек Напишите класс, который реализует Стек и его возможности (достаточно будет добавления
# и удаления элемента).
# После этого напишите ещё один класс “Менеджер задач”. В менеджере задач можно выполнить команду
# “новая задача”, в которую передаётся сама задача (str) и её приоритет (int). Сам менеджер работает
# на основе Стэка (не наследование!).  При выводе менеджера в консоль все задачи должны быть отсортированы
# по приоритету: чем меньше число, тем выше задача.

class DublicateError(Exception):
  pass

class Stack:
    def __init__(self):
        self.stack = []

    def pop(self):
        if len(self.stack) == 0:
            return None
        return self.stack.pop()

    def push(self, other):
        self.stack.append(other)

class TaskManager:
    def __init__(self):
        self.tasks = Stack()

    def new_task(self, task, priority):
        for t, p in self.tasks.stack:
            if task == t and priority == p:
                raise DublicateError("Задача уже существует")

        self.tasks.push((task, priority))

    def remove_task(self, task, priority):
        for i, t in enumerate(self.tasks.stack):
            if task == t[0] and priority == t[1]:
                return self.tasks.stack.pop(i)

    def __str__(self):
        sorted_stack = sorted(self.tasks.stack, key = lambda x: x[1])
        output = "Результат:\n"
        for task, priority in sorted_stack:
            output += f"{priority} приоритет - {task}\n"
        return output

manager = TaskManager()
manager.new_task("сделать уборку", 4)
manager.new_task("помыть посуду", 4)
manager.new_task("отдохнуть", 1)
manager.new_task("поесть", 2)
manager.new_task("сдать дз", 2)
print(manager)

# 2 Создайте класс LRU Cache, который хранит ограниченное количество объектов и, при превышении лимита, удаляет
# самые давние (самые старые) использованные элементы.

class LRU_Cache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._cache = {}
        self.update_cache_keys = []

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, new_elem: dict):
        if len(self._cache) >= self.capacity:
            oldest_key = self.update_cache_keys.pop(0)
            del self._cache[oldest_key]

        for key, value in self._cache.items():
            if new_elem[0] == key:
                self._cache[key] = new_elem[1]
                self.update_cache_keys.remove(key)
                self.update_cache_keys.append(key)

        self._cache[new_elem[0]] = new_elem[1]
        self.update_cache_keys.append(new_elem[0])

    def get(self, key):
        if key in self._cache.keys():
            self.update_cache_keys.remove(key)
            self.update_cache_keys.append(key)
            return self._cache[key]
        else:
            print("Такого ключа нет")

    def print_cache(self):
        print("LRU Cache:")
        for key in self.update_cache_keys:
            print(f"{key} : {self._cache[key]}")


cache = LRU_Cache(3)

cache.cache = ("key1", "value1")
cache.cache = ("key2", "value2")
cache.cache = ("key3", "value3")

cache.print_cache()

print(cache.get("key2"))

cache.cache = ("key4", "value4")

cache.print_cache()

# 3 Создайте декоратор, который кэширует (сохраняет для дальнейшего использования) результаты вызова
# функции и, при повторном вызове с теми же аргументами, возвращает сохранённый результат.
#
# Примените его к рекурсивной функции вычисления чисел Фибоначчи.

def benchmark(func):
    dict = {}
    def wrapper(*args):
        key = args
        if key in dict:
            return dict[key]
        else:
            return_value = func(*args)
            dict[key] = return_value
            return return_value
    return wrapper

@benchmark
def fib(n):
    if n == 0:
        return 0
    elif n < 3:
        return 1
    return fib(n-1) + fib(n-2)

print(fib(100))
print(fib(99))

# 4 Крестики-нолики

class Cell:
    def __init__(self, number, busy = False):
        self.number = number
        self.busy = busy
        self.value = ' '

    def set_value(self, value):
        if self.value == ' ':
            self.value = value
            self.busy = True

    def __str__(self):
        return f"{self.value}"

class Board:
    def __init__(self):
        self.board = [Cell(number = i) for i in range(1,10)]

    def show(self):
        print(f'| {self.board[0]} | {self.board[1]} | {self.board[2]} |')
        print('-------------')
        print(f'| {self.board[3]} | {self.board[4]} | {self.board[5]} |')
        print('-------------')
        print(f'| {self.board[6]} | {self.board[7]} | {self.board[8]} |')

    def make_move(self, cell_num, symbol):
        if 1 <= cell_num <= 9 and not self.board[cell_num - 1].busy:
            self.board[cell_num - 1].set_value(symbol)
            return True
        else:
            return False

    def check_win(self, symbol):
        winning_comb = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                        [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for c in winning_comb:
            if all(self.board[i].value == symbol for i in c):
                return True
        return False

    def is_full(self):
        return all(cell.busy for cell in self.board)

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def make_move(self, board: Board):
        while True:
            move = int(input(f'{self.name}, введите номер клетки (1-9): '))
            if 1 <= move <= 9 and board.make_move(move, self.symbol):
                break
            else:
                print('Неверный ввод')

def play_game(name1:str, name2:str) -> str:
    board = Board()
    player1 = Player(name1, 'X')
    player2 = Player(name2, 'O')
    player = player1

    game = True
    while game:
        board.show()
        player.make_move(board)

        if board.check_win(player.symbol):
            board.show()
            game = False
            return f"Выиграл(a) {player.name}"

        elif board.is_full():
            board.show()
            game = False
            return f"Ничья"

        player = player2 if player == player1 else player1

print(play_game('Маша', 'Саша'))