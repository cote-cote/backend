from app.application.port.outbound.cote_lock_key import CoteLockKeyPort


class CoteLockKeyAdapter(CoteLockKeyPort):
    def generate_key(self, key_id: str) -> str:
        return f"cote_{key_id}"
