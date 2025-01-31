class Distortion:
    def __init__(self, gain=1.0):
        self.gain = gain
        self.name = "Distortion"

    def process(self, signal):
        """
        Aplica distorção ao sinal. Se o sinal for um array NumPy, 
        a multiplicação funciona diretamente. Se for uma lista, é necessário processar cada elemento.
        """
        if isinstance(signal, list):  # Se for uma lista comum, processa elemento por elemento
            return [min(1.0, max(-1.0, s * self.gain)) for s in signal]  
        return signal * self.gain  # Se for um NumPy array, a multiplicação funciona diretamente
