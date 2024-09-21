"""
This script represents a vending machine program that allows users to add products,
 add money, remove money, generate product and money reports, and process purchases.

- main: The main function that runs the vending machine program.
Note: This script requires a configuration file to be provided in order to initialize
the vending machine with products and money.

Author: Delio Fernando Palacios Viafara - 30000115782

"""

from Configuration.config_loader import load_configuration
from Configuration.quick_purchases1 import process_quick_purchases1
from Configuration.quick_purcharses2 import process_quick_purchases2
from Interfaces import admin_interface, customer_interface
from Models.Administrator import Administrator
from Models.Customer import Customer
from Models.VendingMachine import VendingMachine


def main():
    machine1 = VendingMachine()
    admin = Administrator(machine1)
    customer = Customer(machine1)

    while True:
        print("\n--- Menú Principal ---")
        print("1. Modo Cliente")
        print("2. Modo Administrador")
        print("3. Cargar configuración 1 (archivo)")
        print("4. Ejecutar compras 1 (archivo)")
        print("5 Cargar configuración 2 (archivo)")
        print("6. Ejecutar compras 2 (archivo)")
        print("7. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            customer_interface.run_customer_interface(customer)
        elif choice == '2':
            admin_interface.run_admin_interface(admin)
        elif choice == '3':
            config_file = 'ConfiguracionExercise.txt'
            print("Cargando configuración...")
            load_configuration(config_file, machine1)
            print("Configuración cargada.")
            #
        elif choice == '4':
            config_file = 'ConfiguracionExercise.txt'
            process_quick_purchases1(config_file, machine1)
        elif choice == '5':
            config_file2 = 'ConfiguracionExercise2.txt'
            print("Cargando configuración...")
            load_configuration(config_file2, machine1)
            print("Configuración cargada.")
        elif choice == '6':
            process_quick_purchases2(config_file2, machine1)
        elif choice == '7':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()
