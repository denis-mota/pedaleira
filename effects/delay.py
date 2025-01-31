import numpy as np

class Delay:
    def __init__(self, delay_time=0.5, feedback=0.5, sample_rate=44100):
        self.name = "Delay"
        self.delay_time = delay_time  # Tempo do delay em segundos
        self.feedback = feedback  # Intensidade do feedback
        self.sample_rate = sample_rate  # Taxa de amostragem em Hz
        self.buffer_size = int(self.sample_rate * self.delay_time)  # Tamanho do buffer
        self.buffer = np.zeros(self.buffer_size)  # Inicializa o buffer com zeros
        self.index = 0  # Índice do buffer circular

    def process(self, signal):
        """
        Aplica o efeito de delay a um sinal. Suporta sinais NumPy e listas.
        """
        if isinstance(signal, list):
            signal = np.array(signal)  # Converte para NumPy se for lista

        delayed_signal = self.buffer[self.index]  # Obtém o sinal atrasado
        output = signal + delayed_signal  # Mistura o sinal original com o delay
        
        # Armazena no buffer com feedback
        self.buffer[self.index] = signal + delayed_signal * self.feedback
        
        # Atualiza o índice do buffer circular
        self.index = (self.index + 1) % self.buffer_size

        return output
