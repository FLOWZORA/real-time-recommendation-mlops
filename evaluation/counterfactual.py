def ips(reward, propensity):
    return reward / max(float(propensity), 1e-6)

