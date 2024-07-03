
# Rakuten Securities Asset Management Automation

## 概要

このプロジェクトは、楽天証券から資産情報のCSVファイルをダウンロードし、Googleスプレッドシートに自動的にインポートするPythonスクリプトです。これにより、手動でのデータ管理作業を自動化し、定期的に最新の資産情報をスプレッドシートで管理することができます。

### 特徴

- **CSVファイルの自動ダウンロード**: 楽天証券のサイトから資産情報のCSVファイルを自動でダウンロードします。
- **Googleスプレッドシートへのアップロード**: ダウンロードしたCSVファイルのデータをGoogleスプレッドシートにアップロードします。
- **Google Apps Scriptのトリガー**: データのアップロード後にGoogle Apps Scriptをトリガーして、追加の処理を実行します。


### インストール方法

このプロジェクトをローカル環境にインストールするには、以下の手順に従ってください。

## 環境変数を設定する
PYTHONSCR_KEYFILE_PATH=credentials/pythonscr-380420-036213d91a2c.json
GAS_WEB_APP_URL_FILE=credentials/gas_web_app_url.json
LOGIN_INFO_FILE=credentials/login_info.json



### 使用ライブラリ
このプロジェクトでは以下のライブラリが必要です。requirements.txtファイルにはこれらのライブラリのバージョンが含まれています。

# selenium - ウェブブラウザの自動操作を行うためのライブラリ
# gspread - Googleスプレッドシートと連携するためのライブラリ
# chardet - 文字エンコーディングを自動検出するためのライブラリ
# requests - HTTPリクエストを送信するためのライブラリ
# oauth2client - Google APIの認証情報を管理するためのライブラリ



### Chrome WebDriverの設定

本プロジェクトはChrome WebDriverを使用します。以下の手順でChrome WebDriverを設定してください。

Chrome WebDriverのダウンロードページから、使用しているChromeのバージョンに対応したWebDriverをダウンロードします。
ダウンロードしたchromedriverをシステムのPATHに追加するか、プロジェクトのルートディレクトリに配置します。
スプレッドシートAPIの設定
Google Sheets APIを有効にし、Google Cloud コンソールから以下の形式のサービスアカウントキーを保存してください。このキーはcredentials/pythonscr-380420-036213d91a2c.jsonとして保存します。

```json
{
  "type": "service_account",
  "project_id": "aaa",
  "private_key_id": "aaa",
  "private_key": "-----BEGIN PRIVATE KEY-----\naaa\n-----END PRIVATE KEY-----\n",
  "client_email": "id-aaa.com",
  "client_id": "aaa",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/aaa.com",
  "universe_domain": "googleapis.com"
}
```

### 楽天証券の情報の設定
楽天証券のID、パスワード、およびログインURLを以下の形式で準備し、credentials/login_info.jsonに保存してください。
```json
{
  "bank_rakuten": {
    "id": "1234567890",
    "pass": "password",
    "url": "https://fes.rakuten-bank.co.jp/MS/main/RbS?CurrentPageID=START&&COMMAND=LOGIN"
  },
  "sec_rakuten": {
    "id": "AAAA1111",
    "pass": "Abcd1234",
    "url": "https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html"
  }
}
```
