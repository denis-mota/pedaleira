import numpy as np
from scipy.io import wavfile
from scipy.signal import convolve
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Função para carregar o arquivo IR
def load_ir(ir_file):
    _, ir = wavfile.read(ir_file)
    return ir

# Função de distorção com threshold e ganho
def distorcao(audio_data, threshold=0.9, gain=3.0):
    audio_data = audio_data * gain
    audio_data = np.clip(audio_data, -threshold, threshold)
    return audio_data

# Função de equalização simples (filtro passa-baixa)
def equalizacao(audio_data, cutoff=3000, fs=44100):  
    from scipy.signal import butter, filtfilt
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(1, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, audio_data)
    return filtered_data

# Função de simulação de alto-falante com IR
def speaker_simulation_with_ir(audio_data, ir_file='mesa_4x12_ir.wav'):
    ir = load_ir(ir_file)
    audio_with_speaker = convolve(audio_data, ir, mode='same')
    return audio_with_speaker

# Função para processar o áudio com parâmetros da GUI
def process_audio():
    try:
        # Carregar arquivo WAV
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if not file_path:
            return
        
        samplerate, data = wavfile.read(file_path)

        if len(data.shape) > 1:
            data = data[:, 0]  # Pega apenas o canal esquerdo, por exemplo
        
        # Normalizar o áudio
        data = data / np.max(np.abs(data), axis=0)
        
        # Pegar os parâmetros da interface
        threshold = threshold_slider.get()
        gain = gain_slider.get()
        cutoff = cutoff_slider.get()
        
        # Processamento de áudio
        audio_dist = distorcao(data, threshold=threshold, gain=gain)
        audio_eq = equalizacao(audio_dist, cutoff=cutoff)
        audio_speaker = speaker_simulation_with_ir(audio_eq)
        
        # Normalizar para evitar clipping
        audio_speaker = np.int16(audio_speaker / np.max(np.abs(audio_speaker)) * 32767)

        # Salvar o arquivo processado
        output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if output_file:
            wavfile.write(output_file, samplerate, audio_speaker)
            messagebox.showinfo("Processamento concluído", f"Áudio processado e salvo em {output_file}")
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o áudio: {e}")

# Criar a janela principal
ctk.set_appearance_mode("System")  # Modo escuro ou claro conforme o sistema
ctk.set_default_color_theme("blue")  # Escolher o tema

root = ctk.CTk()
root.title("Simulador de Amplificador com Distorção")

# Definir o tamanho da janela
root.geometry("400x400")

# Parâmetros de controle
threshold_label = ctk.CTkLabel(root, text="Threshold")
threshold_label.pack(pady=10)

threshold_slider = ctk.CTkSlider(root, from_=0, to_=1, resolution=0.01)
threshold_slider.set(0.9)
threshold_slider.pack(pady=10)

gain_label = ctk.CTkLabel(root, text="Gain")
gain_label.pack(pady=10)

gain_slider = ctk.CTkSlider(root, from_=1, to_=10, resolution=0.1)
gain_slider.set(3.0)
gain_slider.pack(pady=10)

cutoff_label = ctk.CTkLabel(root, text="Cutoff (Hz)")
cutoff_label.pack(pady=10)

cutoff_slider = ctk.CTkSlider(root, from_=100, to_=10000, resolution=10)
cutoff_slider.set(3000)
cutoff_slider.pack(pady=10)

# Botão para processar o áudio
process_button = ctk.CTkButton(root, text="Processar Áudio", command=process_audio)
process_button.pack(pady=20)

# Iniciar a interface gráfica
root.mainloop()
