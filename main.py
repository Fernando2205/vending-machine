"""
This script represents a vending machine program that allows users to add products,
 add money, remove money, generate product and money reports, and process purchases.

- process_quick_purchases: Processes quick purchases from the configuration file.
- main: The main function that runs the vending machine program.
Note: This script requires a configuration file to be provided in order to initialize
the vending machine with products and money.

Author: Delio Fernando Palacios Viafara - 30000115782

"""

import re

from VendingMachine import VendingMachine


def load_configuration(file_path: str, vending_machine: VendingMachine):
    """
    Loads the configuration file and initializes the vending machine with
the specified products and money.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
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
        print(f"ERROR: La ruta'{file_path}' no fue encontrada.")


def process_quick_purchases(file_path: str, vending_machine: VendingMachine):
    """
     Processes quick purchases from the configuration file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Process basic quick purchases
        quick_purchase_section = re.search(
            r'Quick Purchase.*?(?=\n\n)', content, re.DOTALL)
        if quick_purchase_section:
            # Skip the header line with [1:]
            for line in quick_purchase_section.group().split('\n')[1:]:
                parts = line.split(',')
                if len(parts) == 3:
                    name, quantity, money = parts
                    success, change = vending_machine.process_purchase(
                        name.strip(), int(quantity), int(money))
                    if success:
                        print(f"Cambio {change}")
                    print()
                else:
                    print("No se encontró linea de definicion para quick")
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
        print(f"ERROR: La ruta'{file_path}' no fue encontrada.")
    # except Exception as e:
    #     print(f"Error processing quick purchases: {str(e)}")


def main():
    """Main function that runs the vending machine program."""
    vending_machine = VendingMachine()
    config_file = 'ConfiguracionExercise.txt'

    print("Loading configuration...")
    load_configuration(config_file, vending_machine)
    print("Configuration loaded.")

    while True:
        print("\n1. Process Quick Purchases")
        print("2. Product Report")
        print("3. Money Report")
        print("4. Exit")
        choice = input("Seleccionar opcion: ")

        if choice == '1':
            process_quick_purchases(config_file, vending_machine)
        elif choice == '2':
            vending_machine.product_report()
        elif choice == '3':
            vending_machine.money_report()
        elif choice == '4':
            break
        else:
            print("Opcion inválida, seleccione otra.")


if __name__ == "__main__":
    main()
