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
