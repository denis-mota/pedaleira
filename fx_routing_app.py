import customtkinter as ctk
import sounddevice as sd 
import numpy as np
from signal_chain import SignalChain
from effects import Distortion, AnalogDelay, ReverbPlate
from models.vox_ac30 import VoxAC30
import threading

# --- Novo: Definição do efeito Gate ---
class Gate:
    def __init__(self, threshold=0.05, attack=0.01, release=0.1):
        """
        threshold: Amplitude abaixo da qual o sinal é silenciado.
        attack: Tempo de abertura do gate (não implementado de forma dinâmica neste exemplo).
        release: Tempo de fechamento do gate (não implementado de forma dinâmica neste exemplo).
        """
        self.threshold = threshold
        self.attack = attack
        self.release = release
        self.name = "Gate"

    def process(self, signal):
        """ Se a amplitude do sinal estiver abaixo do threshold, zera o sinal. """
        return np.where(np.abs(signal) < self.threshold, 0, signal)

# Exibe os dispositivos de áudio disponíveis para depuração
print(sd.query_devices())

class FXRoutingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FX Routing")
        self.root.geometry("900x600")
        self.chain = SignalChain()
        self.selected_effect = None  

        # Controle de áudio
        self.is_muted = False
        self.is_listening = True

        # Configuração dos dispositivos de áudio (ajuste os índices conforme necessário)
        self.input_device_index = 1
        self.output_device_index = 7

        self.samplerate = 44100
        self.blocksize = 1024  # Tamanho do bloco

        # Cria e inicia os streams de áudio
        
        self.input_stream = sd.InputStream(device=self.input_device_index,
                                           channels=1,
                                           samplerate=self.samplerate,
                                           blocksize=self.blocksize,
                                           dtype=np.int16,
                                           callback=self.audio_callback)
        self.output_stream = sd.OutputStream(device=self.output_device_index,
                                             channels=1,
                                             samplerate=self.samplerate,
                                             blocksize=self.blocksize,
                                             dtype=np.int16)
        self.input_stream.start()
        self.output_stream.start()

        # Configuração do tema
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue")  

        self.create_sidebar()
        self.create_chain_area()
        self.create_controls_area()

    def create_sidebar(self):
        """ Cria o menu lateral expansível/retrátil e os controles de áudio. """
        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y, padx=5, pady=5)

        self.toggle_button = ctk.CTkButton(self.sidebar, text="Menu", command=self.toggle_menu)
        self.toggle_button.pack(pady=5)

        self.menu_frame = ctk.CTkFrame(self.sidebar)
        self.menu_frame.pack(fill=ctk.BOTH, expand=True)

        # Botões para adicionar efeitos
        self.add_distortion_button = ctk.CTkButton(self.menu_frame, text="Add Distortion", 
                                                   command=lambda: self.add_block(Distortion()))
        self.add_distortion_button.pack(pady=2)

        self.add_AnalogDelay_button = ctk.CTkButton(self.menu_frame, text="Add AnalogDelay", 
                                              command=lambda: self.add_block(AnalogDelay()))
        self.add_AnalogDelay_button.pack(pady=2)

        # Atualizado: Parâmetros do ReverbPlate; pre_delay em segundos (0.05 = 50ms)
        self.add_ReverbPlate_button = ctk.CTkButton(self.menu_frame, text="Add ReverbPlate", 
                                         command=lambda: self.add_block(ReverbPlate(mix=0.5, decay=2.0, pre_delay=0.05, 
                                                                                   cut_grave=100, cut_agudo=8000, volume=1.0, sample_rate=self.samplerate)))
        self.add_ReverbPlate_button.pack(pady=2)

        self.add_vox_button = ctk.CTkButton(self.menu_frame, text="Add Vox AC30", 
                                            command=lambda: self.add_block(VoxAC30(gain=1.5, volume=0.8)))
        self.add_vox_button.pack(pady=2)
        
        # Novo: Botão para adicionar o Gate
        self.add_gate_button = ctk.CTkButton(self.menu_frame, text="Add Gate", 
                                             command=lambda: self.add_block(Gate(threshold=0.05, attack=0.01, release=0.1)))
        self.add_gate_button.pack(pady=2)

        self.menu_visible = True  

        # Botões de controle de áudio
        self.mute_button = ctk.CTkButton(self.sidebar, text="Mute", command=self.toggle_mute)
        self.mute_button.pack(pady=5)

        self.listen_button = ctk.CTkButton(self.sidebar, text="Listen", command=self.toggle_listening)
        self.listen_button.pack(pady=5)

    def toggle_menu(self):
        """ Mostra ou esconde o menu lateral. """
        if self.menu_visible:
            self.menu_frame.pack_forget()
        else:
            self.menu_frame.pack(fill=ctk.BOTH, expand=True)
        self.menu_visible = not self.menu_visible

    def toggle_mute(self):
        """ Alterna entre mudo e áudio normal. """
        self.is_muted = not self.is_muted

    def toggle_listening(self):
        """ Alterna entre ouvir e não ouvir o áudio processado. """
        self.is_listening = not self.is_listening

    def create_chain_area(self):
        """ Cria a área onde os efeitos aparecem em sequência. """
        self.chain_area = ctk.CTkFrame(self.root)
        self.chain_area.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=5)

        self.chain_display_label = ctk.CTkLabel(self.chain_area, text="Cadeia de Efeitos", font=("Arial", 16))
        self.chain_display_label.pack(pady=5)

        self.chain_list = ctk.CTkFrame(self.chain_area)
        self.chain_list.pack(fill=ctk.BOTH, expand=True)

    def create_controls_area(self):
        """ Cria a área de controles na parte inferior. """
        self.controls_area = ctk.CTkFrame(self.root, height=150)
        self.controls_area.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=5)

        self.controls_label = ctk.CTkLabel(self.controls_area, text="Parâmetros do efeito selecionado:", font=("Arial", 14))
        self.controls_label.pack(pady=5)

        self.controls_container = ctk.CTkFrame(self.controls_area)
        self.controls_container.pack(fill=ctk.BOTH, expand=True)

    def add_block(self, block):
        """ Adiciona um efeito à cadeia e atualiza a interface. """
        self.chain.add_block(block)
        self.update_chain_display()

    def update_chain_display(self):
        """ Atualiza a exibição da cadeia de efeitos. """
        for widget in self.chain_list.winfo_children():
            widget.destroy()

        if self.chain.blocks:
            for i, block in enumerate(self.chain.blocks):
                button = ctk.CTkButton(self.chain_list, text=f"{i+1}. {block.__class__.__name__}", 
                                       command=lambda b=block: self.select_effect(b))
                button.pack(pady=2)
        else:
            label = ctk.CTkLabel(self.chain_list, text="Sem efeitos na cadeia.")
            label.pack(pady=2)

    def select_effect(self, effect):
        """ Atualiza a área de controles para exibir os parâmetros do efeito selecionado. """
        self.selected_effect = effect
        self.update_controls_area()

    def update_controls_area(self):
        """ Atualiza os sliders na parte inferior conforme o efeito selecionado. """
        for widget in self.controls_container.winfo_children():
            widget.destroy()

        if not self.selected_effect:
            return

        effect_name = self.selected_effect.__class__.__name__
        self.controls_label.configure(text=f"Parâmetros de {effect_name}:")

        params = vars(self.selected_effect)
        for param, value in params.items():
            if isinstance(value, (int, float)):
                frame = ctk.CTkFrame(self.controls_container)
                frame.pack(fill=ctk.X, pady=2)

                label = ctk.CTkLabel(frame, text=param.capitalize(), width=100)
                label.pack(side=ctk.LEFT)

                slider = ctk.CTkSlider(frame, from_=0, to=10, number_of_steps=100,
                                       command=lambda v, p=param: self.update_param(p, v))
                slider.set(value)
                slider.pack(side=ctk.RIGHT, fill=ctk.X, expand=True)

    def update_param(self, param, value):
        if self.selected_effect:
            setattr(self.selected_effect, param, float(value))
            if param == "pre_delay":
                self.selected_effect.pre_delay_samples = int(self.selected_effect.pre_delay * self.selected_effect.sample_rate)
            
    def process_signal(self, input_data):
        """ Processa o sinal de áudio através da cadeia de efeitos. """
        # Converte os dados de entrada (int16) para float entre -1 e 1
        audio_data = input_data.astype(np.float32) / 32768.0
        print("Áudio antes do processamento:", audio_data[:10])

        for block in self.chain.blocks:
            audio_data = block.process(audio_data)
        
        print("Áudio depois do processamento:", audio_data[:10])

        # Converte de volta para int16
        output_data = np.int16(audio_data * 32768)
        return output_data

    def audio_callback(self, indata, frames, time, status):
        """ Callback para processar o áudio. """
        if status:
            print("Status do áudio:", status)
        
        print("Entrada de áudio recebida:", indata[:10])
        processed_audio = self.process_signal(indata)
        
        if not self.is_muted and self.is_listening:
            try:
                self.output_stream.write(processed_audio)
            except Exception as e:
                print("Erro ao escrever no stream de saída", e)

    def stop_streams(self):
        """ Fecha as streams de áudio. """
        self.input_stream.stop()
        self.input_stream.close()
        self.output_stream.stop()
        self.output_stream.close()
        print("Streams fechadas.")

# Iniciar a aplicação
if __name__ == "__main__":
    root = ctk.CTk()
    app = FXRoutingApp(root)
    root.mainloop()
