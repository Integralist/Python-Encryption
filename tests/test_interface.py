import pytest

from secure.interface import ArgumentError, generate_digest, validate_digest, decrypt_digest


message = "my-message"
password = "my-password"
salt = "my-salt-is-long-enough"


def test_generate_digest_with_both_a_password_and_a_salt():
    """Providing both a password and a salt should raise an exception."""

    with pytest.raises(ArgumentError):
        generate_digest(message, salt=salt, password=password)


def test_generate_digest_with_a_password():
    """Generating a digest with a password should be non-deterministic."""

    digest1 = generate_digest(message, password=password)
    digest2 = generate_digest(message, password=password)
    digest3 = generate_digest(message, password=password, maxtime=1.5)
    digest4 = generate_digest(message, password=password, maxtime=1.5)
    digest5 = generate_digest(message, password=password, maxtime=int(1))
    digest6 = generate_digest(message, password=password, maxtime=int(1))

    assert digest1 != digest2
    assert digest3 != digest4
    assert digest5 != digest6


def test_generate_digest_without_a_password():
    """Generating a digest without a password should be deterministic."""

    digest1 = generate_digest(message)
    digest2 = generate_digest(message)
    digest3 = generate_digest(message, salt=salt)
    digest4 = generate_digest(message, salt=salt)
    digest5 = generate_digest(message, length=128)
    digest6 = generate_digest(message, length=128)

    assert digest1 == digest2
    assert digest3 == digest4
    assert len(digest5) == len(digest6)


def test_generate_digest_with_different_salt_lengths():
    """Salts should be at least 128bits (~16 characters) in length."""

    generate_digest(message, salt=salt)

    with pytest.raises(ArgumentError):
        generate_digest(message, salt="too-short")

def test_validate_digest():
    """Validation only applies to digests generated with a password."""

    digest1 = generate_digest(message, password=password)
    digest2 = generate_digest(message, password=password)
    digest3 = generate_digest(message, password=password, maxtime=1.5)
    digest4 = generate_digest(message, password=password, maxtime=1.5)
    digest5 = generate_digest(message, password=password, maxtime=int(1))
    digest6 = generate_digest(message, password=password, maxtime=int(1))

    assert not validate_digest(digest1, 'incorrect-password')
    assert validate_digest(digest1, password)
    assert validate_digest(digest3, password, maxtime=1.5)
    assert validate_digest(digest5, password, maxtime=int(1))


def test_decrypt_digest():
    """Decryption is possible given the right password."""

    digest = generate_digest(message, password=password)

    assert decrypt_digest(digest, password) == message
