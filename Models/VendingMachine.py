
from typing import Dict, List, Tuple

from .Product import Product


class VendingMachine:
    """
    Represents a vending machine with methods to add products, add money,
remove money, generate reports, and process purchases.

Attributes:
    - products (Dict[str, Product]): A dictionary that stores the products in the vending machine, where the key is the name of the product and the value is an instance of the Product class.
    - money (Dict[int, int]): A dictionary that stores the money in the vending machine, where the key is the denomination of the money and the value is the quantity of that denomination.
    """

    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.money: Dict[int, int] = {}

    def add_product(self, name: str, price: int, quantity: int) -> None:
        """
        Adds a product to the vending machine.
        Returns:
        None
        """

        if len(self.products) >= 50:
            print(
                "Se ha alcanzado el limite de productos en la maquina, no es posible agregar más.")
            return

        if name in self.products:
            self.products[name].quantity += quantity
            # Update price in case it changed
            self.products[name].price = price
        else:
            self.products[name] = Product(name, price, quantity)

    def add_money(self, denomination: int, quantity: int) -> None:
        if denomination not in self.money:
            self.money[denomination] = 0

        self.money[denomination] += quantity

    def add_money_in_highest_denominations(self, money: int) -> bool:
        """
            Converts the entered money into the highest possible denominations
            and adds them using the add_money method. If it is not possible to add
            all the money due to reaching the limit, it returns False and reverts
            the added money.
            """
        # To record how much money was added for each denomination
        remaining_money = money
        added_money = {}

        # Available denominations, sorted from highest to lowest
        available_denominations = sorted(self.money.keys(), reverse=True)

        for denomination in available_denominations:
            if remaining_money >= denomination:
                # How many bills of this denomination
                quantity = remaining_money // denomination

                # Attempt to add the money with add_money
                initial_quantity = self.money[denomination]
                self.add_money(denomination, quantity)

                # Calculate how many were actually added
                added = self.money[denomination] - initial_quantity
                remaining_money -= denomination * added

                # Record how much money has been added for each denomination
                if added > 0:
                    added_money[denomination] = added

                # Check if there is no space left in the machine
                if self.money[denomination] == 100 and remaining_money >= denomination:
                    # If we reach the limit, revert what was added
                    self.revert_added_money(added_money)
                    return False

        return True

    def revert_added_money(self, added_money: Dict[int, int]) -> None:
        """
        Revierte el dinero que se ha agregado a la máquina.

        Args:
            added_money (Dict[int, int]): Diccionario con las denominaciones y cantidades que se agregaron.
        """
        for denomination, quantity in added_money.items():
            self.money[denomination] -= quantity

    def has_sufficient_change(self, amount: int) -> bool:
        """
            Checks if the machine has enough change to return the specified amount.
            Returns:
            bool: True if there is enough change, False otherwise.
        """
        available_money = {denom: qty for denom, qty in self.money.items()}
        remaining_amount = amount

        for denomination in sorted(available_money.keys(), reverse=True):
            while available_money[denomination] > 0 and remaining_amount >= denomination:
                available_money[denomination] -= 1
                remaining_amount -= denomination

        return remaining_amount == 0

    def remove_money(self, amount: int) -> Dict[int, int]:
        removed_money = {}
        remaining_amount = amount

        for denomination in sorted(self.money.keys(), reverse=True):
            while self.money[denomination] > 0 and remaining_amount >= denomination:
                if denomination not in removed_money:
                    removed_money[denomination] = 0
                removed_money[denomination] += 1
                self.money[denomination] -= 1
                remaining_amount -= denomination

        return removed_money

    def product_report(self) -> None:
        total_value = 0
        n = 1
        print("Reporte de productos")
        for name, product in self.products.items():
            print(
                f"{n}. Nombre: {name}, Precio: {product.price}, Cantidad: {product.quantity}")
            n += 1
            total_value += product.price * product.quantity
        print(f"Valor total de los productos: {total_value}")

    def money_report(self) -> None:
        total_value = 0
        print("Reporte de dinero")
        for denomination, quantity in sorted(self.money.items()):
            print(f"Denominación: {denomination}, Cantidad: {quantity}")
            total_value += denomination * quantity
        print(f"Cantidad total de dinero: {total_value}")

    def process_purchase(self, product_name: str, quantity: int, money_inserted: int) -> Tuple[bool, Dict[int, int]]:
        if product_name not in self.products:
            print(f"ERROR: Producto '{product_name}' no encontrado")
            return False, {}

        product = self.products[product_name]

        if product.quantity < quantity:
            print(
                f"ERROR: No hay suficientes productos '{product_name}'. Disponible: {product.quantity}, Solicitado: {quantity}")
            return False, {}

        total_price = product.price * quantity

        if money_inserted < total_price:
            print(
                f"ERROR: No tiene suficiente dinero para realizar la compra. Requerido {total_price}, Ingresado: {money_inserted}")
            return False, {}

        if not self.add_money_in_highest_denominations(money_inserted):
            print("ERROR: Se excede la capacidad de la máquina. El dinero se devuelve..")
            return False, {}

        change_amount = money_inserted - total_price

        if not self.has_sufficient_change(change_amount):
            print(f"ERROR: La máquina no tiene suficiente cambio para devolver {
                  change_amount}. Se devuelve el dinero ingresado {money_inserted}.")
            return False, {}

        # If we reach here, we have enough product, the customer has enough money,
        # and the machine have enough change
        product.quantity -= quantity
        change = self.remove_money(change_amount)

        print(f"Compraste {quantity} {'unidad' if quantity == 1 else 'unidades'} de '{
              product_name}' por {total_price}, con {money_inserted}")
        return True, change

    def process_advanced_purchase(self, purchases: List[Tuple[str, int]], money_inserted: int) -> Tuple[bool, Dict[int, int]]:
        for product_name, quantity in purchases:
            if product_name not in self.products:
                print(f"ERROR: Producto '{product_name}' no encontrado.")
                return False, {}

            product = self.products[product_name]

            if product.quantity < quantity:
                print(
                    f"ERROR: No hay suficiente stock de'{product_name}'. Disponible: {product.quantity}")
                return False, {}

            total_price = product.price * quantity

        if money_inserted < total_price:
            print(
                f"ERROR: No tienes dinero suficiente para realizar la compra. Requerido: {total_price}, Ingresado: {money_inserted}")
            return False, {}

        if not self.add_money_in_highest_denominations(money_inserted):
            print("ERROR: Se excede la capacidad de la máquina. El dinero se devuelve.")
            return False, {}
        change_amount = money_inserted - total_price
        if not self.has_sufficient_change(change_amount):
            print(f"ERROR: La máquina no tiene suficiente cambio para devolver {
                  change_amount}. Se devuelve el dinero ingresado {money_inserted}.")
            return False, {}

        for product_name, quantity in purchases:
            self.products[product_name].quantity -= quantity
            print(
                f"Compraste {quantity} {'unidad' if quantity == 1 else 'unidades'} de '{product_name}' por {total_price}, con {money_inserted}")

        change = self.remove_money(money_inserted - total_price)
        return True, change
