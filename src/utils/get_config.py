"""下载更新GitHub上提供的配置"""

from .tool.download import Download
from utils.tool.text_editor import TxtManager
from .tool.update_checker import UpdateChecker

class GetConfig:
    def __init__(self, list_path: str, save_path: str):
        self.file_path = list_path
        self.save_path = save_path
        config = TxtManager(self.file_path)
        self.urls = config.read_clean()
        self.failed_count = 0
        self.updated_count = 0

        self.urls_count = len(self.urls)
        if self.urls_count <= 2:
            print("未找到可拉取的远程配置。")
            return
        else:
            self._load_conf()



    def _load_conf(self)-> None:
        # 更新其他仓库的配置
        print(f"需要拉取配置: {self.urls_count - 2} 条。")
        if self.urls_count == 0:
            return

        sr_save_path = self.save_path + "/sr"
        clash_save_path = self.save_path + "/clash"

        checker = UpdateChecker()
        flag = 0
        success_count = 0
        failed_urls = []

        for url in self.urls:
            if url.startswith("\""):
                flag = flag + 1
                continue

            try:
                if flag == 1:
                    dl = Download(url, sr_save_path, checker=checker)
                    if dl.updated:
                        self.updated_count += 1
                    success_count += 1
                elif flag == 2:
                    dl = Download(url, clash_save_path, checker=checker)
                    if dl.updated:
                        self.updated_count += 1
                    success_count += 1
            except Exception as e:
                self.failed_count += 1
                failed_urls.append((url, str(e)))

        # 打印统计结果
        unchanged_count = success_count - self.updated_count
        print(f"\n拉取配置完成 - 成功: {success_count} (更新: {self.updated_count}, 未变更: {unchanged_count}), 失败: {self.failed_count}")
        # if failed_urls:
        #     print("失败的URL:")
        #     for url, error in failed_urls:
        #         print(f"  - {url}: {error}")

    def get_failed_count(self) -> int:
        return self.failed_count

    def get_updated_count(self) -> int:
        return self.updated_count

    def get_urls_count(self) -> int:
        return self.urls_count

if __name__ == "__main__":
    GetConfig("../cache/remote_conf.txt", "../../remote_config")
