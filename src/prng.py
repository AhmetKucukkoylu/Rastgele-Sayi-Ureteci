import struct
import time
from collatz_core import next_collatz, extended_collatz

class CollatzRNG:
    """
    A Pseudo-Random Number Generator based on the chaotic behavior of Collatz sequences.
    WARNING: This is valid for experimental/educational use only.
    """
    def __init__(self, seed_val: int = None):
        if seed_val is None:
            seed_val = int(time.time() * 1000)
        self.state = seed_val
        # Avoid the trivial cycle 4-2-1 by creating a larger internal state
        self.micro_state = seed_val ^ 0xCAFEBABE
        
    def seed(self, seed_val: int):
        self.state = seed_val
        self.micro_state = seed_val ^ 0xCAFEBABE

    def _churn(self):
        """Advances the internal state using mixed Collatz dynamics to increase entropy."""
        # Primary state evolution: Standard Collatz
        self.state = next_collatz(self.state)
        if self.state == 1:
             # Re-inject entropy if we hit the limit, using micro_state
            self.state = (self.micro_state * 3 + 1) ^ 0x12345678
            
        # Secondary state evolution: Generalized Collatz for divergence
        # Using 5n+1 for odd steps to mix it up
        self.micro_state = extended_collatz(self.micro_state, a=5, b=1)
        
        # Mix the two states
        combined = self.state ^ self.micro_state
        return combined

    def next_int(self, bits: int = 32) -> int:
        """Generates a random integer with the specified number of bits."""
        result = 0
        bits_generated = 0
        
        while bits_generated < bits:
            val = self._churn()
            # Extract lower 8 bits from the churned value
            chunk = val & 0xFF
            result = (result << 8) | chunk
            bits_generated += 8
            
        # Trim to exact bit length
        mask = (1 << bits) - 1
        return result & mask

    def next_bytes(self, length: int) -> bytes:
        """Generates random bytes."""
        data = bytearray()
        for _ in range(length):
            val = self._churn()
            data.append(val & 0xFF)
        return bytes(data)
