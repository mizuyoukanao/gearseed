import argparse

parser = argparse.ArgumentParser(description='seedからこの先に付くギアパワーを計算し表示する')
parser.add_argument('seed', type=lambda hx: int(hx, 0), help='16進数のseed(先頭は0xを付ける)')
parser.add_argument('brand', type=str, help='ギアのブランド名')
parser.add_argument('--drink', type=str, help='ドリンクで付きやすくなっているギアパワーを指定する(無い場合は"なし")', default='なし')
parser.add_argument('--display', type=int, help='結果の表示数')
args = parser.parse_args()

seed = args.seed

ability_order = [
    "インク効率アップ(メイン)",
    "インク効率アップ(サブ)",
    "インク回復力アップ",
    "ヒト移動速度アップ",
    "イカダッシュ速度アップ",
    "スペシャル増加量アップ",
    "スペシャル減少量ダウン",
    "スペシャル性能アップ",
    "復活時間短縮",
    "スーパージャンプ時間短縮",
    "サブ性能アップ",
    "相手インク影響軽減",
    "サブ影響軽減",
    "アクション強化"
]

brand_order = {
    "バトロイカ": [11, 0],
    "アイロニック": [9, 8],
    "クラーゲス": [4, 12],
    "ロッケンベルグ": [3, 4],
    "エゾッコ": [6, 5],
    "フォーリマ": [7, 1],
    "ホッコリー": [1, 2],
    "ホタックス": [8, 6],
    "ジモン": [0, 3],
    "シグレニ": [12, 13],
    "アロメ": [2, 9],
    "ヤコ": [5, 7],
    "アナアキ": [1, 6],
    "エンペリー": [10, 11],
    "タタキケンサキ": [0, 10],
    "バラズシ": [13, 10],
    "シチリン": [13, 5],
    "クマサン商会": None,
    "アタリメイド": None,
    "amiibo": None
}

brand_weight = [2,2,2,2,2,2,2,2,2,2,2,2,2,2]
brand = brand_order[args.brand]
drink = None if args.drink == 'なし' else ability_order.index(args.drink)

def xor32(x32):
    x32 = x32 ^ (x32 << 13 & 0xFFFFFFFF)
    x32 = x32 ^ (x32 >> 17 & 0xFFFFFFFF)
    x32 = x32 ^ (x32 << 5 & 0xFFFFFFFF)
    return x32 & 0xFFFFFFFF

def max_brand_num():
    global brand_weight
    if brand is not None:
        brand_weight[brand[0]] = 10
        brand_weight[brand[1]] = 1
    return sum(brand_weight)

def max_brand_num_drink():
    global brand_weight
    if drink is not None:
        brand_weight[drink] = 0
    return sum(brand_weight)

def weighted_ability(ability_roll):
    global brand_weight
    ability = -1
    while(ability_roll >= 0):
        ability += 1
        ability_roll -= brand_weight[ability]
    return ability

def get_branded_ability():
    global seed
    ability_roll = seed % max_brand_num()
    return weighted_ability(ability_roll)

def get_branded_ability_drink():
    global seed
    ability_roll = seed % max_brand_num_drink()
    return weighted_ability(ability_roll)

def advance_seed():
    global seed
    seed = xor32(seed)

def get_ability():
    global seed
    advance_seed()
    ret = get_branded_ability()
    if drink is not None:
        if(seed % 0x64 <= 0x1D):
            return 0xFFFFFFFF
        advance_seed()
        ret = get_branded_ability_drink()
    return ret

def print_result():
    x = get_ability()
    if x == 0xFFFFFFFF:
        print(ability_order[drink])
    else:
        print(ability_order[x])

for i in range(args.display):
    print_result()