import re
from Models.VendingMachine import VendingMachine

Config_folder = "Configuration/"


def load_configuration(file_name: str, vending_machine: VendingMachine):
    """
    Loads the configuration file and initializes the vending machine with
the specified products and money.
    """

    try:
        with open(Config_folder + file_name, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse money configuration
        money_section = re.search(r'Dollars.*?(?=\n\n)', content, re.DOTALL)
        if money_section:
            # Skip the header line
            for line in money_section.group().split('\n')[1:]:
                parts = line.split(',')
                if len(parts) == 2:
                    denomination, quantity = map(int, parts)
                    vending_machine.add_money(denomination, quantity)
                else:
                    print(
                        f"AVISO: Linea de definicion de dinero incorrecta {line}")

        # Parse products configuration
        products_section = re.search(
            r'Products.*?(?=\n\n)', content, re.DOTALL)
        if products_section:
            a = 1
            # Skip the header line with [1:]
            for line in products_section.group().split('\n')[1:]:

                parts = line.split(',')
                if len(parts) == 3:
                    name, price, quantity = parts
                    vending_machine.add_product(
                        name.strip(), int(price), int(quantity))
                    print(f"{a} producto agregado")
                    print(parts)
                    a += 1

                else:
                    print(
                        f"AVISO: Linea de definición de producto incorrecta: \n{line}")

    except FileNotFoundError:
        print(f"ERROR: El archivo'{
              file_name}' no fue encontrado en la carpeta Configuration.")


def process_quick_purchases(file_name: str, vending_machine: VendingMachine):
    """
     Processes quick purchases from the configuration file.
    """
    try:
        with open(Config_folder + file_name, 'r', encoding='utf-8') as file:
            content = file.read()

        # Process basic quick purchases
        quick_purchase_section = re.search(
            r'Quick Purchase.*?(?=\n\n)', content, re.DOTALL)
        if quick_purchase_section:
            contador = 1
            # Skip the header line with [1:]
            for line in quick_purchase_section.group().split('\n')[1:]:
                parts = line.split(',')
                if len(parts) == 3:
                    name, quantity, money = parts
                    print(contador)
                    success, change = vending_machine.process_purchase(
                        name.strip(), int(quantity), int(money))
                    if success:
                        print(f"Cambio {change}")
                    print()
                else:
                    print("No se encontró linea de definicion para quick")
                contador += 1
        print("--------------------------------")
        # Process advanced quick purchases
        advanced_purchase_section = re.search(
            r'Quick Purchase 2.*', content, re.DOTALL)
        if advanced_purchase_section:
            # Skip the header line with [1:]
            for line in advanced_purchase_section.group().split('\n')[1:]:
                if line.strip():
                    try:
                        purchases_str, money = line.strip('()').rsplit(';', 1)
                        purchases = [tuple(item.strip().rsplit(',', 1))
                                     for item in purchases_str.split(';')]
                        purchases = [(name.strip(), int(quantity))
                                     for name, quantity in purchases]
                        print(f"{purchases_str} | plata: {money}")
                        success, change = vending_machine.process_advanced_purchase(
                            purchases, int(money))
                        if success:
                            print(f"Cambio: {change}")
                        print()
                    except ValueError:
                        print(
                            "No se encontró linea de definición para quick purchase 2")

    except FileNotFoundError:
        print(f"ERROR: El archivo'{
              file_name}' no fue encontrado en la carpeta Configuration.")
