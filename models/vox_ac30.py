class VoxAC30:
    def __init__(self, preamp, equalizer, poweramp, speaker):
        self.preamp = preamp
        self.equalizer = equalizer
        self.poweramp = poweramp
        self.speaker = speaker
        self.name = "VoxAC30"

    def process(self, signal):
        """
        Processa o sinal através de todos os estágios do amplificador Vox AC30: 
        pré-amplificador -> equalizador -> amplificador de potência -> alto-falante
        """
        signal = self.preamp.process(signal)
        signal = self.equalizer.process(signal)
        signal = self.poweramp.process(signal)
        signal = self.speaker.process(signal)
        return signal