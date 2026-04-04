"""
Google Drive上のExcelファイルまたはGoogle Sheetsからデータを取得するモジュール。
認証情報は credentials/service_account.json に配置してください（gitignore済み）。
"""

import io
import os
import re
from pathlib import Path

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_PATH = Path(__file__).parent / "credentials" / "bq-sql-447114-dd629c593c7f.json"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
SHEETS_MIME = "application/vnd.google-apps.spreadsheet"
XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def extract_file_id(url_or_id: str) -> str:
    """
    Google DriveのURLまたはファイルIDからファイルIDを抽出する。
    URLの場合は /d/XXXX/ の部分を、そうでなければそのまま返す。
    """
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url_or_id)
    if match:
        return match.group(1)
    return url_or_id.strip()


def _get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        str(CREDENTIALS_PATH), scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


def load_muscle_data(file_id: str, sheet_name: str = "workout") -> pd.DataFrame:
    """
    Google Drive上のExcelファイルまたはGoogle Sheetsをダウンロードして
    DataFrameとして返す。Google Sheetsの場合はxlsx形式でエクスポートする。

    Parameters
    ----------
    file_id : str
        Google DriveのファイルID
        （URLの /d/XXXXXXXX/edit の XXXXXXXX 部分）
    sheet_name : str
        読み込むシート名（デフォルト: "workout"）

    Returns
    -------
    pd.DataFrame
    """
    service = _get_drive_service()

    file_meta = service.files().get(fileId=file_id, fields="mimeType").execute()
    mime_type = file_meta.get("mimeType", "")

    if mime_type == SHEETS_MIME:
        request = service.files().export_media(fileId=file_id, mimeType=XLSX_MIME)
    else:
        request = service.files().get_media(fileId=file_id)

    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buffer.seek(0)
    df = pd.read_excel(buffer, sheet_name=sheet_name)
    return df


def get_file_id_from_env() -> str:
    """環境変数 GDRIVE_FILE_ID からファイルIDを取得する。"""
    file_id = os.getenv("GDRIVE_FILE_ID", "")
    if not file_id:
        raise ValueError(
            "GDRIVE_FILE_ID が未設定です。.env ファイルに設定するか、"
            "アプリのサイドバーからURLを入力してください。"
        )
    return file_id
