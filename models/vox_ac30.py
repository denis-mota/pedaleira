class VoxAC30:
    def __init__(self, gain=1.0, volume=1.0, bass=0.5, mid=0.5, treble=0.5, presence=0.5, cut=0.5, preamp=None, equalizer=None, poweramp=None, speaker=None):
        """ Processa o sinal através do Vox AC30 """
        # Verifica se 'gain' é um número
        if isinstance(gain, (int, float)):
            self.gain = gain
        else:
            raise TypeError(f"Erro: 'gain' deve ser um número, mas recebeu {type(gain)}.")
        
        # Atribui outros componentes (caso você queira usá-los na classe)
        self.preamp = preamp
        self.equalizer = equalizer
        self.poweramp = poweramp
        self.speaker = speaker
        
        self.volume = volume
        self.bass = bass
        self.mid = mid
        self.treble = treble
        self.presence = presence
        self.cut = cut
        self.name = "VoxAC30"

    def process(self, signal):
        """ Processa o sinal através do Vox AC30 """
        # Simulação simples de ganho
        signal *= self.gain

        # Simulação de equalização
        signal *= (self.bass + self.mid + self.treble) / 3

        # Ajuste de presença
        signal *= (1 + self.presence * 0.2)

        # Controle de "cut" (simula um filtro passa-baixa)
        signal *= (1 - self.cut * 0.3)

        # Aplica o volume geral do amplificador
        return signal * self.volume
