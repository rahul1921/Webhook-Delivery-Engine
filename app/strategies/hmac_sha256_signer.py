import json
import hmac
import hashlib

from interfaces.signer_interface import SignerInterface

class HmacSHA256Signer(SignerInterface):

    def sign(self, secret: str, payload: dict) -> str:
        payload_bytes = json.dumps(payload).encode()

        return hmac.new(
            secret.encode(),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()
