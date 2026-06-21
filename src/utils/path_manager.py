"""项目路径管理器，统一管理所有关键路径"""

from pathlib import Path


class PathManager:
    """路径管理器，集中定义项目中使用的所有关键路径"""

    # 项目根目录（基于当前工作目录，等同于运行时的 ./）
    _root: Path = Path(".").resolve()

    @classmethod
    def root(cls) -> str:
        return str(cls._root)

    # ── custom 目录 ────────────────────────────
    @classmethod
    def custom_dir(cls) -> str:
        """自定义规则和远程配置列表存放目录"""
        return str(cls._root / "custom")

    @classmethod
    def remote_config_list(cls) -> str:
        """远程配置 URL 列表文件"""
        return str(cls._root / "custom" / "remote_config.txt")

    @classmethod
    def manual_proxy(cls) -> str:
        return str(cls._root / "custom" / "manual_proxy.txt")

    @classmethod
    def manual_direct(cls) -> str:
        return str(cls._root / "custom" / "manual_direct.txt")

    @classmethod
    def manual_reject(cls) -> str:
        return str(cls._root / "custom" / "manual_reject.txt")

    # ── lib 目录 ───────────────────────────────
    @classmethod
    def lib_dir(cls) -> str:
        return str(cls._root / "lib")

    @classmethod
    def sr_template(cls) -> str:
        """SR 配置模板（由步骤 3 生成）"""
        return str(cls._root / "lib" / "sr_template.conf")

    @classmethod
    def verge_template(cls) -> str:
        """Clash/Verge 配置模板"""
        return str(cls._root / "lib" / "verge_template.yaml")

    # ── cache 目录 ─────────────────────────────
    @classmethod
    def cache_dir(cls) -> str:
        return str(cls._root / "cache")

    @classmethod
    def cache_file(cls, policy: str) -> str:
        """按策略名获取缓存规则库文件路径"""
        return str(cls._root / "cache" / f"{policy.lower()}.txt")

    @classmethod
    def cache_proxy(cls) -> str:
        return cls.cache_file("proxy")

    @classmethod
    def cache_direct(cls) -> str:
        return cls.cache_file("direct")

    @classmethod
    def cache_reject(cls) -> str:
        return cls.cache_file("reject")

    # ── dist 目录 ──────────────────────────────
    @classmethod
    def dist_dir(cls) -> str:
        return str(cls._root / "dist")

    @classmethod
    def sr_output(cls) -> str:
        return str(cls._root / "dist" / "sr_config.conf")

    @classmethod
    def clash_output(cls) -> str:
        return str(cls._root / "dist" / "clash_config.yaml")

    # ── remote_config 目录 ─────────────────────
    @classmethod
    def remote_config_dir(cls) -> str:
        """下载的远程配置根目录"""
        return str(cls._root / "remote_config")

    @classmethod
    def remote_sr_dir(cls) -> str:
        return str(cls._root / "remote_config" / "sr")

    @classmethod
    def remote_clash_dir(cls) -> str:
        return str(cls._root / "remote_config" / "clash")

    @classmethod
    def remote_sr_file(cls, name: str = "lazy.conf") -> str:
        return str(cls._root / "remote_config" / "sr" / name)
