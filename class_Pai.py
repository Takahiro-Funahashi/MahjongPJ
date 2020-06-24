import random

import tkinter as tk


class class_Pai (object):
    # ---[0:初期値
    def __init__(self):
        # 牌山の列数
        self.NUM_YAMA = 17
        # 牌山の段数
        self.NUM_YAMA_STEPS = 2
        # 牌種別数
        self.NUM_PATTERN = 4
        # 数字牌の種類
        self.NUM_PAI = 9
        # 風牌の種類
        self.NUM_TSUU_PAI = 4
        # 三元牌の種類
        self.NUM_3GEN_PAI = 3
        # １種類の牌数
        self.NUM_TYPES = 4
        # 牌の合計数　136
        self.TOTAL_PAI = ((self.NUM_PATTERN-1)*self.NUM_PAI +
                          self.NUM_TSUU_PAI+self.NUM_3GEN_PAI)*self.NUM_TYPES

        # 牌のリスト
        self.pais_list = list()

        self.PAI_CHAR_DEF = [
            # デバッグ用表示（環境依存）
            # 萬子
            ['一', 'ニ', '三', '四', '五', '六', '七', '八', '九'],
            # 筒子
            ['➀', '➁', '➂', '➃', '➄', '➅', '➆', '➇', '➈'],
            # 索子
            ['１', '２', '３', '４', '５', '６', '７', '８', '９'],
            # 字牌
            ['東', '南', '西', '北', '⬜︎', '発', '中'],
        ]
        self.PAI_DEF = [
            # 萬子
            [i for i in range(11, 11+self.NUM_PAI)],
            # 筒子
            [i for i in range(21, 21+self.NUM_PAI)],
            # 索子
            [i for i in range(31, 31+self.NUM_PAI)],
            # 字牌(東南西北白発中)
            [i for i in range(41, 41+self.NUM_TSUU_PAI)] + \
            [i for i in range(51, 51+self.NUM_3GEN_PAI)],
        ]

        return

    def _image_pai_(self):
        import os
        from PIL import Image, ImageTk, ImageDraw

        self.HEAD_N_DEF = [
            'man', 'pin', 'sou', 'ji',
        ]
        TSUU_N_DEF = [
            '-ton', '-nan', '-sha', '-pei', '-haku', '-hatsu', '-chun',
        ]
        _ura_ = 'ura'
        _aka_ = '-aka5'
        _e_ = '.gif'

        _image_path_ = os.path.abspath("image")

        self.PAI_IMG = dict()
        self.PAI_ROTATE_IMG = dict()

        f_path = os.path.join(_image_path_, _ura_ + _e_)
        _img_obj_ = Image.open(f_path).resize((30, 40))
        _img_ = ImageTk.PhotoImage(_img_obj_)
        self.PAI_IMG_URA = _img_

        for i, types in enumerate(self.PAI_DEF):
            _header_ = self.HEAD_N_DEF[i]
            for j, hai in enumerate(types):
                if i == 3:
                    _num_ = str(j+1) + TSUU_N_DEF[j]
                else:
                    _num_ = str(j+1)
                f_path = os.path.join(_image_path_, _header_ + _num_ + _e_)
                _img_obj_ = Image.open(f_path).resize((30, 40))
                _img_ = ImageTk.PhotoImage(_img_obj_)
                self.PAI_IMG.setdefault(hai, _img_)
                _img_obj_r = _img_obj_.rotate(90, expand=True)
                _img_ = ImageTk.PhotoImage(_img_obj_r)
                self.PAI_ROTATE_IMG.setdefault(hai, _img_)
        else:
            aka5 = [115, 125, 135]
            for i, key in enumerate(aka5):
                f_path = os.path.join(
                    _image_path_, self.HEAD_N_DEF[i] + _aka_ + _e_)
                _img_obj_ = Image.open(f_path).resize((30, 40))
                _img_ = ImageTk.PhotoImage(_img_obj_)
                self.PAI_IMG.setdefault(key, _img_)
                _img_obj_r = _img_obj_.rotate(90, expand=True)
                _img_ = ImageTk.PhotoImage(_img_obj_r)
                self.PAI_ROTATE_IMG.setdefault(key, _img_)

        return

    # ---[1:洗牌
    def shey_pai(self):
        # 牌の合計数分の数字リストを生成
        self.pais_list = list(range(self.TOTAL_PAI))
        # シャッフル（洗牌）
        random.shuffle(self.pais_list)

        return self.pais_list

    # ---[2:牌山作成
    def create_haiyama(self, num_player):
        # 洗牌
        pai_yama_list = self.shey_pai()

        # 牌山を17牌、2段に分ける。
        self.pai_yama_list = [
            pai_yama_list[
                self.NUM_YAMA_STEPS*self.NUM_YAMA*i:self.NUM_YAMA_STEPS*self.NUM_YAMA*(i+1)
            ]
            for i in range(num_player)
        ]

        return self.pai_yama_list

    # ---[3:牌種を計算
    def get_pai_kind_num(self, pai_number):
        __pai_type__ = int(pai_number/self.NUM_PATTERN/self.NUM_PAI)
        __pai_indv__ = int(pai_number/self.NUM_PATTERN % self.NUM_PAI)

        return (__pai_type__, __pai_indv__)

    # ---[4:牌のIDおよび表示文字
    def set_pai_char(self, pai_number, isAka=False):
        (__pai_type__, __pai_indv__) = self.get_pai_kind_num(pai_number)

        if __pai_type__ < self.NUM_PATTERN and __pai_indv__ < self.NUM_PAI:
            pai_char = self.PAI_CHAR_DEF[__pai_type__][__pai_indv__]
            pai_id = self.PAI_DEF[__pai_type__][__pai_indv__]
            if isAka:
                if __pai_type__ >= 0 and __pai_type__ <= 2 and __pai_indv__ == 5-1:
                    if (pai_number % (self.NUM_PATTERN*self.NUM_PAI)) % (self.NUM_TYPES*(5-1)) == 0:
                        pai_id += 100

        return pai_char, pai_id

    # ---[5:配牌リストをIDおよび表示文字に変換
    def set_haipai_char(self, haipai, isAka=False):
        haipai_list = list()
        haipai_char_list = list()
        if isinstance(haipai, list):
            for pai in haipai:
                pai_char, pai_id = self.set_pai_char(pai, isAka)
                haipai_list.append(pai_id)
                haipai_char_list.append(pai_char)
        return haipai_list, haipai_char_list

    # ---[5:配牌IDリストを表示文字に変換
    def set_haipai_disp(self, haipai_list, isAka=False):
        disp_list = list()
        for pai in haipai_list:
            pai = pai % 100
            num = pai % 10-1
            pat = int(pai/10)-1
            if pat == 4:  # 三元牌のみ別計算
                pat -= 1
                num += self.NUM_TSUU_PAI

            disp_list.append(self.PAI_CHAR_DEF[pat][num])

        return disp_list

    def _Debug_View_1(self, haipai_list):
        import tkinter as tk

        width, height = 800, 600
        _view_ = tk.Tk()
        _view_.geometry(f'{width}x{height}+300+300')
        _view_.title('麻雀')

        self._image_pai_()

        self.canvas = tk.Canvas(
            _view_, bg='green', width=width, height=height)
        self.canvas.pack()

        for y, haipai in enumerate(haipai_list):
            for x, hai in enumerate(haipai):
                img = self.PAI_IMG[hai]
                self.canvas.create_image(
                    30+35*x, 40+45*y, image=img, anchor=tk.NW)
        _view_.mainloop()

        return

    def _Debug_View_2(self):
        import tkinter as tk

        width, height = 800, 800
        _view_ = tk.Tk()
        _view_.geometry(f'{width}x{height}+300+300')
        _view_.title('麻雀')

        self._image_pai_()

        self.canvas = tk.Canvas(
            _view_, bg='green', width=width, height=height)
        self.canvas.pack()

        for y, types in enumerate(self.PAI_DEF):
            for x, hai in enumerate(types):
                for i in range(4):
                    img = self.PAI_IMG[hai]
                    self.canvas.create_image(
                        10+32*x, 10+(42*i)+(42*4)*y, image=img, anchor=tk.NW)
        _view_.mainloop()

        return

    def _Debug_View_3(self):
        self.select_haipai = dict()
        self.t_select = dict()
        self.haipai = list()
        self.furo = list()

        width, height = 700, 700
        _view_ = tk.Tk()
        _view_.geometry(f'{width}x{height}+300+300')
        _view_.title('麻雀 役判定エディター')

        self._image_pai_()

        self.canvas = tk.Canvas(
            _view_, bg='green', width=width, height=height-240)
        self.canvas.pack()
        self.t_canvas = tk.Canvas(
            _view_, bg='darkgreen', width=width, height=100)
        self.t_canvas.pack()

        self.InFrame = tk.Frame(_view_, bg='lightgray')
        self.InFrame.pack()
        self.InTextFrame = tk.Frame(_view_, bg='lightgray')
        self.InTextFrame.pack()

        self.btnClear = tk.Button(
            self.InFrame, text='Reset', command=self.canvas_reset)
        self.btnClear.pack(side=tk.LEFT)
        self.btnRandom = tk.Button(
            self.InFrame, text='Random', command=self.set_random)
        self.btnRandom.pack(side=tk.LEFT)
        self.btnChey = tk.Button(
            self.InFrame, text='チー', command=self.chey)
        self.btnChey.pack(side=tk.LEFT)
        self.btnPon = tk.Button(
            self.InFrame, text='ポン', command=self.pon)
        self.btnPon.pack(side=tk.LEFT)
        self.btnKan = tk.Button(
            self.InFrame, text='明カン', command=self.minkan)
        self.btnKan.pack(side=tk.LEFT)
        self.btnKan = tk.Button(
            self.InFrame, text='暗カン', command=self.ankan)
        self.btnKan.pack(side=tk.LEFT)
        self.btnTsumo = tk.Button(
            self.InFrame, text='ツモ', command=self.tsumo)
        self.btnTsumo.pack(side=tk.LEFT)
        self.btnRon = tk.Button(
            self.InFrame, text='ロン', command=self.ron)
        self.btnRon.pack(side=tk.LEFT)

        self.renew_feild()

        self.isDrag = False
        self.isTsel = False
        self.canvas.bind('<Button-1>', self.mouse_left_clicked)
        self.canvas.bind('<Motion>', self.mouse_move_on)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_release)

        self.t_canvas.bind('<Button-1>', self.t_mouse_left_clicked)

        _view_.mainloop()

        return

    def renew_feild(self):
        wlist = self.canvas.find_all()
        for i in wlist:
            self.canvas.delete(i)

        for pai_number in range(int(self.TOTAL_PAI)):
            (_, pai_id) = self.set_pai_char(pai_number, True)
            img = self.PAI_IMG[pai_id]
            pai_id = (pai_id % 100)
            if pai_id > 50:
                pai_id = pai_id-10+4
            mp0_sj1 = int((int(pai_id/10)-1)/2)
            ms0_oj1 = (int(pai_id/10)-1) % 2
            num = pai_id % (self.NUM_PAI+1)

            x = 10+32*num+(32*(self.NUM_PAI+1))*ms0_oj1
            y = 20+(42*(pai_number % self.NUM_TYPES))+(42*4)*mp0_sj1
            tag_name = 'pai_' + \
                self.HEAD_N_DEF[int(pai_id/10)-1]+'_'+str(num) + \
                '_'+str((pai_number % self.NUM_TYPES) + 1)
            self.canvas.create_image(
                x, y, image=img, anchor=tk.NW, tag=tag_name)

        for i in range(14):
            x = 80+35*i
            if i == 13:
                x += 15
            y = 390
            w, h = 30, 40
            self.canvas.create_rectangle(x, y, x+w, y+h,
                                         fill='white', stipple='gray25', tag=f'tehai_{i}')
        return

    def canvas_reset(self):
        self.renew_feild()
        wlist = self.t_canvas.find_all()
        for i in wlist:
            self.t_canvas.delete(i)
        self.t_select.clear()
        self.haipai.clear()
        self.furo.clear()
        self.isTsel = False
        return

    def canvas_coords(self, canvas):
        sx = x = int(canvas.winfo_rootx())
        sy = y = int(canvas.winfo_rooty())
        w = int(canvas['width'])
        h = int(canvas['height'])
        ex = sx + w - 1
        ey = sy + h - 1

        return (sx, sy, ex, ey)

    def chk_canvas_coords(self, canvas, point):
        _canvas_coords = self.canvas_coords(canvas)

        SX = X = 0
        SY = Y = 1
        EX = 2
        EY = 3

        if ((point[X] >= _canvas_coords[SX] and point[X] <= _canvas_coords[EX])
                and (point[Y] >= _canvas_coords[SY] and point[Y] <= _canvas_coords[EY])):
            return True

        return False

    def mouse_left_clicked(self, event):
        self.start_tag = None
        self.moveon_tag = None
        self.d_mouse = (0, 0)
        self.W_origin = None

        canvas = self.canvas

        point = (event.x_root, event.y_root)
        if self.chk_canvas_coords(canvas, point):
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)
            obj_list = canvas.find_overlapping(x, y, x, y)

            for target in obj_list:
                tag_list = canvas.gettags(target)
                for tag in tag_list:
                    if 'pai' in tag:
                        if self.isTsel:
                            _hai_ = tag.split('_')[1:]
                            ty, n, o = _hai_
                            typ = self.HEAD_N_DEF.index(ty)+1
                            if typ == 4 and int(n) > 4:
                                typ = 5
                                n = int(n) - 4
                            pai_id = typ*10+int(n)
                            if typ < 4 and int(n) == 5 and int(o) == 1:
                                pai_id = pai_id + 100
                            _tag_ = list(self.t_select.keys())[0]
                            t = self.t_select[_tag_]
                            tag_name = 'tehai_'+_tag_
                            x, y = self.t_canvas.coords(tag_name)
                            self.t_canvas.delete(tag_name)
                            img = self.PAI_IMG[pai_id]
                            self.t_canvas.create_image(
                                x, y, image=img, anchor=tk.NW, tag=tag_name)
                            self.t_canvas.tag_raise(t, tag_name)
                            self.haipai[int(_tag_)] = pai_id
                            print(self.haipai)
                        else:
                            self.start_tag = tag
                            self.isDrag = True
                            self.d_mouse = (x, y)
                            self.W_origin = canvas.coords(self.start_tag)
                        break
        return

    def mouse_move_on(self, event):
        X, Y = 0, 1
        if self.isDrag:
            isOnW = False
            x, y = event.x_root, event.y_root

            canvas = self.canvas

            point = (event.x_root, event.y_root)
            if self.chk_canvas_coords(canvas, point):
                x = canvas.canvasx(event.x)
                y = canvas.canvasy(event.y)
                obj_list = canvas.find_overlapping(x, y, x, y)

                dx = x-self.d_mouse[X]
                dy = y-self.d_mouse[Y]

                if self.start_tag is not None:
                    canvas.move(self.start_tag, dx, dy)
                    self.d_mouse = (x, y)

                for target in obj_list:
                    tag_list = canvas.gettags(target)
                    for tag in tag_list:
                        if 'tehai' in tag:
                            isOnW = True
                            if self.moveon_tag != tag:
                                if self.moveon_tag is not None:
                                    canvas.itemconfigure(
                                        self.moveon_tag, fill='white')
                                self.moveon_tag = tag
                                canvas.itemconfigure(
                                    self.moveon_tag, fill='orange')
                            break
                if not isOnW and self.moveon_tag is not None:
                    canvas.itemconfigure(self.moveon_tag, fill='white')
                    self.moveon_tag = None
        return

    def mouse_release(self, event):
        self.isDrag = False

        canvas = self.canvas

        if self.moveon_tag is not None:
            if self.start_tag is not None:
                sx, sy = canvas.coords(self.start_tag)
                ex, ey, _, _ = canvas.coords(self.moveon_tag)
                dx = ex-sx
                dy = ey-sy
                canvas.move(self.start_tag, dx, dy)
                canvas.tag_raise(self.start_tag, self.moveon_tag)
                canvas.delete(self.moveon_tag)
                self.select_haipai.setdefault(self.moveon_tag, self.start_tag)
                canvas.dtag(self.start_tag, self.start_tag)
                if len(self.select_haipai) > 13:
                    self.set_calc_canvas()
                    pass
        else:
            if self.start_tag is not None:
                sx, sy = canvas.coords(self.start_tag)
                if self.W_origin is not None:
                    ex, ey = self.W_origin
                    dx = ex-sx
                    dy = ey-sy
                    canvas.move(self.start_tag, dx, dy)

        self.W_origin = None
        self.start_tag = None
        self.moveon_tag = None

        return

    def t_mouse_left_clicked(self, event):

        canvas = self.t_canvas

        point = (event.x_root, event.y_root)
        if self.chk_canvas_coords(canvas, point):
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)
            obj_list = canvas.find_overlapping(x, y, x, y)

            for target in obj_list:
                tag_list = canvas.gettags(target)
                for tag in tag_list:
                    if 'tehai_' in tag:
                        x, y = canvas.coords(tag)
                        w, h = 30, 40
                        tag = tag.strip('tehai_')
                        if tag in self.t_select:
                            tag_name = self.t_select[tag]
                            canvas.delete(tag_name)
                            self.t_select.pop(tag)
                        else:
                            tag_name = f'sel_{tag}'
                            canvas.create_rectangle(x, y, x+w, y+h,
                                                    fill='red', stipple='gray50', tag=tag_name)
                            self.t_select.setdefault(tag, tag_name)
                        break
        if len(self.t_select) == 1:
            self.isTsel = True
        else:
            self.isTsel = False
        return

    def set_calc_canvas(self):
        wlist = self.t_canvas.find_all()
        for i in wlist:
            self.t_canvas.delete(i)
        self.t_select.clear()
        self.haipai.clear()
        self.furo.clear()
        self.isTsel = False

        temp_tehai = [v.split('_')[1:] for v in self.select_haipai.values()]
        for _hai_ in temp_tehai:
            ty, n, o = _hai_
            typ = self.HEAD_N_DEF.index(ty)+1
            if typ == 4 and int(n) > 4:
                typ = 5
                n = int(n) - 4
            pai_id = typ*10+int(n)
            if typ < 4 and int(n) == 5 and int(o) == 1:
                pai_id = pai_id + 0.5
            self.haipai.append(pai_id)
        else:
            self.haipai.sort()
            if 15.5 in self.haipai:
                index = self.haipai.index(15.5)
                self.haipai[index] = 125
            if 25.5 in self.haipai:
                index = self.haipai.index(25.5)
                self.haipai[index] = 125
            if 35.5 in self.haipai:
                index = self.haipai.index(35.5)
                self.haipai[index] = 135

            self.write_t_canvas()

        return

    def write_t_canvas(self):
        last_index = len(self.haipai)-1
        for i, pai_id in enumerate(self.haipai):
            img = self.PAI_IMG[pai_id]
            x = 20 + 35 * i
            if i == last_index:
                x += 10
            y = 30
            tag_name = f'tehai_{i}'
            self.t_canvas.create_image(
                x, y, image=img, anchor=tk.NW, tag=tag_name)

    def set_random(self):
        self.canvas_reset()

        pai_yama_list = self.create_haiyama(num_player=4)
        haipai = pai_yama_list[0][0:14]
        _haipai_list_, _ = self.set_haipai_char(
            haipai, isAka=True)
        _haipai_list_.sort()

        self.haipai = _haipai_list_
        self.write_t_canvas()

    def del_t_select(self):
        wlist = self.t_canvas.find_all()
        for i in wlist:
            self.t_canvas.delete(i)
        self.t_select.clear()
        self.write_t_canvas()
        return

    def write_furo(self):
        offset = 0
        for f in self.furo:
            select = list()
            for k, v in f.items():
                flen = len(k)
                for i in range(int(flen/2)):
                    pid = int(k[i*2:i*2+2])
                    select.append(pid)
                offset += 32*int(flen/2) + 5
                if v[0] != 0:
                    offset += 10
                for i, pai_id in enumerate(select):
                    if i == 0 and v[0] != 0:
                        y = 40
                        x = 680-offset
                        img = self.PAI_ROTATE_IMG[pai_id]
                    else:
                        x = 680-offset+10+32*i
                        y = 30
                        img = self.PAI_IMG[pai_id]
                    if (i == 0 or i == 3) and v[0] == 0:
                        img = self.PAI_IMG_URA
                    self.t_canvas.create_image(
                        x, y, image=img, anchor=tk.NW)
            if v[0] == 0:
                offset -= 10
        return

    def chey(self):
        pop_index = list()
        select = list()
        for key in self.t_select:
            a = self.haipai[int(key)]
            select.append(a)
            pop_index.append(int(key))
        else:
            pop_index.sort()

        if len(select) == 3 and len(set(select)) == 3:
            select.sort()
            if select[2] - select[0] == 2:
                for i, p_index in enumerate(pop_index):
                    self.haipai.pop(p_index-i)
                self.del_t_select()

                key = f'{select[0]}{select[1]}{select[2]}'
                self.furo.append({key: (3, select[0])})
                print(self.furo)
                self.write_furo()
                '''
                offset = 0
                for f in self.furo:
                    for k, v in f.items():
                        flen = len(k)
                        offset += 32*int(flen/2) + 5
                        if v[0] != 0:
                            offset += 10

                for i, pai_id in enumerate(select):
                    if i == 0:
                        x = 580-offset
                        y = 40
                        img = self.PAI_ROTATE_IMG[pai_id]
                    else:
                        x = 580-offset+10+32*i
                        y = 30
                        img = self.PAI_IMG[pai_id]
                    self.t_canvas.create_image(
                        x, y, image=img, anchor=tk.NW)
                self.furo.append({key: (3, select[0])})
                '''

    def pon(self):
        pop_index = list()
        select = list()
        for key in self.t_select:
            a = self.haipai[int(key)]
            select.append(a)
            pop_index.append(int(key))
            pop_index.sort()

        if len(select) == 3 and len(set(select)) == 1:
            for i, p_index in enumerate(pop_index):
                self.haipai.pop(p_index-i)
            self.del_t_select()
            pai_id = select[0]
            key = f'{pai_id}{pai_id}{pai_id}'
            self.furo.append({key: (3, pai_id)})
            self.write_furo()
            return

            offset = 0
            for f in self.furo:
                for k, v in f.items():
                    flen = len(k)
                    offset += 32*int(flen/2) + 5
                    if v[0] != 0:
                        offset += 10

            for i, pai_id in enumerate(select):
                if i == 0:
                    x = 580-offset
                    y = 40
                    img = self.PAI_ROTATE_IMG[pai_id]
                else:
                    x = 580-offset+10+32*i
                    y = 30
                    img = self.PAI_IMG[pai_id]
                self.t_canvas.create_image(
                    x, y, image=img, anchor=tk.NW)
            self.furo.append({key: (3, pai_id)})

    def minkan(self):
        pop_index = list()
        select = list()
        for key in self.t_select:
            a = self.haipai[int(key)]
            select.append(a)
            pop_index.append(int(key))
        else:
            select.append(a)
            pop_index.sort()

        if len(select) == 4 and len(set(select)) == 1:
            for i, p_index in enumerate(pop_index):
                self.haipai.pop(p_index-i)
            self.del_t_select()
            pai_id = select[0]
            key = f'{pai_id}{pai_id}{pai_id}{pai_id}'
            self.furo.append({key: (3, pai_id)})
            self.write_furo()
            return

            offset = 0
            for f in self.furo:
                for k, v in f.items():
                    flen = len(k)
                    offset += 32*int(flen/2) + 5
                    if v[0] != 0:
                        offset += 10

            for i, pai_id in enumerate(select):
                if i == 0:
                    x = 580-32-offset
                    y = 40
                    img = self.PAI_ROTATE_IMG[pai_id]
                else:
                    x = 580-32-offset+10+32*i
                    y = 30
                    img = self.PAI_IMG[pai_id]
                self.t_canvas.create_image(
                    x, y, image=img, anchor=tk.NW)
            self.furo.append({key: (3, pai_id)})

    def ankan(self):
        pop_index = list()
        select = list()
        for key in self.t_select:
            a = self.haipai[int(key)]
            select.append(a)
            pop_index.append(int(key))
        else:
            select.append(a)
            pop_index.sort()

        if len(select) == 4 and len(set(select)) == 1:
            for i, p_index in enumerate(pop_index):
                self.haipai.pop(p_index-i)
            self.del_t_select()
            pai_id = select[0]
            key = f'{pai_id}{pai_id}{pai_id}{pai_id}'
            self.furo.append({key: (0, pai_id)})
            self.write_furo()
            return

            offset = 0
            for f in self.furo:
                for k, v in f.items():
                    flen = len(k)
                    offset += 32*int(flen/2) + 5
                    if v[0] != 0:
                        offset += 10

            for i, pai_id in enumerate(select):
                x = 580-32-offset+10+32*i
                y = 30
                if i == 0 or i == 3:
                    img = self.PAI_IMG_URA
                else:
                    img = self.PAI_IMG[pai_id]
                self.t_canvas.create_image(
                    x, y, image=img, anchor=tk.NW)
            self.furo.append({key: (0, pai_id)})

    def tsumo(self):
        return

    def ron(self):
        return


