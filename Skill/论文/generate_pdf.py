#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用xhtml2pdf生成论文PDF（支持中文）
"""
import os
import re
from xhtml2pdf import pisa
from io import BytesIO

def extract_text_from_tex(filepath):
    """从LaTeX文件中提取文本"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除LaTeX命令但保留参数
        content = re.sub(r'\\textbf\{([^}]*)\}', r'<b>\1</b>', content)
        content = re.sub(r'\\textit\{([^}]*)\}', r'<i>\1</i>', content)
        content = re.sub(r'\\emph\{([^}]*)\}', r'<em>\1</em>', content)
        
        # 移除其他LaTeX命令
        content = re.sub(r'\\begin\{[^}]*\}', '', content)
        content = re.sub(r'\\end\{[^}]*\}', '', content)
        content = re.sub(r'\\section\{([^}]*)\}', r'<h2>\1</h2>', content)
        content = re.sub(r'\\subsection\{([^}]*)\}', r'<h3>\1</h3>', content)
        content = re.sub(r'\\subsubsection\{([^}]*)\}', r'<h4>\1</h4>', content)
        content = re.sub(r'\\input\{[^}]*\}', '', content)
        content = re.sub(r'\\label\{[^}]*\}', '', content)
        content = re.sub(r'\\ref\{[^}]*\}', '', content)
        content = re.sub(r'\\cite\{[^}]*\}', '', content)
        
        # 清理多余的转义字符
        content = re.sub(r'\\%', '%', content)
        content = re.sub(r'\\\$', '$', content)
        content = re.sub(r'\\&', '&', content)
        content = re.sub(r'\\\|', '|', content)
        content = re.sub(r'~', ' ', content)
        
        # 清理多余空白
        content = re.sub(r'\n\s*\n+', '</p><p>', content)
        content = re.sub(r'\n', ' ', content)
        
        return content.strip()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""

def generate_pdf():
    """生成PDF"""
    paper_dir = r"c:\Users\tnc\Links\Mrite\Skill\论文"
    output_file = os.path.join(paper_dir, "论文.pdf")
    
    # 收集所有tex文件内容
    tex_files = [
        "0.摘要.tex",
        "1.引言.tex", 
        "2.总体分析.tex",
        "3.模型假设.tex",
        "4.符号说明.tex",
        "5.1.问题1的建立求解.tex",
        "5.2.问题2的建立求解.tex",
        "5.3.问题3的建立求解.tex",
        "5.4.问题4的建立求解.tex",
        "6.模型检验.tex",
        "7.模型评价.tex",
        "8.模型改进推广.tex",
        "9.参考文献.tex",
        "10.附录.tex"
    ]
    
    print("开始生成PDF...")
    
    # 构建HTML内容
    html_content = """
    <html>
    <head>
        <meta charset="UTF-8" />
        <style>
            body { font-family: Arial, SimSun; font-size: 12pt; line-height: 1.6; margin: 20px; }
            h1 { text-align: center; font-size: 24pt; margin: 20px 0; }
            h2 { font-size: 16pt; margin-top: 15px; margin-bottom: 10px; border-bottom: 1px solid #ccc; }
            h3 { font-size: 14pt; margin-top: 12px; margin-bottom: 8px; }
            h4 { font-size: 12pt; margin-top: 10px; margin-bottom: 6px; }
            p { margin: 5px 0; text-align: justify; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { border: 1px solid #999; padding: 5px; text-align: left; }
            th { background-color: #f0f0f0; font-weight: bold; }
            .page-break { page-break-after: always; }
        </style>
    </head>
    <body>
        <h1>基于Python的慢性健康管理与数据可视化系统</h1>
        <p style="text-align: center; font-size: 14pt;">学位论文</p>
    """
    
    # 添加内容
    for i, tex_file in enumerate(tex_files):
        filepath = os.path.join(paper_dir, tex_file)
        
        if os.path.exists(filepath):
            print(f"处理: {tex_file}")
            text = extract_text_from_tex(filepath)
            
            if text:
                html_content += f"<div class='page-break'><p>{text}</p></div>\n"
    
    html_content += """
    </body>
    </html>
    """
    
    # 转换为PDF
    try:
        result_file = open(output_file, "w+b")
        pisa_status = pisa.CreatePDF(
            html_content,
            dest=result_file,
            encoding='UTF-8'
        )
        result_file.close()
        
        if pisa_status.err:
            print(f"PDF生成出错: {pisa_status.err}")
            return False
        
        print(f"\nPDF已生成: {output_file}")
        
        # 验证文件
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"文件大小: {file_size / 1024:.2f} KB")
            return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False
    
    return False

if __name__ == "__main__":
    success = generate_pdf()
    if success:
        print("\n✓ PDF生成成功！")
    else:
        print("\n✗ PDF生成失败")
