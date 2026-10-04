from cryptography.fernet import Fernet

fernet_key = input("Enter Fernet key: ").strip()
refresh_token = input("Enter refresh token: ").strip()

cipher = Fernet(fernet_key.encode())

encrypted = cipher.encrypt(refresh_token.encode())

print("\nENCRYPTED_REFRESH_TOKEN:")
print(encrypted.decode())