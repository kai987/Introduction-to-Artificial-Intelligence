import math


def shannon_entropy(probs):
    """
    Calculate Shannon entropy:
        H(X) = -sum(p * log2(p) for p in probs)
    """
    return -sum(p * math.log2(p) for p in probs if p > 0)

# Given distribution
# probs = [0.4, 0.3, 0.1, 0.2]
probs = [0.5, 0.2, 0.1, 0.1, 0.1]
entropy_value = shannon_entropy(probs)

# Display formula and result
print(f"Calculated entropy for {probs}: {entropy_value:.4f} bits")