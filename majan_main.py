import random
import class_Pai as Pai
import class_SheetOrder as Sheet


class Game (object):
    # ---[0:初期化
    def __init__(self):
        self.init_config()
        self.pai_obj = Pai.class_Pai()

        # プレイヤー数
        self.num_player = 4
        # 手牌数
        self.num_tehai = 13
        # 牌山の列数
        self.NUM_YAMA = self.pai_obj.NUM_YAMA
        # 牌山の段数
        self.NUM_YAMA_STEPS = self.pai_obj.NUM_YAMA_STEPS
        # 牌種別数
        self.NUM_PATTERN = self.pai_obj.NUM_PATTERN
        # 数字牌の種類
        self.NUM_PAI = self.pai_obj.NUM_PAI
        # 風牌の種類
        self.NUM_TSUU_PAI = self.pai_obj.NUM_TSUU_PAI
        # 三元牌の種類
        self.NUM_3GEN_PAI = self.pai_obj.NUM_3GEN_PAI
        # １種類の牌数
        self.NUM_TYPES = self.pai_obj.NUM_TYPES
        # 牌の合計数　136
        self.TOTAL_PAI = self.pai_obj.TOTAL_PAI

        # 場
        self.BA_DICT = {
            0: '東', 1: '南', 2: '西', 3: '北'
        }

        self.Sheet = Sheet.class_SheetOrder()

        return

    # ---[1:設定値初期化
    def init_config(self):
        # ================================
        # 原点
        self.conf_StartPoint = 25000
        # 基準点
        self.conf_BasePoint = 30000
        # ハコ割れドボンの有無
        self.conf_isDobon = False
        # ラス親の Top 時上がり止め
        self.conf_isAgriYame = True
        # リーチ棒が出せない千点以下リーチ可否
        self.conf_isNotHasReach = True
        # 南場における親番で平局（全員聴牌なし）時に流局する
        self.conf_isNanNagere = False
        # 南場における親番の流局判断で、親が聴牌しなければ流局
        # isNanNagere=False,isNanNagerePlus=True 時、親がノー聴牌、他が聴牌のときは流局
        self.conf_isNanNagerePlus = True
        # 流局時自動的に聴牌宣言の可否
        self.conf_isAutoTenpai = True
        # 形式聴牌の可否
        self.conf_isKeisikiTenpai = True
        # 喰いタン可否:True
        self.conf_isKuitan = True
        # 後付け可否:True
        self.conf_isAto = True
        # 完全先付け有無:False
        self.conf_isKanSaki = False
        # 槓裏ドラの有無:True
        self.conf_isKanUra = True
        # 赤ドラの有無:False
        self.conf_isAkadora = False
        # pai_number の一巡目 No.0-33 のときの 5 を赤牌とする。赤五萬 No.4,赤筒子 No,13,赤索子 No.22
        # pai_number/(TOTAL_PAI/NUM_TYPES)==0 のとき、PaiType==0-3 and __pai_indv__==(5-1)
        # 3 桁目 1 を付加して区別する。赤五萬 115、赤筒子 125、赤索子 135
        # 半荘以上のルールにおいて一度も上がれない場合の罰可否
        self.conf_isYakitori = False
        self.conf_YakitoriPoint = 3000
        # 5本場以上で二飜縛り可否:True
        self.conf_is5ren = True
        # ウマの有無
        self.conf_isUma = False
        self.conf_UmaPoint = [20000, 10000]

        # ================================
        # ダブルロンあり:True
        self.conf_isDoubleRon = True
        # トリプルロンあり:False
        self.conf_isTripleRon = False
        # 三家和時に上がり無効(isTripleRon が有効時は無視):True
        # ※基本は頭ハネとなる。
        self.conf_isSanTyaNagashi = True
        # オープンリーチの可否:False
        self.conf_isOpenReach = False
        # 流し万貫の可否:True
        self.conf_isNagashiMangan = True
        # フリテンリーチの可否:True
        self.conf_isFuritenReach = True
        # 海底、河底、嶺上、搶槓のみで成立可否:True
        self.conf_isAtoYaku = True
        # ダブル役満の可否:True
        self.conf_isDoubleYakuman = True
        # トリプル役満以上の可否:True
        # ※字一色、大四喜（ダブル）、四暗刻単騎（ダブル）=Max5 倍役満
        self.conf_isTripleYakuman = True
        # 数え役満の可否:True
        self.conf_isKazoeYakuman = True
        # 人和の可否:False
        self.conf_isTyenhoYakuman = False
        # 八連荘の可否:False
        self.conf_isParenYakuman = False
        # 十三不塔の可否:False
        self.conf_isSeasanputaYakuman = False
        # 十三無靠の可否:False
        self.conf_isSeasanushiYakuman = False

    # ---[2:ゲームパラメータの初期化
    def init_game(self):
        # ================================
        # ゲームパラメータの初期化
        # 場
        self.game_ba = 0
        # 局
        self.game_kyoku = 0
        # 本場
        self.game_honba = 0
        # プレイヤー点
        self.player_point = [
            self.conf_StartPoint for i in range(self.num_player)]
        # プレイヤー焼き鳥
        self.player_yakitori = [False for i in range(self.num_player)]

        # 場決め
        player = self._set_current_player()
        self.player_oya = player
        self.current_player = player

    # ---[3:プレイヤーエントリー番号をシャッフル
    def _player_order(self):
        # 親決めのくじ引き/サイコロの順番に使用する
        player_order = [i for i in range(self.num_player)]
        random.shuffle(player_order)
        return player_order

    # ---[4:起家を直接決める
    def _set_current_player(self):
        player = random.randint(0, 3)
        return player

    # ---[5:場の初期化
    def init_ba(self):

        # プレイヤー手牌
        self.player_tehai = [list() for i in range(self.num_player)]
        # プレイヤー捨牌
        self.player_sutehai = [list() for i in range(self.num_player)]
        # プレイヤー副露（泣き牌）
        self.player_furo = [list() for i in range(self.num_player)]
        # プレイヤー自模牌
        self.player_tsumo = [None for i in range(self.num_player)]

        # ドラ表示
        self.dora_list = list()
        # 配牌最大値
        self.haipai_max = self.TOTAL_PAI - \
            ((self.NUM_YAMA_STEPS*2+1)*self.num_player)

        self.haipai_num = 0

    # ---[6:賽の目による割れ目、ドラの初期化
    def init_wareme(self, dise):
        # Wareme_indexは親Index=0とした場合のPlayer_index、左回り順
        self.wareme_index = (dise % self.num_player)

        # Indexを右回りにするために奇数(1,3)の入れ替え
        self.haipai_yama_index = (
            self.num_player-self.wareme_index)*(self.wareme_index % 2)

        self.haipai_index = dise*self.NUM_YAMA_STEPS

        # ドラ表示のインデックス
        if dise < 3:
            self.dora_yama_index = self.haipai_yama_index - 1
            if self.dora_yama_index < 0:
                self.dora_yama_index = 3
            self.dora_index = (
                self.NUM_YAMA*self.NUM_YAMA_STEPS-1) - (self.haipai_index - 6)
        else:
            self.dora_yama_index = self.haipai_yama_index
            self.dora_index = self.haipai_index - 6

        __dora_view__ = self.pai_yama_list[self.dora_yama_index][self.dora_index]

        pai_char, pai_id = self.pai_obj.set_pai_char(__dora_view__)
        self.dora_list.append(pai_id)

    def init_haipai(self):
        # 配牌13枚
        # 各プレイヤー3巡目まで4枚ずつ、4巡目は1枚ずつ
        for haipai_num in range(4*self.num_player):
            if haipai_num >= 3 * self.num_player:
                r = 1
            else:
                r = 4

            # PlayerIndex
            player = haipai_num % self.num_player

            self.player_tehai[player].extend(
                self.pai_yama_list[self.haipai_yama_index][self.haipai_index:self.haipai_index+r])
            if self.haipai_index+r > self.NUM_YAMA_STEPS*self.NUM_YAMA:
                self.haipai_index = self.haipai_index + \
                    r - (self.NUM_YAMA_STEPS*self.NUM_YAMA)
                self.haipai_yama_index += 1
                if self.haipai_yama_index >= 4:
                    self.haipai_yama_index = 0
                self.player_tehai[player].extend(
                    self.pai_yama_list[self.haipai_yama_index][0:self.haipai_index])
            else:
                self.haipai_index = self.haipai_index+r
                if self.haipai_index >= self.NUM_YAMA_STEPS*self.NUM_YAMA:
                    self.haipai_index = 0
                    self.haipai_yama_index += 1
                    if self.haipai_yama_index >= 4:
                        self.haipai_yama_index = 0

        return self.player_tehai

    def _inc_haiyama_index_(self):
        self.haipai_index += 1
        if self.haipai_index >= self.NUM_YAMA_STEPS*self.NUM_YAMA:
            self.haipai_index = 0
            self.haipai_yama_index += 1
            if self.haipai_yama_index >= 4:
                self.haipai_yama_index = 0
        return

    def tsumo(self):
        tsumo = self.pai_yama_list[self.haipai_yama_index][self.haipai_index]
        pai_char, pai_id = self.pai_obj.set_pai_char(tsumo)

        self.player_tsumo[self.current_player] = pai_id
        self._inc_haiyama_index_()

        # Debug
        for p in range(self.num_player):
            judge_pai = self.player_tehai[p]
            if self.player_tsumo[p] is not None:
                judge_pai.extend([self.player_tsumo[p]])
            pai_char = self.pai_obj.set_haipai_disp(judge_pai)
            print(pai_char)
        return

    def tsumo_judge(self):

        judge_pai = self.player_tehai[self.current_player] + \
            [self.player_tsumo[self.current_player]]

        # ツモ上がりを判断

        # 暗カン、加カンを判断

        return

    def sute_judge(self, sute):

        sute_kind_num = self.pai_obj.get_pai_kind_num(sute)

        shimo_cha = self.current_player + 1
        if shimo_cha == self.num_player:
            shimo_cha = 0

        sute_judge = [dict() for i in range(self.num_player)]

        for set_dict in sute_judge:
            set_dict.setdefault('pon', list())
            set_dict.setdefault('chee', list())
            set_dict.setdefault('kan', list())
            set_dict.setdefault('ron', list())

        for num, haipai in enumerate(self.player_tehai):
            if num != self.current_player:
                haipai_chk = list()
                for pai in haipai:
                    pai_kind_num = self.pai_obj.get_pai_kind_num(pai)
                    haipai_chk.append(pai_kind_num)
                else:
                    # 下家の場合、チーを判断
                    if num == shimo_cha:
                        # 字牌は判断しない。
                        if sute_kind_num[0] < 3:

                            chee_list = list()
                            key_num = sute_kind_num[1]
                            # チーのパターン
                            chee_def = (
                                (-2, -1),
                                (-1, 1),
                                (1, 2),
                            )
                            for chk in chee_def:
                                p1 = key_num + chk[0]
                                p2 = key_num + chk[1]

                                if (p1 >= 0 and p1 < 9) and (p2 >= 0 and p2 < 9):
                                    p1 = (sute_kind_num[0], p1)
                                    p2 = (sute_kind_num[0], p2)

                                    if p1 in haipai_chk and p2 in haipai_chk:

                                        sute_judge[num]['chee'].append(
                                            (p1, p2))
                        pass

                    # ポンを判断
                    if haipai_chk.count(sute_kind_num) == 2:
                        sute_judge[num]['pon'].append(sute_kind_num)

                    # 明カンを判断
                    elif haipai_chk.count(sute_kind_num) == 3:
                        sute_judge[num]['kan'].append(sute_kind_num)

                        pass
                pass
        return sute_judge

    def run(self):
        # ================================
        # GameMenu & Config
        pass

        # ================================
        # プレイヤーエントリー

        # くじ引き順を決める
        player_order = self._player_order()
        # くじを生成
        lottery = self.Sheet.direction_lottery()
        # くじ引き
        pass
        # 場決め
        pass
        # 仮親
        dise1, dise2 = self.Sheet.roll_dise()
        dise = dise1+dise2
        player = (dise % self.num_player)-1

        # 省略形
        player = self._set_current_player()

        # 親プレイヤー
        self.player_oya = player
        # 現在のプレイヤー
        self.current_player = player

        # ================================
        # ゲーム初期化
        self.init_game()

        # ================================
        # 局/場のループ
        is_kyokuloop = True
        while(is_kyokuloop):
            # ================================
            # 場の初期化
            self.init_ba()

            # ================================
            # 牌山の生成
            self.pai_yama_list = self.pai_obj.create_haiyama(self.num_player)

            # ================================
            # 親のサイコロ振り
            dise1, dise2 = self.Sheet.roll_dise()

            # ================================
            # 割れ目およびドラ、配牌インデックス
            self.init_wareme(dise1+dise2)

            # ================================
            # 配牌13枚ずつ（PaiNumberでの配布）
            self.init_haipai()

            # ================================
            # 配牌を牌種別に変換
            for index, pai_list in enumerate(self.player_tehai):
                pai_list.sort()
                haipai_list, haipai_char_list = self.pai_obj.set_haipai_char(
                    pai_list)
                self.player_tehai[index] = haipai_list

                # ================================
                # 九種九牌アクション

            # ================================
            # 闘牌のループ
            is_toukailoop = True
            while(is_toukailoop):
                # ================================
                # CurrentPlayerの自模
                self.tsumo()

                # ================================
                # CurrentPlayerの自模判定
                self.tsumo_judge()

                # ================================
                # 自模上がりアクション

                # ================================
                # 他Playerの明槓/暗槓アクション
                # 槍槓/国士無双の放銃判定

                # ================================
                # CurrentPlayerの捨て牌

                # 捨て牌選択
                pass
                # 捨て牌リスト更新
                pass
                # 捨て牌表示
                pass

                # ================================
                # 他Playerの捨てアクション
                # 放銃判定
                # ポン判定
                # チー判定

                # ================================
                # 流局判定
                # 四風連打判定

                # ================================
                # 闘牌継続
                self.current_player += 1

                if self.current_player >= self.num_player:
                    self.current_player = 0

        return


if __name__ == '__main__':
    game = Game()
    game.run()
