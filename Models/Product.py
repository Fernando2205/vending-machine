
class Product:
    """
    Represents a product in the vending machine.
    Attributes:
        name (str): The name of the product.
        price (int): The price of the product.
        quantity (int): The quantity of the product available.
    """

    def __init__(self, name: str, price: int, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity
