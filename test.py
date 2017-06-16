import rsa

print("Trwa generowanie klucza!")
(
    pubkey,
    privkey
) = rsa.newkeys(2048)

message = "Test".encode('utf8')
print(message)

encrypted = rsa.encrypt(message, pubkey)
print(encrypted)

print(rsa.decrypt(encrypted, privkey))
