> ...ソースから云々やあれこれも要らないと思うけど。。。

まず、シングルユーザモードとしてU-bootからカーネル起動

一分３０秒（実質は２分程）して、エマージェンシーモード付のシングルユーザモードでシリアル接続の状態で入り、

ここでは何もせずに、/etc/fstabに設定した/dev/mmcblk0p4を？？？に
```
mount -a
```
でマウントして、
そのまま`exit`で通常モードで起動しました。


そして、TeraTermからssh接続（非ROOTユーザー）ログインOK

さらに、いつもの通り`ssh localhost -l`でrootにログインOK

で、以下の通り、いわゆる普通のUbuntu22.04LTSなら有るであろうファイル

---
cmdline.txtが無い
```
root@localhost:~# ls -la /boot/cmdline.txt
ls: cannot access '/boot/cmdline.txt': No such file or directory
root@localhost:~#
```
---
あー。カーネルモジュールがないのね・・
```
root@localhost:~# ls -la /lib/modules/$(uname -r)
ls: cannot access '/lib/modules/3.13.0-00298-g3c7cbb9-dirty': No such file or directory
root@localhost:~# ls -la /lib/modules/
ls: cannot access '/lib/modules/': No such file or directory
root@localhost:~#
```
---
これらが無いのですね。


'/lib/modules/3.13.0-00298-g3c7cbb9-dirty'でググるとありましたよ
私と同じように「これがないのだけど」と、、、ビンゴです。

https://forum-rocketboards-org.translate.goog/t/arrow-sockit-problems-with-canbus/601?_x_tr_sl=auto&_x_tr_tl=ja&_x_tr_hl=ja&_x_tr_hist=true

であるからして、Ubuntu22.04LTSがダイレクトCPUで稼働するマシンとして
ライトウエイトなのですね。

よって、ソースからカーネルビルドをする必要があるが、
敢えてクロス環境を用意してやらずに、実機でこれを行うというのが
色んな意味で、異種（であるが故、）格闘しなければ成らぬのでごわす。

# アプローチを変更！！extlinux機構で拡張エリアからLinuxカーネルを起動する。

## まず、別のSDCARD（32GB)へWindowPC（SDCARDスロット有りを私は利用）でextlinuxを利用したイメージから起動ディスクを`Rufus`で作成
- ブートイメージの取得参照ページ
　https://www.rocketboards.org/foswiki/Documentation/CycloneVSoCGSRD#HPSBootFlow  
  から、`https://releases.rocketboards.org/2022.11/gsrd/c5_gsrd/sdimage.tar.gz`をPCでDLしgunzip->tar解凍  
  - そして、解凍して得たイメージファイル名を`gsrd-console-image-cyclone5.wic`から`sdimage.img`へ変更

  <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20212238.png"/>

  - Rufusで起動ディスク作成

    <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20213919.png" title="Rufusにより起動ディスク作成その１" width="50%"/>

    <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20213950.png" title="Rufusにより起動ディスク作成その２" width="30%"/>

    <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20214023.png" title="Rufusにより起動ディスク作成その３" width="25%"/>
    <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20214056.png" title="Rufusにより起動ディスク作成その３" width="25%"/>

    <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20215933.png" title="Rufusにより起動ディスク作成その４" width="30%"/>

## 次に、WindowsPCエクスプローラーにて参照出来るBootディスクパーティション(FAT)からWindowPCの任意ディレクトリへコピー
- 任意のディレクトリへコピー

  <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20223321.png" title="起動ディスクパーティションを任意のディレクトリへコピーその１" width="70%"/>

  <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20224228.png" title="起動ディスクパーティションを任意のディレクトリへコピーその２" width="45%"/>

  <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20224407.png" title="起動ディスクパーティションを任意のディレクトリへコピーその３" width="45%"/>
  <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20224446.png" title="起動ディスクパーティションを任意のディレクトリへコピーその３" width="45%"/>

  - そして中身を見る

    <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20224519.png" title="起動ディスクパーティションを任意のディレクトリへコピーその４" width="45%"/>
    <img src="https:///engbjapan.github.io/Programming/de0-nano-SOC-intelCycloneVSOC/docs/etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20225446.png" title="起動ディスクパーティションを任意のディレクトリへコピーその１" width="80%"/>
---
- **この超解釈**
    > Bootパーティション（パーティション番号1であり、FATフォーマット）に`extlinux`ディレクトリが有れば、  
    >  その中の`extlinux.conf`を参照し、  
    >  `extlinux`ディレクトリ直下のカーネルイメージ`zImage`を`/dev/mmcblok0p2`デバイスにLOADし、  
    >  U-bootから`root=/dev/mmcblk0p2 rootwait rw earlyprintk console=ttyS0,115200n8`をカーネルへ`bootargs`として引き渡し起動する。 


