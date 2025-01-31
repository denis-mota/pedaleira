class Preamp:
    def __init__(self, volume=1.0):
        self.volume = volume
        self.name = "Preamp"

    def process(self, signal):
        # Aplica o ganho do pré-amplificador
        return signal * self.volume