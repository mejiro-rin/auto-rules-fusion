"""
从指定 URL 下载文件并以原名保存到指定目录。
"""

import requests
import os

class Download:
    def __init__(self, target_url, save_path):
        self.target_url = target_url
        self.save_path = save_path
        self._download()

    def _download(self):

        try:
            # 1. 自动从 URL 中提取文件名
            file_name = self.target_url.split('/')[-1]

            # 2. 拼接完整的保存路径
            # 如果 save_path 是文件夹，则在该文件夹下创建同名文件
            if os.path.isdir(self.save_path) or not os.path.splitext(self.save_path)[1]:
                os.makedirs(self.save_path, exist_ok=True)
                final_dest = os.path.join(self.save_path, file_name)
            else:
                # 如果 save_path 包含文件名，则直接使用
                os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
                final_dest = self.save_path

            # 3. 执行下载 (使用 stream=True 避免大文件占用内存)
            print(f"正在下载: {file_name} -> {final_dest}")
            with requests.get(self.target_url, stream=True, timeout=15) as r:
                r.raise_for_status()
                # 以二进制写模式 ('wb') 打开，不涉及编码问题，直接搬运数据
                with open(final_dest, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            print("下载完成。")

        except Exception as e:
            print(f"URL: {self.target_url}, 错误: {e}")
            print(f"下载过程中出错: {e}")