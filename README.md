# pgp-email-security-python
Python implementation as a PoC for Mailvelope extension's simulation. This is part of the Advanced Security Protocols coursework. - Muhammad Bilal Hassan



# 🔐 PGP Mail Emulator – Proof of Concept (PoC)

This repository contains a **Proof of Concept (PoC)** developed for the *Advanced Security Protocols* coursework presentation by **Muhammad Bilal Hassan**.  
It demonstrates how **PGP (Pretty Good Privacy)** works by implementing a simple secure-mail emulator where users can:

- Generate new RSA keypairs  
- Encrypt messages using a recipient’s public key  
- Decrypt encrypted `.asc` messages using matching private keys  

This project is intended purely for **educational and demonstration** purposes.


---

## 🐍 Python Version

Recommended:

- **Python 3.10+**

Compatible with:

- Python 3.7 → 3.12

### ⚠️ *Note about `imghdr` errors*  
Some Python versions may fail due to the removal of `imghdr`. If this happens, manually add:

```python
import imghdr
````

This ensures compatibility with libraries that still depend on it internally.

---

## 📦 Installation

Install dependencies using pip:

```bash
pip install pgpy
```

If you encounter cryptography backend issues:

```bash
pip install --upgrade cryptography
```

---

## 🔗 Open Source Libraries Used

### **PGPy – PGP implementation in Python**

* GitHub: [https://github.com/SecurityInnovation/PGPy](https://github.com/SecurityInnovation/PGPy)
* PyPI: [https://pypi.org/project/PGPy/](https://pypi.org/project/PGPy/)

---

## 📁 Project Structure

```plaintext
users/                         # Auto-created user folders holding keypairs
  └── user@example.com/
      ├── user@example.com_private.asc
      └── user@example.com_public.asc

messages/                      # Encrypted message storage
  └── message_001.asc

pgp_mail_emulator.py           # Main Python script
```

---

## 🚀 Usage Instructions

Run the main script:

```bash
python pgp_mail_emulator.py
```

---

## ✉️ 1. Compose & Encrypt a Message

* Provide sender email
* Provide recipient email
* Script checks if keys exist
* If not, it **auto-generates RSA PGP keypairs**
* Message is encrypted using the **recipient’s public key**
* Encrypted output saved as:

```
messages/message_XXX.asc
```

You will also see the encrypted text printed in the console.

---

## 🔓 2. Decrypt a Message

* The script lists all encrypted files in `messages/`
* Select a message by number
* The script tries **every private key** inside `users/`
* If the correct key is found, the plaintext is displayed

---

## 🎯 Purpose of This PoC

This Proof of Concept is designed to help students understand:

* How PGP keys are generated and stored
* How asymmetric cryptography secures communications
* Public-key encryption workflow
* How encrypted messages are represented in `.asc` format
* Practical OpenPGP operations using Python

It forms part of the Advanced Security Protocols coursework presentation.

## 👨‍🏫 Author

**Muhammad Bilal Hassan**
*Advanced Security Protocols* – PoC Implementation


