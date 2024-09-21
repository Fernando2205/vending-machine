import re
from Models.VendingMachine import VendingMachine
from Configuration.config_loader import Config_folder


def process_quick_purchases1(file_name: str, vending_machine: VendingMachine):
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
                        total_value = 0
                        for p in change:
                            total_value += p * change[p]

                        print(f"Cambio {change} | {total_value}")
                else:
                    print("No se encontró linea de definicion para quick")
                contador += 1
        print("--------------------------------")
        # Process advanced quick purchases
        advanced_purchase_section = re.search(
            r'Quick Purchase 2.*', content, re.DOTALL)
        if advanced_purchase_section:
            # Skip the header line with [1:]
            for line in advanced_purchase_section.group().split('\n\n')[1:]:
                if line.strip():
                    try:
                        total_price = 0
                        purchases_str, money = line.strip('()').rsplit(';', 1)
                        purchases = [tuple(item.strip().rsplit(',', 1))
                                     for item in purchases_str.split(';')]
                        purchases = [(name.strip(), int(quantity))
                                     for name, quantity in purchases]

                        for name, quantity in purchases:
                            product = vending_machine.products[name]
                            total_price += product.price * quantity

                        print(f"{purchases_str} | Dinero: {
                              money} | Total: {total_price}")
                        success, change = vending_machine.process_advanced_purchase(
                            purchases, int(money))
                        if success:
                            total_value = 0
                            for p in change:
                                total_value += p * change[p]
                            print(f"Cambio: {change} | {total_value}")

                    except ValueError:
                        print(
                            "No se encontró linea de definición para quick purchase 2")

    except FileNotFoundError:
        print(f"ERROR: El archivo'{
              file_name}' no fue encontrado en la carpeta Configuration.")
