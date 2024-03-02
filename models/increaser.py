import shared_vars as sv


class GeneralIncreaser:
    def __init__(self):
        self.increase_border = 0
        self.increaser_1 = Increaser()
        self.increaser_5 = Increaser()
        self.increaser_15 = Increaser()


class Increaser:
    def __init__(self):
        self.offon = 0
        self.triger = False