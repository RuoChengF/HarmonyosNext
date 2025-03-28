import os
import re
import requests
from pathlib import Path
import hashlib

def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f'下载图片失败: {url}, 错误: {str(e)}')
        return False

def generate_image_name(url):
    # 使用URL的哈希值作为文件名的一部分，确保唯一性
    hash_obj = hashlib.md5(url.encode())
    hash_str = hash_obj.hexdigest()[:8]
    return f'img_{hash_str}.png'

def process_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配Markdown中的图片链接
    pattern = r'!\[([^\]]*)\]\((https?://[^\)]+)\)'

    def replace_image(match):
        alt_text = match.group(1)
        url = match.group(2)

        # 只处理指定域名的图片
        if not url.startswith('https://files.mdnice.com/'):
            return match.group(0)

        # 生成图片文件名
        image_name = generate_image_name(url)
        image_dir = os.path.join(os.path.dirname(file_path), '..', 'images')
        os.makedirs(image_dir, exist_ok=True)

        image_path = os.path.join(image_dir, image_name)
        relative_path = os.path.join('..', 'images', image_name)

        # 如果图片不存在则下载
        if not os.path.exists(image_path):
            if not download_image(url, image_path):
                return match.group(0)

        # 返回更新后的Markdown图片链接
        return f'![{alt_text}]({relative_path})'

    # 替换所有匹配的图片链接
    new_content = re.sub(pattern, replace_image, content)

    # 如果内容有变化，写回文件
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'已处理文件: {file_path}')

def main():
    blogs_dir = '/Users/chengruo/Desktop/mycode/harmonyosBlogs/blogs'

    # 递归遍历所有markdown文件
    for root, dirs, files in os.walk(blogs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_markdown_file(file_path)

if __name__ == '__main__':
    main()
