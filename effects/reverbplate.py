import numpy as np
from scipy.signal import lfilter

def one_pole_lowpass(signal, cutoff, sample_rate):
    dt = 1.0 / sample_rate
    RC = 1.0 / (2 * np.pi * cutoff)
    alpha = dt / (RC + dt)
    b = [alpha]
    a = [1, alpha - 1]
    return lfilter(b, a, signal)

def one_pole_highpass(signal, cutoff, sample_rate):
    dt = 1.0 / sample_rate
    RC = 1.0 / (2 * np.pi * cutoff)
    alpha = RC / (RC + dt)
    b = [alpha, -alpha]
    a = [1, alpha - 1]
    return lfilter(b, a, signal)

class ReverbPlate:
    def __init__(self, mix=0.5, decay=2.0, pre_delay=0.01, 
                 cut_grave=100, cut_agudo=8000, volume=1.0, sample_rate=44100):
        """
        mix: Proporção entre sinal seco e reverberado (0 a 1).
        decay: Tempo de decaimento do reverb (em segundos).
        pre_delay: Tempo de pré-delay (em segundos).
        cut_grave: Frequência de corte para graves (em Hz).
        cut_agudo: Frequência de corte para agudos (em Hz).
        volume: Ganho final.
        sample_rate: Taxa de amostragem (Hz).
        """
        self.mix = mix
        self.decay = decay
        self.pre_delay = pre_delay  # Armazena o tempo de pré-delay em segundos
        self.pre_delay_samples = int(pre_delay * sample_rate)
        self.cut_grave = cut_grave
        self.cut_agudo = cut_agudo
        self.volume = volume
        self.sample_rate = sample_rate

        # Buffer para pré-delay (1D, mono)
        self.pre_delay_buffer = np.zeros(self.pre_delay_samples, dtype=np.float32)

        # Filtros comb paralelos (exemplos de tempos para reverb Schroeder)
        comb_delays = [0.0297, 0.0371, 0.0411, 0.0437]  # em segundos
        self.comb_filters = []
        for d in comb_delays:
            delay_samples = int(d * sample_rate)
            # Feedback aproximado para o decaimento
            feedback = np.exp(-3.0 * d / decay)
            self.comb_filters.append({
                'delay': delay_samples,
                'buffer': np.zeros(delay_samples, dtype=np.float32),
                'index': 0,
                'feedback': feedback
            })
            

        # Filtros all-pass em série (exemplos de tempos pequenos)
        allpass_delays = [0.005, 0.0017]  # em segundos
        self.allpass_filters = []
        for d in allpass_delays:
            delay_samples = int(d * sample_rate)
            feedback = 0.7  # Valor típico para all-pass
            self.allpass_filters.append({
                'delay': delay_samples,
                'buffer': np.zeros(delay_samples, dtype=np.float32),
                'index': 0,
                'feedback': feedback
            })

    def process(self, signal):
        """ Aplica o reverb plate ao sinal de entrada. """
        # Se o sinal tiver mais de 1 dimensão (por exemplo, estéreo), converte para mono
        if signal.ndim > 1:
            signal = np.mean(signal, axis=1)

        # Recalcula o número de amostras de pré-delay (garante ser inteiro)
        pre_delay_samples = int(self.pre_delay * self.sample_rate)
        if pre_delay_samples != self.pre_delay_samples:
            self.pre_delay_samples = pre_delay_samples
            self.pre_delay_buffer = np.zeros(self.pre_delay_samples, dtype=np.float32)

        # 1. Pré-delay: concatena o buffer de pré-delay com o sinal e corta o excesso
        if self.pre_delay_samples > len(signal):
            self.pre_delay_samples = len(signal)  # Evita que coma todo o sinal

        print("Sinal após Pré-Delay:", np.max(np.abs(signal)))  # Deve ser maior que 0


        # 2. Processamento paralelo com filtros comb
        comb_sum = np.zeros_like(signal, dtype=np.float32)
        for filt in self.comb_filters:
            comb_out = np.zeros_like(signal, dtype=np.float32)
            for i in range(len(signal)):
                delayed_sample = filt['buffer'][filt['index']]
                comb_out[i] = delayed_sample
                filt['buffer'][filt['index']] = signal[i] + delayed_sample * filt['feedback']
                filt['index'] = (filt['index'] + 1) % filt['delay']
            comb_sum += comb_out
        comb_sum /= len(self.comb_filters)  # Média dos filtros comb
        print("Saída dos filtros Comb:", np.max(np.abs(comb_sum)))  # Deve ser maior que 0


        # 3. Processamento em série com filtros all-pass
        allpass_out = comb_sum.copy()
        for filt in self.allpass_filters:
            temp_out = np.zeros_like(allpass_out, dtype=np.float32)
            for i in range(len(allpass_out)):
                delayed_sample = filt['buffer'][filt['index']]
                temp_out[i] = -filt['feedback'] * allpass_out[i] + delayed_sample
                filt['buffer'][filt['index']] = allpass_out[i] + filt['feedback'] * temp_out[i]
                filt['index'] = (filt['index'] + 1) % filt['delay']
            allpass_out = temp_out

        # 4. Aplica os filtros de corte:
        # Corte de graves (passa-alto)
        wet = one_pole_highpass(allpass_out, self.cut_grave, self.sample_rate)
        # Corte de agudos (passa-baixa)
        wet = one_pole_lowpass(wet, self.cut_agudo, self.sample_rate)

        # 5. Mistura sinal seco e reverberado, e aplica o volume final
        processed = (1 - self.mix) * signal + self.mix * wet
        processed *= self.volume
        print("Reverb Output:", np.max(np.abs(processed)))  # Deve ser maior que 0
        print("Input Signal:", np.max(np.abs(signal)))  # Deve ser maior que 0



        return processed
