import os
from pathlib import Path

def scan_folders(folders: list[str]) -> list[str]:
    """
    扫描多个目录下的所有文件并返回所有文件路径列表
    :param folders: 目录列表
    :return: 文件路径列表
    """
    file_links = []
    for folder in folders:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    # 将文件路径转换为字符串并传入函数
                    file_link = str(Path(file_path))
                    file_links.append(file_link)
    return file_links


def scan_folder(directory: str)-> list[str]:
    """
    扫描单个目录下的所有文件并返回文件路径列表
    :param directory: 目录路径
    :return: 文件路径列表
    """
    file_links = []
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                # 将文件路径转换为字符串并传入函数
                file_link = str(Path(file_path))
                file_links.append(file_link)
    return file_links
