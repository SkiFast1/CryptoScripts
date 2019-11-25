from cryptography.fernet import Fernet
cipher_key=b'[YOUR_KEY]'
cipher = Fernet(cipher_key)
encrypted_text = b'[ENC_TEXT]'
decrypted_text = cipher.decrypt(encrypted_text)
print(decrypted_text)

