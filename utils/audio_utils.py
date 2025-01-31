import numpy as np

def normalize_signal(signal):
    """
    Normaliza o sinal para evitar clipping.
    Se o maior valor absoluto do sinal for zero, retorna o próprio sinal para evitar divisão por zero.
    """
    max_val = np.max(np.abs(signal))
    return signal / max_val if max_val > 0 else signal
