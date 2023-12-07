# アプローチを変更！！extlinux機構で拡張エリアからLinuxカーネルを起動する。

## まず、別のSDCARD（32GB)へWindowPC（SDCARDスロット有りを私は利用）でextlinuxを利用したイメージから起動ディスクを`Rufus`で作成
- ブートイメージの取得参照ページ
　https://www.rocketboards.org/foswiki/Documentation/CycloneVSoCGSRD#HPSBootFlow  
  から、`https://releases.rocketboards.org/2022.11/gsrd/c5_gsrd/sdimage.tar.gz`をPCでDLしgunzip->tar解凍  
  - そして、解凍して得たイメージファイル名を`gsrd-console-image-cyclone5.wic`から`sdimage.img`へ変更

  <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20212238.png"/>

  - Rufusで起動ディスク作成

    <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20213919.png" title="Rufusにより起動ディスク作成その１" width="50%"/><br>

    <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20213950.png" title="Rufusにより起動ディスク作成その２" width="30%"/>

    <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20214023.png" title="Rufusにより起動ディスク作成その３" width="25%"/>
    <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20214056.png" title="Rufusにより起動ディスク作成その３" width="25%"/>

    <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20215933.png" title="Rufusにより起動ディスク作成その４" width="30%"/>

## 次に、WindowsPCエクスプローラーにて参照出来るBootディスクパーティション(FAT)からWindowPCの任意ディレクトリへコピー
- 任意のディレクトリへコピー

  <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20223321.png" title="起動ディスクパーティションを任意のディレクトリへコピーその１" width="70%"/>

  <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20224228.png" title="起動ディスクパーティションを任意のディレクトリへコピーその２" width="45%"/>

  <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20224407.png" title="起動ディスクパーティションを任意のディレクトリへコピーその３" width="45%"/>
  <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20224446.png" title="起動ディスクパーティションを任意のディレクトリへコピーその３" width="45%"/>

  - そして中身を見る

    <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20224519.png" title="起動ディスクパーティションを任意のディレクトリへコピーその４" width="45%"/>
    <img src="./etc/images/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202023-12-07%20225446.png" title="起動ディスクパーティションを任意のディレクトリへコピーその１" width="80%"/>
---
- **この超解釈**
    > Bootパーティション（パーティション番号1であり、FATフォーマット）に`extlinux`ディレクトリが有れば、  
    >  その中の`extlinux.conf`を参照し、  
    >  `extlinux`ディレクトリ直下のカーネルイメージ`zImage`を`/dev/mmcblok0p2`デバイスにLOADし、  
    >  U-bootから`root=/dev/mmcblk0p2 rootwait rw earlyprintk console=ttyS0,115200n8`をカーネルへ`bootargs`として引き渡し起動する。 

## SDCARD(128GB)へLXDEイメージから起動ディスク作成し直し、extlinux機構導入
- オペレーションイメージ
![オペレーションイメージ](./etc/images/de0-nano-socs-extlinus-freedam.svg)
