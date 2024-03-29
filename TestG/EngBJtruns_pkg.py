import os as iＯＳ
import urllib.request as iリックエスト
import json as iジェイソン
import getpass as iパスゲット
from IPython.display import clear_output as i出力クリア
import portpicker as iポートピック
#https://docs.python.org/ja/3/library/shlex.html#module-shlex
from shlex import quote as i安全なシェル向けクオーティング
from shlex import split as iクオーティングsplit
from subprocess import Popen as iプロセス生成と管理
from subprocess import PIPE as fパイプ
from subprocess import STDOUT as ｆ標準出力

ワークディレクトリ="/content"

def 指定の変数の値を取得します(変数名):
  return iＯＳ.environ[変数名]

def 指定の変数の値を設定します(変数名,値):
  iＯＳ.environ[変数名] = 値
  return 指定の変数の値を取得します(変数名)

def 環境変数にメッセージ出して入力を設定(
      変数名
      ,メッセージ="入れてください："
      ,デホルト値指定=""
      ,ダメな文字列=""):
  環境変数名 = f"ENGBJ_{変数名}"
  良い = False
  while not 良い :
    入力値 = i安全なシェル向けクオーティング(input(f"{メッセージ}:"))
    指定の変数の値を設定します(
        環境変数名
      ,(入力値 if (  デホルト値指定 == "" or 入力値 != "" )  else デホルト値指定)
    )
    if (ダメな文字列!="" and ダメな文字列==入力値):
      print("それは入力してはいけません！もう一度！！")
      continue
    良い = (input(
          f"{指定の変数の値を取得します(環境変数名)}　これで良いです？(y/n):"
            ) == "y")

  return 指定の変数の値を取得します(環境変数名)

変えないでね = ["http://localhost",":4040","_url"] #マークブロック
変えないで2 = ["lic","pub","nels","/api","/tun"] #マークブロック

def パブリックアクセス情報の取得():
  import time 
  リトライ回数=0
  ホストポートリスト=[]
  while リトライ回数<10 :
    try:
      time.sleep(1.0)
      with iリックエスト.urlopen(f"{変えないでね[0]}{変えないでね[1]}{変えないで2[3]}{変えないで2[4]}{変えないで2[2]}") as response:
        取得ジェイソン =iジェイソン.loads(response.read().decode())
        for トンネルず in 取得ジェイソン[f"tun{変えないで2[2]}"]:
          トンネル名=トンネルず["name"];ホスト名=トンネルず[f"{変えないで2[1]}{変えないで2[0]}{変えないでね[2]}"]
          ホストポートリスト.append(f"{トンネル名}:{ホスト名}")

        break      
    except  IndexError :
     リトライ回数+=1
     continue
    
  return ホストポートリスト

def パブリックアクセス情報表示():
  パブ=パブリックアクセス情報の取得()
  if len(パブ) <= 0 :
    print("取得できていませんでした")
    return None
  print(f"{'※'*24}")
  for ホスト＿ポートタプル in パブ:
    print(f"""
    ホスト:ポート{ホスト＿ポートタプル}
    {'-'*48}
    """)
  print(f"{'※'*24}")
  return パブ

def システムコマンド実行(コマンド文字列):
  return get_ipython().system_raw(コマンド文字列)

def プロセス実行bash(
      コマンド列=[""]
      ,実行時ユーザ=""
      ,書き換え環境変数={
        'LANG':'ja_JP.UTF-8'
        ,'OLDPWD':f'{ワークディレクトリ}/ENNB_USERTAG'
        ,'ENV':f'{ワークディレクトリ}/ENNB_USERTAG/.bashrc'
        ,'PWD':f'{ワークディレクトリ}/ENNB_USERTAG'
        ,'HOME':f'{ワークディレクトリ}/ENNB_USERTAG'
        ,'DISPLAY':':99.0'
        ,"USER":"ENNB_USERTAG"
        ,"USERNAME":"ENNB_USERTAG"}
        ,BASHC="bash -c "):
  """
  ・コマンド列には実行したいコマンド文字列の配列を渡します（順序バック起動）
  ・実行時ユーザにはそのユーザーとしてコマンド列を実行します
  ・実行時ユーザが指定されていれば、その環境変数を起動時の環境変数COPYに書き換え環境変数で上書き追加します。
  　デホルトを変更、追加したい場合には指定してください。
  戻り値：プロセス配列で、実行（Popen）した時の戻り値がコマンド配列毎にセットされています。
  出力とリターンコードの表示には「プロセス結果表示」が使えます
  （ただし、コマンド中にバックグラウンド起動する物や待ち合わせるものがある場合、それが終わるまで待たされます）
  参照：
  [Python のサブプロセスで環境変数を扱う方法](https://hawksnowlog.blogspot.com/2021/06/python-subproces-with-environment-variables.html)
  [Popen コンストラクター](https://docs.python.org/ja/3.7/library/subprocess.html#popen-constructor)
  """
  ＲＯＯＴ環境変数Copy = iＯＳ.environ.copy()
  環境変数={}
  書き換え環境変数USER置き換え={}
  if 実行時ユーザ!="" :
      for マッピング要素文字 in list(map(
        lambda  key: 
            f'{key}'+"="+f'\"{書き換え環境変数[key].replace("ENNB_USERTAG",実行時ユーザ)}\"'
        ,list(書き換え環境変数)) ):
        
            書き換え環境変数USER置き換え.update(eval(f"dict({マッピング要素文字})"))

      ＲＯＯＴ環境変数Copy.update(書き換え環境変数USER置き換え) #if 実行時ユーザ!="" else ＲＯＯＴ環境変数Copy
      環境変数 = ＲＯＯＴ環境変数Copy
  else:
      環境変数 = ＲＯＯＴ環境変数Copy
  print(str(書き換え環境変数USER置き換え))#後で消す
  print(str(環境変数)) #後で消す
  プロセス配列=[]
  BASHC=f"sudo --user={実行時ユーザ} {BASHC}" if 実行時ユーザ!="" else BASHC
  for コマンド in コマンド列:
    区切ったコマンド配列 = iクオーティングsplit(f"{BASHC}'{コマンド}'")
    print(f":{区切ったコマンド配列}")#後で消す
    print(f"> {コマンド}")

    if 実行時ユーザ!="" :
      プロセス = iプロセス生成と管理(区切ったコマンド配列, stdout=fパイプ, env=環境変数,stderr=f標準出力)
    else:
      プロセス = iプロセス生成と管理(区切ったコマンド配列, stdout=fパイプ, stderr=f標準出力)
    プロセス配列.append(プロセス)
    print(f"PID:{プロセス.pid}")
    
  return プロセス配列

