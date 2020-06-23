import math
from statistics import stdev, mean

import class_Pai
import class_SheetOrder

# ---[randomを使用した関数の乱数をテスト

# ---[テスト用順列式


def permutations_count(n, r):
    return math.factorial(n) // math.factorial(n - r)


class vf_direction_lottery():
    def __init__(self):

        insSheetOrder = class_SheetOrder.class_SheetOrder()

        # ---[テスト　direction_lotteryの検証
        sv_list = list()
        key_number = permutations_count(4, 4)

        for j in range(10):
            verif_dict = dict()
            test_times = key_number * 10
            for i in range(test_times):
                ans = insSheetOrder.direction_lottery()
                key = ''.join(ans)
                if key in verif_dict:
                    verif_dict[key] = verif_dict[key] + 1
                else:
                    verif_dict.setdefault(key, 1)
            else:
                result = sorted(verif_dict.items(), key=lambda x: x[1])
                #print(' key num {}:{}'.format(key_number,len(result)))
                n_list = list(verif_dict.values())

                sv = stdev(n_list)
                sv_list.append(sv)
        else:
            print(sv_list)
            m = mean(sv_list)
            print(m)


class vf_roll_dise():
    def __init__(self):
        insSheetOrder = class_SheetOrder.class_SheetOrder()

        # ---[テスト　roll_diseの検証
        sv_list = list()
        key_number = 6*6

        for j in range(10):
            verif_dict = dict()
            test_times = key_number * 10
            for i in range(test_times):
                ans = insSheetOrder.roll_dise()

                key = '{}{}'.format(ans[0], ans[1])
                if key in verif_dict:
                    verif_dict[key] = verif_dict[key] + 1
                else:
                    verif_dict.setdefault(key, 1)
            else:
                result = sorted(verif_dict.items(), key=lambda x: x[1])
                #print(' key num {}:{}'.format(key_number,len(result)))
                n_list = list(verif_dict.values())

                sv = stdev(n_list)
                sv_list.append(sv)
        else:
            print(sv_list)
            m = mean(sv_list)
            print(m)


class vf_shey_pai():
    def __init__(self):

        insPai = class_Pai.class_Pai()
        number = insPai.TOTAL_PAI

        # ---[テスト　direction_lotteryの検証
        sv_list = list()
        key_number = permutations_count(number, number)
        print(key_number)

        for j in range(10):
            verif_dict = dict()
            test_times = 100
            for i in range(test_times):
                pai_list = insPai.shey_pai()
                _, pai_list = insPai.set_haipai_char(pai_list)

                pai_set = list(set(pai_list))

                for key in pai_set:
                    if key in verif_dict:
                        verif_dict[key] = verif_dict[key] + pai_set.count(key)
                    else:
                        verif_dict.setdefault(key, pai_set.count(key))
            else:
                print(set(verif_dict.values()))


if __name__ == '__main__':
    # vf_direction_lottery()
    # vf_roll_dise()
    vf_shey_pai()
