import os
import shutil

# 元のPDFファイル
source_pdf = "/Users/ringo_ame/Desktop/Self_Made_APP/pdf_search_app/dummy_raw_pdfs/ITの社会的責任及び演習_3.pdf"

# 保存先のベースフォルダ（変更可能）
base_folder = "/Users/ringo_ame/Desktop/Self_Made_APP/pdf_search_app/dummy_raw_pdfs"

# フォルダが存在しない場合は作成
os.makedirs(base_folder, exist_ok=True)

# 新しいファイル名で保存
for i in range(1, 9):
    # 新しいPDFのパス
    new_pdf_name = f"簿記入門Ⅱ_{i}.pdf"
    save_path = os.path.join(base_folder, new_pdf_name)

    # ファイルをコピーして新しい名前で保存
    shutil.copy(source_pdf, save_path)

    print(f"コピー作成: {save_path}")

print("PDFのリネーム＆保存が完了しました。")
