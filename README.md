#Sample configuration

```
[general]
ssh_auth_sock = '~/.ssh/agent1.sock'

[cards]
[cards.somecard]
path = "/usr/lib/ssl/engines/libpkcs11.so"
token_serial_number = "ffffffffffffffff"
pin = 123456
remember_pin = true

[keys]
[keys.main]
path = '~/.ssh/id_rsa'
pin = 'some passphrase'
remember_pin = true
ssh_auth_sock = '~/.ssh/agent2.sock'
```

#SSH config example
```
Host *.smartcard
    User thuck
    IdentitiesOnly yes
    PKCS11Provider /usr/lib/ssl/engines/libpkcs11.so

Host *.key
    User thuck
    IdentitiesOnly yes
    IdentityFile ~/.ssh/id_rsa

```

Using *IdentitiesOnly* together with *PKCS11Provider* or *IdentityFile* avoids the error **Received disconnect from UNKNOWN port 65535:2: too many authentication failures** since it makes ssh to send only the proper key to the remote host.  

**OS dependency**  
gir1.2-notify
