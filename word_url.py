import re

def main(params):
    """直接从原始字符串中提取URL"""
    print("开始执行URL提取")
    print(f"输入参数类型: {type(params)}")
    print(f"输入参数内容: {params}")
    
    word_url = ""
    
    # 获取word_text内容
    if 'word_text' in params:
        word_text = params['word_text']
        print(f"原始word_text: {word_text}")
        
        # 直接使用正则表达式匹配docx URL
        # 匹配 https://file.duhuitech.com/o/.../...docx 格式的URL
        url_pattern = r'https://file\.duhuitech\.com/o/[a-zA-Z0-9]+/[a-zA-Z0-9-]+\.docx'
        matches = re.findall(url_pattern, word_text)
        
        if matches:
            word_url = matches[0]
            print(f"直接提取到URL: {word_url}")
        else:
            print("未找到匹配的URL")
            
            # 尝试更宽松的匹配模式
            url_pattern2 = r'https://[^"]+\.docx'
            matches2 = re.findall(url_pattern2, word_text)
            
            if matches2:
                word_url = matches2[0]
                print(f"使用宽松模式提取到URL: {word_url}")
    
    result = {
        "word_url": word_url,
        "md_url": word_url
    }
    
    print(f"输出结果: {result}")
    return result

# 平台调用
try:
    if 'lke_system_params' in locals():
        main_result = main(lke_system_params)
    elif 'lke_system_params' in globals():
        main_result = main(lke_system_params)
    else:
        # 使用你提供的测试数据
        test_params = {
            "word_text": '{"content":{"word_url":"https://file.duhuitech.com/o/59dc99cefa133ae97964829327dd3bb87/0812d6d4-1642-4f89-bc5b-a10a936bd41a.docx""""size":20193},"description":"Size(size(返回word的字节数)); WordUrl(word url(返回word的ur1))"}'
        }
        main_result = main(test_params)
except Exception as e:
    print(f"执行失败: {e}")
    main_result = {"word_url": "", "md_url": ""}