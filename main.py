import os
import csv
import glob
import json
import time
import chardet
import gspread
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from oauth2client.service_account import ServiceAccountCredentials


def download_asset_file():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    login_info = json.load(open("credentials/login_info.json", "r", encoding="utf-8"))
    site_name = "sec_rakuten"
    url_login = login_info[site_name]["url"]
    username = login_info[site_name]["id"]
    password = login_info[site_name]["pass"]

    driver.get(url_login)
    wait = WebDriverWait(driver, 500)
    username_field = wait.until(EC.presence_of_element_located((By.ID, "form-login-id")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "form-login-pass")))
    username_field.clear()
    password_field.clear()
    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = wait.until(EC.presence_of_element_located((By.ID, "login-btn")))
    login_button.click()

    # ログイン後のページがロードされるまで待機
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pcmm-btlk-link span.pcmm-btlk__text')))
        print("ログイン後のページがロードされました。")
    except:
        print("ログイン後のページのロードに失敗しました。")

    # リンクを取得して新しいタブで開く
    try:
        url_element = driver.find_element(By.CSS_SELECTOR, '.pcmm-btlk-link span.pcmm-btlk__text').find_element(By.XPATH, '..')
        url = url_element.get_attribute('href')
        if url:
            driver.execute_script("window.open(arguments[0] + '#possess_lst_detail', '_blank');", url)
            
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)

            csv_save_link = driver.find_element(By.CSS_SELECTOR, '[onclick="csvOutput(); return false;"]')
            csv_save_link.click()

            wait = WebDriverWait(driver, 10)
            download_complete = wait.until(EC.url_contains('.csv'))

        if download_complete:
            print("CSVファイルのダウンロードが開始されました。")
        else:
            print("CSVファイルのダウンロードが開始されましたが、完了までに時間がかかっています。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

def get_latest_file(download_folder):
    files = glob.glob(os.path.join(download_folder, "*"))
    if not files:
        raise FileNotFoundError("ダウンロードフォルダにファイルが存在しません。")
    return max(files, key=os.path.getmtime)

def normalize_number(value):
    if isinstance(value, str):
        try:
            return float(value.replace(',', '').strip())
        except ValueError:
            return value.strip()
    else:
        return value


def upload_to_google_sheets(file_path, spreadsheet_id):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials/pythonscr-380420-036213d91a2c.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(spreadsheet_id)

    worksheet_title = os.path.splitext(os.path.basename(file_path))[0]

    try:
        worksheet = sheet.worksheet(worksheet_title)
        print(f'"{worksheet_title}" のシートが見つかりました。上書きします。')
        worksheet.clear()

    except gspread.exceptions.WorksheetNotFound:
        print(f'"{worksheet_title}" のシートが見つからないので新しいシートを作成します。')
        worksheet = sheet.add_worksheet(title=worksheet_title, rows="100", cols="20")

    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    with open(file_path, 'r', encoding=encoding) as f:
        csv_reader = csv.reader(f)
        batch_data = []
        for row in csv_reader:
            normalized_row = [normalize_number(value) for value in row]
            batch_data.append(normalized_row)
        
        if batch_data:
            worksheet.update(batch_data, value_input_option='USER_ENTERED')


def wait_for_download(download_folder, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        files = glob.glob(os.path.join(download_folder, "*"))
        if files and any(f.endswith('.csv') for f in files):
            print("CSVファイルのダウンロードが完了しました。")
            break
        time.sleep(1)
    else:
        raise TimeoutError("ダウンロードがタイムアウトしました。")

def trigger_gas_script(web_app_url):
    response = requests.get(web_app_url)
    if response.status_code == 200:
        print("Google Apps Scriptが正常に実行されました。")
    else:
        print(f"Google Apps Scriptの実行に失敗しました。ステータスコード: {response.status_code}")


if __name__ == "__main__":
    try:
        download_asset_file()
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        latest_file = get_latest_file(download_folder)
        print("最新のファイル:", latest_file)

        # spreadsheet_id = "14mfuqIFzjls0Zyz4Q20Istzhx3VcSFE2qrQjXPkYLws"
        with open('credentials/gas_web_app_url.json', 'r') as file:
            config = json.load(file)
            
        spreadsheet_id = config['spreadsheet_id']

            
            

        upload_to_google_sheets(latest_file, spreadsheet_id)
        wait_for_download(download_folder)
        print("ファイルのアップロードが完了しました。")

        # Google Apps ScriptのWebアプリURLを指定してmain関数を呼び出す
        # gas_web_app_url = "https://script.google.com/macros/s/AKfycbyJFOsAK6MUzoZnNx8JiA1vTjUyj8iXK8vbUTXBBn0B0Tw1V-cVu2j2r9GoCDj9XF3gwg/exec"
        # trigger_gas_script(gas_web_app_url)

        
        # JSONファイルを読み込む

        # URLを取得する
        gas_web_app_url = config['gas_web_app_url']

        # 既存の関数を呼び出す
        trigger_gas_script(gas_web_app_url)

    except Exception as e:
        import traceback
        print(f"エラーが発生しました: {e}")
        traceback.print_exc()