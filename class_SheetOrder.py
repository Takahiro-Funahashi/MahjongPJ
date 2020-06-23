import random


class class_SheetOrder():
    # ---[0:initialize
    def __init__(self):
        return

    # ---[1:東西南北牌による席決め
    def direction_lottery(self):
        direction_pai = ['東', '南', '西', '北']
        random.shuffle(direction_pai)

        return direction_pai

    # ---[2:サイコロを降る
    def roll_dise(self):
        dise1 = random.randint(1, 6)
        dise2 = random.randint(1, 6)

        return (dise1, dise2)


if __name__ == '__main__':
    Sheet = class_SheetOrder()

    for _ in range(10):
        dise1, dise2 = Sheet.roll_dise()
        print('dise:', dise1, dise2)

        direction_pai = Sheet.direction_lottery()
        print('pai:', direction_pai)
