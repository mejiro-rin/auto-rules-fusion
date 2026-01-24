"""
用于读写文本文件
"""

from datetime import datetime
from utils.tool.check import ensure_directory_exists
class TxtManager:
    """
    文本文件管理器
    负责文本文件的读写操作
    """
    def __init__(self, file_path: str):
        """
        初始化文本文件管理器
        :param file_path: 文件路径
        """
        if not ensure_directory_exists(file_path):
            # 如果无法创建目录，后续操作都会失败，所以直接抛出异常
            raise IOError(f"初始化失败：无法创建或访问目录 {file_path}")

        self.file_path = file_path

    def reset(self, title: str) -> None:
        """
        重置文本文件，写入更新时间头部与标题
        :param title:
        :return: None
        """
        rewrite_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"# 更新日期: {rewrite_time}\n\n"
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("# " + title + "\n")
            f.write(header)

    def append(self, content: list[str] | str)-> None:
        """
        追加写入文本文件
        :param content: 文本内容
        :return: None
        """
        with open(self.file_path, "a", encoding="utf-8") as f:
            if isinstance(content, str):
                f.write(content + "\n")
            elif isinstance(content, list):
                for line in content:
                    if line == "\n":
                        f.write("\n")
                    else:
                        f.write(line + "\n")

    def write(self, content: list[str])-> None:
        """
        写入文本文件内容
        :param content: 文本内容列表
        :return: None
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            self.reset("请输入文本")
            for line in content:
                f.write(line + "\n")

    def read_clean(self)-> list[str]:
        """
        读取文本文件，忽略空行和以 '#' 开头的备注行，返回纯文本。
        :return: 纯文本文件内容
        """
        text = []

        with open(self.file_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()  # 去除行首尾空白字符
                if not line or line.startswith("#"):
                    continue
                text.append(line)
        return text

    def read_blank(self)-> list[str]:
        """
        读取文本文件，忽略备注行，返回包含空间隔行与内容的列表。
        :return: 文件内容，包括空行
        """
        text = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()  # 去除行首尾空白字符
                if not line or line.startswith("#"):
                    continue
                text.append(line)
        return text

    def read_all(self) -> list[str]:
        """
        读取文本文件内容，包括空行和备注行）。
        :return: 全部文本文件内容
        """
        text = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                text.append(raw)
        return text