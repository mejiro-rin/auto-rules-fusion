"""
配置文件生成器，用于生成配置文件
"""

import re
from .tool.check import check_file
from .data_manager import CacheManager, UserLibManager
from utils.tool.text_editor import TxtManager
from abc import ABC, abstractmethod


class ConfigBuilder(ABC):
    def __init__(self, template_path: str, output_filename: str, save_path: str = "./dist"):
        """
        初始化配置生成器，设置模板文件路径。
        :param template_path: 模板文件路径
        :param output_filename: 生成配置文件的文件名
        :param save_path: 生成配置文件的保存路径
        :return: None
        """
        self.template_path = template_path
        self.save_path = save_path
        self.output_file = self.save_path + "/" + output_filename
        # 检查模板文件是否存在
        self._check_template()
        # 收集整理元数据
        self.raw_rules = ConfigBuilder._mate_final_rules()
        self.final_rules = []

    @abstractmethod
    def _final_rules(self):
        pass

    @abstractmethod
    def build(self):
        """
        生成配置文件
        """
        pass

    def _check_template(self):
        """
        检查资源文件是否存在。
        """
        if not check_file(self.template_path):
            raise FileNotFoundError(f"模板文件 {self.template_path} 未找到。")

    @staticmethod
    def _parse_raw_text_to_metadata(text: str):
        """
        通用解析引擎：将原始行解析为元数据
        返回: (type, content, is_comment)
        """
        text = text.strip()
        if not text or text.startswith("#"):
            return None, text, True

        # 如果已经是标准规则 (兼容用户直接写规则)
        if "," in text:
            parts = text.split(',')
            if parts[0].upper() in ["DOMAIN", "DOMAIN-SUFFIX", "IP-CIDR"]:
                return parts[0].upper(), parts[1], False

        # 自动识别逻辑
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(/\d+)?$|^([a-fA-F0-9:]+:+)+[a-fA-F0-9]+'
        if re.match(ip_pattern, text):
            return "IP-CIDR", text, False
        return "DOMAIN-SUFFIX", text, False

    @staticmethod
    def _mate_final_rules(parse_lib: CacheManager = CacheManager(), custom_lib: UserLibManager = UserLibManager()) -> list[str]:
        """
        生成配置文件的最终规则列表。
        :param parse_lib: 规则缓存管理器
        :param custom_lib: 自定义规则库管理器
        :return: 最终规则列表
        """
        # 读取规则库内容
        rules_dict = parse_lib.read()
        custom_raw_dict = custom_lib.read()

        # 将用户自定义列表规则化
        custom_formatted_dict = {}
        for policy, lines in custom_raw_dict.items():
            formatted_lines = []
            for line in lines:
                # 调用通用解析函数
                rtype, content, is_comment = ConfigBuilder._parse_raw_text_to_metadata(line)
                if is_comment:
                    # 如果是注释或空行，直接保留
                    formatted_lines.append(content)
                else:
                    # 默认格式化逻辑
                    suffix = ",no-resolve" if rtype == "IP-CIDR" else ""
                    final_line = f"{rtype},{content},{policy.upper()}{suffix}"
                    formatted_lines.append(final_line)

            custom_formatted_dict[policy] = formatted_lines

        # 插入规则到模板
        # 优先级为: 自定义 > 拒绝 > 代理 > 直连
        final_rules = []
        for policy in ["REJECT", "PROXY", "DIRECT"]:
            lines = custom_formatted_dict.get(policy, [])
            if lines:  # 只在有内容时添加
                final_rules.extend(lines)
                final_rules.append("")

        for policy in ["REJECT", "PROXY", "DIRECT"]:
            lines = rules_dict.get(policy, [])
            if lines:
                final_rules.extend(lines)
                final_rules.append("")
        return final_rules


class SRConfigBuilder(ConfigBuilder):
    def __init__(self, template_path: str = "./src/lib/sr_template.conf", save_path: str = "./dist"):
        """
        初始化配置生成器，设置模板文件路径。
        :param template_path: 模板文件路径
        :param save_path: 生成配置文件的保存路径
        :return: None
        """
        super().__init__(template_path, "sr_config.conf", save_path)


    def build(self) -> None:
        """
        生成配置文件。
        :return: None
        """
        # 读取模板
        template_file = TxtManager(self.template_path)
        template_content = template_file.read_clean()
        # 生成最终规则列表
        self._final_rules()

        # 插入规则到模板
        final_content = []
        for line in template_content:
            line = line.strip()
            if line.startswith("[Rule]"):
                final_content.append(line)
                final_content.extend(self.final_rules)
                continue
            if len(line) > 1 and line[0] == "[":
                final_content.append("\n")
            if line.startswith("[Proxy Group]"):
                final_content.append(line)
                final_content.append("# 目前不支持划分代理组，若有需求手动修改或添加\n")
                continue
            final_content.append(line)

        # 保存生成的配置文件
        output_file = TxtManager(self.output_file)
        output_file.reset("生成的SR配置文件")
        output_file.append(final_content)

    def _final_rules(self):
        self.final_rules = self.raw_rules



class ClashConfigBuilder(ConfigBuilder):
    def __init__(self, output_filename = "clash_config.yaml", template_path: str = "./src/lib/verge_template.yaml", save_path: str = "./dist"):
        """
        初始化配置生成器，设置模板文件路径。
        :param template_path: 模板文件路径
        :param save_path: 生成配置文件的保存路径
        :return: None
        """
        super().__init__(template_path, output_filename, save_path)


    def build(self) -> None:
        """
        生成配置文件。
        :return: None
        """
        # 读取模板
        template_file = TxtManager(self.template_path)
        template_content = template_file.read_tab()

        # 生成最终规则列表
        self._final_rules()

        # 插入规则到模板
        final_content = []
        for line in template_content:
            # line = line.strip()
            if line.startswith("rules:"):
                final_content.append(line)
                final_content.extend(self.final_rules)
                continue
            final_content.append(line)

        # 保存生成的配置文件
        output_file = TxtManager(self.output_file)
        output_file.reset("生成的Verge配置文件")
        output_file.append(final_content)


    # def _final_rules(self):
    #     """
    #     转换为clash格式
    #     :return: 最终规则列表
    #     """
    #
    #     for rule in self.raw_rules:
    #         if rule.startswith("#") or rule == "":
    #             self.final_rules.append("  " + rule)
    #             continue
    #         self.final_rules.append(f"  - {rule}")

    def _final_rules(self):
        """转换为 Clash 格式"""
        self.final_rules = []

        for rule in self.raw_rules:
            stripped = rule.strip()

            if not stripped:  # 空行
                self.final_rules.append("")
                continue

            if stripped.startswith("#"):  # 注释
                self.final_rules.append(f"  {stripped}")
                continue

            # 规则行：统一转大写策略 + 加 2 空格 -
            upper_rule = stripped.upper().replace(',REJECT', ',REJECT').replace(',REJECT', ',REJECT')  # 防大小写混用
            # 更通用写法：找最后一个逗号后的 policy
            if ',' in stripped:
                prefix, policy = stripped.rsplit(',', 1)
                policy = policy.strip().upper()
                upper_rule = f"{prefix},{policy}"
            else:
                upper_rule = stripped

            self.final_rules.append(f"  - {upper_rule}")