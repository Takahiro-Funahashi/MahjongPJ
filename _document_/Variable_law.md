# Variable

---

## ルール設定

- 荘数  
  GameMode  
  =1:東風荘  
  =2:半荘  
  =3:一荘
  =4:半荘延長あり（基準点未達時に西場入り）
- ルール
  - conf_StartPoint = 25000
  - conf_BasePoint = 30000
  - conf_isDobon:ハコ割れドボンの有無:False
  - conf_isAgriYame:ラス親の Top 時上がり止め:True
  - conf_isNotHasReach:リーチ棒が出せない千点以下リーチ可否:True
  - conf_isNanNagere:南場における親番で平局（全員聴牌なし）時に流局する:False
  - conf_isNanNagerePlus:南場における親番の流局判断で、親が聴牌しなければ流局:True  
    ※conf_isNanNagere=False,conf_isNanNagerePlus=True 時、親がノー聴牌、他が聴牌のときは流局
  - conf_isAutoTenpai:流局時自動的に聴牌宣言の可否:True
  - conf_isKeisikiTenpai:形式聴牌の可否:True
  - conf_isKuitan:喰いタン可否:True
  - conf_isAto:後付け可否:True
  - conf_isKanSaki:完全先付け有無:False
  - conf_isKanUra:槓裏ドラの有無:True
  - conf_isAkadora:赤ドラの有無:False
    pai_number の一巡目のときの 5 を赤牌とする。赤五萬 No.4,赤筒子 No,13,赤索子 No.22  
    **pai_type**==0-2 and **pai_indv**==(5-1) and (pai_number % (NUM_PATTERN*NUM_PAI)) % (NUM_TYPES*(5-1)) == 0  
    3 桁目 1 を付加して区別する。赤五萬 115、赤筒子 125、赤索子 135
  - conf_isYakitori:半荘以上のルールにおいて一度も上がれない場合の罰可否:False
  - conf_YakitoriPoint = 3000
  - conf_is5ren:5 本場以上で二飜縛り可否:True
  - conf_isUma:ウマの有無:False
  - conf_UmaPoint = [20000,10000]
- 上がりルール
  - conf_isDoubleRon:ダブルロンあり:True
  - conf_isTripleRon:トリプルロンあり:False
  - conf_isSanTyaNagashi:三家和時に上がり無効(conf_isTripleRon が有効時は無視):True  
    ※基本は頭ハネとなる。
  - conf_isOpenReach:オープンリーチの可否:False
  - conf_isNagashiMangan:流し万貫の可否:True
  - conf_isFuritenReach:フリテンリーチの可否:True
  - conf_isAtoYaku:海底、河底、嶺上、搶槓のみで成立可否:True
  - conf_isDoubleYakuman:ダブル役満の可否:True
  - conf_isTripleYakuman:トリプル役満以上の可否:True  
    　※字一色、大四喜（ダブル）、四暗刻単騎（ダブル）=Max5 倍役満
  - conf_isKazoeYakuman:数え役満の可否:True
  - conf_isTyenhoYakuman:人和の可否:False
  - conf_isParenYakuman:八連荘の可否:False
  - conf_isSeasanputaYakuman:十三不塔の可否:False
  - conf_isSeasanushiYakuman:十三無靠の可否:False

---

## プレイヤー

- プレイヤーの数
  ```
  num_player = 4
  ```
- プレイヤーの手牌  
  player_tehai[player_index]
  0-12
  手牌（暗牌）
  ```
  player_tehai[player_index] = list()
  ```
  手牌（泣き：明牌{暗槓含む}）  
  例：[[{'111213':(3,11)},{'212121':(2,21)}]]  
  → 萬子の 1,2,3 を上家から 1 をチー、筒子の 1 を対面からポンの順で泣いた  
  0：自分（暗槓の場合のみ）、1：下家、2：対面、3：上家  
  明刻は加槓可能なので、自模時の判定に加える。  
  また加槓は槍槓によるロン牌となるので、判定に加える。
  ```
  player_furo[player_index] = list()
  ```
  自模牌
  ```
  player_tsumo[player_index]:int
  ```
  ※手牌（暗牌）、自模牌は組合せパターンにより順子、対子を判断する。  
  ※手牌（明牌）は順子、対子確定
- プレイヤーの捨牌  
  リストの Index が巡目となる。  
  常に親のリスト長が最大となるようにする。  
  ポン、チー、カン（明槓）時に各プレイヤーの player_sutehai は空を追加し、巡目の整合性を取る。  
  天和、地和、人和（特殊ルール）、ダブルリーチ、一発の判定に使用する  
  泣かれた牌はそのまま player_sutehai に残し、フリテンの判断に使用する。
  ```
  player_sutehai[player_index] = list()
  ```

---

## 牌

- 牌の絵柄数（萬子、筒子、索子、字牌）
  ```
  NUM_PATTERN = 4
  ```
- 牌の種類数（1-9）
  ```
  NUM_PAI = 9
  NUM_TSUU_PAI = 4
  NUM_3GEN_PAI = 3
  ```
- 牌の数
  ```
  NUM_TYPES = 4
  ```
- 牌の総数
  ```
  TOTAL_PAI = ((NUM_PATTERN-1)*NUM_PAI + NUM_TSUU_PAI+NUM_3GEN_PAI)*NUM_TYPES = 136
  ```
- 牌のリスト  
  リストの生成 pais_list = list(range(TOTAL_PAI))  
  洗牌（シーパイ）
  ```
  random.shuffle(pais_list)
  ```
