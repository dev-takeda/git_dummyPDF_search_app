import os
import sqlite3
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)
db_file = "dummy_database.sqlite"
PDF_FOLDER = os.path.join(app.root_path, "dummy_raw_pdfs")

# タグ一覧と科目区分を取得する関数
def get_unique_subjects_tags():
    with sqlite3.connect(db_file) as conn:
        query_subject = "SELECT DISTINCT 科目区分 FROM dummy_syllabus WHERE 科目区分 IS NOT NULL AND 科目区分 != ''"
        raw_subjects = [row[0] for row in conn.execute(query_subject).fetchall()]

        query_tag = "SELECT DISTINCT タグ FROM dummy_syllabus WHERE タグ IS NOT NULL AND タグ != ''"
        raw_tags = [row[0] for row in conn.execute(query_tag).fetchall()]

    unique_subjects = set()
    for subject_group in raw_subjects:
        for subject in subject_group.split(" / "):
            unique_subjects.add(subject.strip())

    unique_tags = set()
    for tag_group in raw_tags:
        for tag in tag_group.split(" / "):
            unique_tags.add(tag.strip())

    return sorted(unique_subjects), sorted(unique_tags)

# 科目区分・タグからPDFデータを取得する関数
def get_pdfs_from_db(data_type, value):
    with sqlite3.connect(db_file) as conn:
        if data_type == "subject":
            query = """
                SELECT 講義資料, 課題_レポート FROM dummy_syllabus 
                WHERE 科目区分 LIKE ? AND (講義資料 IS NOT NULL OR 課題_レポート IS NOT NULL)
            """
        elif data_type == "tag":
            query = """
                SELECT 講義資料, 課題_レポート FROM dummy_syllabus 
                WHERE タグ LIKE ? AND (講義資料 IS NOT NULL OR 課題_レポート IS NOT NULL)
            """
        else:
            return []

        results = conn.execute(query, (f"%{value}%",)).fetchall()

    pdf_list = []
    for row in results:
        for pdfs in row:
            if pdfs:
                pdf_list.extend([pdf.strip() for pdf in pdfs.split(" / ") if pdf.strip()])

    return pdf_list

# データベースのすべてのカラムからkeyword検索をする関数
def search_in_database(keyword):
    with sqlite3.connect(db_file) as conn:
        query = """
            SELECT 科目ID, 科目名, 講義資料, 課題_レポート FROM dummy_syllabus
            WHERE 科目ID LIKE ? OR 科目区分 LIKE ? OR 科目名 LIKE ?
            OR タグ LIKE ? OR 概要 LIKE ? OR 目標 LIKE ? OR 講義回 LIKE ?
            OR 講義タイトル LIKE ? OR 講義サブタイトル LIKE ? OR 内容 LIKE ?
            OR 講義資料 LIKE ? OR 課題_レポート LIKE ? OR キーワード LIKE ?
        """
        keyword_like = f"%{keyword}%"
        results = conn.execute(query, (keyword_like,) * 13).fetchall()

    pdf_list = []
    for row in results:
        科目ID, 科目名, 講義資料, 課題_レポート = row
        if 講義資料:
            pdf_list.extend([pdf.strip() for pdf in 講義資料.split(" / ") if pdf.strip()])
        if 課題_レポート:
            pdf_list.extend([pdf.strip() for pdf in 課題_レポート.split(" / ") if pdf.strip()])

    return list(set(pdf_list))

# エンドポイントの設定
@app.route("/")
def index():
    subjects, tags = get_unique_subjects_tags()
    return render_template("index.html", subjects=subjects, tags=tags)

@app.route("/get_pdfs")
def get_pdfs():
    data_type = request.args.get("type")
    value = request.args.get("value")

    if not data_type or not value:
        return jsonify([])

    pdf_list = get_pdfs_from_db(data_type, value)
    return jsonify(pdf_list)

@app.route("/search_pdfs")
def search_pdfs_endpoint():
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return jsonify([])

    pdf_list = search_in_database(keyword)
    return jsonify(pdf_list)

@app.route("/pdf/<filename>")
def serve_pdf(filename):
    return send_from_directory(PDF_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
