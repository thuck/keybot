**Sample configuration**

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

**OS dependency**  
gir1.2-notify
