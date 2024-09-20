from typing import Dict
from VendingMachine import VendingMachine


class Administrator:
    def __init__(self, vending_machine: VendingMachine):
        self.vending_machine = vending_machine

    def refill_machine(self, products: Dict[str, Dict[str, int]], money: Dict[int, int]):
        """
        Repone productos y dinero en la máquina expendedora en una sola operación.

        Args:
        products (Dict[str, Dict[str, int]]): Diccionario de productos a agregar o actualizar.
                                              Formato: {'nombre_producto': {'price': precio, 'quantity': cantidad}}
        money (Dict[int, int]): Diccionario de dinero a agregar. 
                                Formato: {denominacion: cantidad}
        """
        for product_name, details in products.items():
            self.vending_machine.add_product(
                product_name, details['price'], details['quantity'])

        for denomination, quantity in money.items():
            self.vending_machine.add_money(denomination, quantity)

        print("Máquina reabastecida exitosamente.")

    def generate_full_report(self):
        """
        Genera un reporte completo del estado de la máquina expendedora.
        """
        print("=== REPORTE COMPLETO DE LA MÁQUINA EXPENDEDORA ===")
        print("\nProductos:")
        self.vending_machine.product_report()
        print("\nDinero:")
        self.vending_machine.money_report()
        print("=== FIN DEL REPORTE ===")

    def optimize_change(self):
        """
        Optimiza las denominaciones de dinero en la máquina para facilitar el cambio.
        """
        # Implementación de la lógica de optimización
        # Este es un método específico del administrador que no existe en la máquina expendedora
        pass

    # Métodos de acceso directo a la máquina expendedora
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
