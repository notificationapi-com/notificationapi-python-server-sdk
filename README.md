# NotificationAPI Python Server SDK

NotificationAPI SDK for server-side (back-end) python projects. 

* Free software: MIT license

# Contribution

## Ubuntu:
1. Install pip:
```bash
sudo apt update
sudo apt install python3-pip 
```

2. Add dependencies to PATH:
```
# Add this to ~/.profile
export PATH=$PATH:/home/sahand/.local/bin/
```

3. Install dev requirements:
```bash
pip install -r requirements_dev.txt
```

4. Run tests:
```bash
# normal:
make test
# coverage
make coverage
# watch
make test-watch
```
5. bump2version major/minor/patch