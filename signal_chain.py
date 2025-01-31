class SignalChain:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def remove_block(self, block):
        if block in self.blocks:
            self.blocks.remove(block)

    def process(self, signal):
        for block in self.blocks:
            signal = block.process(signal)  # Passa o sinal por cada efeito
        return signal
