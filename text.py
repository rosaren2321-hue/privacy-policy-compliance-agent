import requests
import tempfile
import zipfile
import xml.etree.ElementTree as ET
import os

def extract_docx_text(docx_path):
    """提取 docx 文本内容"""
    text = []
    with zipfile.ZipFile(docx_path) as z:
        if 'word/document.xml' not in z.namelist():
            return ""
        xml_content = z.read('word/document.xml')
        root = ET.fromstring(xml_content)
        for node in root.iter():
            if node.tag.endswith('}t') and node.text:
                text.append(node.text)
    return "\n".join(text)

def split_text_by_section(text, keywords=None):
    """
    按指定关键词拆分文本，返回两部分
    keywords: list，例如 ["四、","4、","Ⅳ","4.","四."]
    """
    if not keywords:
        keywords = ["四、","4、","Ⅳ","4.","四."]
    
    # 找到最先出现的关键词的位置
    split_pos = -1
    for kw in keywords:
        pos = text.find(kw)
        if pos != -1:
            if split_pos == -1 or pos < split_pos:
                split_pos = pos
    
    if split_pos == -1:
        # 没找到关键词，就返回原文为第一部分，第二部分为空
        return [text.strip(), ""]
    else:
        part1 = text[:split_pos].strip()
        part2 = text[split_pos:].strip()
        return [part1, part2]

def main(input):
    # 获取文件列表
    file_list = input.get("FileURL")
    if not file_list or len(file_list) == 0:
        return {"text": "Error: FileList empty or missing"}

    file_obj = file_list[0]
    file_url = file_obj.get("FileURL")
    file_type = file_obj.get("FileType")
    file_name = file_obj.get("FileName")

    if not file_url:
        return {"text": "Error: FileURL missing"}

    try:
        response = requests.get(file_url)
        response.raise_for_status()

        suffix = "." + file_type.lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        if file_type.lower() == "docx":
            text = extract_docx_text(tmp_path)
        else:
            text = f"Unsupported file type: {file_type}"

        os.remove(tmp_path)

        # 拆分文本，按标题“4”或“四”
        text_parts = split_text_by_section(text, keywords=["四、","4、","Ⅳ","4.","四."])

        # 返回 obj
        return {
            "FileName": file_name,
            "FileType": file_type,
            "text_part1": text_parts[0],
            "text_part2": text_parts[1]
        }

    except Exception as e:
        return {"text": f"Error extracting document: {str(e)}"}
