from typing import Dict
from Models.VendingMachine import VendingMachine


class Administrator:
    def __init__(self, vending_machine: VendingMachine):
        self.vending_machine = vending_machine

    # def refill_machine(self, products: Dict[str, Dict[str, int]], money: Dict[int, int]):
    #     """
    #     Refills products and money in the vending machine in a single operation.

    #     Args:
    #     products (Dict[str, Dict[str, int]]): Dictionary of products to add or update.
    #                           Format: {'product_name': {'price': price, 'quantity': quantity}}
    #     money (Dict[int, int]): Dictionary of money to add.
    #                 Format: {denomination: quantity}
    #     """
    #     for product_name, details in products.items():
    #         self.vending_machine.add_product(
    #             product_name, details['price'], details['quantity'])

    #     for denomination, quantity in money.items():
    #         self.vending_machine.add_money(denomination, quantity)

    #     print("Máquina reabastecida exitosamente.")

    def generate_full_report(self):
        """
        Generates a complete report of the vending machine's status.
        """
        print("=== REPORTE COMPLETO DE LA MÁQUINA EXPENDEDORA ===")
        print("\nProductos:")
        self.vending_machine.product_report()
        print("\nDinero:")
        self.vending_machine.money_report()
        print("=== FIN DEL REPORTE ===")

    # Direct access methods to the vending machine
    def add_product(self, name: str, price: int, quantity: int):
        return self.vending_machine.add_product(name, price, quantity)

    def add_money(self, denomination: int, quantity: int):
        return self.vending_machine.add_money(denomination, quantity)

    def remove_money(self, amount: int):
        return self.vending_machine.remove_money(amount)

    def product_report(self):
        return self.vending_machine.product_report()

    def money_report(self):
        return self.vending_machine.money_report()
