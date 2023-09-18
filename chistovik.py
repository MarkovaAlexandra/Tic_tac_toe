import random
from tkinter import *

# формируем окно
window = Tk()
window.geometry('300x300')
# текстовая метка с названием игры
label = Label(text="Крестики-нолики")
# размещаем метку в окне, в 0 колонке, 0 строке, растянув по 3 столбцам, по центру
label.grid(row=0, column=0, columnspan=3, sticky=NSEW)
# устан вес каждой колонки (для размерности)
for i in range(3): window.columnconfigure(index=i, weight=1)
# устан вес каждой строки (для размерности)
for i in range(1, 4): window.rowconfigure(index=i, weight=1)

# создаем список кнопок, ф-ция push передает номер нажатой кнопки (x= i(индекс кнопки в списке) при нажатии на кнопку i
buttons = [Button(command=lambda x=i: push(x)) for i in range(9)]
row = 1
col = 0
for i in range(9):
    buttons[i].grid(row=row, column=col, sticky=NSEW)
    col += 1
    if col == 3:
        row += 1
        col = 0

# список с поставленными х и 0
game = [None] * 9
# список оставшихся в игре кнопок
game_left = list(range(9))
# номер хода
turn = 0


# Игра
def push(b):  # принимает b = номер нажатой игроком кнопки
    global game
    global game_left
    global turn
    buttons[b].config(text='x', state='disabled', bg='white', font=20)  # на кнопке игрока пишем х, кнопку отключаем
    game[b] = 'x'  # сохраняем поле в списке поставленных х и 0
    game_left.remove(b)  # из списка оставшихся в игре кнопок убираем нажатую
    if wincheck('x') is True:  # проверяем, победили ли крестики
        print("Ты победил!")
        label.config(text="Ты победил!")
        stop_game()
    else:
        if b == 4 and turn == 0:  # если игрок походил в центр первым ходом
            t = random.choice(game_left)  # ход бота - рандомно из списка оставшихся кнопок
        elif b != 4 and turn == 0:  # если игрок не походил в центр первым ходои
            t = 4  # это сделает бот
        if turn > 0:  # если ход не первый
            # 1. Проверяем возможность победы через центр

            if perehvat_centra() != -1:  # если функцие вернула не -1
                t = perehvat_centra()

            # 2. Если победить не можем,
            # блокируем победу противника через центр(если центр занят,ходим в клетку,
            # противоположную номеру переданной (b), если она не занята
            elif game[4] == 'x' and (8 - b) in game_left:
                t = 8 - b
            # 3. Проверяем периметры
            elif perehvat_perimetra('0') != -1:
                t = perehvat_perimetra('0')
            elif perehvat_perimetra('x') != -1:
                t = perehvat_perimetra('x')
            else:
                t = random.choice(game_left)
        # Сохраняем ход бота
        buttons[t].config(text='0', state='disabled', bg='white')  # на кнопке бота пишем 0, кнопку отключаем
        game[t] = '0'  # сохраняем поле в списке
        game_left.remove(t)  # из списка оставшихся в игре кнопок убираем нажатую
        # Проверяем, не победил ли бот
        if wincheck('0') is True:
            print("Я победил!")
            label.config(text="Я победил!")
            stop_game()
        # Если свободных клеток не осталось
        if len(game_left) == 0:
            label.config(text="Игра окончена")

        turn += 1


def wincheck(gamer):  # функция написана по-дурацки, но она сразу красит кнопки победной строки
    global game
    if game[0] == game[1] == game[2] == gamer:
        buttons[0].config(bg='red')
        buttons[1].config(bg='red')
        buttons[2].config(bg='red')
        return True
    if game[3] == game[4] == game[5] == gamer:
        buttons[3].config(bg='red')
        buttons[4].config(bg='red')
        buttons[5].config(bg='red')
        return True
    if game[6] == game[7] == game[8] == gamer:
        buttons[6].config(bg='red')
        buttons[7].config(bg='red')
        buttons[8].config(bg='red')
        return True
    if game[0] == game[3] == game[6] == gamer:
        buttons[0].config(bg='red')
        buttons[3].config(bg='red')
        buttons[6].config(bg='red')
        return True
    if game[1] == game[4] == game[7] == gamer:
        buttons[1].config(bg='red')
        buttons[4].config(bg='red')
        buttons[7].config(bg='red')
        return True
    if game[2] == game[5] == game[8] == gamer:
        buttons[2].config(bg='red')
        buttons[5].config(bg='red')
        buttons[8].config(bg='red')
        return True
    if game[0] == game[4] == game[8] == gamer:
        buttons[0].config(bg='red')
        buttons[4].config(bg='red')
        buttons[8].config(bg='red')
        return True
    if game[2] == game[4] == game[6] == gamer:
        buttons[2].config(bg='red')
        buttons[4].config(bg='red')
        buttons[6].config(bg='red')
        return True


def wincheck_new(gamer):  # альтернативная хорошая функция, но не могу придумать, как покрасить победную линию
    global game
    win_lines = [(game[0], game[1], game[2]), (game[3], game[4], game[5]), (game[6], game[7], game[8]),
                 (game[0], game[3], game[6]), (game[1], game[4], game[7]), (game[2], game[5], game[8]),
                 (game[0], game[4], game[8]), (game[2], game[4], game[6])]
    for line in win_lines:
        if line[0] == line[1] == line[2] == gamer:
            return True


def stop_game():
    global game_left
    for i in game_left:
        buttons[i].config(state='disabled', bg='white')


def perehvat_centra():
    global game
    global game_left
    if game[4] == '0':
        for i in range(8):
            if game[i] == '0' and (8 - i) in game_left:
                t = 8 - i
                return t
    return -1


def perehvat_perimetra(gamer):  # тут надо подумать и как-то сократить это безобразие
    global game_left
    global game
    # верхняя горизонталь
    if game[0] == game[1] == gamer and 2 in game_left:
        t = 2
        return t
    elif game[1] == game[2] == gamer and 0 in game_left:
        t = 0
        return t
    elif game[0] == game[2] == gamer and 1 in game_left:
        t = 1
        return t
    # нижняя горизонталь
    elif game[6] == game[7] == gamer and 8 in game_left:
        t = 8
        return t
    elif game[6] == game[8] == gamer and 7 in game_left:
        t = 7
        return t
    elif game[7] == game[8] == gamer and 6 in game_left:
        t = 6
        return t
    elif game[0] == game[3] == gamer and 6 in game_left:
        t = 6
        return t
    # правая вертикаль
    elif game[0] == game[6] == gamer and 3 in game_left:
        t = 3
        return t
    elif game[3] == game[6] == gamer and 0 in game_left:
        t = 0
        return t
    # левая вертикаль
    elif game[2] == game[5] == gamer and 8 in game_left:
        t = 8
        return t
    elif game[2] == game[8] == gamer and 5 in game_left:
        t = 5
        return t
    elif game[5] == game[8] == gamer and 2 in game_left:
        t = 2
        return t
    else:
        return -1


window.mainloop()
