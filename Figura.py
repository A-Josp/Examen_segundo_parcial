import math

class Figura:
    def __init__(self, tipo: str, radio: float):
        self.tipo = tipo.lower()
        self.radio = radio

    def area(self):
        if self.tipo == "circular":
            return math.pi * (self.radio ** 2)
        elif self.tipo == "esferica":
            return 4 * math.pi * (self.radio ** 2)
        else:
            raise ValueError("No se reconocio ninguna figura.")

    def volumen(self):
        if self.tipo == "esferica":
            return (4/3) * math.pi * (self.radio ** 3)
        elif self.tipo == "circular":
            return 0
        else:
            raise ValueError("No se reconocio ninguna figura.")



