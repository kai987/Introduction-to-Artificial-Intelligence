import math


def shannon_entropy(probs):
    """
    シャノン(Shannon)のエントロピー(平均情報量)を計算します:
    H(X) = -sum(p * log2(p) for p in probs)
    """
    return -sum(p * math.log2(p) for p in probs if p > 0)

# 与えられた分布
probs = [0.4, 0.3, 0.1, 0.2]
# probs = [0.5, 0.2, 0.1, 0.1, 0.1]
entropy_value = shannon_entropy(probs)

# 計算式と結果を表示する
print(f"計算されたエントロピー {probs}: {entropy_value:.4f} bits")
# 結果
# 計算されたエントロピー [0.5, 0.2, 0.1, 0.1, 0.1]: 1.9610 bits
# 計算されたエントロピー for [0.4, 0.3, 0.1, 0.2]: 1.8464 bits