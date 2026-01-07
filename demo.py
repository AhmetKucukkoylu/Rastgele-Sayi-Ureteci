import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from cipher import CollatzBlockCipher

def main():
    print("=== Collatz Crypto Demo ===")
    
    # 1. Setup Key
    key = b'SecretKey_123456' # 16 bytes
    print(f"Key: {key}")
    
    # 2. Setup Cipher
    cipher = CollatzBlockCipher(key)
    print("Cipher initialized with Collatz Key Expansion.")
    
    # 3. Encrypt
    plaintext = b'Attack at Dawn!!' # Exact 16 bytes for this demo
    print(f"\nPlaintext: {plaintext}")
    
    ciphertext = cipher.encrypt(plaintext)
    print(f"Ciphertext (hex): {ciphertext.hex()}")
    
    # 4. Decrypt
    decrypted = cipher.decrypt(ciphertext)
    print(f"Decrypted: {decrypted}")
    
    if plaintext == decrypted:
        print("\nSUCCESS: Decryption matched original plaintext.")
    else:
        print("\nFAILURE: Decryption did not match.")

if __name__ == "__main__":
    main()
