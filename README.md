**Sample configuration**

```
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
```

**OS dependency**  
gir1.2-notify
