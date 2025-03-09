# MultiffMaker

このツールは、複数の画像からマルチページTIFFを作成するためのツールです。  

現状、マルチページTIFFを読み込んで編集するような機能は持たせていません。  

## 開発環境

|ソフト|バージョン|
| - |-|
|Win|11|
|Python |3.10|
|||
|numpy|2.2.3|
|pillow|11.1.0|
|pyperclip|1.9.0|
|tifffile|2025.2.18|
|TkEasyGUI|1.0.21|

## 使い方

アプリ：[MultiffMaker](./bin/multiffmaker.zip)

使い方：`./doc`参照  


## Exe化方法

Nuitka2.6.7を使用してExe化しています。

Nuitkaでコンパイルする場合、以下のようなコマンドで一応コンパイルできました。  
```cmd
nuitka --standalone --onefile --enable-plugins=numpy --enable-plugins=tk-inter module1.py
```

※Portable Python使用時  
```
python <Portable Pythonインストール先>\App\Python\Lib\site-packages\nuitka\__main__.py --standalone --onefile --enable-plugins=numpy --enable-plugins=tk-inter module1.py
```



## 作成の経緯

xx設計に努めていた頃（201x年頃）...  
  
会社のPCをWindows 2000 から Windows XPにPCを変更したところ  
`Kodak Imaging`が無くなってしまい、  

社内でマルチページTIFFを作成できる環境が無くなってしまいました。  

当時はまだ、官公庁向けに「マルチページTIFF」での納品があったことから、  
同等のソフトが必要になり、いくつかのシェアウェア（1000円~3000円程度）を提案しましたが、  
  
しかし、当時のK部長から、  
```
「もともとフリーだったのだから、何としてでもフリーソフトで探せ。  
見つけられないのは探しようが足りないからだ。見つかるまで帰れると思うな。」
```
  
と残業してでも探すことを強要された事があり、  
仕方がなかったので、  
```
明日の朝までにフリーソフトで探せばいいんですよね。
半日以上探して見つからないのだから、家で作った方が速いです。
今日は帰ります。
```
と言って、  

**「家に帰って一晩で開発し、自分のHPでフリーソフトとして公開した」**  
  
というのがもともとの作成の経緯ですｗ  
  
当時、VS2008を使って、VB.net + .net Framework3.5で作成していたのですが、  
そろそろ.net FrameworkのEOLが来るかなと思い  
当時の記憶を元に再現してみたソフトがこれになります。  

とはいえ、今更需要があるのか？は、疑問ですがｗ