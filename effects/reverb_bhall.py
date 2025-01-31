import numpy as np
import scipy.signal as signal

class HallReverb:
    def __init__(self, mix=0.5, decay=2.0, pre_delay=50, cut_grave=200, cut_agudo=8000, volume=1.0, sample_rate=44100):
        self.mix = mix
        self.decay = decay
        self.pre_delay = pre_delay / 1000.0  # Convertendo ms para segundos
        self.cut_grave = cut_grave
        self.cut_agudo = cut_agudo
        self.volume = volume
        self.sample_rate = sample_rate
    
    def apply_filter(self, signal, cutoff, filter_type):
        nyquist = 0.5 * self.sample_rate
        norm_cutoff = cutoff / nyquist
        b, a = signal.butter(2, norm_cutoff, btype=filter_type)
        return signal.lfilter(b, a, signal)

    def process(self, input_signal):
        # Criando o pré-delay
        pre_delay_samples = int(self.sample_rate * self.pre_delay)
        pre_delayed_signal = np.concatenate((np.zeros(pre_delay_samples), input_signal))
        
        # Criando a cauda de reverb simulada (exponencial)
        decay_factor = np.exp(-np.linspace(0, self.decay, len(pre_delayed_signal)))
        reverb_signal = pre_delayed_signal * decay_factor
        
        # Aplicando filtros
        reverb_signal = self.apply_filter(reverb_signal, self.cut_grave, 'high')
        reverb_signal = self.apply_filter(reverb_signal, self.cut_agudo, 'low')
        
        # Mixando o sinal original com o reverberado
        output_signal = (1 - self.mix) * input_signal + self.mix * reverb_signal[:len(input_signal)]
        
        # Ajustando o volume
        output_signal *= self.volume
        
        return output_signal