from pathlib import Path

def check_folder_file(folder_path: str) -> int:
    """
    检查文件夹中的文件数量
    :param folder_path: 文件夹路径
    :return: 文件数量，如果文件夹不存在返回 -1
    """
    path_obj = Path(folder_path)

    if not path_obj.exists() or not path_obj.is_dir():
        return -1

    return len([f for f in path_obj.iterdir() if f.is_file()])


def ensure_file(file_path: str) -> bool:
    """
    检查文件是否存在
    :param file_path: 文件路径
    :return: 如果文件存在返回 True，否则返回 False
    """
    path_obj = Path(file_path)
    return path_obj.exists() and path_obj.is_file()


def ensure_directory_exists(file_path: str) -> bool:
    """
    检查文件所在的目录是否存在，不存在则创建。
    :param file_path: 文件的完整路径或相对路径
    :return: 成功返回 True，失败返回 False
    """
    try:
        path = Path(file_path)
        # 提取父目录
        parent_dir = path.parent

        # parents=True: 递归创建不存在的父目录 (类似 mkdir -p)
        # exist_ok=True: 如果目录已存在，不抛出异常
        parent_dir.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False

def no_chinese(string: str)-> bool:
    """
    使用Unicode检查字符串中是否包含中文字符
    :param string: 输入字符串
    :return: 如果不包含中文字符返回 True，否则返回 False
    """
    for char in string:
        # 中文字符的Unicode范围：\u4e00-\u9fff
        if '\u4e00' <= char <= '\u9fff':
            return False
    return True

def bring_policy_rule (line: str) -> bool:
    """
    检查一行文本是否为带有策略的规则或规则集
    规则或规则集以 "DIRECT"、"PROXY" 或 "REJECT" 结尾（区分大小写）
    :param line: 输入行文本
    :return: 如果带策略返回 True，否则返回 False
    """
    return line.rstrip().endswith(("DIRECT", "PROXY", "REJECT", "Direct", "Proxy", "Reject")) and not line.startswith(("GEOIP", "FINAL"))


if __name__ == "__main__":
    # 检查文件夹
    count = check_folder_file(PathManager.remote_sr_dir())
    print(f"文件数量: {count}")

    # 检查文件
    exists = ensure_file("check.py")
    print(f"文件存在: {exists}")
from utils.path_manager import PathManager