if __name__ == '__main__':
    Pai = class_Pai()
    '''
    # 洗牌の確認
    pais_list = Pai.shey_pai()
    print(pais_list)
    '''
    '''

    haipai_list = list()

    for i in range(1):
        # 牌山の生成
        pai_yama_list = Pai.create_haiyama(num_player=4)
        # 牌山の中身を確認
        c_Pai_Yama_List = list()
        for Yama in pai_yama_list:
            Yama_list = list()
            # print(len(Yama), Yama)
            for P in Yama:
                # __pai_type__, __pai_indv__ = Pai.get_pai_kind_num(pai_number=P)
                # print(__pai_type__, __pai_indv__)
                pai_char, pai_id = Pai.set_pai_char(pai_number=P, isAka=True)
                # Yama_list.append(pai_char)
                Yama_list.append(pai_id)
            else:
                c_Pai_Yama_List.append(Yama_list)
        else:
            # print(c_Pai_Yama_List)
            key_dict = dict()
            for cYama in c_Pai_Yama_List:
                for key in set(cYama):
                    if key in key_dict:
                        key_dict[key] += cYama.count(key)
                    else:
                        key_dict.setdefault(key, cYama.count(key))
            else:
                print(key_dict)  # 牌の個数をカウントする
                print(len(key_dict.keys()))  # 牌種別数
        # 仮の配牌時
        haipai = pai_yama_list[0][0:14]
        _haipai_list_, haipai_char_list = Pai.set_haipai_char(
            haipai, isAka=True)
        print(_haipai_list_)
        print(haipai_char_list)
        haipai_list.append(_haipai_list_)
    '''
    '''
    Pai._Debug_View_1(haipai_list)
    '''

    Pai._Debug_View_3()
