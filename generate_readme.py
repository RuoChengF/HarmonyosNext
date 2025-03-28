import os
import re

def extract_number(filename):
    # 从文件名中提取数字
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

def get_first_h1_title(file_path):
    # 读取md文件并提取第一个一级标题
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 匹配以#开头的一级标题
            match = re.search(r'^\s*#\s+(.+)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    return None

def process_directory(dir_path, base_path, indent_level=0):
    # 获取目录下的所有文件和文件夹
    items = os.listdir(dir_path)

    # 分离文件和目录
    md_files = [f for f in items if f.endswith('.md')]
    directories = [d for d in items if os.path.isdir(os.path.join(dir_path, d))]

    # 按文件名中的数字排序
    md_files.sort(key=extract_number)
    directories.sort()

    content = ''

    # 处理当前目录下的md文件
    for file in md_files:
        file_path = os.path.join(dir_path, file)
        # 尝试获取文件中的第一个一级标题
        title = get_first_h1_title(file_path)
        if not title:
            # 如果没有找到一级标题，使用文件名（去掉.md后缀）
            title = os.path.splitext(file)[0]
        # 计算相对路径
        rel_path = os.path.relpath(file_path, base_path)
        # 对文件名进行URL编码，将空格转换为%20
        encoded_path = rel_path.replace(' ', '%20')
        # 添加缩进
        content += '  ' * indent_level + f'- [{title}](/{encoded_path})\n'

    # 递归处理子目录
    for directory in directories:
        dir_title = directory
        content += '  ' * indent_level + f'- **{dir_title}**\n'
        # 递归处理子目录
        sub_dir_path = os.path.join(dir_path, directory)
        content += process_directory(sub_dir_path, base_path, indent_level + 1)

    return content

def generate_readme():
    # 获取blogs目录的路径
    blogs_dir = os.path.join(os.path.dirname(__file__), 'blogs')
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')

    # 生成README内容
    content = '# HarmonyOS NEXT 系列教程\n\n'
    content += '本仓库包含了HarmonyOS NEXT相关的系列教程文章，涵盖了组件开发、性能优化、最佳实践等多个方面。\n\n'
    content += '## 文章目录\n\n'

    # 递归处理blogs目录
    content += process_directory(blogs_dir, os.path.dirname(blogs_dir))

    # 写入README.md
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    generate_readme()