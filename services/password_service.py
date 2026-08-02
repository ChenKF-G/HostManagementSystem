"""
密码轮换业务（services/password_service.py）

负责 root 密码的：
- 加密存储（追加历史记录 + 标记当前有效）
- 定时轮换（每 8 小时，SSH 修改主机密码）
- 当前密码解密（用于 SSH 操作）
- 密码历史查询
"""
import logging
import secrets
import string
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.host.models import Host, HostPasswordHistory
from utils import encrypt

logger = logging.getLogger("app")

# 密码有效期（8 小时，与轮换周期一致）
PASSWORD_VALID_HOURS = 8
# 密码轮换间隔（秒）
ROTATE_INTERVAL_SECONDS = 8 * 60 * 60


def _generate_strong_password(length=20) -> str:
    """生成强随机密码（大小写字母 + 数字 + 特殊字符）"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*_-+=?"
    while True:
        pwd = "".join(secrets.choice(alphabet) for _ in range(length))
        if (
            any(c.islower() for c in pwd)
            and any(c.isupper() for c in pwd)
            and any(c.isdigit() for c in pwd)
            and any(c in "!@#$%^&*_-+=?" for c in pwd)
        ):
            return pwd


class PasswordService:
    @staticmethod
    def store_password(host, plain_password: str) -> HostPasswordHistory:
        """加密并存储一个密码，标记为当前有效，同时使旧密码失效"""
        with transaction.atomic():
            # 使当前所有有效密码失效
            HostPasswordHistory.objects.filter(host=host, is_active=1).update(is_active=0)

            now = timezone.now()
            encrypted = encrypt.encrypt_password(plain_password)
            return HostPasswordHistory.objects.create(
                host=host,
                encrypted_password=encrypted,
                is_active=1,
                valid_from=now,
                expire_at=now + timedelta(hours=PASSWORD_VALID_HOURS),
            )

    @staticmethod
    def decrypt_current_password(host) -> str:
        """解密主机当前有效的 root 密码，用于 SSH 操作"""
        record = (
            HostPasswordHistory.objects.filter(host=host, is_active=1)
            .order_by("-valid_from")
            .first()
        )
        if not record:
            raise ValueError(f"主机 {host.hostname} 没有有效密码")
        return encrypt.decrypt_password(record.encrypted_password)

    @staticmethod
    def rotate_password(host) -> bool:
        """
        对单台主机执行密码轮换：
        1. 生成新随机密码；
        2. 通过 Paramiko SSH 连接并修改 root 密码；
        3. 加密后追加到历史表并标记为当前有效。
        SSH 失败则保留旧密码（可回滚）。
        """
        old_password = None
        try:
            old_password = PasswordService.decrypt_current_password(host)
        except ValueError:
            old_password = None

        new_password = _generate_strong_password()

        # 通过 Paramiko SSH 修改远程主机 root 密码
        changed = PasswordService._ssh_change_password(host, old_password, new_password)
        if not changed:
            logger.warning(f"主机 {host.hostname} SSH 改密失败，保留旧密码")
            return False

        # SSH 成功，落库新密码
        PasswordService.store_password(host, new_password)
        logger.info(f"主机 {host.hostname} root 密码轮换成功")
        return True

    @staticmethod
    def rotate_all() -> dict:
        """轮换所有主机 root 密码，返回成功/失败统计"""
        success, failed = 0, 0
        for host in Host.objects.all():
            try:
                if PasswordService.rotate_password(host):
                    success += 1
                else:
                    failed += 1
            except Exception as e:  # noqa: BLE001
                logger.error(f"主机 {host.hostname} 密码轮换异常: {e}")
                failed += 1
        logger.info(f"密码轮换完成：成功 {success}，失败 {failed}")
        return {"success": success, "failed": failed}

    @staticmethod
    def get_history(host, masked=True) -> list:
        """获取主机密码历史（默认脱敏展示）"""
        records = HostPasswordHistory.objects.filter(host=host).order_by("-valid_from")
        result = []
        for r in records:
            # 脱敏：只展示加密串摘要，不展示明文
            raw = r.encrypted_password
            masked_str = f"{raw[:20]}...{raw[-10:]}" if masked and raw else ""
            result.append(
                {
                    "id": r.id,
                    "masked_encrypted": masked_str,
                    "is_active": r.is_active,
                    "valid_from": r.valid_from,
                    "expire_at": r.expire_at,
                }
            )
        return result

    @staticmethod
    def _ssh_change_password(host, old_password, new_password) -> bool:
        """
        通过 Paramiko SSH 修改主机 root 密码。
        host 未配置有效密码或连接失败时返回 False。
        """
        import paramiko

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=host.ip,
                port=host.port,
                username="root",
                password=old_password,
                timeout=10,
            )
            # 修改 root 密码（两种常见写法，按系统类型选择）
            command = f"echo 'root:{new_password}' | chpasswd"
            stdin, stdout, stderr = client.exec_command(command, timeout=10)
            exit_code = stdout.channel.recv_exit_status()
            client.close()
            return exit_code == 0
        except Exception as e:  # noqa: BLE001
            logger.error(f"SSH 连接/改密失败 {host.ip}:{host.port} -> {e}")
            return False
