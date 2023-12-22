import bcrypt


class PasswordUtil:
    @staticmethod
    def encrypt(raw_password: str) -> str:
        return bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def check_password(original_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(original_password.encode(), hashed_password.encode())
