# Máquina Expendedora

Este proyecto implementa una máquina expendedora en Python. La máquina expendedora puede gestionar productos, procesar compras y manejar dinero.

## Características

- **Gestión de Productos**: Agregar, eliminar y actualizar productos en la máquina expendedora.
- **Gestión de Dinero**: Agregar y retirar dinero de la máquina expendedora.
- **Procesamiento de Compras**: Procesar compras de productos y devolver el cambio adecuado.
- **Reportes**: Generar reportes de productos y dinero disponibles en la máquina.

## Instalación

1. Clona el repositorio:

   ```sh
   git clone <https://github.com/Fernando2205/vending-machine.git>
   ```

## Uso

1. Sigue las instrucciones en pantalla para interactuar con la máquina expendedora.

## Archivos Principales

- `Main.py`: Archivo principal que ejecuta la máquina expendedora.
- `VendingMachine.py`: Contiene la clase `VendingMachine` y sus métodos.
- `Product.py`: Contiene la clase `Product`.
- `configuracion.txt`: Archivo de configuración opcional para productos y dinero.

<!-- ## Ejemplos de Uso

### Agregar un Producto

```python
from maquina_expendedora import MaquinaExpendedora
from producto import Producto

maquina = MaquinaExpendedora()
producto = Producto(codigo=1, nombre="Soda", precio=150, cantidad=10)
maquina.agregar_producto(producto)
``` -->
