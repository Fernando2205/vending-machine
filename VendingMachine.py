
from typing import Dict, List, Tuple

from Product import Product


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

        if self.money[denomination] + quantity > 100:
            print(
                f"AVISO: La maquina no puede tener más de 100 billetes de ${denomination}, se agregará la máxima cantidad posible")
            quantity = 100 - self.money[denomination]

        self.money[denomination] += quantity

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

        if remaining_amount > 0:
            print(
                f"AVISO: No hay suficiente dinero para sacar {amount}. Devueltos {amount - remaining_amount}.")
            for denomination, quantity in removed_money.items():
                self.money[denomination] += quantity
            return {}

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

    def process_purchase(self, product_name: str, quantity: int, money: int) -> Tuple[bool, Dict[int, int]]:
        if product_name not in self.products:
            print(f"ERROR: Producto '{product_name}' no encontrado")
            return False, {}

        product = self.products[product_name]

        if product.quantity < quantity:
            print(
                f"ERROR: No hay suficientes productos'{product_name}'. Disponible: {product.quantity}")
            return False, {}

        total_price = product.price * quantity

        if money < total_price:
            print(
                f"ERROR: No tiene suficiente dinero para realizar la compra. Requerido {total_price}, Ingresado: {money}")
            return False, {}

        product.quantity -= quantity
        if product.quantity < 0:
            product.quantity = 0
        change = self.remove_money(money - total_price)

        print(
            f"Compraste {quantity} {'unidad' if quantity == 1 else 'unidades'} de '{product_name}' por {total_price}")
        return True, change

    def process_advanced_purchase(self, purchases: List[Tuple[str, int]], money: int) -> Tuple[bool, Dict[int, int]]:
        total_price = 0
        for product_name, quantity in purchases:
            if product_name not in self.products:
                print(f"ERROR: Producto '{product_name}' no encontrado.")
                return False, {}

            product = self.products[product_name]

            if product.quantity < quantity:
                print(
                    f"ERROR: No hay suficiente stock de'{product_name}'. Disponible: {product.quantity}")
                return False, {}

            total_price += product.price * quantity

        if money < total_price:
            print(
                f"ERROR: No tienes dinero suficiente para realizar la compra. Requerido: {total_price}, Ingresado: {money}")
            return False, {}

        for product_name, quantity in purchases:
            self.products[product_name].quantity -= quantity
            print(
                f"Compraste {quantity} {'unidad' if quantity == 1 else 'unidades'} de '{product_name}' por {total_price}")

        change = self.remove_money(money - total_price)
        return True, change
