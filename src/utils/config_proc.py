"""
解析配置文件
"""
from .storage.text_editor import TxtManager
from .tool.check import bring_policy_rule
from .tool.check import check_file

class SRProcessor:
    """
    处理SR格式配置文件的类，提供解析规则集和General部分内容的方法。
    """
    def __init__(self, conf_path: str):
        """
        初始化配置处理器，读取并存储配置文件内容。
        :param conf_path: 要解析的配置文件路径
        """
        # 记录单个配置具体路径
        if check_file(conf_path):
            self.conf_path = conf_path
        else :
            raise FileNotFoundError(f"配置文件未找到: {conf_path}")

        # configure = TxtManager(self.conf_path)
        # self.content = configure.read_clean("")

    def get_rule(self)-> list[str] | None:
        """
        解析配置文件内容，提取规则列表。
        :return: list[str]
        """
        if not hasattr(self, 'conf_path'):
            print("配置文件路径未定义，无法解析规则。")
            return None
        configure = TxtManager(self.conf_path)
        content = configure.read_clean()
        rules = []
        in_rule = False
        for line in content:
            if line.startswith("[Rule]"):
                in_rule = True
                continue
            if in_rule:
                if line.startswith("[") :
                    break
                if bring_policy_rule(line) and not line.startswith("RULE-SET"):
                    rules.append(line)
        return rules

    def get_rule_set(self) -> list[str] | None:
        """
        解析配置文件内容，提取规则集列表。
        :return: list[str]
        """
        if not hasattr(self, 'conf_path'):
            print("配置文件路径未定义，无法解析规则集。")
            return None
        configure = TxtManager(self.conf_path)
        content = configure.read_clean()
        rule_sets = []
        in_rule_set = False
        for line in content:
            if line.startswith("[Rule]"):
                in_rule_set = True
                # rule_sets.append(line)
                continue
            if in_rule_set:
                if line.startswith("[") :
                    break
                if bring_policy_rule(line) and line.startswith("RULE-SET"):
                    rule_sets.append(line)
        return rule_sets

    def get_general(self)-> list[str] | None:
        """
        解析配置文件内容，提取General部分内容。
        :return: list[str]
        """
        if not hasattr(self, 'conf_path'):
            print("配置文件路径未定义，无法解析General部分。")
            return None
        config = TxtManager(self.conf_path)
        content = config.read_all()
        general = []
        in_general = False
        for line in content:
            if line.startswith("[General]"):
                in_general = True
                # general.append(line)
                continue
            if in_general:
                if line.startswith("["):
                    break
                general.append(line)
        return general


    def get_template(self) -> list[str] | None:
        """
        解析配置文件内容，提取模板内容。
        :return: lib[str]
        """
        if not hasattr(self, 'conf_path'):
            print("配置文件路径未定义，无法解析模板内容。")
            return None
        config = TxtManager(self.conf_path)
        content = config.read_clean()
        template = []
        in_template = True
        for line in content:
            # 跳过规则和代理组部分
            if line.startswith("[Rule]") or line.startswith("[Proxy Group]"):
                in_template = False
                template.append(line)
                if line.startswith("[Proxy Group]"):
                    template.append("# 目前不支持划分代理组，若有需求手动修改或添加")
                elif line.startswith("[Rule]"):
                    template.append("# 规则部分")
                continue
            if line.startswith("GEOIP"):
                in_template = True
                template.append(line)
                continue
            if in_template:
                template.append(line)

        return template


if __name__ == "__main__":
    sr_conf = SRProcessor("../../remote_config/sr/lazy_group.conf")
    _rules = sr_conf.get_rule_set()
    for rule in _rules:
        print(rule)