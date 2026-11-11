
from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Mã hóa mật khẩu bằng Argon2."""
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """Kiểm tra mật khẩu người dùng nhập."""
    return password_hasher.verify(
        plain_password,
        hashed_password
    )
