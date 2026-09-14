def gini(values):
    """
    Compute Gini coefficient of an array of values.
    Returns 0.0 for perfect equality, approaching 1.0 for extreme inequality.
    """
    if not values:
        return 0.0
    values = sorted(values)
    n = len(values)
    total = float(sum(values))
    if total == 0.0:
        return 0.0
    return sum((2 * i - n + 1) * v for i, v in enumerate(values)) / (n * total)

if __name__ == "__main__":
    print(f"[OK] Equal distribution Gini: {gini([10, 10, 10, 10]):.4f}")
    print(f"[OK] Skewed distribution Gini: {gini([0, 0, 0, 100]):.4f}")

