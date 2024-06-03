import os
import webbrowser
from bs4 import BeautifulSoup
import re


def beautify_plot(plot_config):
    plot_config['width'] = 400
    plot_config['height'] = 300
    if 'axis' not in plot_config['encoding']['x']:
        plot_config['encoding']['x']['axis'] = {}
    plot_config['encoding']['x']['axis']['titleFontSize'] = 12
    plot_config['encoding']['x']['axis']['labelFontSize'] = 12
    if 'axis' not in plot_config['encoding']['y']:
        plot_config['encoding']['y']['axis'] = {}
    plot_config['encoding']['y']['axis']['titleFontSize'] = 12
    plot_config['encoding']['y']['axis']['labelFontSize'] = 12
    # if 'color' in plot_config['encoding']:
    #     del plot_config['encoding']['color']
    return plot_config


def save_html(plot_html, desc, query_sql, df_sample, display):
    file_path = ".temp/chart.html"
    os.makedirs('.temp', exist_ok=True)
    with open(file_path, "w") as f:
        f.write(plot_html)
    add_content_html(file_path, "查询语句: " + query_sql, 'p')
    add_content_html(file_path, df_sample)
    add_content_html(file_path, desc, 'h2')
    if display:
        filename = 'file:///' + os.getcwd() + '/' + file_path
        webbrowser.open(filename)
    with open(file_path, "r") as f:
        return f.read()


def format_code(code):
    # 拆分成单行，并在每一行前添加">"符号
    lines = code.splitlines()
    lines_with_arrow = ["> " + line for line in lines]

    # 重新组合成一个多行字符串
    result_string = "\n".join(lines_with_arrow)
    return result_string


def add_content_html(file_path, content, tag=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    vega_div = soup.find('div', id='vega-chart')

    if tag is None:
        new_content = BeautifulSoup(content, 'html.parser')
        vega_div.insert_before(new_content)
    else:
        new_tag = soup.new_tag(tag)
        new_tag.string = content
        vega_div.insert_before(new_tag)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))


def parse_first_markdown_code(markdown_text):
    # 检查是否是正确的 Markdown 代码块格式
    markdown_text=markdown_text.strip()
    pattern = r'^```([\w+]*?)\n([\s\S]*?)\n```$'
    if not re.search(pattern, markdown_text, re.MULTILINE):
        return 'unknown', markdown_text  # 如果格式不正确,返回原文本

    code_block = re.search(r'```([\w+]*?)\n([\s\S]*?)\n```', markdown_text, re.MULTILINE)
    if code_block:
        code_type = code_block.group(1) if code_block.group(1) else None
        code_content = code_block.group(2)
        return code_type, code_content

    return None, None


def remove_comments(text):
    # 定义正则表达式模式，匹配 // 和 /* */ 样式的注释
    pattern = r'//.*?$'
    # 使用 re.sub() 函数删除匹配到的注释内容
    text = re.sub(pattern, '', text, flags=re.MULTILINE)
    return text
