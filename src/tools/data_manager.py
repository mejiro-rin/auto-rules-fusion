"""管理规则库列表文件的读写操作"""

from pathlib import Path
from utils.text_editor import TxtManager
from utils.check import ensure_file
from utils.path_manager import PathManager


class CacheManager:
    """
    规则库文件管理器
    负责规则库文件的读写操作
    """
    def __init__(self, lib_path: str = PathManager.cache_dir()):
        self.lib_path = lib_path
        self.proxy_file_path = lib_path + "/proxy.txt"
        self.direct_file_path = lib_path + "/direct.txt"
        self.reject_file_path = lib_path + "/reject.txt"

    def write(self, rules: list[str], rule_sets: list[str]) -> None:
        """
        写入规则库文件，覆盖原有内容。
        :param rules: 规则列表
        :param rule_sets: 规则集列表
        :return: None
        """
        # 去重、排序并写入文档
        rules = list(dict.fromkeys(rules))
        rule_sets = list(dict.fromkeys(rule_sets))
        direct = []
        reject = []
        proxy = []
        for rule in rules:
            if rule.endswith(("DIRECT", "Direct")):
                direct.append(rule)
            elif rule.endswith(("REJECT", "Reject")):
                reject.append(rule)
            else:
                proxy.append(rule)
        for rule_set in rule_sets:
            if rule_set.endswith(("DIRECT", "Direct")):
                direct.append(rule_set)
            elif rule_set.endswith(("REJECT", "Reject")):
                reject.append(rule_set)
            else:
                proxy.append(rule_set)

        proxy_file = TxtManager(self.proxy_file_path)
        proxy_file.reset("PROXY 规则库")
        proxy_file.append([rule for rule in proxy])
        direct_file = TxtManager(self.direct_file_path)
        direct_file.reset("DIRECT 规则库")
        direct_file.append([rule for rule in direct])
        reject_file = TxtManager(self.reject_file_path)
        reject_file.reset("REJECT 规则库")
        reject_file.append([rule for rule in reject])


    def read(self)-> dict[str, list[str]]:
        """
        读取规则库文件内容。
        :return: 规则库内容字典
        """
        proxy_file = TxtManager(self.proxy_file_path)
        direct_file = TxtManager(self.direct_file_path)
        reject_file = TxtManager(self.reject_file_path)
        return {
            "PROXY": proxy_file.read_all(),
            "DIRECT": direct_file.read_all(),
            "REJECT": reject_file.read_all()
        }


class UserLibManager:
    """
    自定义规则库文件管理器
    负责自定义规则库文件的读取操作
    """
    def __init__(self, path: str = PathManager.custom_dir()):
        # self.path = path
        # if check_file(self.path + "/manual_proxy.txt"):
        #     self.proxy_file_path = path + "/manual_proxy.txt"
        # if check_file(self.path + "/manual_direct.txt"):
        #     self.direct_file_path = path + "/manual_direct.txt"
        # if check_file(self.path + "/manual_reject.txt"):
        #     self.reject_file_path = path + "/manual_reject.txt"
        base = Path(path).resolve()
        self.path = str(base)

        proxy_path = base / "manual_proxy.txt"
        direct_path = base / "manual_direct.txt"
        reject_path = base / "manual_reject.txt"

        if ensure_file(str(proxy_path)):
            self.proxy_file_path = str(proxy_path)
        if ensure_file(str(direct_path)):
            self.direct_file_path = str(direct_path)
        if ensure_file(str(reject_path)):
            self.reject_file_path = str(reject_path)

    def read(self) -> dict[str, list[str]]:
        """
        读取自定义规则库文件内容。
        :return: 自定义规则库内容字典
        """
        custom_lib = {}
        if hasattr(self, 'proxy_file_path'):
            proxy_file = TxtManager(self.proxy_file_path)
            custom_lib["PROXY"] = proxy_file.read_all()
        if hasattr(self, 'direct_file_path'):
            direct_file = TxtManager(self.direct_file_path)
            custom_lib["DIRECT"] = direct_file.read_all()
        if hasattr(self, 'reject_file_path'):
            reject_file = TxtManager(self.reject_file_path)
            custom_lib["REJECT"] = reject_file.read_all()
        return custom_lib