- 牌の特定  
  牌の番号：Pais_List 内の番号：PaiNumber
  - 種別
    ```
    __pai_type__ = int(牌の番号：Pais_List 内の番号：PaiNumber/NUM_PATTERN/NUM_PAI)
    ```
  - 牌種
    ```
    __pai_indv__ = int(牌の番号：Pais_List 内の番号：PaiNumber/NUM_PATTERN%NUM_PAI)
    ```
  - 辞書  
    [**pai_type**][paiindv]で指定する。
    ```
    PAI_CHAR_DEF = [
    #デバッグ用表示（環境依存）
    #萬子
    ['一','ニ','三','四','五','六','七','八','九'],
    #筒子
    ['➀','➁','➂','➃','➄','➅','➆','➇','➈'],
    #索子
    ['１','２','３','４','５','６','７','８','９'],
    #字牌
    ['東','南','西','北','⬜︎','発','中'],
    ]
    PAI_DEF = [
    #萬子
    [i for i in range(11,11+9)],
    #筒子
    [i for i in range(21,21+9)],
    #索子
    [i for i in range(31,31+9)],
    #字牌(東南西北白発中)
    [i for i in range(41,41+4)]+[i for i in range(51,51+3)],
    ]
    ```

---

## 牌山

- 牌山の段数
  ```
  NUM_YAMA_STEPS = 2
  ```
- 牌山の列数
  ```
  NUM_YAMA = 17
  ```
- 牌山リスト(砌牌：チーパイ)
  ```
  pai_yama_list = [num_player][NUM_YAMA*NUM_YAMA_STEPS]
  ```
  代入式
  ```
  pai_yama_list = [pais_list[NUM_YAMA_STEPS*NUM_YAMA:NUM_YAMA_STEPS*NUM_YAMA*(i*1)] for i in range(num_player)]
  ```
- 牌山
  - 親から見て、目の前の山を haipai_yama_index=0 とする。  
    親手前：index=0  
    下家：index=1  
    対面：index=2  
    上家：index=3  
    ※ 自模順と逆回りの時計回り
  - 親から見て、右端の上の牌を haipai_index=0 とする。  
    　　列数 ｜ 17|16|15|14|13|12|11|10|09|08|07|06|05|04|03|02|01|  
    　　 index ｜ 32|30|28|26|24|22|20|18|16|14|12|10|08|06|04|02|00|  
    　　 index ｜ 33|31|29|27|25|23|21|19|17|15|13|11|09|07|05|03|01|

---

## 局/場

- 場
  東風荘ルール（東）  
  半荘ルール（東南）  
  一荘ルール（東南西北）  
  半荘延長ルール（南場終了時、どのプレイヤーも基準点（ほとんどの場合 30000 点）に届かないときに西場入り）
  ```
  game_ba:int 0-3
  ```
  ```
    BA_DICT = {
    0:'東',1:'南',2:'西',3:'北'
    }
  ```
- 局
  ```
  game_kyoku:int 0-3
  ```
- 本場
  局の連荘数  
  ルールによって 5 本場以上が二飜縛りとなる
  ```
  game_honba:int 0-
  ```
- 場決め
  - 牌取り順/仮順
    便宜上、選択順を決定する。プレイヤーエントリー順に下記乱数で決定
    ```
    random.randint(0, 残数（最大値3）)
    ```
  - 牌取り方式
    GUI による選択  
    東南西北白の牌をランダムに並べ選択させる  
    プレイヤーがコンピュータの場合は、random.randint(0, 残数)により、選択する牌をランダム選択とする。
  - 席順
    牌取り方式による席順（東南西北）左回り  
    あるいは仮順番号通りの左回り
  - 親決め
    席順 0 番（東）によるサイコロ  
    サイコロ出目によって、席順 0 番（東）を 1 として左回りにカウントした位置が親  
    1、5、9：（自）、2、6、10：（右、下家）、3、7、11：（対面）、4、8、12：（左、上家）
    ```
    dise1 = random.randint(1,6)
    dise2 = random.randint(1,6)
    ```

---

## 配牌

- 親による割れ目決め
  親（起家：チーチャ）によるサイコロ  
  サイコロ出目によって、席順 0 番（東）を 1 として左回りにカウントした位置が親  
  1、5、9：（自）、2、6、10：（右、下家）、3、7、11：（対面）、4、8、12：（左、上家）  
  割れ目の山：Pai_Yama_List[出目カウント-1]

  ```
  dise1 = random.randint(1,6)
  dise2 = random.randint(1,6)
  ```

- 牌山
  便宜上、親の Index=0 として、Pai_Yama_List[Index]として牌山の位置を特定する。  
  割れ目による特殊ルールを採用する場合に Index 位置が関係する。
- 配牌
  pai_yama_list[出目カウント-1]の牌山から、  
  pai_yama_list[出目カウント-1][(出目カウント-1)*num_yama_steps(=2)]が配牌開始位置  
  配牌時は、親は Index=haipai_index+0-3,16-19,32-35,48 の牌を配牌として受け取る  
  親の一巡目自模は、Index=haipai_index+52  
  配牌 Index

  ```
  #山
  haipai_yama_index:int 0-3
  #牌
  haipai_index:int 0-(NUM_YAMA*NUM_YAMA_STEPS-1)
  ```

- ドラ表示牌
  Index

  ```
  #山
  dora_yama_index
  #牌
  dora_index
  ```

  表示牌の次牌がドラ  
  槓するたびに追加する。  
  Index は最初のドラ表示牌とし、裏ドラは Index から求める

  ```
  dora_list
  ```

- 配牌リミット
  初期値：haipai_max = TOTAL_PAI(=136) - (((NUM_YAMA_STEPS*2+1)*num_player)=13)  
  親 1 巡目自模（いわゆる配牌最後のチョンチョンの最後の牌）からカウントダウンを始める。  
  槓するごとに配牌リミット数を減じる
  ```
  haipai_max
  ```
