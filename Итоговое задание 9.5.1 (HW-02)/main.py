from random import randint

# Классы пользовательских исключений для более эффективной обработки ошибок
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы выстрелили за пределы игрового поля!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

# Класс Dot представляет точку на игровом поле
class Dot:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

# Класс Ship представляет корабль на игровом поле
class Ship:
    def __init__(self, bow, length, direction):
        self.bow = bow
        self.length = length
        self.direction = direction
        self.lives = length

    def dots(self):
        ship_dots = []
        for i in range(self.length):
            row = self.bow.row
            col = self.bow.col
            if self.direction == 0:  # горизонтальный корабль
                col += i
            elif self.direction == 1:  # вертикальный корабль
                row += i
            ship_dots.append(Dot(row, col))
        return ship_dots

# Класс Board представляет игровое поле
class Board:
    def __init__(self, size):
        self.size = size
        self.field = [['O'] * size for _ in range(size)]
        self.ships = []

    def __str__(self, hid=False):
        result = "  | 1 | 2 | 3 | 4 | 5 | 6 |\n"
        for i, row in enumerate(self.field, 1):
            if hid:
                masked_row = ['O' if cell == '■' else cell for cell in row]
            else:
                masked_row = row
            result += f"{i} | {' | '.join(masked_row)} |\n"
        return result

    def out(self, dot):
        return not (0 <= dot.row < self.size and 0 <= dot.col < self.size)

    def contour(self, ship, verb=False):
        near = [(i, j) for i in range(ship.bow.row - 1, ship.bow.row + ship.length + 1)
                for j in range(ship.bow.col - 1, ship.bow.col + ship.length + 1)
                if 0 <= i < self.size and 0 <= j < self.size]
        for dot in ship.dots():
            for i, j in near:
                if self.field[i][j] == 'O':
                    if verb:
                        self.field[i][j] = '.'
                    else:
                        return False
        return True

    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out(dot) or self.field[dot.row][dot.col] != 'O':
                raise BoardException("Невозможно разместить корабль")
        for dot in ship.dots():
            self.field[dot.row][dot.col] = '■'
        self.ships.append(ship)
        self.contour(ship, verb=True)

    def reset_board(self):
        self.field = [['O'] * self.size for _ in range(self.size)]
        self.ships = []

    def shot(self, target):
        if self.out(target):
            raise BoardOutException()

        if self.field[target.row][target.col] == 'T' or self.field[target.row][target.col] == 'X':
            raise BoardUsedException()

        for ship in self.ships:
            if target in ship.dots():
                print("Попадание!")
                ship.lives -= 1
                self.field[target.row][target.col] = 'X'  # отмечаем попадание
                if ship.lives == 0:
                    print("Корабль уничтожен!")
                return False

        self.field[target.row][target.col] = 'T'  # отмечаем промах
        print("Мимо!")
        return False

# Класс Player с методом для запроса ввода пользователя
class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                result = self.enemy_board.shot(target)
                return result
            except BoardException as e:
                print(e)

# Класс AI, который случайным образом выбирает цель для выстрела
class AI(Player):
    def ask(self):
        row = randint(0, self.enemy_board.size - 1)
        col = randint(0, self.enemy_board.size - 1)
        print(f"Компьютер стреляет в строку {row+1}, столбец {col+1}")
        return Dot(row, col)

# Класс User, который принимает ввод от пользователя
class User(Player):
    def ask(self):
        while True:
            try:
                row = int(input("Введите номер строки (1-6): ")) - 1
                col = int(input("Введите номер столбца (1-6): ")) - 1
                target = Dot(row, col)
                if self.enemy_board.out(target):
                    raise BoardOutException()
                return target
            except ValueError:
                print("Введите числа!")
            except BoardException as e:
                print(e)

# Класс Game, который оркестрирует ход игры
class Game:
    def __init__(self):
        self.size = 6
        self.ai_board = Board(self.size)
        self.user_board = Board(self.size)
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def greet(self):
        print("Добро пожаловать в игру 'Морской бой'!")

    def random_board(self, board, ship_counts):
        for length, count in ship_counts.items():
            for _ in range(count):
                for _ in range(1000):  # Ограничение числа попыток
                    ship = Ship(Dot(randint(0, self.size - 1), randint(0, self.size - 1)), length, randint(0, 1))
                    try:
                        board.add_ship(ship)
                        break
                    except BoardException:
                        pass
                else:
                    board.reset_board()
                    return self.random_board(board, ship_counts)

        # После генерации всех кораблей, заменяем все '.' на 'O'
        for i in range(self.size):
            for j in range(self.size):
                if board.field[i][j] == '.':
                    board.field[i][j] = 'O'

    def loop(self):
        while True:
            print("Доска пользователя:")
            print(self.user_board)
            print("Доска компьютера:")
            print(game.ai_board.__str__(hid=True))
            if self.user.move():
                break
            if all(ship.lives == 0 for ship in self.ai_board.ships):
                print("Вы победили!")
                break
            if self.ai.move():
                break
            if all(ship.lives == 0 for ship in self.user_board.ships):
                print("Компьютер победил!")
                break

    def start(self):
        self.greet()
        self.random_board(self.ai_board, {3: 1, 2: 2, 1: 4})
        self.random_board(self.user_board, {3: 1, 2: 2, 1: 4})
        self.loop()

if __name__ == "__main__":
    game = Game()
    game.start()
