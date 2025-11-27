import os
import warnings
from pgpy import PGPKey, PGPUID, PGPMessage
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

# warning library is used to suppress warnings as this bloats the output in the console
warnings.filterwarnings("ignore")

# users folder will be created to develope the repo for senders and reciever's addresses
USERS_DIR = "users"
# the same is true for any messages that has been encrypted. this is also from where the messages are read for decryption for verification
MESSAGES_DIR = "messages"

# making sure if the directories are there or needs to be created
os.makedirs(USERS_DIR, exist_ok=True)
os.makedirs(MESSAGES_DIR, exist_ok=True)

# creates directory for every new reciever or sender addresses
def user_dir(email):
    """Return the path for the user's directory."""
    path = os.path.join(USERS_DIR, email)
    os.makedirs(path, exist_ok=True)
    return path

# creates directory for every new reciever or sender addresses' key pairs
def key_paths(email):
    """Return file paths for a user's public and private keys."""
    user_path = user_dir(email)
    return (
        os.path.join(user_path, f"{email}_private.asc"),
        os.path.join(user_path, f"{email}_public.asc")
    )

def key_exists(email):
    """Check if key pair already exists."""
    priv, pub = key_paths(email)
    return os.path.exists(priv) and os.path.exists(pub)

def generate_keypair(name, email):
    """Generate and save a key pair for the given email."""
    print(f"🔐 Generating key pair for {email}...")
    key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 2048)
    uid = PGPUID.new(name, email=email)

    key.add_uid(
        uid,
        usage={KeyFlags.Sign, KeyFlags.EncryptCommunications},
        hashes=[HashAlgorithm.SHA256],
        ciphers=[SymmetricKeyAlgorithm.AES256],
        compression=[CompressionAlgorithm.ZLIB]
    )

    priv, pub = key_paths(email)
    with open(priv, "w") as f:
        f.write(str(key))
    with open(pub, "w") as f:
        f.write(str(key.pubkey))

    print(f"✅ Key pair created for {email}")
    return key

def load_public_key(email):
    """Load user's public key."""
    _, pub = key_paths(email)
    with open(pub, "r") as f:
        pubkey, _ = PGPKey.from_blob(f.read())
    return pubkey

def load_private_key(email):
    """Load user's private key."""
    priv, _ = key_paths(email)
    with open(priv, "r") as f:
        privkey, _ = PGPKey.from_blob(f.read())
    return privkey

def next_message_filename():
    """Generate next available encrypted message filename."""
    count = 1
    while os.path.exists(os.path.join(MESSAGES_DIR, f"message_{count:03}.asc")):
        count += 1
    return os.path.join(MESSAGES_DIR, f"message_{count:03}.asc")

# comments are written in-functions
def compose_and_encrypt():
    """Compose and encrypt a new message."""
    sender_email = input("\nEnter sender's email: ").strip()
    sender_name = sender_email.split("@")[0].capitalize()

    # Check/generate sender keys
    if not key_exists(sender_email):
        generate_keypair(sender_name, sender_email)
    else:
        print(f"🔑 Existing key found for {sender_email}")

    recipient_email = input("\nEnter recipient's email: ").strip()
    recipient_name = recipient_email.split("@")[0].capitalize()

    # Check/generate recipient keys
    if not key_exists(recipient_email):
        generate_keypair(recipient_name, recipient_email)
    else:
        print(f"🔑 Existing key found for {recipient_email}")

    message = input("\n✉️ Enter the message: ")
    full_message = f"From: {sender_email}\nTo: {recipient_email}\n\n{message}"

    # Encrypt with recipient's public key
    recipient_pubkey = load_public_key(recipient_email)
    encrypted_msg = recipient_pubkey.encrypt(PGPMessage.new(full_message))

    filename = next_message_filename()
    with open(filename, "w") as f:
        f.write(str(encrypted_msg))

    print(f"\n✅ Message encrypted and saved as: {filename}")
    print("=" * 60)
    print(str(encrypted_msg))
    print("=" * 60)
    print("💡 You can view and decrypt this message later from the menu.")

def decrypt_message():
    """List encrypted messages and decrypt selected one."""
    messages = sorted(
        [f for f in os.listdir(MESSAGES_DIR) if f.startswith("message_") and f.endswith(".asc")]
    )

    if not messages:
        print("\n❌ No encrypted messages found.")
        return

    print("\n📬 Available encrypted messages:")
    for i, msg in enumerate(messages, start=1):
        print(f"{i}. {msg}")

    try:
        choice = int(input("\nSelect a message to decrypt (number): "))
        selected_file = os.path.join(MESSAGES_DIR, messages[choice - 1])
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return

    with open(selected_file, "r") as f:
        enc_msg = PGPMessage.from_blob(f.read())

    # Try all private keys
    user_dirs = [os.path.join(USERS_DIR, d) for d in os.listdir(USERS_DIR)]
    all_privkeys = []
    for dir in user_dirs:
        for file in os.listdir(dir):
            if file.endswith("_private.asc"):
                all_privkeys.append(os.path.join(dir, file))

    if not all_privkeys:
        print("❌ No private keys available. Generate one first.")
        return

    for key_file in all_privkeys:
        try:
            with open(key_file, "r") as f:
                privkey, _ = PGPKey.from_blob(f.read())
            with privkey.unlock(""):
                dec_msg = privkey.decrypt(enc_msg)
                print(f"\n✅ Decrypted using key: {os.path.basename(key_file)}")
                print("-" * 60)
                print(dec_msg.message)
                print("-" * 60)
                return
        except Exception:
            continue

    print("❌ Decryption failed with all available keys.")

# this menu simulates a user interface for the presentation =
def main_menu():
    while True:
        print("\n=== 🔐 PGP Mail Emulator ===")
        print("1️⃣  Compose and encrypt a new message")
        print("2️⃣  Decrypt a saved message")
        print("3️⃣  Exit")

        choice = input("\nSelect an option (1-3): ").strip()
        if choice == "1":
            compose_and_encrypt()
        elif choice == "2":
            decrypt_message()
        elif choice == "3":
            print("\n👋 Exiting. Stay secure!")
            break
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()
