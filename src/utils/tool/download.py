"""
从指定 URL 下载文件并以原名保存到指定目录。
支持通过 UpdateChecker 发送条件请求，检测文件是否有更新。
"""

import requests
import os

class Download:
    def __init__(self, target_url, save_path, checker=None):
        """
        :param target_url: 要下载的文件 URL
        :param save_path: 保存目录或完整文件路径
        :param checker: UpdateChecker 实例，用于条件请求；为 None 时直接下载
        """
        self.target_url = target_url
        self.save_path = save_path
        self.checker = checker
        self.updated = False  # 文件是否实际被下载/更新
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

            # 3. 构建条件请求头（若有 checker 则附加 If-None-Match / If-Modified-Since）
            headers = {}
            if self.checker:
                headers = self.checker.get_request_headers(self.target_url)

            # 4. 执行下载 (使用 stream=True 避免大文件占用内存)
            print(f"正在检查更新: {file_name}")
            with requests.get(self.target_url, stream=True, timeout=15, headers=headers) as r:
                # 304 Not Modified：文件未变更，无需重新下载
                if r.status_code == 304:
                    print(f"未变更，跳过下载: {file_name}")
                    return

                r.raise_for_status()

                print(f"正在下载: {file_name} -> {final_dest}")
                # 以二进制写模式 ('wb') 打开，不涉及编码问题，直接搬运数据
                with open(final_dest, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

                # 5. 更新缓存的 HTTP 元数据
                if self.checker:
                    self.checker.update_meta(
                        self.target_url,
                        etag=r.headers.get("ETag"),
                        last_modified=r.headers.get("Last-Modified"),
                    )

                self.updated = True
                print("下载完成。")

        except Exception as e:
            print(f"URL: {self.target_url}, 错误: {e}")
            print(f"下载过程中出错: {e}")