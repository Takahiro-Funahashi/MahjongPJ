class class_Yaku (object):
    def __init__(self):
        return

    def judgement(self, tehai_list: list, furo_list: list, tsumo_list: list, sutehai_list: list, dora_list: list, **kwargs):
        yaku_dict = dict()
        isFuro = False
        isHora = False

        if not isinstance(tehai_list, list):
            return

        if not isinstance(furo_list, list):
            return

        if not isinstance(tsumo_list, list):
            return

        if not isinstance(sutehai_list, list):
            return

        if not isinstance(dora_list, list):
            return

        option_key = list(kwargs.keys())
        KEY_DICT = {
            'isReach',
            'isTsumo',
            'Ba',
            'Tya',
        }

        if len(furo_list) > 0:
            isFuro = True
        if len(tsumo_list) > 0:
            isHora = True

        #### 役満　####
        # 四暗刻
        ankan = list()
        isNone = False
        for f in furo_list:
            for k, v in f.items():
                if len(k) != 4*2+3 or v[0] != 0:
                    isNone = True
                else:
                    ankan.extend([v[1], v[1], v[1]])
            if isNone:
                break
        else:
            isHora = False
            Option = None
            tehai = list()
            for t in tehai_list:
                if t > 100:
                    t -= 100
                tehai.append(t)
            if len(ankan) > 0:
                tehai.extend(ankan)
            ts = set(tehai)
            if len(tsumo_list) > 0:
                tsumo = tsumo_list[0]
                if tsumo in ts and len(ts) == 5:
                    if tehai_list.count(tsumo) == 1:
                        Option = '単騎待ち'
                    yaku_dict.setdefault(
                        '四暗刻', {'isHora': True, 'option': Option})
                    isHora = True
                else:
                    ts.add(tsumo)
                    tehai.append(tsumo)
            if not isHora:
                syante = dict()
                for i in ts:
                    c = tehai.count(i)
                    if c in syante:
                        syante[c].append(i)
                    else:
                        syante.setdefault(c, [i])
                else:
                    hc_list = list(syante.keys())
                    hc_list.sort(reverse=True)
                    tehai_c = 0
                    syante_c = 0
                    isCount = True
                    for c in hc_list:
                        for cc in syante[c]:
                            tehai_c += c
                            if 14 - (tehai_c + syante_c) < 2:
                                syante_c += 2-c
                            else:
                                syante_c += 3-c
                            if tehai_c+syante_c >= 14:
                                isCount = False
                                break
                        if not isCount:
                            break
                    if syante_c == 1:
                        if 1 in hc_list:
                            Option = '単騎待ち'
                    yaku_dict.setdefault(
                        '四暗刻', {'syanten': syante_c, 'option': Option})

        # 大三元
        # 字一色
        # 四喜和
        # 大四喜
        # 緑一色
        # 九蓮宝燈
        # 清老頭
        # 四槓子
        # 国士無双
        if not isFuro:
            Option = None

            pat = [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 51, 52, 53, ]
            tehai = sorted(tehai_list)
            tsumo = None
            if len(tsumo_list) > 0:
                tsumo = tsumo_list[0]
                tehai.extend([tsumo])
            f = list(set(pat) - set(tehai))
            y = list(set(tehai) - set(pat))
            s = list(set(pat) & set(tehai))

            if len(f) == 0 and len(y) == 0:
                if tsumo in pat:
                    if tsumo in tehai_list:
                        Option = '十三面待ち'
                    yaku_dict.setdefault(
                        '国士無双', {'isHora': True, 'option': Option})
                else:
                    Option = '十三面待ち'
                    yaku_dict.setdefault(
                        '国士無双', {'syanten': 1, 'option': Option})
            else:
                syante_c = len(f) - (len(f)-len(y)-1)
                if tsumo is None:
                    syante_c += 1
                '''
                else:
                    if tsumo not in pat or tsumo in tehai:
                        syante_c += 1
                '''
                yaku_dict.setdefault(
                    '国士無双', {'syanten': syante_c, 'option': Option})
        # 天和
        # 地和

        #### ローカル役満　####
        # 人和
        # 八連荘
        # 大車輪
        # 大七星
        # 四連刻
        # 十三不塔
        # 十三無靠

        # 立直
        # 二重立直
        # 門前清模和
        # 平和
        # 断么九
        # 一盃口
        # 門風牌
        # 荘風牌
        # 嶺上開花
        # 槍槓
        # 海底撈月
        # 河底撈魚
        # 全帯
        # 混老頭
        # 三色同順
        # 一気通貫
        # 対々和
        # 三色同刻
        # 三暗刻
        # 三槓子
        # 小三元
        # 七対子
        if not isFuro:
            tehai = list()
            for t in tehai_list:
                if t > 100:
                    t -= 100
                tehai.append(t)
            tehai.sort()
            tsumo = None
            if len(tsumo_list) > 0:
                tsumo = tsumo_list[0]
                tehai.extend([tsumo])

            ts = set(tehai)
            if len(ts) == 7:
                if tsumo is not None:
                    yaku_dict.setdefault(
                        '七対子', {'isHora': True})
                else:
                    yaku_dict.setdefault(
                        '七対子', {'syanten': 1})
            else:
                syante = dict()
                for i in ts:
                    c = tehai.count(i)
                    if c in syante:
                        syante[c].append(i)
                    else:
                        syante.setdefault(c, [i])
                else:
                    hc_list = list(syante.keys())
                    hc_list.sort(reverse=True)
                    sante_c = 0
                    cnt = 0
                    for key in hc_list:
                        for i in syante[key]:
                            if cnt < 7:
                                sante_c += abs(key-2)
                                cnt += 1
                            else:
                                break
                        if cnt >= 7:
                            break
                    if cnt < 7:
                        sante_c -= 7-cnt

                    yaku_dict.setdefault(
                        '七対子', {'syanten': sante_c})

        # 二盃口
        # 純全帯
        # 混一色
        # 清一色

        #### ローカル役　####
        # 一色三順
        # 三連刻

        return yaku_dict


