from scene import *
from PIL import Image, ImageDraw

import majan_main

import io
import ui

A = Action


class Taku(Scene):
    # ---[0:initialize
    def __init__(self):
        super().__init__()

        self.background_color = "darkgreen"

        # 選択牌
        self.current_pai = None

        self.m_obj = majan_main.Game()

        # GUI 配牌( )
        self.g_haipai = [list() for i in range(self.m_obj.player_num)]
        # GUI 配牌 オブジェクト
        self.g_haipai_img = [list() for i in range(self.m_obj.player_num)]

        # GUI 捨て牌( )
        self.g_sutehai = [list() for i in range(self.m_obj.player_num)]
        # GUI 捨て牌 オブジェクト
        self.g_sutehai_img = [list() for i in range(self.m_obj.player_num)]

        self._hai_image()
        self._init_taku()

    # ---[1:牌のイメージファイルパス
    def _hai_image(self):
        self.hai_size = (24, 32)

        self.img_path = '../../../images/'

        manz_img_def = ['man{}[{}].gif'.format(i+1, i+1497) for i in range(9)]

        pinz_img_def = ['pin{}[{}].gif'.format(i+1, i+1507) for i in range(9)]

        souz_img_def = ['sou{}[{}].gif'.format(i+1, i+1517) for i in range(9)]

        ji = ['ton', 'nan', 'sha', 'pei', 'haku', 'hatsu', 'chun']
        jihai_img_def = [
            'ji{}-{}[{}].gif'.format(i+1, ji[i], i+1490) for i in range(7)]

        self.pai_img_def = [manz_img_def,
                            pinz_img_def, souz_img_def, jihai_img_def]

        self.pai_fuse_img = 'ura[1527].gif'

    # ---[2:イメージファイルをtextureに変換
    def _set_image_texture(self, pai, rotate):
        path = self.img_path + pai

        img = Image.open(path)
        img = img.rotate(rotate)

        timg = self._set_texture_img(img)

        return timg

    def _set_texture_img(self, img):
        bfile = io.BytesIO()
        img.save(bfile, format='png')
        bimg = bfile.getvalue()
        uimg = ui.Image.from_data(bimg)

        timg = Texture(uimg)

        return timg

    # ---[3:牌山の配置位置
    def _haiyama_node(self, p_num, dan, n):
        pai_size_w = int(self.hai_size[0]*0.5)
        pai_size_h = int(self.hai_size[1]*0.5)

        if p_num == 0:
            self.pai_size = (pai_size_h, pai_size_w)
            position = (self.g_haiyama_position[p_num][0]+self.g_dan_sp *
                        dan, self.g_haiyama_position[p_num][1]+pai_size_w*n)
            pass

        if p_num == 1:
            self.pai_size = (pai_size_w, pai_size_h)
            position = (self.g_haiyama_position[p_num][0]+pai_size_w*n,
                        self.g_haiyama_position[p_num][1]-self.g_dan_sp*dan)
            pass

        if p_num == 2:
            self.pai_size = (pai_size_h, pai_size_w)
            position = (self.g_haiyama_position[p_num][0]-self.g_dan_sp *
                        dan, self.g_haiyama_position[p_num][1]-pai_size_w*n)
            pass

        if p_num == 3:
            self.pai_size = (pai_size_w, pai_size_h)
            position = (self.g_haiyama_position[p_num][0]-pai_size_w*n,
                        self.g_haiyama_position[p_num][1]+self.g_dan_sp*dan)
            pass

        return position

    # ---[4:牌山初期化
    def _init_haiyama(self):
        self.g_haiyama = [list() for i in range(self.m_obj.player_num)]

        self.g_dan_sp = 3

        self.g_haiyama_position = [
            (80, 300),
            (100, 650),
            (300, 490),
            (290, 170),
        ]

        self.pai_rotate = [90, 0, 270, 180]

        pai_img = [self._set_image_texture(
            self.pai_fuse_img, self.pai_rotate[i]) for i in range(self.m_obj.player_num)]

        for p_num in range(self.m_obj.player_num):
            node_list = list()
            for dan in range(self.m_obj.haiyama_dan):
                for n in range(self.m_obj.haiyama_num):
                    position = self._haiyama_node(p_num, dan, n)
                    s_pai_img = pai_img[p_num]
                    pai_node = SpriteNode(s_pai_img, position=position)
                    pai_node.size = self.pai_size
                    self.add_child(pai_node)
                    node_list.append(pai_node)
            else:
                half = int((self.m_obj.haiyama_dan*self.m_obj.haiyama_num)/2)

                odd = node_list[half:]
                even = node_list[:half]

                for num in range(self.m_obj.haiyama_dan*self.m_obj.haiyama_num):
                    if num % 2 == 0:
                        pai = odd[int(num/2)]
                    else:
                        pai = even[int(num/2)]
                    self.g_haiyama[p_num].append(pai)
        return

    def _init_haipai(self):
        self.g_haipai_position = [
            (40, 260),
            (365, 120),
            (340, 560),
            (15, 700),
        ]

        pai_size_w = int(self.hai_size[0])
        pai_size_h = int(self.hai_size[1])

        self.g_pai_size = [
            (pai_size_h, pai_size_w),
            (pai_size_w, pai_size_h),
            (pai_size_h, pai_size_w),
            (pai_size_w, pai_size_h),
        ]

        self.g_haipai_offset = [
            (0, self.g_pai_size[0][1]*(-1)),
            (self.g_pai_size[1][0], 0),
            (0, self.g_pai_size[2][1]),
            (self.g_pai_size[3][0]*(-1), 0),
        ]

        self.pai_num_const = 14

        self.g_haipai_position = [
            (self.g_haipai_position[i][0]-self.g_haipai_offset[i][0]*self.pai_num_const,
             self.g_haipai_position[i][1]-self.g_haipai_offset[i][1]*self.pai_num_const,)
            for i in range(self.m_obj.player_num)
        ]

        self.g_pai_rotate = [270, 0, 90, 180]

        yama_index = self.m_obj.yama_index
        pai_index = self.m_obj.pai_index

        for num in range(len(self.m_obj.player_haipai)):
            self._set_haipai(num)

        return

    def _set_haipai(self, num):
        p_pai = self.m_obj.player_haipai[num]
        p_pai.sort()
        p_shepai = self.m_obj.pai_obj.set_haipai_kind_num(p_pai)
        self.g_haipai[num].append(p_shepai)
        for p_num, pai in enumerate(p_shepai):
            pai_img = self.pai_img_def[pai[0]][pai[1]]
            pai_img = self._set_image_texture(
                pai_img, self.g_pai_rotate[num])

            position = (
                self.g_haipai_position[num][0] +
                self.g_haipai_offset[num][0]*p_num,
                self.g_haipai_position[num][1] +
                self.g_haipai_offset[num][1]*p_num,
            )

            pai_node = SpriteNode(pai_img, position=position)
            pai_node.size = self.g_pai_size[num]
            self.add_child(pai_node)
            self.g_haipai_img[num].append(pai_node)

    def _set_init_dora_view(self):
        wareme_yama = self.m_obj.dora_yama
        dora_index = self.m_obj.dora_index

        dora_position = self.g_haiyama[wareme_yama][dora_index].position

        self.g_haiyama[wareme_yama][dora_index].remove_from_parent()

        (self.dora_kind, self.dora_num) = self.m_obj.pai_obj.get_pai_kind_num(
            self.m_obj.dora_view)

        dora_path = self.pai_img_def[self.dora_kind][self.dora_num]

        dora_rotate = (self.m_obj.player_num - wareme_yama) - 1
        if dora_rotate < 0:
            dora_rotate += self.m_obj.player_num
        if wareme_yama % 2 == 0:
            dora_pai_size = (
                int(self.hai_size[1]*0.5), int(self.hai_size[0]*0.5))
        else:
            dora_pai_size = (
                int(self.hai_size[0]*0.5), int(self.hai_size[1]*0.5))
        dora_rotate = dora_rotate * 90

        dora_img = self._set_image_texture(dora_path, dora_rotate)
        pai_node = SpriteNode(dora_img, position=dora_position)
        pai_node.size = dora_pai_size
        self.add_child(pai_node)

        return

    def _tumo_func(self):
        self.m_obj.tsumo()

        pick_const = 5

        # 選択牌の表示位置変化
        self._take_target_pai_position = [
            (pick_const, 0),
            (0, pick_const),
            (-pick_const, 0),
            (0, -pick_const),
        ]

        # ツモ牌の表示位置
        self._take_target_tumo_position = [
            (0, -pick_const),
            (pick_const, 0),
            (0, pick_const),
            (-pick_const, 0),
        ]

        # ツモって、14牌になったか。
        # ここを喰った牌と合わせて判断する必要がある。
        if len(self.m_obj.player_haipai[self.m_obj.current_player]) == self.pai_num_const:
            self.current_pai = self.pai_num_const - 1

            # 13牌目の位置を取得
            position = self.g_haipai_img[self.m_obj.current_player][-1].position

            # x,yに新しい座標を格納。
            x = position[0] + self.g_haipai_offset[self.m_obj.current_player][0] + \
                self._take_target_pai_position[self.m_obj.current_player][0] + \
                self._take_target_tumo_position[self.m_obj.current_player][0]
            y = position[1] + self.g_haipai_offset[self.m_obj.current_player][1] + \
                self._take_target_pai_position[self.m_obj.current_player][1] + \
                self._take_target_tumo_position[self.m_obj.current_player][1]

            position = (x, y)

            # 14牌目の種類を判別
            tumo_pai = self.m_obj.player_haipai[self.m_obj.current_player][self.pai_num_const-1]

            tumo_pai = self.m_obj.pai_obj.get_pai_kind_num(tumo_pai)
            # イメージを生成、表示
            pai_img = self.pai_img_def[tumo_pai[0]][tumo_pai[1]]
            pai_img = self._set_image_texture(
                pai_img, self.g_pai_rotate[self.m_obj.current_player])
            pai_node = SpriteNode(pai_img, position=position)
            pai_node.size = self.g_pai_size[self.m_obj.current_player]
            self.add_child(pai_node)

            #pai_node.blend_mode = BLEND_MULTIPLY
            # pai_node.color = '#909090'
            self.g_haipai_img[self.m_obj.current_player].append(pai_node)

            # 次の牌にインデックスを移動。
            self.m_obj.pai_index += 1
            if self.m_obj.pai_index >= self.m_obj.haiyama_num*self.m_obj.haiyama_dan:
                self.m_obj.pai_index = 0
                self.m_obj.yama_index += 1
                if self.m_obj.yama_index >= self.m_obj.player_num:
                    self.m_obj.yama_index = 0

        return

    def _sutehai_view(self):
        pai_size_w = int(self.hai_size[0]*0.8)
        pai_size_h = int(self.hai_size[1]*0.8)

        self.g_sute_hai_size = [
            (pai_size_h, pai_size_w),
            (pai_size_w, pai_size_h),
            (pai_size_h, pai_size_w),
            (pai_size_w, pai_size_h),
        ]

        self.g_sutehai_position = [
            (165, 500),
            (120, 260),
            (215, 290),
            (280, 540),
        ]

        self.g_sutehai_raw_offset = [
            (0, -self.g_sute_hai_size[0][1]),
            (self.g_sute_hai_size[1][0], 0),
            (0, self.g_sute_hai_size[2][1]),
            (-self.g_sute_hai_size[3][0], 0),
        ]
        self.g_sutehai_clm_offset = [
            (-self.g_sute_hai_size[0][0], 0),
            (0, -self.g_sute_hai_size[1][1]),
            (self.g_sute_hai_size[2][0], 0),
            (0, self.g_sute_hai_size[3][1])
        ]

        sutehai_index = len(self.g_sutehai[self.m_obj.current_player]) - 1

        sutehai_max_raw = 8

        x = self.g_sutehai_position[self.m_obj.current_player][0] + self.g_sutehai_raw_offset[self.m_obj.current_player][0]*(
            sutehai_index % sutehai_max_raw) + self.g_sutehai_clm_offset[self.m_obj.current_player][0]*int(sutehai_index/sutehai_max_raw)

        y = self.g_sutehai_position[self.m_obj.current_player][1] + self.g_sutehai_raw_offset[self.m_obj.current_player][1]*(
            sutehai_index % sutehai_max_raw) + self.g_sutehai_clm_offset[self.m_obj.current_player][1]*int(sutehai_index/sutehai_max_raw)

        position = (x, y)

        sute_hai = self.g_sutehai[self.m_obj.current_player][-1]

        # イメージを生成、表示
        pai_img = self.pai_img_def[sute_hai[0]][sute_hai[1]]
        pai_img = self._set_image_texture(
            pai_img, self.g_pai_rotate[self.m_obj.current_player])
        pai_node = SpriteNode(pai_img, position=position)
        pai_node.size = self.g_sute_hai_size[self.m_obj.current_player]
        self.add_child(pai_node)
        self.g_sutehai_img[self.m_obj.current_player].append(pai_node)

    def _create_msg_img(self):

        img = Image.new('RGBA', (60, 60), (128, 128, 128, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 59, 59), fill=(
            0, 0, 0, 128), outline=(255, 255, 255))

        timg = self._set_texture_img(img)

        _node = SpriteNode(timg, position=(200, 400))
        self.add_child(_node)

    def _init_taku(self):
        self.label = None

        self._create_msg_img()

        self._init_haiyama()

        self.m_obj.game_init()

        self.m_obj.sheypai()

        dise = self.m_obj.roll_dise()

        self.m_obj.wareme_init(dise[0] + dise[1])

        self.m_obj.haipai_init()

        self._set_init_dora_view()

        self._init_haipai()

        self._tumo_func()

    def setup(self):
        return

    def update(self):
        return

    def touch_began(self, touch):
        touch_l = self.point_from_scene(touch.location)

        for pai_num, pai in enumerate(self.g_haipai_img[self.m_obj.current_player]):
            if touch_l in pai.frame:

                if self.current_pai != pai_num:
                    # 捨て牌選択
                    position = self.g_haipai_img[self.m_obj.current_player][self.current_pai].position

                    x = position[0] - \
                        self._take_target_pai_position[self.m_obj.current_player][0]
                    y = position[1] - \
                        self._take_target_pai_position[self.m_obj.current_player][1]

                    position = (x, y)
                    self.g_haipai_img[self.m_obj.current_player][self.current_pai].position = position

                    position = self.g_haipai_img[self.m_obj.current_player][pai_num].position

                    x = position[0] + \
                        self._take_target_pai_position[self.m_obj.current_player][0]
                    y = position[1] + \
                        self._take_target_pai_position[self.m_obj.current_player][1]

                    position = (x, y)
                    self.g_haipai_img[self.m_obj.current_player][pai_num].position = position

                    self.current_pai = pai_num
                else:
                    # 捨て牌決定
                    sute_hai = self.m_obj.player_haipai[self.m_obj.current_player][self.current_pai]
                    self.m_obj.player_sutehai[self.m_obj.current_player].append(
                        sute_hai)

                    sute_hai_kind_num = self.m_obj.pai_obj.get_pai_kind_num(
                        sute_hai)

                    self.g_sutehai[self.m_obj.current_player].append(
                        sute_hai_kind_num)

                    self._sutehai_view()
                    self.m_obj.player_haipai[self.m_obj.current_player].pop(
                        self.current_pai)
                    self.m_obj.player_haipai[self.m_obj.current_player].sort()
                    self.g_haipai_img[self.m_obj.current_player][self.current_pai].remove_from_parent(
                    )

                    for obj in self.g_haipai_img[self.m_obj.current_player]:
                        obj.remove_from_parent()
                    else:
                        self.g_haipai_img[self.m_obj.current_player].clear()
                        self._set_haipai(self.m_obj.current_player)

                    sute_judge = self.m_obj.sute_judge(sute_hai)

                    print(sute_judge)

                    # プレイヤーインデックスを進める。
                    self.m_obj.current_player += 1
                    if self.m_obj.current_player >= self.m_obj.player_num:
                        self.m_obj.current_player = 0

                    self.current_pai = None

                    self._tumo_func()

                    # 捨て牌に対するアクションを記述
                    # リーチ
                    # ポン、チー、カン、ロン
                    # 流局

                    pass

                msg = '{} '.format(self.m_obj.haipai_num)
                if self.label != None:
                    self.label.remove_from_parent()
                self.label = LabelNode(msg, font=(
                    'Ubuntu Mono', 12), position=(50, 100), color='white')

                self.add_child(self.label)

    def touch_moved(self, touch):
        touch_l = self.point_from_scene(touch.location)

    def touch_ended(self, touch):
        touch_l = self.point_from_scene(touch.location)


if __name__ == '__main__':
    run(Taku(), PORTRAIT)
