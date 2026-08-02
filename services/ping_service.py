"""
Ping 探测业务（services/ping_service.py）

负责探测主机是否可达，并更新 host.status 在线状态。
"""
import logging
import subprocess

from constants.status import OFFLINE, ONLINE

logger = logging.getLogger("app")


class PingService:
    @staticmethod
    def ping_host(host) -> bool:
        """
        探测单台主机是否 ping 可达，并更新状态。
        返回 True 表示在线，False 表示离线。
        """
        # 跨平台：Windows 用 -n，Linux/Mac 用 -c
        import platform

        system = platform.system().lower()
        if system == "windows":
            cmd = ["ping", "-n", "1", "-w", "3000", host.ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "3", host.ip]

        try:
            result = subprocess.run(
                cmd, capture_output=True, timeout=5, text=True
            )
            online = result.returncode == 0
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, Exception):  # noqa: BLE001
            online = False

        host.status = ONLINE if online else OFFLINE
        host.save(update_fields=["status"])
        logger.info(f"Ping 探测 {host.hostname} ({host.ip}) -> {'在线' if online else '离线'}")
        return online

    @staticmethod
    def ping_batch(hosts) -> list:
        """批量探测多台主机，返回每台的探测结果"""
        results = []
        for host in hosts:
            online = PingService.ping_host(host)
            results.append(
                {
                    "id": host.id,
                    "hostname": host.hostname,
                    "ip": host.ip,
                    "status": ONLINE if online else OFFLINE,
                }
            )
        return results
