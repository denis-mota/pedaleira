class Equalizer:
    def __init__(self, bass=0.5, mid=0.5, treble=0.5):
        self.bass = bass
        self.mid = mid
        self.treble = treble

    def process(self, signal):
        # Simula a equalização (exemplo simples)
        return signal * (self.bass + self.mid + self.treble) / 3