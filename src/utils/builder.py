"""
配置文件生成器，用于生成配置文件
"""

import re
from .tool.check import check_file
from .lib_manager import LibManager, CustomLibManager
from .storage.text_editor import TxtManager

def _check_template(template: str) -> bool:
    """
    检查资源文件是否存在。
    :param template: 模板文件路径
    :return: 是否存在
    """
    lib_path = "./lib"
    return check_file(lib_path + template)


def parse_raw_text_to_metadata(text: str):
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





class SRConfigBuilder:
    def __init__(self, save_path: str = "..\\dist\\SR_config.txt"):
        """
        初始化配置生成器，设置模板文件路径。
        :param save_path: 生成配置文件的保存路径
        """
        self.save_path = save_path
        self.template_name = "\\sr_template.conf"

        if not _check_template(self.template_name):
            raise FileNotFoundError("模板文件 sr_template.conf 未找到。")

    def build(self, rules_lib: LibManager, custom_lib: CustomLibManager) -> None:
        """
        生成配置文件。
        :param rules_lib: 规则库管理器
        :param custom_lib: 自定义规则库管理器
        :return: None
        """
        # 读取模板
        template_path = ".\\lib" + self.template_name
        template_file = TxtManager(template_path)
        template_content = template_file.read_clean()
        # 生成最终规则列表
        final_rules = self._final_rules(rules_lib, custom_lib)

        # 插入规则到模板
        final_content = []
        for line in template_content:
            line = line.strip()
            if line.startswith("[Rule]"):
                final_content.append(line)
                final_content.extend(final_rules)
                continue
            if len(line) > 1 and line[0] == "[":
                final_content.append("\n")
            if line.startswith("[Proxy Group]"):
                final_content.append(line)
                final_content.append("# 目前不支持划分代理组，若有需求手动修改或添加\n")
                continue
            final_content.append(line)

        # 保存生成的配置文件
        output_file = TxtManager(self.save_path)
        output_file.reset("生成的SR配置文件")
        output_file.append(final_content)

    def _final_rules(self, rules_lib: LibManager, custom_lib: CustomLibManager) -> list[str]:
        """
        生成配置文件。
        :param rules_lib: 规则库管理器
        :param custom_lib: 自定义规则库管理器
        :return: 最终规则列表
        """

        # 读取规则库内容
        rules_dict = rules_lib.read()
        custom_raw_dict = custom_lib.read()

        #将用户自定义列表规则化
        custom_formatted_dict = {}
        for policy, lines in custom_raw_dict.items():
            formatted_lines = []
            for line in lines:
                # 调用通用解析函数
                rtype, content, is_comment = parse_raw_text_to_metadata(line)

                if is_comment:
                    # 如果是注释或空行，直接保留
                    formatted_lines.append(content)
                else:
                    # Shadowrocket 特有的格式化逻辑
                    # IP 类型增加 no-resolve 提升性能
                    suffix = ",no-resolve" if rtype == "IP-CIDR" else ""
                    final_line = f"{rtype},{content},{policy.upper()}{suffix}"
                    formatted_lines.append(final_line)

            custom_formatted_dict[policy] = formatted_lines


        # 插入规则到模板
        # 优先级为: 自定义 > 拒绝 > 代理 > 直连
        final_rules = []
        final_rules.extend(custom_formatted_dict.get("REJECT", []))
        final_rules.extend("\n\n")
        final_rules.extend(custom_formatted_dict.get("PROXY", []))
        final_rules.extend("\n\n")
        final_rules.extend(custom_formatted_dict.get("DIRECT", []))
        final_rules.extend("\n\n")
        final_rules.extend(rules_dict.get("REJECT", []))
        final_rules.extend("\n\n")
        final_rules.extend(rules_dict.get("PROXY", []))
        final_rules.extend("\n\n")
        final_rules.extend(rules_dict.get("DIRECT", []))
        return final_rules