"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью спе циальных карточек, на которых отмечены числа,
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр,
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается
случайная карточка.

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
    Если цифра есть на карточке - она зачеркивается и игра продолжается.
    Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
    Если цифра есть на карточке - игрок проигрывает и игра завершается.
    Если цифры на карточке нет - игра продолжается.

Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71
--------------------------
-- Карточка компьютера ---
 7 87     - 14    11
      16 49    55 88    77
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать
модуль random: http://docs.python.org/3/library/random.html

"""
import random
from itertools import chain


class StartGame:
    def __init__(self):
        self.name = input('Введите имя игрока: ')
        self.game_card_line = []
        self.game_card = []
        self.computer_card = []

    @property
    def start(self):
        for player in range(2):

            self.pre_card = list(range(1, 91))
            for i in range(3):
                for z in range(9):
                    self.game_card_line.append(self.pre_card.pop(random.choice(range(len(self.pre_card)))))
                    self.game_card_line.sort()
                else:
                    while self.game_card_line.count('☐') != 4:
                        el = random.choice(range(len(self.game_card_line)))
                        self.game_card_line.pop(el)
                        self.game_card_line.insert(el, '☐')

                if player != 1:
                    self.game_card.append(self.game_card_line)
                    self.game_card_line = []
                else:
                    self.computer_card.append(self.game_card_line)
                    self.game_card_line = []

        # перевожу полученый двумерный массив в одну строку для удобства
        self.game_card = list(chain.from_iterable(self.game_card))
        self.computer_card = list(chain.from_iterable(self.computer_card))
        return self.__str__

    @property
    def __str__(self):
        show_game_cad = self.game_card.copy()
        show_comp_cad = self.computer_card.copy()
        for player in range(2):
            if player != 1:
                print('=========================', self.name)
                for i in range(27):
                    if i == 9 or i == 19:
                        show_game_cad.insert(i, '\n')
                show_game_cad.insert(0, '') # смысла нет, просто выравнивает вывод
                print(f'{" ".join(map(str, show_game_cad))}')
            else:
                print('========================= Computer')
                for i in range(27):
                    if i == 9 or i == 19:
                        show_comp_cad.insert(i, '\n')
                show_comp_cad.insert(0, '')  # смысла нет, просто выравнивает вывод
                print(f'{" ".join(map(str, show_comp_cad))}')

    @property
    def take_answer(self):
        # создаем диапазон доступных ответов.
        # так же это поможет избежать дубликатов возможных при обычном рандоме
        # и длинну строки можно использовать как счетчик оставшихся попыток
        self.pre_card = list(range(1, 91))

        while len(self.pre_card) !=0:
            number = self.pre_card.pop(random.choice(range(len(self.pre_card)))) #вынимаем по одному случайному числу
            print('=========================\n', str(len(self.pre_card)) + '/90     текущий номер:', number)

            user_answer = input(' Зачеркнуть цифру? (y/n): ')

            if self.computer_card.count(number) == 1:
                el = self.computer_card.index(number)
                self.computer_card.pop(el)
                self.computer_card.insert(el, '✪')

            if self.game_card.count(number) == 1 and user_answer == 'y':
                el = self.game_card.index(number)
                self.game_card.pop(el)
                self.game_card.insert(el, '✪')
                self.__str__
            elif self.game_card.count(number) == 0 and user_answer == 'y':
                print('    ┏━=━=━=━=━=━=━┓\n    ┇  Game Over  ┇\n    ┗━=━=━=━=━=━=━┛')
                break
            elif self.game_card.count(number) == 1 and user_answer == 'n':
                print('==========================\nПропущено число\nYou loose!')
                break
            elif user_answer != 'y' and user_answer != 'n':
                print('    ┏━=━=━=━=━=━=━┓\n    ┇ miss click  ┇\n    ┗━=━=━=━=━=━=━┛')
                break
            else:
                self.__str__

            if self.computer_card.count('✪') == 15:
                print('   ┏━━━━━━━━━━━━━━┓\n   ┇ Computer WIN ┇\n   ┗━━━━━━━━━━━━━━┛')
                break
            elif self.game_card.count('✪') == 15:
                print(self.name, 'Win!')
                break


new_game = StartGame()
new_game.start
new_game.take_answer
