from models import VoxAC30, Preamp, Equalizer, PowerAmp, Speaker
from effects import Distortion
from utils.audio_utils import normalize_signal
from signal_chain import SignalChain
from fx_routing_app import FXRoutingApp
import customtkinter as ctk # type: ignore

def main():
    # Criando os componentes do Vox AC30
    preamp = Preamp(volume=2.0)
    equalizer = Equalizer(bass=1.0, mid=1.0, treble=1.5)
    poweramp = PowerAmp(volume=3.0)
    speaker = Speaker(model="Celestion Blue")

    # Criando o amplificador com os componentes
    vox_ac30 = VoxAC30(preamp, equalizer, poweramp, speaker)

    # Configurações iniciais
    signal_chain = SignalChain()
    signal_chain.add_block(Distortion(gain=2.0))
    signal_chain.add_block(vox_ac30)  # CERTO!

    # Processamento do sinal
    input_signal = 0.5  # Exemplo de sinal de entrada (ajustar conforme necessário)
    output_signal = signal_chain.process(input_signal)
    

    output_signal = normalize_signal(output_signal)

    print(f"Sinal de saída: {output_signal}")

    # Iniciando a interface gráfica
    root = ctk.CTk()  # Cria a janela principal
    app = FXRoutingApp(root)  # Inicializa o aplicativo gráfico
    root.mainloop()  # Inicia o loop de eventos do customTkinter

if __name__ == "__main__":
    main()
