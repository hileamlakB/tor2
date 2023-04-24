import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as symmetric_padding

# RSA key generation


def generate_rsa_key_pair(size=2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return public_key, private_key

# RSA encryption


def rsa_encrypt(public_key, data):
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data

# RSA decryption


def rsa_decrypt(private_key, encrypted_data):
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data

# AES encryption


def aes_encrypt(key, data):
    padder = symmetric_padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv, encrypted_data

# AES decryption


def aes_decrypt(key, iv, encrypted_data):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = symmetric_padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data


if __name__ == "__main__":

    # RSA key generation
    public_key, private_key = generate_rsa_key_pair()

    # Generate a random AES key
    aes_key = os.urandom(32)

    # Encrypt the AES key with the RSA public key
    encrypted_aes_key = rsa_encrypt(public_key, aes_key)
    print(encrypted_aes_key, type(encrypted_aes_key))

    # Decrypt the AES key with the RSA private key
    decrypted_aes_key = rsa_decrypt(private_key, encrypted_aes_key)

    # Encrypt data using AES
    data = b"Your long data goes here..."
    iv, encrypted_data = aes_encrypt(decrypted_aes_key, data)
    print(type(iv))

    # Decrypt data using AES
    decrypted_data = aes_decrypt(decrypted_aes_key, iv, encrypted_data)

    print("Decrypted data:", decrypted_data)
