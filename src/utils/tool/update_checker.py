"""
通过 HTTP 条件请求（ETag / Last-Modified）检查远程配置文件是否有更新。
将每个 URL 对应的响应头元数据持久化到本地缓存文件中，供下次请求使用。
"""

import json
import os
from pathlib import Path


class UpdateChecker:
    """
    使用 HTTP 条件请求检查远程文件是否有更新。
    将 ETag 和 Last-Modified 信息持久化保存到本地 JSON 文件。
    """

    def __init__(self, cache_path: str = "./src/cache/http_meta.json"):
        self.cache_path = cache_path
        self._meta = self._load()

    def _load(self) -> dict:
        """从缓存文件加载已保存的元数据。"""
        try:
            if os.path.exists(self.cache_path):
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save(self) -> None:
        """将元数据保存到缓存文件。"""
        Path(self.cache_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self._meta, f, ensure_ascii=False, indent=2)

    def get_request_headers(self, url: str) -> dict:
        """
        获取条件请求头（If-None-Match / If-Modified-Since）。
        :param url: 目标 URL
        :return: 请求头字典
        """
        headers = {}
        meta = self._meta.get(url, {})
        if meta.get("etag"):
            headers["If-None-Match"] = meta["etag"]
        if meta.get("last_modified"):
            headers["If-Modified-Since"] = meta["last_modified"]
        return headers

    def update_meta(self, url: str, etag: str = None, last_modified: str = None) -> None:
        """
        更新指定 URL 的元数据并保存到缓存文件。
        只保存服务器实际返回的非空值。
        :param url: 目标 URL
        :param etag: ETag 响应头的值
        :param last_modified: Last-Modified 响应头的值
        """
        entry = {}
        if etag is not None:
            entry["etag"] = etag
        if last_modified is not None:
            entry["last_modified"] = last_modified
        self._meta[url] = entry
        self._save()

    def has_meta(self, url: str) -> bool:
        """检查是否有该 URL 的缓存元数据。"""
        return url in self._meta
