from utils.get_config import GetConfig
from utils.data_manager import CacheManager, UserLibManager
from utils.tool.text_editor import TxtManager
from utils.tool.scan_file import scan_folder
from utils.config_proc import SRProcessor
from utils.builder import SRConfigBuilder, ClashConfigBuilder
"""
主程序入口，负责整体流程控制
运行地址为项目根目录
"""


if __name__ == '__main__':
    ## 0. 定义部分特殊参数 ##
    use_rule_set = True  # 是否使用规则集的标志

    ## 1. 更新拉取仓库提供的配置 ##
    remote_config = GetConfig("./src/custom/remote_config.txt", "./remote_config")
    get_failed = remote_config.get_failed_count()
    if remote_config.get_urls_count() == 0:
        print("未找到可拉取的远程配置。")
        use_rule_set = False
    else:
        # 1.0 检查拉取结果
        # 有失败则提示用户选择
        if get_failed > 0:
            print(f"注意: 拉取远程配置时有 {get_failed} 条失败，请检查网络或URL的有效性。")


    ## 2. 解析拉取到的配置使用的规则与规则集 ##
    while use_rule_set:
        print("解析远程配置文件，生成规则库...")
        sr_folders = "./remote_config/sr"
        # clash_folders = "../remote_config/clash"
        # 遍历目录并收集文件链接
        sr_conf_paths = scan_folder(sr_folders)
        # clash_conf_paths = scan_folder(clash_folders)
        # if len(sr_conf_paths + clash_conf_paths) == 0:
        if len(sr_conf_paths) == 0:
            print("未找到可用的远程配置文件，跳过该步骤。")
            break
        rule_sets = [] # 存储所有规则集
        rules = [] # 存储所有规则
        # 2.1 收集SR配置文件中的规则与规则集
        for conf_file_path in sr_conf_paths:
            rule_sets.extend(SRProcessor(conf_file_path).get_rule_set())
            rules.extend(SRProcessor(conf_file_path).get_rule())
        # 2.2 收集Clash配置文件中的规则与规则集
        # for conf_file_path in clash_conf_paths:
        #     rule_sets.extend(CLProcessor(conf_file_path).get_rule_set())
        #     # rules.extend(SRProcessor(conf_file_path).get_rules())
        # 2.3 写入规则库文件
        lib_manager = CacheManager("./src/cache")
        lib_manager.write(rules, rule_sets)
        print("规则库生成完成。")
        break


    ## 3. 检查并更新模板配置文件 ##
    while True:
        sr_template_processor = SRProcessor("./remote_config/sr/lazy.conf")
        sr_updated = sr_template_processor.get_template()
        # cl_template_processor = CLProcessor("../remote_config/clash/")
        # cl_updated = cl_template_processor.update_template()
        if not sr_updated:  # and not cl_updated:
            print("获取最新模板失败。")
            break
        sr_template = TxtManager("./src/lib/sr_template.conf")
        sr_template.reset("ShadowRocket 配置文件模板")
        sr_template.append(sr_updated)
        # 目前没有合适作为clash模板的配置文件，使用的是AI生成的模板
        # clash_template = TxtManager("./src/lib/verge_template.yaml")
        # clash_template.reset("Clash 配置文件模板")
        # clash_template.append(cl_updated)
        print("模板配置文件更新完成。")
        break

    ## 4. 构建配置 ##
    sr_builder = SRConfigBuilder()
    sr_builder.build()

    verge_builder = ClashConfigBuilder()
    verge_builder.build()
