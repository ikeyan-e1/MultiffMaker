#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ikeyan
#
# Created:     24/02/2025
# Copyright:   (c) ikeyan 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import TkEasyGUI as eg
import os
from PIL import Image

# 画像圧縮方式のリスト
COMPRESSION_DICT ={
    "CCITT Group 3":"group3",
    "CCITT Group 4":"group4",
    "JPEG":"jpeg",
    "LZMA":"lzma",
    "PackBits":"packbits",
    "ADOBE_DEFLATE":"tiff_adobe_deflate",
    "LZW":"tiff_lzw",
    "RAW 16":"tiff_raw_16",
    "SGILOG":"tiff_sgilog",
    "SGILOG 24":"tiff_sgilog24",
    "ThunderScan":"tiff_thunderscan",
    "WebP":"webp",
    "Zstandard":"zstd"
    }

def find_common_prefix(paths):
    '''
    複数のパスの配列から、共通した階層のみを抽出する。
    '''

    #split_paths = [path.replace('\\', '/').split('/') for path in paths]
    split_paths = [path.split(os.sep) for path in paths]
    common_prefix = []
    for parts in zip(*split_paths):
        if all(part == parts[0] for part in parts):
            common_prefix.append(parts[0])
        else:
            break
    return os.sep.join(common_prefix)


def create_multipage_tiff(image_paths, output_path, quality=75, compression='jpeg'):
    """
    画像パスのリストからマルチページTiffを作成する関数

    Args:
        image_paths (list): 各ページに使用する画像のパスのリスト
        output_path (str): 作成するマルチページTiffファイルの保存先
    """

    # 最初の画像をオープン
    if compression in ['group3','group4','tiff_ccitt']:
        # 白黒系のアルゴリズムが選択された場合は、白黒画像として読み込む
        images = [Image.open(path).convert("1") for path in image_paths]
    else:
        images = [Image.open(path) for path in image_paths]


    # 最初の画像を基にしてマルチページTiffを保存
    if compression == "jpeg":
        images[0].save(output_path, save_all=True, append_images=images[1:],
                        compression=compression, quality=quality, format='TIFF')

    else:
        images[0].save(output_path, save_all=True, append_images=images[1:],
        compression=compression, format='TIFF')

    print(f"マルチページTiffを {output_path} に保存しました。")

def move_element(lst, value, direction):
    """
    リスト内の指定された値の位置を一つ前または一つ後ろに移動します。

    Parameters:
        lst (list): 操作対象のリスト
        value (any): 移動させる値
        direction (str): 'up'または'down'で移動方向を指定します

    Returns:
        list: 更新されたリスト
    """
    # 指定値の現在のインデックスを取得
    index = lst.index(value)

    # 移動処理
    if direction == "up" and index > 0:
        # 前に移動
        lst[index], lst[index - 1] = lst[index - 1], lst[index]
    elif direction == "down" and index < len(lst) - 1:
        # 後ろに移動
        lst[index], lst[index + 1] = lst[index + 1], lst[index]
    else:
        print("指定した方向に移動できません")

    return lst


def main():
    # ListBoxの値
    image_file_list = []


    # 画面レイアウトの定義
    layout = [

        [
            eg.Listbox(values=image_file_list, key="-tiffFiles-", size=(50,30), enable_events=True), # 50文字,30行
            eg.Frame("",[
                [eg.Button("ファイル追加",size=(10,1), key="-addFile-")],
                #[eg.Button("フォルダ追加", key="-addFolder-")],
                [eg.Button(" 削除 ", size=(10,1), key="-removeFile-")],
                [eg.Label("")],
                [eg.Button("   ▲   ",size=(10,1), key="-UpIdx-")],
                [eg.Button("   ▼   ",size=(10,1), key="-DownIdx-")]
            ],),
            eg.Image(filename="", key="-image-", size=(300, 300), enable_events=True),
        ],
        [
            eg.Label("圧縮方式："),
            eg.Combo(list(COMPRESSION_DICT.keys()), default_value=list(COMPRESSION_DICT.keys())[0], key="-compression-", enable_events=True),
            eg.Label("", size=(10,1)),
            eg.Button("保存", size=(10,1), key="-save-"),
            eg.Button("終了", size=(10,1), key="Exit")
        ]
    ]

    # ウィンドウを表示する
    try:
        with eg.Window("MultiPageTiff Maker", layout) as window:
            # イベントループを処理する
            for event, values in window.event_iter():
                # 左上のバツボタンでウィンドウを閉じる
                if event in ["Exit", eg.WINDOW_CLOSED]:
                    print("プログラムの終了ボタンが押されました。")
                    break

                if event =="-save-":
                    # 保存ボタン押下時の処理
                    if len(image_file_list) == 0:
                        continue

                    # file types
                    file_types = (("Image files", "*.tiff;*.tif"),)
                    output_path = eg.popup_get_file("", file_types=file_types, save_as=True)
                    if len(output_path) == 0:
                        continue
                    create_multipage_tiff(image_file_list, output_path, quality=75, compression=COMPRESSION_DICT[values["-compression-"]])
                    eg.print(f"マルチページTiffを {output_path} に保存しました。")



                if event == "-addFile-":
                    # ファイル追加ボタン押下時の動作
                    # file types
                    file_types = (
                        ("Image files", "*.tiff;*.tif;*.jpg;*.jpeg;*.jpe;*.heic;*.png;*.gif"),
                        ("All files", "*.*"),
                    )
                    # popup
                    files = eg.popup_get_file(
                        "Please select images.",
                        file_types=file_types,
                        multiple_files=True,
                    )
                    #print(files)
                    image_file_set = set(image_file_list) # 検索の高速化テクニック（リストより集合の方が検索が速いため）
                    image_file_list = image_file_list + [a for a in files if a not in image_file_set]
                    window.get_element_by_key('-tiffFiles-').update(values=image_file_list)

                if event == "-removeFile-":
                    files = values["-tiffFiles-"]
                    if len(files) > 0:
                        _ = image_file_list.pop(image_file_list.index(files[0]))
                        window.get_element_by_key('-tiffFiles-').update(values=image_file_list)

                if event == "-UpIdx-":
                    files = values["-tiffFiles-"]
                    if len(files) > 0:
                        image_file_list = move_element(image_file_list, files[0], direction='up')
                        window.get_element_by_key('-tiffFiles-').update(values=image_file_list)

                if event == "-DownIdx-":
                    files = values["-tiffFiles-"]
                    if len(files) > 0:
                        image_file_list = move_element(image_file_list, files[0], direction='down')
                        window.get_element_by_key('-tiffFiles-').update(values=image_file_list)

                if event == "-tiffFiles-":
                    # ファイルリストを選択したときの動作

                    # 画像プレビュー画面に選択された画像を表示する。
                    files = values["-tiffFiles-"]
                    if len(files) > 0:
                        filename = values["-tiffFiles-"][0]
                        window["-image-"].update(filename=filename)

    except:
        print(sys.exc_info())
        sys.exit()


if __name__ == '__main__':
    main()