if __name__ == '__main__':
    y = class_Yaku()
    tsumo = [
        [53, ],
        [29, ],
        [29, ],
        [125, ],
        [42, ],
        [],
        [],
        [53, ],
        [],
        [11],
        [],
    ]
    tehai = [
        [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 51, 52, 53, ],
        #[11, 11, 11, 19, 31, 31, 31, 19, 38, 38, 38, 19, 29, ],
        [19, 31, 31, 31, 19, 37, 37, 37, 19, 29, ],
        [29, ],
        [12, 13, 14, 21, 22, 23, 31, 31, 27, 28, 29, 23, 24, ],
        [11, 11, 17, 125, 25, 17, 39, 33, 33, 38, 38, 39, 42, ],
        [11, 11, 11, 19, 31, 31, 31, 19, 38, 38, 38, 19, 29, ],
        [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 51, 52, 53, ],
        [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 51, 52, 52, ],
        [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 51, 52, 52, ],
        [19, 19, 19, 29, 39, 39, 39, 42, 43, 44, 51, 52, 52, ],
        [11, 11, 17, 125, 25, 17, 39, 33, 33, 38, 38, 39, 42, ],
    ]
    furo = [
        [],
        [
            {'38_38_38_38': (0, 38)},
        ],
        [
            {'38_38_38_38': (0, 38)},
            {'31_31_31_31': (3, 31)},
            {'19_19_19_19': (0, 19)},
            {'11_11_11_11': (3, 11)}
        ],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]
    for te, ts, f in zip(tehai, tsumo, furo):
        yaku_dict = y.judgement(te, f, ts, [], [16, ], isReach=False,
                                isTsumo=False, Ba='東', Tya='東')
        print(yaku_dict)
