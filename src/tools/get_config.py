"""下载更新GitHub上提供的配置"""

from utils import Download
from utils.text_editor import TxtManager
from utils.path_manager import PathManager

class GetConfig:
    def __init__(self, list_path: str, save_dir: str):
        self.list_file_path = list_path
        self.save_dir_path = save_dir

        # 获取需要下载的链接（未注释）
        config = TxtManager(self.list_file_path)
        self.urls = config.read_clean()
        self.failed_count = 0

        self.urls_count = len(self.urls)
        if self.urls_count <= 2:
            print("未找到可拉取的远程配置。")
            return
        else:
            self._load_conf()



    def _load_conf(self)-> None:
        # 更新其他仓库的配置
        print(f"需要下载远程文件: {self.urls_count - 2} 条。")
        if self.urls_count == 0:
            return

        sr_save_path = self.save_dir_path + "/sr"
        clash_save_path = self.save_dir_path + "/clash"

        flag = 0
        success_count = 0
        failed_urls = []

        for url in self.urls:
            if url.startswith("\""):
                flag = flag + 1
                continue

            try:
                if flag == 1:
                    Download(url, sr_save_path)
                elif flag == 2:
                    Download(url, clash_save_path)
                success_count += 1
            except Exception as e:
                self.failed_count += 1
                failed_urls.append((url, str(e)))

        # 打印统计结果
        print(f"\n拉取配置完成 - 成功: {success_count}, 失败: {self.failed_count}")
        # if failed_urls:
        #     print("失败的URL:")
        #     for url, error in failed_urls:
        #         print(f"  - {url}: {error}")

    def get_failed_count(self) -> int:
        return self.failed_count
    def get_urls_count(self) -> int:
        return self.urls_count

if __name__ == "__main__":
    GetConfig(PathManager.remote_config_list(), PathManager.remote_config_dir())
