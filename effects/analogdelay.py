import numpy as np

class AnalogDelay:
    def __init__(self, delay_time=0.5, feedback=0.5, mix=0.5, sample_rate=44100, lowpass_coef=0.5):
        """
        delay_time: Tempo de atraso em segundos.
        feedback: Fator de feedback (0 a 1) – quanto do sinal atrasado é realimentado.
        mix: Mistura entre sinal seco e sinal com delay (0 = 100% seco, 1 = 100% com delay).
        sample_rate: Taxa de amostragem (ex.: 44100 Hz).
        lowpass_coef: Coeficiente do filtro passa-baixa (entre 0 e 1) aplicado no feedback para simular um delay analógico.
                      Valores maiores suavizam mais o sinal atrasado.
        """
        self.delay_time = delay_time
        self.feedback = feedback
        self.mix = mix
        self.sample_rate = sample_rate
        self.buffer_size = int(self.delay_time * self.sample_rate)
        self.buffer = np.zeros(self.buffer_size, dtype=np.float32)
        self.index = 0
        self.prev_lp = 0.0  # Armazena o valor anterior do filtro passa-baixa
        self.lowpass_coef = lowpass_coef

    def process(self, signal):
        """
        Processa o sinal de entrada (um array NumPy) sample-by-sample.
        Retorna um array do mesmo tamanho com o efeito de delay analógico aplicado.
        """
        output = np.empty_like(signal, dtype=np.float32)
        for i in range(len(signal)):
            # Obtém a amostra atrasada do buffer
            delayed_sample = self.buffer[self.index]
            
            # Aplica um filtro passa-baixa simples (filtro de 1 polo) na amostra atrasada
            # Fórmula: lp = (1 - lowpass_coef) * delayed_sample + lowpass_coef * prev_lp
            lp_sample = (1 - self.lowpass_coef) * delayed_sample + self.lowpass_coef * self.prev_lp
            self.prev_lp = lp_sample

            # Mistura o sinal seco (original) com o sinal com delay (wet)
            dry = signal[i]
            wet = lp_sample
            output[i] = dry * (1 - self.mix) + wet * self.mix

            # Atualiza o buffer: insere o sinal atual somado ao feedback do sinal filtrado
            self.buffer[self.index] = signal[i] + lp_sample * self.feedback

            # Avança o índice do buffer de forma circular
            self.index = (self.index + 1) % self.buffer_size

        return output
