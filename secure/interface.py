import scrypt

from typing import Union


class ArgumentError(Exception):
    pass


def generate_digest(message: str,
                    password: str = None,
                    maxtime: Union[float, int] = 0.5,
                    salt: str = "",
                    length: int = 64) -> bytes:
    """Multi-arity function for generating a digest.

    Use KDF symmetric encryption given a password.
    Use deterministic hash function given a salt (or lack of password).
    """

    if password and salt:
        raise ArgumentError("only provide a password or a salt, not both")

    if salt != "" and len(salt) < 16:
        raise ArgumentError("salts need to be minimum of 128bits (~16 characters)")

    if password:
        return scrypt.encrypt(message, password, maxtime=maxtime)
    else:
        return scrypt.hash(message, salt, buflen=length)


def decrypt_digest(digest: bytes,
                   password: str,
                   maxtime: Union[float, int] = 0.5) -> bytes:
    """Decrypts digest using given password."""

    return scrypt.decrypt(digest, password, maxtime)


def validate_digest(digest: bytes,
                    password: str,
                    maxtime: Union[float, int] = 0.5) -> bool:
    """Validate digest using given password."""

    try:
        scrypt.decrypt(digest, password, maxtime)
        return True
    except scrypt.error:
        return False
