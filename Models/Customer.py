from typing import Dict, List, Tuple
from Models.VendingMachine import VendingMachine


class Customer:
    def __init__(self, vending_machine: VendingMachine):
        self.vending_machine = vending_machine
        self.inserted_money = 0
        self.purchases = []

    def insert_money(self, money: Dict[int, int]) -> int:
        """
        Inserts money into the vending machine.

        Args:
        money (Dict[int, int]): A dictionary where the key is the denomination
                    and the value is the quantity of bills/coins.

        Returns:
        int: The total amount of money inserted.
        """
        total = 0
        for denomination, quantity in money.items():
            if denomination in self.vending_machine.money:
                total += denomination * quantity
                self.vending_machine.add_money(denomination, quantity)
            else:
                print(f"Denominación {denomination} no aceptada.")
        self.inserted_money += total
        print(f"Total insertado: {self.inserted_money}")
        return self.inserted_money

    def select_product(self, product_name: str, quantity: int) -> bool:
        """
        Selects a product and the quantity to purchase.

        Args:
        product_name (str): Name of the product.
        quantity (int): Quantity of the product to purchase.

        Returns:
        bool: True if the selection is valid, False otherwise.
        """
        if product_name not in self.vending_machine.products:
            print(f"Producto '{product_name}' no disponible.")
            return False

        product = self.vending_machine.products[product_name]
        total_price = product.price * quantity

        if product.quantity < quantity:
            print(f"No hay suficiente stock de '{
                  product_name}'. Disponible: {product.quantity}")
            return False

        if self.inserted_money < total_price:
            print(f"Dinero insuficiente. Necesita: {
                  total_price}, Insertado: {self.inserted_money}")
            return False

        self.purchases.append((product_name, quantity))
        self.inserted_money -= total_price
        print(f"Seleccionado: {quantity} x {product_name}")
        return True

    def can_buy_cheapest(self) -> bool:
        """
        Checks if the customer has enough money to buy the cheapest product.

        Returns:
        bool: True if they can buy the cheapest product, False otherwise.
        """
        if not self.vending_machine.products:
            return False
        cheapest_price = min(
            product.price for product in self.vending_machine.products.values())
        return self.inserted_money >= cheapest_price

    def finish_transaction(self) -> Dict[int, int]:
        """
        Finishes the transaction and returns the optimized change.

        Returns:
        Dict[int, int]: A dictionary with the change, where the key is the denomination
                and the value is the quantity of bills/coins.
        """
        change = self.vending_machine.remove_money(self.inserted_money)

        print("Compra finalizada. Sus productos:")
        for product_name, quantity in self.purchases:
            print(f"- {quantity} x {product_name}")

        if change:
            print("Su cambio:")
            for denomination, quantity in change.items():
                print(f"  {quantity} x ${denomination}")
        else:
            print("No hay cambio.")

        self.inserted_money = 0
        self.purchases = []
        return change

    def shop(self):
        """
        Starts the interactive shopping process.
        """
        print("Bienvenido a la máquina expendedora.")
        while True:
            print("1. Insertar dinero")
            print("2. Comprar producto")
            print("3. Finalizar compra")
            action = input("¿Qué desea hacer?").lower()

            if action == "1":
                denominations = {1: 0, 5: 0, 10: 0, 20: 0, 50: 0, }
                for denom in denominations:
                    qty = int(
                        input(f"Cantidad de billetes de ${denom}: "))
                    denominations[denom] = qty
                self.insert_money(denominations)

            elif action == "2":
                product_name = input("Nombre del producto: ")
                quantity = int(input("Cantidad: "))
                if self.select_product(product_name, quantity):
                    if not self.can_buy_cheapest():
                        print(
                            "No tiene suficiente dinero para comprar más productos.")
                        self.finish_transaction()
                        break

            elif action == "3":
                self.finish_transaction()
                break

            else:
                print(
                    "Acción no reconocida. Por favor, ingrese una opción válida.")