def プロセス結果表示(プロセス配列):
  for プロセス in プロセス配列:
    出力データ, _ = プロセス.communicate()
    print(f"PID:{プロセス.pid} 出力:\n{出力データ.decode(encoding='utf-8')}")
    print(f"リターンＣＯＤＥ={プロセス.returncode}")
  return プロセス配列

def プロセス切る(プロセス配列):
  map(lambda プロセス: 
          システムコマンド実行(f"kill -9 {プロセス.pid}")
      ,プロセス配列)
  return プロセス配列

def Colabウェブリンク表示(ソースポート番号,ホスト名,パス="/vnc.html",接続ポート番号="443",接続フルパス=""):
  from google.colab import output
  接続フルパス = 接続フルパス if (接続フルパス=="") else f"{パス}?host={ホスト名}&port={接続ポート番号}"
  output.serve_kernel_port_as_window(ソースポート番号,path=f"[接続フルパス]")
  return f'https://localhost:{ソースポート番号}{接続フルパス}'

# @title **GoogleDrive共有ファイルのスモール、ラージ両方取ってくる**
def GoogleDrive共有ファイル取得(
    ワークDIR="/content" # @param  
    ,
    共有ファイルID="10_wfp1U4rMzc20eiGNrdQa9V2S9ByJwV" # @param
    ):
    import subprocess as iプロセス実行
    from shlex import split as iシェル区切り列作成

    # 関数を日本語変数に紐づける
    fシステムコマンド実行 = get_ipython().system_raw

    fシステムコマンド実行(f"rm -f {ワークDIR}/_cmds")

    コマンドs = f"""
    ConTentPath={ワークDIR}
    FILE_ID="{共有ファイルID}" 
    FILE_NAMES=`wget -O - -qq https://drive.google.com/file/d/$FILE_ID/view | grep '<title>' |perl -pe 's/^.+<title>([^ ]+)[ ]+.*$/${1}/g'`
    wget -O $ConTentPath/viewhtml -qq "https://drive.google.com/uc?export=download&id=$FILE_ID"
    if [ $(grep  'DOCTYPE' $ConTentPath/viewhtml | wc -l) -eq 0 ]; then
      echo "スモールファイル:$ConTentPath/$FILE_NAMES"
      mv $ConTentPath/viewhtml $ConTentPath/$FILE_NAMES
    else
      echo "ラージファイル:$ConTentPath/$FILE_NAMES"
      printf "wget  -O $ConTentPath/$FILE_NAMES -qq 'https://drive.google.com/uc?export=download&id=$FILE_ID&confirm=t&" >  $ConTentPath/FILE_ID_WGET_CMD 
      cat $ConTentPath/viewhtml | perl -pe 's/\r*\n//g' | perl -pe 's/^.*(uuid\=[^\"]+)\".*$/$1/g' >> $ConTentPath/FILE_ID_WGET_CMD 
      printf "&uc-download-link=Download&nbsp;anyway'" >> "$ConTentPath/FILE_ID_WGET_CMD" 
      /bin/bash $ConTentPath/FILE_ID_WGET_CMD
    fi
    """
    #コマンドファイル作成
    with open(f"{ワークDIR}/_cmds","w") as ファイルOBJ :
      ファイルOBJ.write(コマンドs)               #コマンド書き込み
      ファイルOBJ.flush()                        #ファイルのフラッシュと書き込み
      ファイルOBJ.close()

    fシステムコマンド実行(f"chmod 777 {ワークDIR}/_cmds")
    # bashコマンド実行
    プロセス = iプロセス実行.Popen(
          iシェル区切り列作成(
            f"/bin/bash {ワークDIR}/_cmds")
          ,stdout=iプロセス実行.PIPE)
    # Popenのプロセスの関数を日本語変数に紐づける 
    実行結果取得 = プロセス.communicate

    実行結果出力 , エラー結果出力 = 実行結果取得()

    fシステムコマンド実行(f"rm -f {ワークDIR}/_cmds")
    fシステムコマンド実行(f"rm -f {ワークDIR}/FILE_ID_WGET_CMD")

    return (実行結果出力.decode("utf-8"),
            # いわゆ三項演算子
            エラー結果出力.decode("utf-8") if エラー結果出力!=None else "",
            プロセス)
  
