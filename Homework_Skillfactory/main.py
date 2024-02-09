# Вывод игрового поля на экран
def print_board(board):
    print("  0 1 2")
    for i, row in enumerate(board):
        print(i, end=" ")
        print(" ".join(cell if cell != ' ' else '-' for cell in row))

# Проверка наличия выигрышной комбинации для текущего игрока
def check_winner(board, player):

    # Проверка по горизонтали и вертикали
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True

    # Проверка по диагоналям
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# Проверка, заполнено ли игровое поле
def is_board_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

# Инициализация игрового поля и текущего игрока
def tic_tac_toe():
    board = [[' '] * 3 for _ in range(3)]
    current_player = 'X'

    while True:
        print_board(board)  # Вывод игрового поля

        try:
            # Ввод координат от пользователя
            row = int(input(f"Игрок {current_player}, введите номер строки (0, 1, 2): "))
            col = int(input(f"Игрок {current_player}, введите номер столбца (0, 1, 2): "))

            # Проверка корректности ввода
            if row not in [0, 1, 2] or col not in [0, 1, 2]:
                print("Ошибка ввода. Введите число от 0 до 2.")
                continue

        except ValueError:
            print("Ошибка ввода. Введите целое число от 0 до 2.")
            continue

        if board[row][col] == ' ':
            board[row][col] = current_player
        else:
            print("Эта ячейка уже занята. Попробуйте снова.")
            continue

        if check_winner(board, current_player):
            print_board(board)
            print(f"Игрок {current_player} победил!")
            break
        elif is_board_full(board):
            print_board(board)
            print("Ничья!")
            break

        current_player = 'O' if current_player == 'X' else 'X'  # Смена текущего игрока


if __name__ == "__main__":
    tic_tac_toe()