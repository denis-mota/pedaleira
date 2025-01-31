import customtkinter as ctk
from signal_chain import SignalChain
from effects import Distortion, Delay
from models.preamp import Preamp
from models.equalizer import Equalizer
from models.poweramp import PowerAmp
from models.speaker import Speaker
from models.vox_ac30 import VoxAC30

class FXRoutingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FX Routing")
        self.root.geometry("800x500")  # Aumentei um pouco o tamanho para ficar mais confortável
        self.chain = SignalChain()
        self.name = "FXRoutingApp"

        # Configuração do tema
        ctk.set_appearance_mode("dark")  # Modo escuro
        ctk.set_default_color_theme("blue")  # Tema azul

        # Cria os componentes do Vox AC30
        preamp = Preamp(volume=2.0)
        equalizer = Equalizer(bass=0.7, mid=0.5, treble=0.8)
        poweramp = PowerAmp(volume=1.5)
        self.speaker = Speaker(model="Celestion Blue", tone=0.9)  # Inicializa o falante com valor inicial de tom

        # Cria o amplificador Vox AC30
        self.vox_ac30 = VoxAC30(preamp, equalizer, poweramp, self.speaker)

        # Área de blocos disponíveis
        self.block_area = ctk.CTkFrame(root)
        self.block_area.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10, expand=True)

        # Área de cadeia de processamento
        self.chain_area = ctk.CTkFrame(root)
        self.chain_area.pack(side=ctk.RIGHT, fill=ctk.Y, padx=10, pady=10, expand=True)

        # Botões para adicionar blocos
        self.add_distortion_button = ctk.CTkButton(self.block_area, text="Add Distortion", command=lambda: self.add_block(Distortion()))
        self.add_distortion_button.pack(pady=5)

        self.add_delay_button = ctk.CTkButton(self.block_area, text="Add Delay", command=lambda: self.add_block(Delay()))
        self.add_delay_button.pack(pady=5)

        self.add_vox_button = ctk.CTkButton(self.block_area, text="Add Vox AC30", command=lambda: self.add_block(self.vox_ac30))
        self.add_vox_button.pack(pady=5)

        # Slider para ajustar o tom do Speaker
        self.tone_slider = ctk.CTkSlider(self.block_area, from_=-1, to=1, command=self.adjust_tone, number_of_steps=20)
        self.tone_slider.set(0)  # Valor inicial do tom
        self.tone_slider.pack(pady=10)

        # Botão para mostrar a cadeia atual
        self.show_chain_button = ctk.CTkButton(self.block_area, text="Show Chain", command=self.show_chain)
        self.show_chain_button.pack(pady=10)

        # Área de exibição da cadeia de processamento (inicialmente vazia)
        self.chain_display_label = ctk.CTkLabel(self.chain_area, text="Cadeia de Efeitos", font=("Arial", 16))
        self.chain_display_label.pack(pady=10)

    def adjust_tone(self, value):
        """ Ajusta o tom do falante com base no slider """
        self.speaker.set_tone(float(value))  # Atualiza o tom do falante com o valor do slider

    def add_block(self, block):
        """ Adiciona um bloco à cadeia de sinal """
        self.chain.add_block(block)
        self.update_chain_display()

    def update_chain_display(self):
        """ Atualiza a exibição da cadeia de processamento """
        for widget in self.chain_area.winfo_children():
            if isinstance(widget, ctk.CTkLabel):  # Remove apenas as labels que mostram a cadeia
                widget.destroy()

        if self.chain.blocks:
            for i, block in enumerate(self.chain.blocks):
                label = ctk.CTkLabel(self.chain_area, text=f"{i+1}. {block.__class__.__name__}")
                label.pack(pady=2)
        else:
            label = ctk.CTkLabel(self.chain_area, text="Sem efeitos na cadeia.")
            label.pack(pady=2)

    def show_chain(self):
        """ Exibe a cadeia atual no console e na interface """
        print("Cadeia atual:", " -> ".join([block.__class__.__name__ for block in self.chain.blocks]))
        self.update_chain_display()

# Iniciar a aplicação
if __name__ == "__main__":
    root = ctk.CTk()  # Cria a janela principal
    app = FXRoutingApp(root)  # Inicializa o aplicativo gráfico
    root.mainloop()  # Inicia o loop de eventos do Tkinter
