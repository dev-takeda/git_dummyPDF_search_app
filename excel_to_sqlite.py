import pandas as pd
import sqlite3
import os

EXCEL_FOLDER = "dummy_syllabus"
DB_FILE = "dummy_database.sqlite"

# フォルダ内の全エクセルファイルを取得
def get_excel_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]

# エクセルファイルを読み込む
def load_excel(file_path):
    df = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
    return df

# エクセルデータをSQLiteに保存
def save_to_sqlite(df_dict, db_path, filename):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # テーブル作成
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dummy_syllabus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            科目ID TEXT,
            科目区分 TEXT,
            科目名 TEXT,
            タグ TEXT,
            概要 TEXT,
            目標 TEXT,
            講義回 TEXT,
            講義タイトル TEXT,
            講義サブタイトル TEXT,
            内容 TEXT,
            講義資料 TEXT,
            課題_レポート TEXT,
            キーワード TEXT,
            エクセルファイル名 TEXT
        )
    """)
    # クエリエラー防止のため、科目区分とタグは上のセルで追記、NaNは空文字に変換
    for sheet_name, df in df_dict.items():
        df["科目区分"].fillna(method='ffill', inplace=True)
        df["タグ"].fillna(method='ffill', inplace=True)
        df = df.fillna("")
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO dummy_syllabus (科目ID, 科目区分, 科目名, タグ, 概要, 目標, 講義回, 講義タイトル, 講義サブタイトル, 内容, 講義資料, 課題_レポート, キーワード, エクセルファイル名)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(row.get("科目ID", "")), 
                str(row.get("科目区分", "")),  
                str(row.get("科目名", "")), 
                str(row.get("タグ", "")),  
                str(row.get("概要", "")), 
                str(row.get("目標", "")), 
                str(row.get("講義回", "")), 
                str(row.get("講義タイトル", "")), 
                str(row.get("講義サブタイトル", "")), 
                str(row.get("内容", "")), 
                str(row.get("講義資料", "")),  
                str(row.get("課題_レポート", "")), 
                str(row.get("キーワード", "")), 
                filename  
            ))

    conn.commit()
    conn.close()
    print(f"{filename} のデータベース保存完了！")

if __name__ == "__main__":
    if not os.path.exists(EXCEL_FOLDER):
        print("エクセルフォルダが見つかりません！")
    else:
        excel_files = get_excel_files(EXCEL_FOLDER)
        if not excel_files:
            print("エクセルファイルが見つかりません！")
        else:
            for excel_file in excel_files:
                file_path = os.path.join(EXCEL_FOLDER, excel_file)
                df_dict = load_excel(file_path)
                save_to_sqlite(df_dict, DB_FILE, excel_file)
