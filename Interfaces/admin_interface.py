from Models.Administrator import Administrator


def run_admin_interface(admin: Administrator):
    while True:
        print("\n--- Interfaz de Administrador ---")
        print("1. Reporte de Productos")
        print("2. Reporte de Dinero")
        print("3. Agregar Producto")
        print("4. Agregar Dinero")
        print("5. Retirar Dinero")
        print("6. Volver al Menú Principal")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            admin.product_report()
        elif choice == '2':
            admin.money_report()
        elif choice == '3':
            name = input("Nombre del producto: ")
            price = int(input("Precio: "))
            quantity = int(input("Cantidad: "))
            admin.add_product(name, price, quantity)
        elif choice == '4':
            denomination = int(input("Denominación: "))
            quantity = int(input("Cantidad: "))
            admin.add_money(denomination, quantity)
        elif choice == '5':
            amount = int(input("Cantidad a retirar: "))
            admin.remove_money(amount)
        elif choice == '6':
            break
        else:
            print("Opción inválida, intente de nuevo.")
