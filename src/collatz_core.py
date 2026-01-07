def next_collatz(n: int) -> int:
    """Computes the next term in the Collatz sequence."""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def getting_collatz_sequence(start_n: int, max_steps: int = 1000) -> list[int]:
    """Generates a Collatz sequence starting from start_n."""
    seq = [start_n]
    current = start_n
    for _ in range(max_steps):
        if current == 1:
            break
        current = next_collatz(current)
        seq.append(current)
    return seq

def extended_collatz(n: int, a: int = 3, b: int = 1, modulus: int = 0) -> int:
    """
    Computes a step in a generalized Collatz-like sequence:
    n -> n/2 if even
    n -> (a*n + b) if odd
    If modulus > 0, the result is modulo modulus (useful for finite fields).
    """
    if n % 2 == 0:
        res = n // 2
    else:
        res = a * n + b
    
    if modulus > 0:
        return res % modulus
    return res
