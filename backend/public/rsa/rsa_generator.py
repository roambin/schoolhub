import rsa

pubkey, privkey = rsa.newkeys(1024)
pubkey_b = pubkey.save_pkcs1()
with open("pubkey.pem", "wb") as file:
    file.write(pubkey_b)
privkey_b = privkey.save_pkcs1()
with open("privkey.pem", "wb") as file:
    file.write(privkey_b)