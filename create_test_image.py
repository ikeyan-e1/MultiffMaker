from PIL import Image, ImageDraw

# 画像サイズと出力先フォルダ
width, height = 200, 200
output_folder = './test_images/'

# テスト用のTiff画像を5枚作成
for i in range(1, 6):
    # 白い背景の画像を作成
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    # 番号を書き込む
    draw.text((10, 10), f'Test Image {i}', fill='black')

    # ファイル名と保存
    file_name = f'test_image_{i}.tiff'
    img.save(output_folder + file_name)
    print(f'{file_name} を作成しました。')
