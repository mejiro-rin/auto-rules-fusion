"""缓存读写器"""
from datetime import datetime
from typing import List

from utils.tool.check import check_file

class CacheManager:
    def __init__(self, cache_path: str):
        self.path = cache_path

    def reset(self):
        """
        初始化缓存文件：
        1. 强制覆盖原有内容
        2. 写入二进制时间标签
        """
        rewrite_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"# 更新日期: {rewrite_time}\n\n".encode('utf-8')

        with open(self.path, "wb") as f:
            f.write(header)

    def append_result(self, url, content):
        """
        追加写入抓取结果：
        1. 使用 'ab' 模式 (Append Binary) 保证不覆盖前序内容
        2. 处理抓取失败的占位逻辑
        """

        if content:
            entry = f"# Source: {url}\n{content}\n\n"
        else:
            entry = f"# URL: {url}\n# 抓取失败\n\n"

        with open(self.path, "ab") as f:
            f.write(entry.encode('utf-8'))

    def read_cache(self) -> List[str] | None:
        """
        读取无后缀二进制缓存并转换为字符串列表
        """
        # 1. 健壮性检查：如果文件不存在，直接返回空
        if not check_file(self.path):
            return None

        try:
            # 2. 以二进制只读模式 ('rb') 打开
            with open(self.path, 'rb') as f:
                raw_data = f.read()

            # 3. 将字节流解码回 UTF-8 字符串并按行分割
            content = raw_data.decode('utf-8')
            lines = content.splitlines()

            # 4. 返回行列表
            return lines

        except (IOError, UnicodeDecodeError) as e:
            # 处理可能的 IO 错误或编码异常（例如文件被手动损坏）
            print(f"读取缓存文件出错: {e}")
            return None