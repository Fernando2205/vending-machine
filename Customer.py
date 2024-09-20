from typing import Dict, List, Tuple
from VendingMachine import VendingMachine


class Customer:
    def __init__(self, vending_machine: VendingMachine):
        self.vending_machine = vending_machine
        self.inserted_money = 0
        self.purchases = []

    def insert_money(self, money: Dict[int, int]) -> int:
        """
        Introduce dinero en la máquina expendedora.

        Args:
        money (Dict[int, int]): Un diccionario donde la clave es la denominación
                                y el valor es la cantidad de billetes/monedas.

        Returns:
        int: El total de dinero insertado.
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
        Selecciona un producto y la cantidad a comprar.

        Args:
        product_name (str): Nombre del producto.
        quantity (int): Cantidad del producto a comprar.

        Returns:
        bool: True si la selección es válida, False en caso contrario.
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
        Verifica si el cliente tiene suficiente dinero para comprar el producto más barato.

        Returns:
        bool: True si puede comprar el más barato, False en caso contrario.
        """
        if not self.vending_machine.products:
            return False
        cheapest_price = min(
            product.price for product in self.vending_machine.products.values())
        return self.inserted_money >= cheapest_price

    def finish_transaction(self) -> Dict[int, int]:
        """
        Finaliza la transacción y devuelve el cambio optimizado.

        Returns:
        Dict[int, int]: Un diccionario con el cambio, donde la clave es la denominación
                        y el valor es la cantidad de billetes/monedas.
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
        Inicia el proceso de compra interactivo.
        """
        print("Bienvenido a la máquina expendedora.")
        while True:
            action = input(
                "¿Qué desea hacer? (insertar/comprar/finalizar): ").lower()

            if action == "insertar":
                # Ajusta según las denominaciones aceptadas
                denominations = {1: 0, 5: 0, 10: 0, 20: 0, 50: 0, 100: 0}
                for denom in denominations:
                    qty = int(
                        input(f"Cantidad de billetes/monedas de ${denom}: "))
                    denominations[denom] = qty
                self.insert_money(denominations)

            elif action == "comprar":
                product_name = input("Nombre del producto: ")
                quantity = int(input("Cantidad: "))
                if self.select_product(product_name, quantity):
                    if not self.can_buy_cheapest():
                        print(
                            "No tiene suficiente dinero para comprar más productos.")
                        self.finish_transaction()
                        break

            elif action == "finalizar":
                self.finish_transaction()
                break

            else:
                print(
                    "Acción no reconocida. Por favor, elija 'insertar', 'comprar' o 'finalizar'.")
