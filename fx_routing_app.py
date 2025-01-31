import customtkinter as ctk
from signal_chain import SignalChain
from effects import Distortion, Delay, HallReverb
from models.vox_ac30 import VoxAC30

class FXRoutingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FX Routing")
        self.root.geometry("900x600")
        self.chain = SignalChain()
        self.selected_effect = None  

        # Configuração do tema
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue")  

        self.create_sidebar()
        self.create_chain_area()
        self.create_controls_area()

    def create_sidebar(self):
        """ Cria o menu lateral expansível/retrátil. """
        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y, padx=5, pady=5)

        self.toggle_button = ctk.CTkButton(self.sidebar, text="Menu", command=self.toggle_menu)
        self.toggle_button.pack(pady=5)

        self.menu_frame = ctk.CTkFrame(self.sidebar)
        self.menu_frame.pack(fill=ctk.BOTH, expand=True)

        self.add_distortion_button = ctk.CTkButton(self.menu_frame, text="Add Distortion", 
                                                   command=lambda: self.add_block(Distortion()))
        self.add_distortion_button.pack(pady=2)

        self.add_delay_button = ctk.CTkButton(self.menu_frame, text="Add Delay", 
                                              command=lambda: self.add_block(Delay()))
        self.add_delay_button.pack(pady=2)

        self.add_reverb_button = ctk.CTkButton(self.menu_frame, text="Add Hall Reverb", 
                                               command=lambda: self.add_block(HallReverb(mix=0.5, decay=2.0, pre_delay=50, 
                                                                                         cut_grave=100, cut_agudo=8000, volume=1.0)))
        self.add_reverb_button.pack(pady=2)

        self.add_vox_button = ctk.CTkButton(self.menu_frame, text="Add Vox AC30", 
                                            command=lambda: self.add_block(VoxAC30()))
        self.add_vox_button.pack(pady=2)

        self.menu_visible = True  

    def toggle_menu(self):
        """ Mostra ou esconde o menu lateral. """
        if self.menu_visible:
            self.menu_frame.pack_forget()
        else:
            self.menu_frame.pack(fill=ctk.BOTH, expand=True)
        self.menu_visible = not self.menu_visible

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
        """ Adiciona um efeito à cadeia de sinal e atualiza a interface. """
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
            if isinstance(value, (int, float)):  # Só adiciona sliders para valores numéricos
                frame = ctk.CTkFrame(self.controls_container)
                frame.pack(fill=ctk.X, pady=2)

                label = ctk.CTkLabel(frame, text=param.capitalize(), width=100)
                label.pack(side=ctk.LEFT)

                slider = ctk.CTkSlider(frame, from_=0, to=10, number_of_steps=100, command=lambda v, p=param: self.update_param(p, v))
                slider.set(value)
                slider.pack(side=ctk.RIGHT, fill=ctk.X, expand=True)

    def update_param(self, param, value):
        """ Atualiza o parâmetro do efeito selecionado. """
        if self.selected_effect:
            setattr(self.selected_effect, param, float(value))

    def process_signal(self):
        """ Processa o sinal através da cadeia de efeitos. """
        signal = 1.0  # Defina o sinal inicial (valor de exemplo)
        
        # Processa o sinal por cada efeito da cadeia
        for block in self.chain.blocks:
            signal = block.process(signal)
        
        return signal


# Iniciar a aplicação
if __name__ == "__main__":
    root = ctk.CTk()
    app = FXRoutingApp(root)
    root.mainloop()
