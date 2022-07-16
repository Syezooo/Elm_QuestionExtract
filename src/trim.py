from PIL import Image
import glob
import os
import shutil
import argparse
from tqdm import tqdm
import time

# オプション指定
def Options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outtype', type=str, default='pdf', help='保存する拡張子を指定')
    parser.add_argument('--img_path', type=str, default='/workspace/results/img/' , help='pdf→imageの変換で保存された画像が格納されたパスを指定')
    parser.add_argument('--privacy', type=str, default='OFF', help='個人情報をトリミングするか否か。ONにするとq5として保存される。')
    return parser.parse_args()


# メイン関数
def main():
    # options読み込み
    args = Options()
    outtype = '.' + args.outtype
    img_path = args.img_path + '*'

    # トリミングしたい質問数分の保存先パスを指定
    save_path_q1 = '/workspace/results/outputs/q1/'
    save_path_q2 = '/workspace/results/outputs/q2/'
    save_path_q3 = '/workspace/results/outputs/q3/'
    save_path_q4 = '/workspace/results/outputs/q4/'
    save_path_q5 = '/workspace/results/outputs/q5/'

    # 保存先パスとトリミング位置（アンケートごとに変わる）を指定
    ### q1（1曲目）###
    trim_question(img_path, save_path_q1, 0, 370, 1074, 620, outtype)

    ### q2（2曲目）###
    trim_question(img_path, save_path_q2, 0, 600, 1074, 840, outtype)

    ### q3（3曲目）###
    trim_question(img_path, save_path_q3, 0, 820, 1074, 1050, outtype)

    ### q4（その他お気づきの点など）###
    trim_question(img_path, save_path_q4, 0, 1030, 1074, 1200, outtype)

    ### q5（個人情報）###
    if args.privacy == 'ON':
        trim_question(img_path, save_path_q5, 0, 1180, 1074, 1520, outtype)

# 任意の入力（入力画像パス、保存先パス、トリミング位置、出力の拡張子）に沿ってトリミング結果を返す関数
def trim_question(img_path, save_path, x1, y1, x2, y2, outtype):
    folder_refresh(save_path)
    imgs = glob.glob(img_path)
    imgs.sort()
    imgs = tqdm(imgs)
    for img in imgs:
        # 処理結果を標準出力
        imgs.set_description("Processing %s to %s" % (img, save_path))
        # 画像の名前を取得
        img_name = os.path.splitext(os.path.basename(img))[0] 
        im = Image.open(img)
        im_crop = im.crop((x1, y1, x2, y2))
        if outtype == '.pdf':
            im_crop = im_crop.convert('RGB')
        
        im_crop.save(save_path + img_name + outtype)

# 保存先を空にしつつ領域確保する関数
def folder_refresh(save_path):
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.mkdir(save_path)



if __name__ == "__main__":
    main()