class PowerAmp:
    def __init__(self, volume=1.0):
        self.volume = volume
        self.name = "PowerAmp"

    def process(self, signal):
        # Aplica o ganho do amplificador de potência
        return signal * self.volume