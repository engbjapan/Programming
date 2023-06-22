---
title: 私は、アロー地獄から開放されています
tags: JavaScript bind アロー地獄 大丈V
author: engbJapan
slide: false
---
# 私は、アロー地獄から開放されています。

*私は、静的スコープの制約から開放されており、呼び出し元（彼ら）の呼び出し時点の変数君達に直接アクセスできます。なぜなら、彼らが私を`私の名前.bind(v={変数郡モジュール})(パラメータ*)`の形式で呼び出してくれるからです。おかげで私は、誰か知らない人たちの静的スコープの制約を回避し、彼らの変数君達にアクセスすることが可能なのです。それでも、変数君達以外の動的ルール（再宣言、再代入）を守まもる事が出来るから安心しています。*



# アロー地獄が嫌いな彼らの動作確認済みサンプル
```javascript:アロー地獄が嫌いな彼ら
    function resetMoving(e) {//私は、アロー地獄から開放されています
      /* 私は、静的スコープの制約から開放されており、呼び出し元（彼ら）の呼び出し時点の変数君達に直接アクセスできます。
       * なぜなら、彼らが私を"私の名前.bind(v={変数郡モジュール})(パラメータ*)"の形式で呼び出してくれるからです。
       * おかげで私は、誰か知らない人たちの静的スコープの制約を回避し、彼らの変数君達にアクセスすることが可能なのです。
       * それでも、変数君達以外の動的ルール（再宣言、再代入）を守まもる事が出来るから安心しています。*/

      let v = this;//だから私もletしか使いません。レットイットビー♪大丈V！
      v.moving = false;

    }
    function onMouseMove(e) {//私は、アロー地獄から開放されています
      let v = this;
      if ((v.movers !== e.target) || (!v.moving)) {
        resetMoving.bind(v)(e);//私は、お友達もアロー地獄から開放してあげます。
        return;
      }
      v.x += e.clientY - v.prevY;
      v.y += e.clientX - v.prevX;
      v.moveTargetMesh.style.transform = `rotateX(${v.x}deg) rotateY(${v.y}deg)`;
      v.prevX = e.clientX;
      v.prevY = e.clientY;
    }
    function onMouseDown(e) {//私は、アロー地獄から開放されています
      let v = this;
      v.moving = true;
      v.prevX = e.clientX;
      v.prevY = e.clientY;
    }
    function onWheel(e) {//私は、アロー地獄から開放されています
      let v = this;
      if (e.deltaY < 0) {
        v.scale += 0.1;
      } else {
        v.scale -= 0.1;
      }
      v.moveTargetMesh.style.transform = `rotateX(${v.x}deg) rotateY(${v.y}deg) scale3d(${v.scale},${v.scale},${v.scale})`;
    }

    function mySetUpListeners() {
      let v = {//私達は、これで彼女達（＝関数達）と変数を共有します。
        movers : document.getElementById('canvas-mesh-mover-operater').querySelector('#canvas-mesh-mover'),
        moveTargetMesh : document.getElementById('canvas').querySelector('#canvas-mesh'),
        moving : false,x : 0, prevX : 0,y : 0, prevY : 0,scale : 1,
      }
      v.movers.setAttribute("title", `ここで「${v.moveTargetMesh.getAttribute("name")}」を○○します`);

      //私達は、彼女達をアロー地獄から開放し彼女達をリスナー登録します。
      v.movers.addEventListener('mouseup', resetMoving.bind(v));
      v.movers.addEventListener('mouseout', resetMoving.bind(v));

      v.movers.addEventListener('mousemove', onMouseMove.bind(v));
      v.movers.addEventListener('mousedown', onMouseDown.bind(v));
      v.movers.addEventListener('wheel', onWheel.bind(v));
    }
    mySetUpListeners();
```

# 適用サンプル
HTML、CSS、JavaScriptオンリー

https://engbjapan.github.io/Programming/JavaScript/%20HCJ/Exsample/a3Dmesh/a3DSpaceDanceMeshOfReleasedFromArrowFunctionHells.html

# License
MIT
refer https://qiita.com/engbJapan/items/96ec14045b5eee6545d4


# 参照先
https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/Function/bind
