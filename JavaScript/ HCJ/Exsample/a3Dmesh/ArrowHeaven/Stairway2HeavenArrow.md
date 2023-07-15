---
title: 大丈Vシリーズまとめ「アロー天国への階段(Stairway to Arrow Heaven)」（習作）
tags: 大丈V JavaScript アロー天国への階段 X式列 FibonacciSequenceHeaven
author: engbJapan
slide: false
---

# はじめに

この記事は、私が`大丈V`シリーズとしてJavaScriptの学習過程を記録した経緯を一旦復習し更にヒントを得た習作です。  

このシリーズは「`アロー地獄`」と敢えて「地獄」というキーワードを用いた事から端を発したもので、この`アロー達`が私にとって**難解**であり様々なスニペットを**見れば見るほど混乱**していました。 

また、`X式列`の発見は、私がアロー達をPlayGroundでplayするために[`VScode`](https://code.visualstudio.com/)でコード中、いつもの通り**タイポ**（`{`とタイプすべきを`[`とタイプ）をしてしまいシンタックスエラーとなり該当箇所の訂正案に応じた結果、カンマ区切り「**`カンマ演算子`**」でコードを綴り。後に誤りとこれ発見をしたものです。 


そして、式列でのコードを学習しているうちに、**アロー階段**の先は地獄では無く
[天国への階段(*Stairway to Heaven*)](https://ja.wikipedia.org/wiki/%E5%A4%A9%E5%9B%BD%E3%81%B8%E3%81%AE%E9%9A%8E%E6%AE%B5_%28%E3%83%AC%E3%83%83%E3%83%89%E3%83%BB%E3%83%84%E3%82%A7%E3%83%83%E3%83%9A%E3%83%AA%E3%83%B3%E3%81%AE%E6%9B%B2%29)では？と言う思いに至った事を私なりにまとめたものです。

この記事では、主に以下の4点を私が学習し、   
（「コード・コードテストを行い動作可能」  
若しくは「コード無し」=> `TODO`マークが目印
若しくは「コードは有るが目的動作不能」=> `TODO`マークが目印）な物を掲載しています。  

1. [式へステートメントを組み込むチェーンスタイル](#式へステートメントを組み込むチェーンスタイル)
1. [式列配置と記法の参考事項](#式列配置と記法の参考事項)
1. [式列でプロパティ名ブロックスコープを使い自身を再帰的評価するロジック例](#式列でプロパティ名ブロックスコープを使い自身を再帰的に評価するコード例)
1. [テンプレートリテラルX式列呼び出し例](#テンプレートリテラルX式列呼び出し例)

# 本題

## 式へステートメントを組み込むチェーンスタイル

まず、「チェーンスタイル」とは、複数のジェネレーター関数を連結し、一連の値を生成することができるJavaScriptの機能を指しています。

### 無名関数bindチェーンを使いfunctionとして呼び出すスタイル

  ```javascript:
  (function(引数定義){ステートメント;...})
    .bind(依存Object値)(引数),
    //又は、
    //.bind(依存Object値, 引数)(),
    //.bind(依存Object値, 引数).call(),
    //.bind(依存Object値).call(null, 引数),
    //.bind(依存Object値).apply(null ,[引数列]*),
    //.bind(依存Object値, [引数列]).apply(),//?
    //etc?
  ```

  `{ステートメント;...}`内での「依存Object」のプロパティ｜メソッド｜関数 へのアクセスは、

  ```javascript:
    this.propOrMethodOrFunc ...;//のように書くことができます。
    //etc?
  ```

### 無名class new".~"チェーンを使いメソッドとして呼び出すスタイル

  ```javascript:
  (new 
    (class{
        constructor(依存Object, 
                    コンストラクタ引数定義){
            インスタンス初期化ステートメント;...
            this.依存Object = 依存Object;
        }
        メソッド(引数定義){
            {ステートメント;...};...
        }...
    })(依存Object値,コンストラクタ引数))
    .メソッド(引数),
     //etc...
  ```

  `{ステートメント;...}`内での「依存Object」のプロパティ｜メソッド｜関数 へのアクセスは、

  ```javascript:
    this.依存Object.propOrMethodOrFunc ...;//のように書くことができます。
    //etc...
  ```

### アロー関数チェーンを使いアローfunctionとして呼び出すスタイル

  ```javascript:
  ((依存Object, 引数定義) => {ステートメント;...})
    (依存Object値, 引数),
    //又は、
    //.call(null, 依存Object値, 引数),
    //.apply(null, 依存Object値, [引数列]),
  ```

  `{ステートメント;...}`内での「依存Object」のプロパティ｜メソッド｜関数 へのアクセスは、

  ```javascript:
    依存Object.propOrMethodOrFunc ...;//のように書くことができます。
  ```

  - *更に、`.bind`生成した場合は無名関数と同じように*

    ```javascript:
    ((依存Object, 引数定義) => {ステートメント;...})
    .bind(依存Object値)(引数),
    //.bind(依存Object値, 引数)(),
    //.bind(依存Object値, 引数).call(),
    //.bind(依存Object値).call(null, 引数),
    //.bind(依存Object値).apply(null ,[引数列]),
    //.bind(依存Object値, [引数列]).apply(),//?
    //etc?
    ```

    `{ステートメント;...}`内で「依存Object」のプロパティ｜メソッド｜関数 へのアクセスは、

    ```javascript:
    this.propOrMethodOrFunc ...;
    //etc?
    ```

    *とコードすると、this参照を与え同じように動作するかもしれませんが、*  
   *「**アロー天国への階段(*Stairway to ArrowHeaven*)**」へ行くことができないと思われます。*

### チェーンスタイル別のTODO有りコードスニペット及びその説明

この節には、上記で述べた三つのスタイル別のコードスニペットを記載しています。なお、冒頭で述べた通り未完成・目的動作をしないものを私の都合により掲載しています。

ベースとなるロジックは三つ目の「[アロー関数チェーンに於けるcallコード例](#アロー関数チェーンに於けるcallコード例)です。ので、そこから見てください。

そして比較すれば私がこの記事で述べている「**アロー天国への階段**」の意味が分かると思います。

#### 無名関数bindチェーンに於けるcallのコード例
:**TODO**
これは「[アロー関数チェーンに於けるcallコード例](#アロー関数チェーンに於けるcallコード例)」と同様の動作をしません。 

```javascript:無名関数bindチェーンに於けるcall式列
let 大丈VModXFunctionBindCalls = (pmyObject, pmsg) => [//X式列
        (function(//無名関数
          pinmsg, pinParamVam = {addsparam:false, addsArray: []}){
            //@ここからステートメント
            let a = {//このModle（Oblect）は、let(/const/var)文で生成される
                aaa: false,
                bbb: true,
                inmyX: (msgs) => [//X式列//msgs 呼出しxx引数スコープ
                    console.log(msgs),//console Globalスコープ
                      //1> inmyXCall:false
                      //2> inmyFunc:inmyFuncCall:こんにちわ:true
                ],
                inmyFunc: (msgs2) => {//msgs2 呼出しxx引数スコープ
                    a.inmyX(`inmyFunc:${msgs2}`);//a let Modleスコープ
                },
            };
            a.inmyX(`inmyXCall:${a.aaa}`);//a let Modleスコープ
            a.inmyFunc(`inmyFuncCall:${pinmsg}:${a.bbb}`);//pinmsg 引数スコープ
            //this bind Objectに依存するlogメソッド（又は関数）呼び出し
            this.log(`FromStatments:${pinmsg}`);
            console.log(
              `${pinParamVam.addsparam},${pinParamVam.addsArray}`);//pinParamVam 引数スコープ
              //4> true, 1,2,3
            let rVam = {//戻り値Modle（Oblect）の生成
                addsparam: pinParamVam.addsparam,
                addsArray: pinParamVam.addsArray,
            };
            return rVam;// returns [rVam,]
        }).bind(pmyObject).call(null, pmsg, 
                                 {addsparam:true, 
                                  addsArray: ["1", "2", "3"] }),
        //無名関数をbindで生成しfunctionをcallする例
        //（呼び出し先へModule引数`{...}`の引き渡し例を含む）
        //  bindの第一引数は呼び出し先でthis参照(this bindスコープ)となり、
        //   callの第二引数以降は、その引数に割当られる。
]
function entty() {
    let myObject = {
        log: (inmymsgs) => {//アロー関数
            console.log(inmymsgs);
              //3> FromStatments:こんにちわ
        }
    };
    let msg = "こんにちわ";
    let avam = 大丈VModXFunctionBindCalls(myObject, msg)[0];
    /*ここでは、
    大丈VModXFunctionBindCalls式列`Expressions`を呼び出す「評価`Evalute`する」と
    最後に評価した式`Expression`の値が配列に包まれるので
    rVam自体を取得するために[0]を付けてavamへ代入しています。*/
    console.log(`avam.addsparam=${avam.addsparam},avam.addsArray=${avam.addsArray}`);
      //5> avam.addsparam=true,avam.addsArray=1,2,3
}
setTimeout(entty(),3 *1000)
/* console.log:出力想定
inmyXCall:false
inmyFunc:inmyFuncCall:こんにちわ:true
FromStatments:こんにちわ
true, 1,2,3
avam.addsparam=true,avam.addsArray=1,2,3
*/
```

#### 無名class newチェーンに於けるメソッド呼び出しコード例
:**TODO!!**
これは「[アロー関数チェーンに於けるcallコード例](#アロー関数チェーンに於けるcallコード例)」と同様の振る舞いをするコードを書けていません。

#### アロー関数チェーンに於けるcallコード例

```javascript:アロー関数チェーンに於けるcall式列
let 大丈VModXArrowCalls = (pmyObject, pmsg) => [//X式列
        ((pinmyObject,pinmsg, 
          pinParamVam = {
                         addsparam:false, 
                         addsArray: []}) => {//アロー関数
            //@ここからステートメント
            let a = {
                aaa: false,
                bbb: true,
                inmyX: (msgs) => [//X式列
                    console.log(msgs),
                ],
                inmyFunc: (msgs2) => {
                    a.inmyX(`inmyFunc:${msgs2}`);
                },
            };
            a.inmyX(`inmyXCall:${a.aaa}`);
            a.inmyFunc(`inmyFuncCall:
            ${pinmsg}:${a.bbb}`);
            //pinmyObject Object依存のlogメソッド（又は関数）呼び出し
            pinmyObject.log(`FromStatments:${pinmsg}`);

            console.log(`${pinParamVam.addsparam},
              ${pinParamVam.addsArray}`);

            let rVam = pinParamVam;//rVam let 生成
            pinParamVam.addsparam = "こんばんは"; 
            pinParamVam.addsArray[3] = 4;
            return rVam;// returns [rVam,] Inp!
        }).call(null,pmyObject, pmsg, {addsparam:true, 
                                       addsArray: ["1", "2", "3"] }),
        //Or 
        //(pmyObject, pmsg, {addsparam:true, 
        //                   addsArray: ["1", "2", "3"] }),
        //アロー関数で生成されたfunctionをcallする例
        //（呼び出し先へModule引数`{...}`の引き渡し例を含む）
        //  callの第一引数は呼び出し先でthis参照(this bindスコープ)となり、
        //     以降の引数は、その引数に割当られる。
        //アローで生成されたままのfunctionはthis参照がない為、第一引数はnull指定
]
function entty() {
    let myObject = {
        log: (inmymsgs) => {//アロー関数
            console.log(inmymsgs);
        }
    };
    let msg = "こんにちわ";
    let avam = 大丈VModXArrowCalls(myObject, msg)[0];//Inp!!
    console.log(`avam.addsparam=${avam.addsparam},
    avam.addsArray=${avam.addsArray}`);
}
setTimeout(entty,3 *1000)
/* console.log:出力
inmyXCall:false
inmyFunc:inmyFuncCall: こんにちわ:true
FromStatments:こんにちわ
true, 1,2,3
avam.addsparam=こんばんは, avam.addsArray=1,2,3,4
*/
```  

## 式列配置と記法の参考事項

- class構文直下「`class クラス名{...}`」へ配置する場合は「`funcX = (引数*)=>  [`」。
- Module構文内（ブロック内）  
  「`let/const/var varname = {...}`」Or「`definedvars = {...}`」Or  
  「`function fname(params*) {...}`」Or「`(params*)=> {...}`」Or  
  「`methodname(params*) {...}`」Or  
  「`if/for/while etc (conds*) {...}`」etc?へ配置する場合は「`funcX : (引数*)=>  [`」で良いはずです。  
- *要は、該当のブロック内に配列定義を記載する場合と同様の考え＋`(引数*)=>[`です。*

## 式列でプロパティ名ブロックスコープを使い自身を再帰的に評価するコード例

```javascript:式列でプロパティ名ブロックスコープを使い自身を再帰的に評価するコード例
setTimeout(() => [//setTimeout時に実行するX式列ブロック 定義
  console.log(//これで、最終的な値を出力する。

    ((pinmaxn, pinn) => {//無名関数実行型＝アロー実行体
        console.log(`無名関数実行型(${pinmaxn}, ${pinn}) => {`);

        大丈VreCuXs = (maxn,n,rVam) => [//大丈VreCuXsプロパティ//X式列
          console.log(`大丈VreCuXs = (${n},${maxn},${rVam.eIdx}) => [`),
          (n >= maxn) ? //戻り判断 
            rVam.eIdx = n  //then 戻り をrVam.eIdxへセット
            : [//else ネスティング//X式列
              n += 1,
              //大丈VreCuXsプロパティスコープを使い再帰呼出し
              大丈VreCuXs(maxn,n,rVam), /2 大丈VreCuXs => (maxn,n,rVam) [ 
            ]
        ];
        let aVam = {eIdx:"再帰中？"};//VamObject生成
        大丈VreCuXs(pinmaxn, pinn, aVam);////X式列の再帰エントリー呼出し
        return aVam.eIdx;//Console.logへの戻り値
    })
    (5, 0)//アロー実行体の呼出しと引数2 無名関数実行型(pinmaxn, pinn)
  )
],
3 * 1000)//setTimeout時、X式列ブロック呼出しとタイマー引数 
```

```text:console.log
無名関数実行型(5, 0) => {
大丈VreCuXs = (0,5,再帰中？) => [
大丈VreCuXs = (1,5,再帰中？) => [
大丈VreCuXs = (2,5,再帰中？) => [
大丈VreCuXs = (3,5,再帰中？) => [
大丈VreCuXs = (4,5,再帰中？) => [
大丈VreCuXs = (5,5,再帰中？) => [
5
```

このコードは、[*setTimeout*](https://developer.mozilla.org/ja/docs/Web/API/WindowOrWorkerGlobalScope/setTimeout)関数で式列「ブロック」を3秒後に実行します。この`ブロック`では、「無名関数実行型（アロー実行体）」持ち、これに引数5と0を渡して`アロー実行体`を呼び出しています。このアロー実行体は、*`大丈VreCuXs`* という「プロパティX式列」を持ちます。  
*`大丈VreCuXs`*プロパティX式列は「プロパティ名ブロックスコープ」を与えて、引数に最大値（*maxn*）、現在値（*n*）、結果格納用オブジェクト（*rVam*）を受け取り、現在値が最大値以上になるまで*`「プロパティ名ブロックスコープ」を用いて自身を再帰`*的に呼び出します。  
再帰的な呼び出しの際には、現在値に*1*を加えて渡します。最終的には、結果格納用オブジェクトの*eIdxプロパティ*に現在値をセットして戻ります。この戻り値が*console.log*で出力されます。

<details>
  <summary>「プロパティ名ブロックスコープ」での「再帰」と「一時変数によるグローバル名前空間の汚染制御」:Bingからの参考情報</summary>

プロパティ名ブロックスコープ「再帰」と一時変数によるグローバル名前空間の制御

- 「プロパティ名ブロックスコープ」は、オブジェクトのプロパティ名に[ブロック](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/block)（`{...}`）を使って[スコープ](https://developer.mozilla.org/ja/docs/Glossary/Scope)を作ることを示したキーワードです。[これにより、let、const、classなどのブロックスコープ宣言と組み合わせることで、IIFEのように、一時変数がグローバル名前空間を汚染するのを防ぐことができます。](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/block)
例えば、以下のコードでは、let変数xはブロック内で宣言されているため、そのスコープはブロック内に制限されます。

```javascript
let x = 1;
{
  let x = 2;
}
console.log(x); // 1
```

　[このx = 2は、それが定義されたブロックのスコープに制限されています。同じことがconstにも言えます。](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/const)このように、「プロパティ名ブロックスコープ」を使用することで、「変数のスコープを制限」し、データをカプセル化することができます。

ソース:
  1. [ブロック https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/block](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/block)- JavaScript | MDN - MDN Web Docs.
  1. [let https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/let](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/let) - JavaScript | MDN - MDN Web Docs.
  1. [const https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/const](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/const) - JavaScript | MDN - MDN Web Docs.

  - 「プロパティ名ブロックスコープ「再帰」」は、JavaScriptの[式列](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Operators/Comma_Operator)と[プロパティ名](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Operators/Object_initializer#computed_property_names)を使って自身を再帰（[再帰とは、が自分自身を呼び出すことを指します。再帰関数は、複雑なデータ構造の扱いが得すただし、for文の方が早いことが多いので、使いドコロが限られるかもしれません。そでも、プログラミングの幅が広がるという点では学んでおいて損はないかと思われます。再帰は関数型プログラミングにおける重要概念の１つであり、ひょっとしたら新しい世界が開けるかもしれません。](https://qiita.com/chuck0523/items/2c40a5da90a1d73ab956))呼び出しする


  - 「再帰」  
  再帰関数を使用する際には、終了条件を設定することが重要です。終了条件がない場合、関数は無限に呼び出され続けます。終了条件は、再帰関数内のif文などで設定することが重要です。例えば、以下のコードでは、`arrayLength`関数は配列の要素数を返します。
   ```javascript
    var nums = ['1', '2', '3', '4', '5'];
    function arrayLength(array) {
        if(_.isEmpty(array)) {
            return 0;
        } else {
            return 1 + arrayLength(_.rest(array));
        }
     }
     arrayLength(nums);
   ```
   `arrayLength`は再帰関数です。処理の中で自分自身を呼んでいます。 また、if文では、終了条件を規定しています。渡された配列が空だった場合に、再帰呼び出しを終了します。このように、再帰関数を使用することで、複雑な処理を簡潔に記述することができます。

</details>

## テンプレートリテラルX式列呼び出し例

[模倣＋Xの参照先　https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Template_literals](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Template_literals)

```javascript:テンプレートリテラルX式列呼び出し例
//TemplatePlayAtArrowHeaven
/* isImitationGold  from
https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Template_literals
*/
setTimeout(() => {
  let person = "マイケル";

  let 大丈VXTag = (strings, personExp, pTvam,Debug=false) => [
    (Debug) ? 
      console.log(`Debug>"${strings}"@"${personExp}"@"${pTvam}"@`):null,
    strP1 = strings[0], // "That "
    strP2 = strings[1], // " is a "
    strP3 = strings[2], // " . "|"、、さん"
    console.log(`${pTvam.Q}${pTvam.isa}`),
    ageExp = pTvam.isa,
    //ArrowFuncCall
    ((pageExp, ppTvam, ppersonExp, pstrP1,pstrP2,pstrP3) => {
      //ステートメント
      let ageStr;
      if (pageExp > 40) { 
        if (pageExp < 60)  {
          ageStr = "Oyaji。";
        }else if (pageExp < 80) { 
              ageStr = "Jinys!";
           } else {
              ageStr = "God!?fathers";
           }
      }else {
          ageStr = "youngster";
      }
      ppTvam.Ans = `${pstrP1}${ppersonExp}
                    ${pstrP2}${ageStr}${pstrP3}`;
      return ppTvam;
    })(ageExp, pTvam, personExp, strP1,strP2,strP3)
  ];
  let aTvam = {
    Q: "what?",
    isa: null,
    Ans: null,
    //embeds Any arrowX|arrowfuction|Function|Class Or Pops 
  };
  aTvam.isa = 28;
  大丈VXTag`That ${person} is a  ${aTvam}.`;
  console.log(aTvam.Ans); // That マイケル is a youngster.

  aTvam.Ans = null;//省略可
  //NormalCallStyleAndDebug
  大丈VXTag(["That2 "," is a  "," ."],person,aTvam,true);
  console.log(aTvam.Ans); // That マイケル is a youngster.

  大丈VXTag`DBG$$:That3 ${person} is a  .${aTvam}${true}`;
    //Debug>"DBG$$:That , is a .,,"@"マイケル"@"[object Object]"@
  console.log(aTvam.Ans); // DBG$$:That マイケル is a .youngster

  aTvam.isa = 48;
  大丈VXTag`That4 ${person}is a ${aTvam}、、さん`;
  console.log(aTvam.Ans);
  
  aTvam.isa = 68;
  大丈VXTag`That5 ${person} is a  ${aTvam} .`;
  console.log(aTvam.Ans);

  aTvam.isa = 88;
  大丈VXTag`That6 ${person} is a  ${aTvam} .`;
  console.log(aTvam.Ans);
},
3 * 1000);
```

このコードは、3秒後に実行される`setTimeout`関数を含んでいます。その中で、`大丈VXTag`という名前のタグ付きテンプレートリテラル関数が定義され、複数回呼び出されています。この`大丈VXTag`は、与えられた文字列と値を使用して、`aTvam.Ans`プロパティへ処理（評価）結果を格納します。

3秒後に、次のConsole出力が表示されます:

```Text:Console出力
what?28
That マイケル is a youngster。
Debug>"That2 , is a  , ."@"マイケル"@"[object Object]"@
That2 マイケル is a youngster .
Debug>"DBG$$:That3 , is a  .,,"@"マイケル"@"[object Object]"@
DBG$$:That3 マイケル is a .youngster
what?48
That4 マイケルis a Oyaji。、、さん
what?68
That5 マイケル is a Jinys! .
what?88
That6 マイケル is a God!?fathers .
```

- `大丈VXTag`は、タグ付きテンプレートリテラル関数です。この関数は、テンプレートリテラル内の文字列と式を引数として受け取り、それらを使用して処理を行います。

  `大丈VXTag`は、複数回呼び出されており、その都度異なる結果を生成し最終的な`aTvam` オブジェクトの`Ans`プロパティへそれを紐づけています。

  `大丈VXTag`タグ付きテンプレートリテラル関数は、4つの引数を受け取ります。`strings`は、テンプレートリテラル内の文字列部分の配列です。`personExp`は、テンプレートリテラル内の最初の式（この場合は`person`変数）の値です。`pTvam`は、テンプレートリテラル内の2番目の式（この場合は`aTvam`オブジェクト）の値です。最後に、`Debug`は、デバッグモードを有効にするかどうかを指定する真偽値です。

  1. これは、まずデバッグモードが有効な場合にデバッグ情報を出力します。次に、文字列部分を変数に代入し`pTvam.Q`と`pTvam.isa`の値を出力します。
  1. 年齢判定用の「アロー関数」を呼び出します。この関数は、与えられた年齢に基づいて異なる文字列を生成し、それを`ppTvam.Ans`プロパティに格納します。
     - アロー関数内では、年齢が40歳未満の場合は「youngster」、40歳以上60歳未満の場合は「Oyaji。」、60歳以上80歳未満の場合は「Jinys!」、80歳以上の場合は「God!?fathers」を返します。
  1. 最後に、これは配列を返しますが、この配列を呼び出し元では使用せず`aTvam`オブジェクトの`Ans`プロパティに紐づく戻り値をConsoleへ出力しています。

## *再要約*

`(preTransforms) => [//X式列`  
↑も含めたこの中で

- 「代入式の左辺（`名前=式Or値`｜`名前={プロパティ宣言}，`）」  
- 「プロパティ宣言（`名前:式Or値,`｜`名前:{プロパティ宣言}，`）」で記載した名前は、  
全て”その構造でのObjectプロパティ”と判断でき、  
  - `その構造でのObject.プロパティ名...`  
  - `その動的Object参照.set/getAttribute('プロパティ名'...`でアクセス出来ます。  
- 尚、「式」開始部分で`(引数*)=>{ Or [`と記載すれば、  
       その引数へ依存できるfunctionステートメント Or 式列をコード出来ます。  
- また、プロパティ名はその中からブロックスコープとして参照出来ます。  

### これに基づく、目的動作をしない事を確認済みのコードスニペット **TODO!!**

このコードはコメント中にある「`//目的とする出力>...`」を得ることが出来ませんでした。  もし、興味が有ればコメント欄などに示して下さると幸いです。

```javascript:動作確認済みコードスニペット
(
(preTransforms) => [//X式列
//↑も含めたこの中で
// - 「代入式の左辺（`名前=式Or値`｜`名前={プロパティ宣言}，`）」  
// - 「プロパティ宣言（`名前:式Or値,`｜`名前:{プロパティ宣言}，`）」で記載した名前は、  
//全て”その構造でのObjectプロパティ”と判断でき、  
//    - `その構造でのObject.プロパティ名...`  
//    - `その動的Object参照.set/getAttribute('プロパティ名'...`でアクセス出来ます。  
// - 尚、「式」開始部分で`(引数*)=>{ Or [`と記載すれば、  
//       その引数へ依存できるfunctionステートメント Or 式列をコード出来ます。  
// - また、プロパティ名はその中からブロックスコープとして参照出来ます。  
console.log(`preTransforms =${preTransforms}`),
  //> rotateX(40deg) rotateY(30deg) scale3d(3,3,3) translateX(-10px) translateY(-40px) translateY(50px) translateX(-33px)
Sg = String,//Stringクラス参照用のショートカットプロパティ「Sg」を定義
spPm = {
  sTrs: 'translate',
  ptXY: '[X|Y]',
  ptCsm:{
    ptCS: Sg.raw`\(`,//ThisIsPython r'...' Like
    ptCI: Sg.raw`[^\)]+`,
    ptCE: Sg.raw`\)`},
  ptNum: Sg.raw`[\-|\+|\.|0-9]+`,
  sDc: Sg.raw`"`,sSc: Sg.raw`"`,
  re: (//以下のパラメータディフォルト値は実行時参照となるため、
       //宣言時プロパティ名経由=`spPm.`で指定する必要があります。
    ptstr=spPm.sTrs+spPm.ptXY+spPm.ptCsm.ptCS+spPm.ptCsm.ptCI+spPm.ptCsm.ptCE,
    gis="g") => {
      return new RegExp(Sg.raw`${ptstr}`, Sg.raw`${gis}`); 
  },
  //クラスプロパティ定義
  InCS:class{//At `new spPm.InCS(iv1,iv2) ` Instances Play!
       constructor(iv1,iv2) {
         console.log(
           `constructor callBy new propname.InCS(${iv1},${iv2}) !
           I have inner Cluse this refer`);    
       }
  }
},
rejectedTransraters =  preTransforms.replace(spPm.re(),""),
console.log(`rejectedTransraters =${rejectedTransraters}`),
  //> rejectedTransraters =rotateX(40deg) rotateY(30deg) scale3d(3,3,3) 
new spPm.InCS("aaa","bbb"),
  //> constructor callBy new propname.InCS(aaa,bbb) !I have inner Cluse this refer
gettsTransraters = preTransforms.replace(rejectedTransraters,""),
console.log(`gettsTransraters=${gettsTransraters}`),
  //??> gettsTransraters=rotateX(40deg) rotateY(30deg) scale3d(3,3,3) translateX(-10px) translateY(-40px) translateY(50px) translateX(-33px)
  //目的とする出力> gettsTransraters=translateX(-10px) translateY(-40px) translateY(50px) translateX(-33px)

])
(
`rotateX(40deg) rotateY(30deg) scale3d(3,3,3) translateX(-10px) 
translateY(-40px) translateY(50px) translateX(-33px)`
);
```

## メモリー考察への道？

[Memory management https://developer.mozilla.org/ja/docs/Web/JavaScript/Memory_Management](https://developer.mozilla.org/ja/docs/Web/JavaScript/Memory_Management)

### １ターゲット　WeakMap、WeakSet、WeakRef

*WeakMap、WeakSet、WeakRefなどのAPIは、ガベージコレクションに関連するデータ構造やAPIです。これらはオブジェクトを**弱く保持**することで、ガベージコレクションの観察やメモリ使用の最適化に役立ちます。*

例えば、WeakMapはキーと値のペアを保持することができますが、キーが弱く保持されるため、キーが他に参照されていない場合はガベージコレクションの対象となります。これにより、不要なオブジェクトがメモリ上に残り続けることを防ぐことができます。

また、WeakRefはオブジェクトへの弱い参照を提供します。これにより、オブジェクトがガベージコレクションされるまでの間、その内容を読み取ることができます。キャッシュシステムなどで役立ちます。

これらのAPIは、長時間実行されるプログラムでメモリ使用量を最適化するために使用されます。詳しい情報はMDN Web Docsの[WeakMap](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/WeakMap)、[WeakSet](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/WeakSet)、[WeakRef](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/WeakRef)のページを参照してください。

## 本記事主題を把握する為の「フィボナッチ数列」（from Bing):

これは、私が本記事の要約をBingへ依頼した時に得た情報です。  
私的に「フィボナッチ数列」？？？となっておりますが有識者であれば、この「まとまりの無い記事」を把握する為に役立つかもしれません。

---

このページの記事では、[*フィボナッチ数列*](https://ja.wikipedia.org/wiki/%E3%83%95%E3%82%A3%E3%83%9C%E3%83%8A%E3%83%83%E3%83%81%E6%95%B0)に関するコードやロジックの例を紹介しています。例えば、以下のようなものです。

- 式へステートメントを組み込む".~"チェーンスタイル
- 式列配置と記法の参考事項
- 式列でプロパティ名ブロックスコープを使い自身を再帰的に評価するロジック例
- テンプレートリテラルX式列呼び出し例

これらの例は、JavaScriptの構文や機能を使って、フィボナッチ数列を生成したり、操作したりする方法を示しています。

「フィボナッチ数列」は、数学の分野で広く研究されている数列の一つです。この数列は、イタリアの数学者であるフィボナッチ(1170 - 1259年)が名付けたもので、「1、1、2、3、5、8、13、21、34、55、89、144、233…」のように、前の数字を足した数が続く法則のことです。

フィボナッチ数列は、自然界における成長や**増殖などの現象を表す**際にも用いられることがあります。また、フィボナッチ数列に基づく「黄金比」は、美術や建築など様々な分野で応用されています。

---

# おわりに

*この記事がご覧頂いた方々にとって何らかの参考になれば幸いです。*

# 参照情報他
:::note info
- この記事は、私がJavaScriptコード及び文章ドラフトを[`Github`](https://engbjapan.github.jo/Programming/JavaScript//%20HCJ/Exsample/a3Dmesh/ArrowHeaven/Stairway2HeavenArrow.md)へMarkdownファイルとして作成し、`MicrosoftEdge`で閲覧しながら`Bing`を用いて記事の精査、補足情報の収集etcを行い作成したものです。  

以下は、Bingからの紹介文です。

---

  `Microsoft Bing`は、Microsoftが提供する検索エンジンです。Bingは、Web、画像、動画、地図などの検索サービスを提供しています。

   - **Web検索**: Bingは、Webページの検索結果を提供します。
   - **画像検索**: Bingは、画像の検索結果を提供します。
   - **動画検索**: Bingは、動画の検索結果を提供します。
   - **地図検索**: Bingは、地図の検索結果を提供します。

  Bingは、Microsoftが提供する検索エンジンであり、Web、画像、動画、地図などの検索サービスを提供しています。Bingは、高度な検索アルゴリズムと人工知能技術を使用して、ユーザーに最適な検索結果を提供します。

---
- 「天国への階段(Stairway to Heaven)」は、イギリスのロックグループ、レッド・ツェッペリンの代表曲です。ジミー・ペイジとロバート・プラントによる共作です。

  - 天国への階段 (レッド・ツェッペリンの曲) - Wikipedia: [https://ja.wikipedia.org/wiki/天国への階段_(レッド・ツェッペリンの曲)](https://ja.wikipedia.org/wiki/%E5%A4%A9%E5%9B%BD%E3%81%B8%E3%81%AE%E9%9A%8E%E6%AE%B5_%28%E3%83%AC%E3%83%83%E3%83%89%E3%83%BB%E3%83%84%E3%82%A7%E3%83%83%E3%83%9A%E3%83%AA%E3%83%B3%E3%81%AE%E6%9B%B2%29)

- MDN Web Docs: [https://developer.mozilla.org/](https://developer.mozilla.org/)

- TypeScript Playground: [https://www.typescriptlang.org/play](https://www.typescriptlang.org/play)

- Microsoft Bing: [https://www.bing.com/](https://www.bing.com/)
  
- Microsoft Edge: [https://www.microsoft.com/en-us/edge](https://www.microsoft.com/en-us/edge)

- Microsoft Visual Studio Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)

---
- **2 Fibonacci sequence Heaven!!**(From Bing)

「フィボナッチ数列」的な思考で、いわゆる「IK」物理学的IKをJavaScriptで実装することが可能です。実際に、GitHubには、**lo-th/fullik**というリポジトリがあります。これは、**three.js**上で動作する、**Inverse Kinematics**のための高速な反復ソルバーです。このライブラリは、JavaからCalikoライブラリへの変換であり、Calikoライブラリは、Dr. Andreas AristidouによるFABRIK逆運動学アルゴリズムの実装です¹。

また、他にも、**Matter.js**という2D剛体JavaScript物理エンジンがあります。これは、Web用の2D物理エンジンであり、剛体、複合体、複合体、凹凸ハルなどの機能があります²。

これらのライブラリを使用することで、「IK」物理学的IKをJavaScriptで実装することが可能です。

(1) GitHub - lo-th/fullik: javascript fast iterative solver for Inverse .... https://github.com/lo-th/fullik

(2) Matter.js - a 2D rigid body JavaScript physics engine · code .... http://brm.io/matter-js/

(3) Build a simple 2D physics engine for JavaScript games. https://developer.ibm.com/tutorials/wa-build2dphysicsengine/

:::

最新版：https://qiita.com/engbJapan/items/f6ad007cd83723e61b00/

:License: MIT