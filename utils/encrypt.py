"""
密码加解密工具（utils/encrypt.py）

基于 cryptography 库的 Fernet（AES-128-CBC + HMAC）实现对称加密。
密钥通过环境变量 ENCRYPT_KEY 注入，不入代码仓库。

加密用途：
- root 密码加密后存储到 host_password_history.encrypted_password
- SSH 操作时解密取得明文密码
"""
import os

from cryptography.fernet import Fernet, InvalidToken


def _get_fernet() -> Fernet:
    # 每次调用时动态读取环境变量，避免模块导入时固定、后期变更失效
    key = os.environ.get("ENCRYPT_KEY")
    if not key:
        raise RuntimeError("环境变量 ENCRYPT_KEY 未配置，无法进行加解密")
    return Fernet(key.encode())


def generate_key() -> str:
    """生成一个新的 Fernet 密钥（首次部署时使用）"""
    return Fernet.generate_key().decode()


def encrypt_password(plain: str) -> bytes:
    """加密明文密码，返回 bytes（可存入 VARBINARY 字段）"""
    if not plain:
        raise ValueError("明文密码不能为空")
    return _get_fernet().encrypt(plain.encode("utf-8"))


def decrypt_password(encrypted: bytes) -> str:
    """解密密码，返回明文字符串"""
    try:
        return _get_fernet().decrypt(encrypted).decode("utf-8")
    except InvalidToken:
        raise ValueError("密码解密失败：密钥不匹配或数据被篡改")
