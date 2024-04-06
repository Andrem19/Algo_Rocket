

class Position:
    def __init__(self, amount, entry_price):
        self.amount_coin = amount
        self.base_amount = amount
        self.zero_point = entry_price
        self.level = 1
