"""AES-256-GCM 복호화 유틸 — Java AesEncryptionUtil과 동일한 전략.

저장 형식: Base64( IV[12 bytes] || GCM_Ciphertext+AuthTag )
키 도출:   ENCRYPTION_SECRET_KEY 환경변수 → SHA-256 → 256-bit AES 키
"""
from __future__ import annotations

import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_IV_LENGTH = 12


class AesDecryptionUtil:
    """AES-256-GCM 복호화 유틸리티.

    Backend의 AesEncryptionUtil(Java)과 동일한 키 도출 및 저장 형식을 사용한다.
    """

    def __init__(self, secret_key: str | None = None) -> None:
        raw_key = secret_key or os.environ.get("ENCRYPTION_SECRET_KEY", "ChangeThisSecretKeyInProduction!!")
        key_bytes = hashlib.sha256(raw_key.encode("utf-8")).digest()
        self._aesgcm = AESGCM(key_bytes)

    def decrypt(self, encrypted: str) -> str:
        """Base64 인코딩된 암호문(IV 포함)을 복호화하여 평문 반환."""
        combined = base64.b64decode(encrypted)
        iv = combined[:_IV_LENGTH]
        ciphertext_with_tag = combined[_IV_LENGTH:]
        plaintext = self._aesgcm.decrypt(iv, ciphertext_with_tag, None)
        return plaintext.decode("utf-8")
