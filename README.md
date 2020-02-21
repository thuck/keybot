# Sample configuration

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

[totp]
[totp.google]
secret = '33THUCKSECRET333'
path = '~/.totp_file_output'
```

# SSH config example
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

# SSH agent systemd

```
[Unit]
Description=OpenSSH private key agent
StartLimitIntervalSec=1s

[Service]
Type=forking
ExecStartPre=/bin/rm -f %h/.ssh/ssh-agent.socket
ExecStart=/usr/bin/ssh-agent -a %h/.ssh/ssh-agent.socket -P '/usr/lib/*,/usr/local/lib/*,/lib/*'
Restart=on-failure

[Install]
WantedBy=default.target

```
Copy sample to *.config/systemd/user/ssh-agent.service*

systemctl --user enable ssh-agent
systemctl --user start ssh-agent

**OS dependency**  
gir1.2-notify
