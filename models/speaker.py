class Speaker:
    def __init__(self, model="Generic Speaker", tone=0.0):
        self.model = model  # Define o modelo do falante
        self.name = f"Speaker: {self.model}"
        self.tone = tone  # Agora aceita o parâmetro tone

    def set_tone(self, tone_value):
        #Ajusta o tom do falante, de grave a agudo. """
        self.tone = tone_value
        print(f"Tom ajustado para: {self.tone}")
        
    def process(self, signal):
        # Simula a resposta do falante com base no tom. """
        if self.tone < 0:
            # Tom mais grave, aumenta os graves
            signal *= 1 + (0.5 * abs(self.tone))  # Aumenta a intensidade do sinal de graves
        elif self.tone > 0:
            # Tom mais agudo, aumenta os agudos (simulado aqui como atenuação)
            signal *= 1 - (0.5 * self.tone)  # Diminui a intensidade do sinal de agudos
        else:
            # Tom neutro
            signal *= 1  # Não altera o sinal

        # Atenuação geral do falante (simulada)
        return signal * 0.9  # Atenua o sinal do falante em 10%
