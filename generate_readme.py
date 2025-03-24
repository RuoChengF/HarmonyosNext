import os
import re

def extract_number(filename):
    # 从文件名中提取数字
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

def generate_readme():
    # 获取blogs目录的路径
    blogs_dir = os.path.join(os.path.dirname(__file__), 'blogs')
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')

    # 获取所有md文件
    md_files = [f for f in os.listdir(blogs_dir) if f.endswith('.md')]

    # 按文件名中的数字排序
    md_files.sort(key=extract_number)

    # 生成README内容
    content = '# HarmonyOS NEXT 系列教程\n\n'
    content += '本仓库包含了HarmonyOS NEXT相关的系列教程文章，涵盖了组件开发、性能优化、最佳实践等多个方面。\n\n'
    content += '## 文章目录\n\n'

    for file in md_files:
        # 去掉.md后缀
        title = os.path.splitext(file)[0]
        # 对文件名进行URL编码，将空格转换为%20
        encoded_file = file.replace(' ', '%20')
        content += f'- [{title}](/blogs/{encoded_file})\n'

    # 写入README.md
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    generate_readme()