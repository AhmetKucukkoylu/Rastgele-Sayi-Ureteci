import unittest
import math
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from prng import CollatzRNG
from cipher import CollatzBlockCipher

def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = data.count(x) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

class TestCollatzCrypto(unittest.TestCase):
    
    def test_prng_entropy(self):
        print("\nTesting PRNG Entropy...")
        rng = CollatzRNG()
        # Generate 100KB of random data
        data = rng.next_bytes(100 * 1024)
        entropy = calculate_entropy(data)
        print(f"Generated 100KB. Shannon Entropy: {entropy:.4f} (Ideal: 8.0)")
        # Expect high entropy (> 7.8 usually, but let's be lenient > 7.5)
        self.assertGreater(entropy, 7.5, "PRNG entropy is too low!")

    def test_cipher_correctness(self):
        print("\nTesting Cipher Correctness...")
        key = b'0123456789abcdef' # 16 bytes
        cipher = CollatzBlockCipher(key)
        
        plaintext = b'Hello World 123!' # 16 bytes
        ciphertext = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(ciphertext)
        
        print(f"Original: {plaintext}")
        print(f"Encrypted (hex): {ciphertext.hex()}")
        print(f"Decrypted: {decrypted}")
        
        self.assertEqual(plaintext, decrypted, "Decryption failed to recover original plaintext")
        self.assertNotEqual(plaintext, ciphertext, "Ciphertext should not match plaintext")

    def test_avalanche_effect(self):
        print("\nTesting Avalanche Effect...")
        key = b'0123456789abcdef'
        cipher = CollatzBlockCipher(key)
        
        block1 = b'0000000000000000'
        # Flip 1 bit in the input
        block2 = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        
        c1 = cipher.encrypt(block1)
        c2 = cipher.encrypt(block2)
        
        diff_bits = 0
        for b1, b2 in zip(c1, c2):
            diff_bits += bin(b1 ^ b2).count('1')
            
        print(f"Bit difference: {diff_bits} / 128")
        # Ideal avalanche is 50% (64 bits) changed for 1 bit input change.
        # We'll valid if it's somewhat chaotic > 20 bits changed.
        self.assertGreater(diff_bits, 20, "Avalanche effect is weak")

if __name__ == '__main__':
    unittest.main()
