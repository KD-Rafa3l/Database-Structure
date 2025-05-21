import sys
import mysql.connector
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                            QComboBox, QMessageBox, QTabWidget, QFormLayout, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',  # Cambiar por tu usuario
                password='Nath@ly+22.',  # Cambiar por tu contraseña
                database='Libreria_papeleria',
                auth_plugin='mysql_native_password'
            )
            if self.connection.is_connected():
                print("¡Conexión exitosa a MySQL!")
                return True
        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error de Conexión a la Base de Datos")
            msg.setInformativeText(f"No se pudo conectar a la base de datos:\n{e}\n\n"
                                 "Verifique que:\n"
                                 "1. MySQL esté corriendo\n"
                                 "2. Las credenciales sean correctas\n"
                                 "3. La base de datos 'libreria_papeleria' exista")
            msg.setWindowTitle("Error")
            msg.exec_()
            return False

    def execute_query(self, query, params=None, fetch=False):
        if not self.connection or not self.connection.is_connected():
            if not self.connect_to_db():
                return None

        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.lastrowid if "INSERT" in query.upper() else None
            return result
        except mysql.connector.Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            cursor.close()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        if not self.db.connection:
            sys.exit(1)

        self.setWindowTitle("Sistema de Gestión - Librería/Papelería")
        self.setGeometry(100, 100, 1000, 700)

        # Variables para ventas
        self.current_sale_items = []
        self.current_sale_total = 0.0

        # Crear pestañas principales
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Crear las pestañas
        self.create_product_tab()
        self.create_client_tab()
        self.create_sale_tab()
        self.create_inventory_tab()
        self.create_report_tab()
        self.create_employee_tab()  # Nueva pestaña para empleados

        # Cargar datos iniciales
        self.load_initial_data()

    def create_product_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Formulario de producto
        form = QFormLayout()
        
        self.product_id = QLineEdit()
        self.product_id.setReadOnly(True)
        self.product_name = QLineEdit()
        self.product_barcode = QLineEdit()
        self.product_description = QLineEdit()
        self.product_purchase = QLineEdit()
        self.product_price = QLineEdit()
        self.product_stock = QLineEdit()
        self.product_min_stock = QLineEdit("5")
        self.product_category = QComboBox()
        self.product_supplier = QComboBox()
        self.product_active = QComboBox()
        self.product_active.addItems(["Activo", "Inactivo"])

        form.addRow("ID:", self.product_id)
        form.addRow("Nombre*:", self.product_name)
        form.addRow("Código Barras:", self.product_barcode)
        form.addRow("Descripción:", self.product_description)
        form.addRow("Precio Compra*:", self.product_purchase)
        form.addRow("Precio Venta*:", self.product_price)
        form.addRow("Stock Inicial:", self.product_stock)
        form.addRow("Stock Mínimo:", self.product_min_stock)
        form.addRow("Categoría*:", self.product_category)
        form.addRow("Proveedor:", self.product_supplier)
        form.addRow("Estado:", self.product_active)

        # Botones
        btn_layout = QHBoxLayout()
        self.add_product_btn = QPushButton("Agregar")
        self.add_product_btn.clicked.connect(self.add_product)
        self.update_product_btn = QPushButton("Actualizar")
        self.update_product_btn.clicked.connect(self.update_product)
        self.delete_product_btn = QPushButton("Eliminar")
        self.delete_product_btn.clicked.connect(self.delete_product)
        self.clear_product_btn = QPushButton("Limpiar")
        self.clear_product_btn.clicked.connect(self.clear_product_form)

        btn_layout.addWidget(self.add_product_btn)
        btn_layout.addWidget(self.update_product_btn)
        btn_layout.addWidget(self.delete_product_btn)
        btn_layout.addWidget(self.clear_product_btn)

        # Tabla de productos
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(9)
        self.products_table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Precio", "Stock", "Categoría", "Proveedor", "Código", "Mínimo", "Estado"]
        )
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.cellClicked.connect(self.load_product_data)

        # Añadir al layout
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        layout.addWidget(self.products_table)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Productos")

    def create_client_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Formulario de cliente
        form = QFormLayout()
        
        self.client_id = QLineEdit()
        self.client_id.setReadOnly(True)
        self.client_name = QLineEdit()
        self.client_lastname = QLineEdit()
        self.client_phone = QLineEdit()
        self.client_email = QLineEdit()
        self.client_address = QLineEdit()
        self.client_rfc = QLineEdit()
        self.client_points = QLineEdit()
        self.client_points.setReadOnly(True)

        form.addRow("ID:", self.client_id)
        form.addRow("Nombre*:", self.client_name)
        form.addRow("Apellidos:", self.client_lastname)
        form.addRow("Teléfono:", self.client_phone)
        form.addRow("Email:", self.client_email)
        form.addRow("Dirección:", self.client_address)
        form.addRow("RFC:", self.client_rfc)
        form.addRow("Puntos:", self.client_points)

        # Botones
        btn_layout = QHBoxLayout()
        self.add_client_btn = QPushButton("Agregar")
        self.add_client_btn.clicked.connect(self.add_client)
        self.update_client_btn = QPushButton("Actualizar")
        self.update_client_btn.clicked.connect(self.update_client)
        self.delete_client_btn = QPushButton("Eliminar")
        self.delete_client_btn.clicked.connect(self.delete_client)
        self.clear_client_btn = QPushButton("Limpiar")
        self.clear_client_btn.clicked.connect(self.clear_client_form)

        btn_layout.addWidget(self.add_client_btn)
        btn_layout.addWidget(self.update_client_btn)
        btn_layout.addWidget(self.delete_client_btn)
        btn_layout.addWidget(self.clear_client_btn)

        # Tabla de clientes
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(8)
        self.clients_table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Apellidos", "Teléfono", "Email", "Dirección", "RFC", "Puntos"]
        )
        self.clients_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.clients_table.cellClicked.connect(self.load_client_data)

        # Añadir al layout
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        layout.addWidget(self.clients_table)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Clientes")

    def create_sale_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Formulario de venta
        form = QFormLayout()
        
        self.sale_id = QLineEdit()
        self.sale_id.setReadOnly(True)
        self.sale_date = QDateEdit(QDate.currentDate())
        self.sale_date.setCalendarPopup(True)
        self.sale_client = QComboBox()
        self.sale_employee = QComboBox()
        self.sale_payment = QComboBox()
        self.sale_payment.addItems(["Efectivo", "Tarjeta", "Transferencia"])

        form.addRow("ID Venta:", self.sale_id)
        form.addRow("Fecha:", self.sale_date)
        form.addRow("Cliente*:", self.sale_client)
        form.addRow("Empleado*:", self.sale_employee)
        form.addRow("Método Pago*:", self.sale_payment)

        # Sección para agregar productos
        product_layout = QHBoxLayout()
        self.sale_product = QComboBox()
        self.sale_quantity = QLineEdit("1")
        self.sale_price = QLineEdit()
        self.sale_price.setReadOnly(True)
        self.sale_stock = QLineEdit()
        self.sale_stock.setReadOnly(True)

        product_layout.addWidget(QLabel("Producto*:"))
        product_layout.addWidget(self.sale_product)
        product_layout.addWidget(QLabel("Cantidad*:"))
        product_layout.addWidget(self.sale_quantity)
        product_layout.addWidget(QLabel("Precio:"))
        product_layout.addWidget(self.sale_price)
        product_layout.addWidget(QLabel("Stock:"))
        product_layout.addWidget(self.sale_stock)

        self.add_to_sale_btn = QPushButton("Agregar a Venta")
        self.add_to_sale_btn.clicked.connect(self.add_product_to_sale)
        self.remove_from_sale_btn = QPushButton("Quitar Seleccionado")
        self.remove_from_sale_btn.clicked.connect(self.remove_product_from_sale)

        # Tabla de productos en venta
        self.sale_items_table = QTableWidget()
        self.sale_items_table.setColumnCount(6)
        self.sale_items_table.setHorizontalHeaderLabels(
            ["ID", "Producto", "Cantidad", "P. Unitario", "Importe", "Stock"]
        )
        self.sale_items_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Totales
        totals_layout = QHBoxLayout()
        self.sale_subtotal = QLineEdit("0.00")
        self.sale_subtotal.setReadOnly(True)
        self.sale_iva = QLineEdit("0.00")
        self.sale_iva.setReadOnly(True)
        self.sale_total = QLineEdit("0.00")
        self.sale_total.setReadOnly(True)
        self.sale_points = QLineEdit("0")
        self.sale_points.setReadOnly(True)

        totals_layout.addWidget(QLabel("Subtotal:"))
        totals_layout.addWidget(self.sale_subtotal)
        totals_layout.addWidget(QLabel("IVA (16%):"))
        totals_layout.addWidget(self.sale_iva)
        totals_layout.addWidget(QLabel("Total:"))
        totals_layout.addWidget(self.sale_total)
        totals_layout.addWidget(QLabel("Puntos:"))
        totals_layout.addWidget(self.sale_points)

        # Botones finales
        btn_layout = QHBoxLayout()
        self.process_sale_btn = QPushButton("Procesar Venta")
        self.process_sale_btn.clicked.connect(self.process_sale)
        self.cancel_sale_btn = QPushButton("Cancelar")
        self.cancel_sale_btn.clicked.connect(self.cancel_sale)
        self.print_sale_btn = QPushButton("Imprimir Ticket")
        self.print_sale_btn.clicked.connect(self.print_sale)

        btn_layout.addWidget(self.process_sale_btn)
        btn_layout.addWidget(self.cancel_sale_btn)
        btn_layout.addWidget(self.print_sale_btn)

        # Añadir al layout
        layout.addLayout(form)
        layout.addWidget(QLabel("Detalle de Venta:"))
        layout.addLayout(product_layout)
        layout.addWidget(self.add_to_sale_btn)
        layout.addWidget(self.remove_from_sale_btn)
        layout.addWidget(self.sale_items_table)
        layout.addLayout(totals_layout)
        layout.addLayout(btn_layout)

        # Conectar eventos
        self.sale_product.currentIndexChanged.connect(self.update_product_price)
        self.sale_quantity.textChanged.connect(self.update_sale_totals)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Ventas")

    def create_inventory_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Filtros
        filter_layout = QHBoxLayout()
        self.inventory_filter_product = QComboBox()
        self.inventory_filter_product.addItem("Todos los productos", None)
        self.inventory_filter_type = QComboBox()
        self.inventory_filter_type.addItem("Todos los tipos", None)
        self.inventory_filter_type.addItems(["Entrada", "Salida", "Ajuste"])
        self.inventory_filter_date_from = QDateEdit(QDate.currentDate().addMonths(-1))
        self.inventory_filter_date_to = QDateEdit(QDate.currentDate())
        self.inventory_filter_btn = QPushButton("Filtrar")
        self.inventory_filter_btn.clicked.connect(self.load_inventory_data)

        filter_layout.addWidget(QLabel("Producto:"))
        filter_layout.addWidget(self.inventory_filter_product)
        filter_layout.addWidget(QLabel("Tipo:"))
        filter_layout.addWidget(self.inventory_filter_type)
        filter_layout.addWidget(QLabel("Desde:"))
        filter_layout.addWidget(self.inventory_filter_date_from)
        filter_layout.addWidget(QLabel("Hasta:"))
        filter_layout.addWidget(self.inventory_filter_date_to)
        filter_layout.addWidget(self.inventory_filter_btn)

        # Formulario de movimiento
        form = QFormLayout()
        self.inventory_id = QLineEdit()
        self.inventory_id.setReadOnly(True)
        self.inventory_product = QComboBox()
        self.inventory_type = QComboBox()
        self.inventory_type.addItems(["Entrada", "Salida", "Ajuste"])
        self.inventory_quantity = QLineEdit("1")
        self.inventory_reason = QLineEdit()
        self.inventory_date = QDateEdit(QDate.currentDate())
        self.inventory_date.setCalendarPopup(True)

        form.addRow("ID:", self.inventory_id)
        form.addRow("Producto*:", self.inventory_product)
        form.addRow("Tipo*:", self.inventory_type)
        form.addRow("Cantidad*:", self.inventory_quantity)
        form.addRow("Motivo:", self.inventory_reason)
        form.addRow("Fecha:", self.inventory_date)

        # Botones
        btn_layout = QHBoxLayout()
        self.add_inventory_btn = QPushButton("Registrar Movimiento")
        self.add_inventory_btn.clicked.connect(self.add_inventory_movement)
        self.clear_inventory_btn = QPushButton("Limpiar")
        self.clear_inventory_btn.clicked.connect(self.clear_inventory_form)

        btn_layout.addWidget(self.add_inventory_btn)
        btn_layout.addWidget(self.clear_inventory_btn)

        # Tabla de inventario
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(7)
        self.inventory_table.setHorizontalHeaderLabels(
            ["ID", "Fecha", "Producto", "Tipo", "Cantidad", "Motivo", "Referencia"]
        )
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.inventory_table.cellClicked.connect(self.load_inventory_data_row)

        # Añadir al layout
        layout.addLayout(filter_layout)
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        layout.addWidget(self.inventory_table)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Inventario")

    def create_report_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Reporte de productos bajos en stock
        self.low_stock_label = QLabel("Productos con Stock Bajo:")
        self.low_stock_table = QTableWidget()
        self.low_stock_table.setColumnCount(5)
        self.low_stock_table.setHorizontalHeaderLabels(
            ["ID", "Producto", "Categoría", "Stock Actual", "Stock Mínimo"]
        )

        # Reporte de productos más vendidos
        self.top_products_label = QLabel("Productos Más Vendidos:")
        self.top_products_table = QTableWidget()
        self.top_products_table.setColumnCount(5)
        self.top_products_table.setHorizontalHeaderLabels(
            ["ID", "Producto", "Categoría", "Unidades Vendidas", "Ingresos"]
        )

        # Reporte de ventas por cliente
        self.sales_by_client_label = QLabel("Ventas por Cliente:")
        self.sales_by_client_table = QTableWidget()
        self.sales_by_client_table.setColumnCount(5)
        self.sales_by_client_table.setHorizontalHeaderLabels(
            ["ID", "Cliente", "Total Ventas", "Monto Total", "Última Compra"]
        )

        # Botón para actualizar reportes
        self.refresh_reports_btn = QPushButton("Actualizar Reportes")
        self.refresh_reports_btn.clicked.connect(self.load_reports_data)

        # Añadir al layout
        layout.addWidget(self.low_stock_label)
        layout.addWidget(self.low_stock_table)
        layout.addWidget(self.top_products_label)
        layout.addWidget(self.top_products_table)
        layout.addWidget(self.sales_by_client_label)
        layout.addWidget(self.sales_by_client_table)
        layout.addWidget(self.refresh_reports_btn)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Reportes")

    def create_employee_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Formulario de empleado
        form = QFormLayout()
        
        self.employee_id = QLineEdit()
        self.employee_id.setReadOnly(True)
        self.employee_name = QLineEdit()
        self.employee_lastname = QLineEdit()
        self.employee_position = QComboBox()
        self.employee_position.addItems(["Gerente", "Vendedor", "Cajero", "Almacenista"])
        self.employee_phone = QLineEdit()
        self.employee_email = QLineEdit()
        self.employee_salary = QLineEdit()
        self.employee_status = QComboBox()
        self.employee_status.addItems(["Activo", "Inactivo"])

        form.addRow("ID:", self.employee_id)
        form.addRow("Nombre*:", self.employee_name)
        form.addRow("Apellidos*:", self.employee_lastname)
        form.addRow("Puesto:", self.employee_position)
        form.addRow("Teléfono:", self.employee_phone)
        form.addRow("Email:", self.employee_email)
        form.addRow("Salario:", self.employee_salary)
        form.addRow("Estado:", self.employee_status)

        # Botones
        btn_layout = QHBoxLayout()
        self.add_employee_btn = QPushButton("Agregar")
        self.add_employee_btn.clicked.connect(self.add_employee)
        self.update_employee_btn = QPushButton("Actualizar")
        self.update_employee_btn.clicked.connect(self.update_employee)
        self.delete_employee_btn = QPushButton("Eliminar")
        self.delete_employee_btn.clicked.connect(self.delete_employee)
        self.clear_employee_btn = QPushButton("Limpiar")
        self.clear_employee_btn.clicked.connect(self.clear_employee_form)

        btn_layout.addWidget(self.add_employee_btn)
        btn_layout.addWidget(self.update_employee_btn)
        btn_layout.addWidget(self.delete_employee_btn)
        btn_layout.addWidget(self.clear_employee_btn)

        # Tabla de empleados
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(7)
        self.employees_table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Apellidos", "Puesto", "Teléfono", "Email", "Estado"]
        )
        self.employees_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.employees_table.cellClicked.connect(self.load_employee_data)

        # Añadir al layout
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        layout.addWidget(self.employees_table)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Empleados")

    def load_initial_data(self):
        # Cargar categorías
        categories = self.db.execute_query("SELECT id_categoria, nombre FROM categorias ORDER BY nombre", fetch=True)
        if categories:
            self.product_category.clear()
            for cat in categories:
                self.product_category.addItem(cat['nombre'], cat['id_categoria'])

        # Cargar proveedores
        suppliers = self.db.execute_query("SELECT id_proveedor, nombre FROM proveedores ORDER BY nombre", fetch=True)
        if suppliers:
            self.product_supplier.clear()
            self.product_supplier.addItem("Seleccionar...", None)
            for sup in suppliers:
                self.product_supplier.addItem(sup['nombre'], sup['id_proveedor'])

        # Cargar productos para inventario y ventas
        products = self.db.execute_query("SELECT id_producto, nombre FROM productos ORDER BY nombre", fetch=True)
        if products:
            self.inventory_product.clear()
            self.inventory_filter_product.clear()
            self.inventory_product.addItem("Seleccionar...", None)
            self.inventory_filter_product.addItem("Todos los productos", None)
            for prod in products:
                self.inventory_product.addItem(prod['nombre'], prod['id_producto'])
                self.inventory_filter_product.addItem(prod['nombre'], prod['id_producto'])

        # Cargar clientes
        self.load_clients_data()
        self.load_clients_for_sale()

        # Cargar empleados
        self.load_employees_data()
        self.load_employees_for_sale()

        # Cargar productos para ventas
        self.load_products_for_sale()

        # Cargar datos iniciales en tablas
        self.load_products_data()
        self.load_inventory_data()
        self.load_reports_data()

    def load_products_data(self):
        query = """
        SELECT p.id_producto, p.nombre, p.precio_venta, p.codigo_barras, p.stock_minimo, p.activo,
               (SELECT SUM(CASE WHEN tipo_movimiento = 'Entrada' THEN cantidad ELSE -cantidad END) 
                FROM inventario WHERE id_producto = p.id_producto) AS stock,
               c.nombre AS categoria, prov.nombre AS proveedor
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor
        ORDER BY p.nombre
        """
        products = self.db.execute_query(query, fetch=True)
        
        if products:
            self.products_table.setRowCount(len(products))
            for row, prod in enumerate(products):
                self.products_table.setItem(row, 0, QTableWidgetItem(str(prod['id_producto'])))
                self.products_table.setItem(row, 1, QTableWidgetItem(prod['nombre']))
                self.products_table.setItem(row, 2, QTableWidgetItem(f"${prod['precio_venta']:.2f}"))
                stock = prod['stock'] if prod['stock'] is not None else 0
                self.products_table.setItem(row, 3, QTableWidgetItem(str(stock)))
                self.products_table.setItem(row, 4, QTableWidgetItem(prod['categoria']))
                self.products_table.setItem(row, 5, QTableWidgetItem(prod['proveedor'] or ""))
                self.products_table.setItem(row, 6, QTableWidgetItem(prod['codigo_barras'] or ""))
                self.products_table.setItem(row, 7, QTableWidgetItem(str(prod['stock_minimo'])))
                self.products_table.setItem(row, 8, QTableWidgetItem("Activo" if prod['activo'] else "Inactivo"))

    def load_clients_data(self):
        clients = self.db.execute_query(
            "SELECT id_cliente, nombre, apellidos, telefono, email, direccion, rfc, puntos_acumulados "
            "FROM clientes ORDER BY nombre", 
            fetch=True
        )
        
        if clients:
            self.clients_table.setRowCount(len(clients))
            for row, client in enumerate(clients):
                self.clients_table.setItem(row, 0, QTableWidgetItem(str(client['id_cliente'])))
                self.clients_table.setItem(row, 1, QTableWidgetItem(client['nombre']))
                self.clients_table.setItem(row, 2, QTableWidgetItem(client['apellidos'] or ""))
                self.clients_table.setItem(row, 3, QTableWidgetItem(client['telefono'] or ""))
                self.clients_table.setItem(row, 4, QTableWidgetItem(client['email'] or ""))
                self.clients_table.setItem(row, 5, QTableWidgetItem(client['direccion'] or ""))
                self.clients_table.setItem(row, 6, QTableWidgetItem(client['rfc'] or ""))
                self.clients_table.setItem(row, 7, QTableWidgetItem(str(client['puntos_acumulados'])))

    def load_clients_for_sale(self):
        clients = self.db.execute_query(
            "SELECT id_cliente, CONCAT(nombre, ' ', IFNULL(apellidos, '')) AS nombre_completo "
            "FROM clientes ORDER BY nombre", 
            fetch=True
        )
        if clients:
            self.sale_client.clear()
            self.sale_client.addItem("Seleccionar...", None)
            for client in clients:
                self.sale_client.addItem(client['nombre_completo'], client['id_cliente'])

    def load_employees_data(self):
        employees = self.db.execute_query(
            "SELECT id_empleado, nombre, apellidos, puesto, telefono, email, activo "
            "FROM empleados ORDER BY nombre", 
            fetch=True
        )
        
        if employees:
            self.employees_table.setRowCount(len(employees))
            for row, emp in enumerate(employees):
                self.employees_table.setItem(row, 0, QTableWidgetItem(str(emp['id_empleado'])))
                self.employees_table.setItem(row, 1, QTableWidgetItem(emp['nombre']))
                self.employees_table.setItem(row, 2, QTableWidgetItem(emp['apellidos']))
                self.employees_table.setItem(row, 3, QTableWidgetItem(emp['puesto'] or ""))
                self.employees_table.setItem(row, 4, QTableWidgetItem(emp['telefono'] or ""))
                self.employees_table.setItem(row, 5, QTableWidgetItem(emp['email'] or ""))
                self.employees_table.setItem(row, 6, QTableWidgetItem("Activo" if emp['activo'] else "Inactivo"))

    def load_employees_for_sale(self):
        employees = self.db.execute_query(
            "SELECT id_empleado, CONCAT(nombre, ' ', apellidos) AS nombre_completo "
            "FROM empleados WHERE activo = 1 ORDER BY nombre", 
            fetch=True
        )
        if employees:
            self.sale_employee.clear()
            self.sale_employee.addItem("Seleccionar...", None)
            for emp in employees:
                self.sale_employee.addItem(emp['nombre_completo'], emp['id_empleado'])

    def load_products_for_sale(self):
        query = """
        SELECT p.id_producto, p.nombre, p.precio_venta, 
               (SELECT SUM(CASE WHEN tipo_movimiento = 'Entrada' THEN cantidad ELSE -cantidad END) 
                FROM inventario WHERE id_producto = p.id_producto) AS stock
        FROM productos p
        WHERE p.activo = 1
        ORDER BY p.nombre
        """
        products = self.db.execute_query(query, fetch=True)
        if products:
            self.sale_product.clear()
            self.sale_product.addItem("Seleccionar...", None)
            for prod in products:
                stock = prod['stock'] if prod['stock'] is not None else 0
                self.sale_product.addItem(
                    f"{prod['nombre']} (${prod['precio_venta']:.2f} - Stock: {stock})", 
                    (prod['id_producto'], prod['precio_venta'], stock)
                )

    def load_inventory_data(self):
        product_id = self.inventory_filter_product.currentData()
        movement_type = self.inventory_filter_type.currentText() if self.inventory_filter_type.currentIndex() > 0 else None
        date_from = self.inventory_filter_date_from.date().toString("yyyy-MM-dd")
        date_to = self.inventory_filter_date_to.date().toString("yyyy-MM-dd")

        query = """
        SELECT i.id_movimiento, i.fecha_movimiento, p.nombre AS producto, 
               i.tipo_movimiento, i.cantidad, i.motivo, i.id_referencia
        FROM inventario i
        JOIN productos p ON i.id_producto = p.id_producto
        WHERE 1=1
        """
        params = []

        if product_id:
            query += " AND i.id_producto = %s"
            params.append(product_id)
            
        if movement_type:
            query += " AND i.tipo_movimiento = %s"
            params.append(movement_type)
            
        query += " AND DATE(i.fecha_movimiento) BETWEEN %s AND %s"
        params.extend([date_from, date_to])
        
        query += " ORDER BY i.fecha_movimiento DESC"

        movements = self.db.execute_query(query, params, fetch=True)
        
        if movements is not None:
            self.inventory_table.setRowCount(len(movements))
            for row, mov in enumerate(movements):
                self.inventory_table.setItem(row, 0, QTableWidgetItem(str(mov['id_movimiento'])))
                self.inventory_table.setItem(row, 1, QTableWidgetItem(str(mov['fecha_movimiento'])))
                self.inventory_table.setItem(row, 2, QTableWidgetItem(mov['producto']))
                self.inventory_table.setItem(row, 3, QTableWidgetItem(mov['tipo_movimiento']))
                self.inventory_table.setItem(row, 4, QTableWidgetItem(str(mov['cantidad'])))
                self.inventory_table.setItem(row, 5, QTableWidgetItem(mov['motivo'] or ""))
                self.inventory_table.setItem(row, 6, QTableWidgetItem(str(mov['id_referencia']) if mov['id_referencia'] else ""))

    def load_reports_data(self):
        # Productos bajos en stock
        query = """
        SELECT p.id_producto, p.nombre, c.nombre AS categoria, 
               (SELECT SUM(CASE WHEN tipo_movimiento = 'Entrada' THEN cantidad ELSE -cantidad END) 
                FROM inventario WHERE id_producto = p.id_producto) AS stock_actual,
               p.stock_minimo
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        HAVING stock_actual <= p.stock_minimo OR stock_actual IS NULL
        ORDER BY stock_actual
        """
        low_stock = self.db.execute_query(query, fetch=True)
        
        if low_stock is not None:
            self.low_stock_table.setRowCount(len(low_stock))
            for row, prod in enumerate(low_stock):
                self.low_stock_table.setItem(row, 0, QTableWidgetItem(str(prod['id_producto'])))
                self.low_stock_table.setItem(row, 1, QTableWidgetItem(prod['nombre']))
                self.low_stock_table.setItem(row, 2, QTableWidgetItem(prod['categoria']))
                stock = prod['stock_actual'] if prod['stock_actual'] is not None else 0
                self.low_stock_table.setItem(row, 3, QTableWidgetItem(str(stock)))
                self.low_stock_table.setItem(row, 4, QTableWidgetItem(str(prod['stock_minimo'])))

        # Productos más vendidos (últimos 30 días)
        query = """
        SELECT p.id_producto, p.nombre, c.nombre AS categoria,
               SUM(dv.cantidad) AS unidades_vendidas,
               SUM(dv.importe) AS ingreso_total
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        JOIN detalle_ventas dv ON p.id_producto = dv.id_producto
        JOIN ventas v ON dv.id_venta = v.id_venta
        WHERE v.fecha_venta >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY p.id_producto, p.nombre, c.nombre
        ORDER BY unidades_vendidas DESC
        LIMIT 10
        """
        top_products = self.db.execute_query(query, fetch=True)
        
        if top_products is not None:
            self.top_products_table.setRowCount(len(top_products))
            for row, prod in enumerate(top_products):
                self.top_products_table.setItem(row, 0, QTableWidgetItem(str(prod['id_producto'])))
                self.top_products_table.setItem(row, 1, QTableWidgetItem(prod['nombre']))
                self.top_products_table.setItem(row, 2, QTableWidgetItem(prod['categoria']))
                self.top_products_table.setItem(row, 3, QTableWidgetItem(str(prod['unidades_vendidas'])))
                self.top_products_table.setItem(row, 4, QTableWidgetItem(f"${prod['ingreso_total']:.2f}"))

        # Ventas por cliente
        query = """
        SELECT c.id_cliente, 
               CONCAT(c.nombre, ' ', IFNULL(c.apellidos, '')) AS cliente,
               COUNT(v.id_venta) AS total_ventas,
               SUM(v.total) AS monto_total,
               MAX(v.fecha_venta) AS ultima_compra
        FROM clientes c
        LEFT JOIN ventas v ON c.id_cliente = v.id_cliente
        GROUP BY c.id_cliente, cliente
        ORDER BY monto_total DESC
        """
        sales_by_client = self.db.execute_query(query, fetch=True)
        
        if sales_by_client is not None:
            self.sales_by_client_table.setRowCount(len(sales_by_client))
            for row, client in enumerate(sales_by_client):
                self.sales_by_client_table.setItem(row, 0, QTableWidgetItem(str(client['id_cliente'])))
                self.sales_by_client_table.setItem(row, 1, QTableWidgetItem(client['cliente']))
                self.sales_by_client_table.setItem(row, 2, QTableWidgetItem(str(client['total_ventas'])))
                self.sales_by_client_table.setItem(row, 3, QTableWidgetItem(f"${client['monto_total'] or 0:.2f}"))
                self.sales_by_client_table.setItem(row, 4, QTableWidgetItem(str(client['ultima_compra'] or "N/A")))

    def load_product_data(self, row):
        product_id = self.products_table.item(row, 0).text()
        query = """
        SELECT p.*, 
               (SELECT SUM(CASE WHEN tipo_movimiento = 'Entrada' THEN cantidad ELSE -cantidad END) 
                FROM inventario WHERE id_producto = p.id_producto) AS stock
        FROM productos p
        WHERE p.id_producto = %s
        """
        product = self.db.execute_query(query, (product_id,), fetch=True)
        
        if product:
            product = product[0]
            self.product_id.setText(str(product['id_producto']))
            self.product_name.setText(product['nombre'])
            self.product_barcode.setText(product['codigo_barras'] or "")
            self.product_description.setText(product['descripcion'] or "")
            self.product_purchase.setText(str(product['precio_compra']))
            self.product_price.setText(str(product['precio_venta']))
            stock = product['stock'] if product['stock'] is not None else 0
            self.product_stock.setText(str(stock))
            self.product_min_stock.setText(str(product['stock_minimo']))
            
            # Seleccionar categoría
            index = self.product_category.findData(product['id_categoria'])
            if index >= 0:
                self.product_category.setCurrentIndex(index)
            
            # Seleccionar proveedor
            if product['id_proveedor']:
                index = self.product_supplier.findData(product['id_proveedor'])
                if index >= 0:
                    self.product_supplier.setCurrentIndex(index)
            else:
                self.product_supplier.setCurrentIndex(0)
            
            # Estado
            self.product_active.setCurrentIndex(0 if product['activo'] else 1)

    def load_client_data(self, row):
        client_id = self.clients_table.item(row, 0).text()
        client = self.db.execute_query(
            "SELECT * FROM clientes WHERE id_cliente = %s", 
            (client_id,), fetch=True
        )
        
        if client:
            client = client[0]
            self.client_id.setText(str(client['id_cliente']))
            self.client_name.setText(client['nombre'])
            self.client_lastname.setText(client['apellidos'] or "")
            self.client_phone.setText(client['telefono'] or "")
            self.client_email.setText(client['email'] or "")
            self.client_address.setText(client['direccion'] or "")
            self.client_rfc.setText(client['rfc'] or "")
            self.client_points.setText(str(client['puntos_acumulados']))

    def load_employee_data(self, row):
        employee_id = self.employees_table.item(row, 0).text()
        employee = self.db.execute_query(
            "SELECT * FROM empleados WHERE id_empleado = %s", 
            (employee_id,), fetch=True
        )
        
        if employee:
            employee = employee[0]
            self.employee_id.setText(str(employee['id_empleado']))
            self.employee_name.setText(employee['nombre'])
            self.employee_lastname.setText(employee['apellidos'])
            
            if employee['puesto']:
                index = self.employee_position.findText(employee['puesto'])
                if index >= 0:
                    self.employee_position.setCurrentIndex(index)
            
            self.employee_phone.setText(employee['telefono'] or "")
            self.employee_email.setText(employee['email'] or "")
            self.employee_salary.setText(str(employee['salario']) if employee['salario'] else "")
            self.employee_status.setCurrentIndex(0 if employee['activo'] else 1)

    def load_inventory_data_row(self, row):
        movement_id = self.inventory_table.item(row, 0).text()
        query = """
        SELECT i.*, p.nombre AS producto_nombre
        FROM inventario i
        JOIN productos p ON i.id_producto = p.id_producto
        WHERE i.id_movimiento = %s
        """
        movement = self.db.execute_query(query, (movement_id,), fetch=True)
        
        if movement:
            movement = movement[0]
            self.inventory_id.setText(str(movement['id_movimiento']))
            
            index = self.inventory_product.findData(movement['id_producto'])
            if index >= 0:
                self.inventory_product.setCurrentIndex(index)
            
            index = self.inventory_type.findText(movement['tipo_movimiento'])
            if index >= 0:
                self.inventory_type.setCurrentIndex(index)
            
            self.inventory_quantity.setText(str(movement['cantidad']))
            self.inventory_reason.setText(movement['motivo'] or "")
            
            movement_date = movement['fecha_movimiento']
            if isinstance(movement_date, str):
                movement_date = datetime.strptime(movement_date, "%Y-%m-%d %H:%M:%S")
            self.inventory_date.setDate(QDate(movement_date.year, movement_date.month, movement_date.day))

    def update_product_price(self):
        product_data = self.sale_product.currentData()
        if product_data:
            product_id, price, stock = product_data
            self.sale_price.setText(f"{price:.2f}")
            self.sale_stock.setText(str(stock))
            self.update_sale_totals()

    def update_sale_totals(self):
        product_data = self.sale_product.currentData()
        if not product_data:
            return

        try:
            quantity = int(self.sale_quantity.text())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return

        product_id, price, stock = product_data
        total = quantity * price
        self.sale_price.setText(f"{total:.2f}")

    def add_product(self):
        # Validar campos obligatorios
        if not all([self.product_name.text(), self.product_purchase.text(), 
                   self.product_price.text(), self.product_category.currentData()]):
            QMessageBox.warning(self, "Error", "Los campos marcados con * son obligatorios")
            return

        try:
            purchase_price = float(self.product_purchase.text())
            sale_price = float(self.product_price.text())
            min_stock = int(self.product_min_stock.text()) if self.product_min_stock.text() else 5
            initial_stock = int(self.product_stock.text()) if self.product_stock.text() else 0
            
            if purchase_price <= 0 or sale_price <= 0 or min_stock < 0 or initial_stock < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Los valores numéricos deben ser positivos")
            return

        # Preparar datos
        data = {
            'nombre': self.product_name.text(),
            'codigo_barras': self.product_barcode.text() or None,
            'descripcion': self.product_description.text() or None,
            'precio_compra': purchase_price,
            'precio_venta': sale_price,
            'stock_minimo': min_stock,
            'id_categoria': self.product_category.currentData(),
            'id_proveedor': self.product_supplier.currentData() if self.product_supplier.currentData() else None,
            'activo': self.product_active.currentIndex() == 0
        }

        # Insertar producto
        query = """
        INSERT INTO productos (nombre, codigo_barras, descripcion, precio_compra, precio_venta, 
                             stock_minimo, id_categoria, id_proveedor, activo)
        VALUES (%(nombre)s, %(codigo_barras)s, %(descripcion)s, %(precio_compra)s, %(precio_venta)s,
               %(stock_minimo)s, %(id_categoria)s, %(id_proveedor)s, %(activo)s)
        """
        product_id = self.db.execute_query(query, data)
        
        if product_id:
            # Registrar stock inicial si es mayor a 0
            if initial_stock > 0:
                query = """
                INSERT INTO inventario (id_producto, tipo_movimiento, cantidad, motivo)
                VALUES (%s, 'Entrada', %s, 'Stock inicial')
                """
                self.db.execute_query(query, (product_id, initial_stock))
            
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente")
            self.clear_product_form()
            self.load_products_data()
            self.load_products_for_sale()
            self.load_inventory_data()

    def update_product(self):
        if not self.product_id.text():
            QMessageBox.warning(self, "Error", "Seleccione un producto para actualizar")
            return

        # Validar campos obligatorios
        if not all([self.product_name.text(), self.product_purchase.text(), 
                   self.product_price.text(), self.product_category.currentData()]):
            QMessageBox.warning(self, "Error", "Los campos marcados con * son obligatorios")
            return

        try:
            purchase_price = float(self.product_purchase.text())
            sale_price = float(self.product_price.text())
            min_stock = int(self.product_min_stock.text()) if self.product_min_stock.text() else 5
            
            if purchase_price <= 0 or sale_price <= 0 or min_stock < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Los valores numéricos deben ser positivos")
            return

        # Preparar datos
        data = {
            'id_producto': int(self.product_id.text()),
            'nombre': self.product_name.text(),
            'codigo_barras': self.product_barcode.text() or None,
            'descripcion': self.product_description.text() or None,
            'precio_compra': purchase_price,
            'precio_venta': sale_price,
            'stock_minimo': min_stock,
            'id_categoria': self.product_category.currentData(),
            'id_proveedor': self.product_supplier.currentData() if self.product_supplier.currentData() else None,
            'activo': self.product_active.currentIndex() == 0
        }

        # Actualizar producto
        query = """
        UPDATE productos 
        SET nombre = %(nombre)s, codigo_barras = %(codigo_barras)s, descripcion = %(descripcion)s,
            precio_compra = %(precio_compra)s, precio_venta = %(precio_venta)s, stock_minimo = %(stock_minimo)s,
            id_categoria = %(id_categoria)s, id_proveedor = %(id_proveedor)s, activo = %(activo)s
        WHERE id_producto = %(id_producto)s
        """
        if self.db.execute_query(query, data):
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente")
            self.load_products_data()
            self.load_products_for_sale()
            self.load_inventory_data()

    def delete_product(self):
        if not self.product_id.text():
            QMessageBox.warning(self, "Error", "Seleccione un producto para eliminar")
            return

        product_id = int(self.product_id.text())
        
        # Verificar si el producto tiene ventas asociadas
        query = "SELECT COUNT(*) FROM detalle_ventas WHERE id_producto = %s"
        result = self.db.execute_query(query, (product_id,), fetch=True)
        
        if result and result[0]['COUNT(*)'] > 0:
            QMessageBox.warning(self, "Error", "No se puede eliminar el producto porque tiene ventas asociadas")
            return

        # Confirmar eliminación
        reply = QMessageBox.question(
            self, 'Confirmar', 
            f"¿Está seguro de eliminar el producto {self.product_name.text()}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Eliminar movimientos de inventario primero
            query = "DELETE FROM inventario WHERE id_producto = %s"
            self.db.execute_query(query, (product_id,))
            
            # Eliminar producto
            query = "DELETE FROM productos WHERE id_producto = %s"
            if self.db.execute_query(query, (product_id,)):
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
                self.clear_product_form()
                self.load_products_data()
                self.load_products_for_sale()
                self.load_inventory_data()

    def clear_product_form(self):
        self.product_id.clear()
        self.product_name.clear()
        self.product_barcode.clear()
        self.product_description.clear()
        self.product_purchase.clear()
        self.product_price.clear()
        self.product_stock.clear()
        self.product_min_stock.setText("5")
        self.product_category.setCurrentIndex(0)
        self.product_supplier.setCurrentIndex(0)
        self.product_active.setCurrentIndex(0)

    def add_client(self):
        if not self.client_name.text():
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return

        data = {
            'nombre': self.client_name.text(),
            'apellidos': self.client_lastname.text() or None,
            'telefono': self.client_phone.text() or None,
            'email': self.client_email.text() or None,
            'direccion': self.client_address.text() or None,
            'rfc': self.client_rfc.text() or None
        }

        query = """
        INSERT INTO clientes (nombre, apellidos, telefono, email, direccion, rfc)
        VALUES (%(nombre)s, %(apellidos)s, %(telefono)s, %(email)s, %(direccion)s, %(rfc)s)
        """
        if self.db.execute_query(query, data):
            QMessageBox.information(self, "Éxito", "Cliente agregado correctamente")
            self.clear_client_form()
            self.load_clients_data()
            self.load_clients_for_sale()

    def update_client(self):
        if not self.client_id.text():
            QMessageBox.warning(self, "Error", "Seleccione un cliente para actualizar")
            return

        if not self.client_name.text():
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return

        data = {
            'id_cliente': int(self.client_id.text()),
            'nombre': self.client_name.text(),
            'apellidos': self.client_lastname.text() or None,
            'telefono': self.client_phone.text() or None,
            'email': self.client_email.text() or None,
            'direccion': self.client_address.text() or None,
            'rfc': self.client_rfc.text() or None
        }

        query = """
        UPDATE clientes 
        SET nombre = %(nombre)s, apellidos = %(apellidos)s, telefono = %(telefono)s,
            email = %(email)s, direccion = %(direccion)s, rfc = %(rfc)s
        WHERE id_cliente = %(id_cliente)s
        """
        if self.db.execute_query(query, data):
            QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente")
            self.load_clients_data()
            self.load_clients_for_sale()

    def delete_client(self):
        if not self.client_id.text():
            QMessageBox.warning(self, "Error", "Seleccione un cliente para eliminar")
            return

        client_id = int(self.client_id.text())
        
        # Verificar si el cliente tiene ventas asociadas
        query = "SELECT COUNT(*) FROM ventas WHERE id_cliente = %s"
        result = self.db.execute_query(query, (client_id,), fetch=True)
        
        if result and result[0]['COUNT(*)'] > 0:
            QMessageBox.warning(self, "Error", "No se puede eliminar el cliente porque tiene ventas asociadas")
            return

        # Confirmar eliminación
        reply = QMessageBox.question(
            self, 'Confirmar', 
            f"¿Está seguro de eliminar al cliente {self.client_name.text()}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            query = "DELETE FROM clientes WHERE id_cliente = %s"
            if self.db.execute_query(query, (client_id,)):
                QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
                self.clear_client_form()
                self.load_clients_data()
                self.load_clients_for_sale()

    def clear_client_form(self):
        self.client_id.clear()
        self.client_name.clear()
        self.client_lastname.clear()
        self.client_phone.clear()
        self.client_email.clear()
        self.client_address.clear()
        self.client_rfc.clear()
        self.client_points.clear()

    def add_employee(self):
        if not all([self.employee_name.text(), self.employee_lastname.text()]):
            QMessageBox.warning(self, "Error", "Nombre y apellidos son obligatorios")
            return

        try:
            salary = float(self.employee_salary.text()) if self.employee_salary.text() else None
            if salary is not None and salary < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "El salario debe ser un número positivo")
            return

        data = {
            'nombre': self.employee_name.text(),
            'apellidos': self.employee_lastname.text(),
            'puesto': self.employee_position.currentText() if self.employee_position.currentIndex() > 0 else None,
            'telefono': self.employee_phone.text() or None,
            'email': self.employee_email.text() or None,
            'salario': salary,
            'activo': self.employee_status.currentIndex() == 0
        }

        query = """
        INSERT INTO empleados (nombre, apellidos, puesto, telefono, email, salario, activo)
        VALUES (%(nombre)s, %(apellidos)s, %(puesto)s, %(telefono)s, %(email)s, %(salario)s, %(activo)s)
        """
        if self.db.execute_query(query, data):
            QMessageBox.information(self, "Éxito", "Empleado agregado correctamente")
            self.clear_employee_form()
            self.load_employees_data()
            self.load_employees_for_sale()

    def update_employee(self):
        if not self.employee_id.text():
            QMessageBox.warning(self, "Error", "Seleccione un empleado para actualizar")
            return

        if not all([self.employee_name.text(), self.employee_lastname.text()]):
            QMessageBox.warning(self, "Error", "Nombre y apellidos son obligatorios")
            return

        try:
            salary = float(self.employee_salary.text()) if self.employee_salary.text() else None
            if salary is not None and salary < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "El salario debe ser un número positivo")
            return

        data = {
            'id_empleado': int(self.employee_id.text()),
            'nombre': self.employee_name.text(),
            'apellidos': self.employee_lastname.text(),
            'puesto': self.employee_position.currentText() if self.employee_position.currentIndex() > 0 else None,
            'telefono': self.employee_phone.text() or None,
            'email': self.employee_email.text() or None,
            'salario': salary,
            'activo': self.employee_status.currentIndex() == 0
        }

        query = """
        UPDATE empleados 
        SET nombre = %(nombre)s, apellidos = %(apellidos)s, puesto = %(puesto)s,
            telefono = %(telefono)s, email = %(email)s, salario = %(salario)s, activo = %(activo)s
        WHERE id_empleado = %(id_empleado)s
        """
        if self.db.execute_query(query, data):
            QMessageBox.information(self, "Éxito", "Empleado actualizado correctamente")
            self.load_employees_data()
            self.load_employees_for_sale()

    def delete_employee(self):
        if not self.employee_id.text():
            QMessageBox.warning(self, "Error", "Seleccione un empleado para eliminar")
            return

        employee_id = int(self.employee_id.text())
        
        # Verificar si el empleado tiene ventas asociadas
        query = "SELECT COUNT(*) FROM ventas WHERE id_empleado = %s"
        result = self.db.execute_query(query, (employee_id,), fetch=True)
        
        if result and result[0]['COUNT(*)'] > 0:
            QMessageBox.warning(self, "Error", "No se puede eliminar el empleado porque tiene ventas asociadas")
            return

        # Confirmar eliminación
        reply = QMessageBox.question(
            self, 'Confirmar', 
            f"¿Está seguro de eliminar al empleado {self.employee_name.text()}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            query = "DELETE FROM empleados WHERE id_empleado = %s"
            if self.db.execute_query(query, (employee_id,)):
                QMessageBox.information(self, "Éxito", "Empleado eliminado correctamente")
                self.clear_employee_form()
                self.load_employees_data()
                self.load_employees_for_sale()

    def clear_employee_form(self):
        self.employee_id.clear()
        self.employee_name.clear()
        self.employee_lastname.clear()
        self.employee_position.setCurrentIndex(0)
        self.employee_phone.clear()
        self.employee_email.clear()
        self.employee_salary.clear()
        self.employee_status.setCurrentIndex(0)

    def add_product_to_sale(self):
        product_data = self.sale_product.currentData()
        if not product_data:
            QMessageBox.warning(self, "Error", "Seleccione un producto válido")
            return

        try:
            quantity = int(self.sale_quantity.text())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "La cantidad debe ser un número positivo")
            return

        product_id, price, stock = product_data
        
        # Verificar stock
        if stock < quantity:
            QMessageBox.warning(self, "Error", f"No hay suficiente stock. Disponible: {stock}")
            return

        # Verificar si el producto ya está en la venta
        for row in range(self.sale_items_table.rowCount()):
            if int(self.sale_items_table.item(row, 0).text()) == product_id:
                # Actualizar cantidad
                current_qty = int(self.sale_items_table.item(row, 2).text())
                new_qty = current_qty + quantity
                
                if stock < new_qty:
                    QMessageBox.warning(self, "Error", f"No hay suficiente stock. Disponible: {stock}")
                    return
                
                self.sale_items_table.item(row, 2).setText(str(new_qty))
                self.sale_items_table.item(row, 4).setText(f"${price * new_qty:.2f}")
                self.update_sale_totals()
                return

        # Agregar nuevo producto a la venta
        row = self.sale_items_table.rowCount()
        self.sale_items_table.insertRow(row)
        
        self.sale_items_table.setItem(row, 0, QTableWidgetItem(str(product_id)))
        self.sale_items_table.setItem(row, 1, QTableWidgetItem(self.sale_product.currentText().split(' (')[0]))
        self.sale_items_table.setItem(row, 2, QTableWidgetItem(str(quantity)))
        self.sale_items_table.setItem(row, 3, QTableWidgetItem(f"${price:.2f}"))
        self.sale_items_table.setItem(row, 4, QTableWidgetItem(f"${price * quantity:.2f}"))
        self.sale_items_table.setItem(row, 5, QTableWidgetItem(str(stock)))
        
        self.update_sale_totals()

    def remove_product_from_sale(self):
        selected = self.sale_items_table.currentRow()
        if selected >= 0:
            self.sale_items_table.removeRow(selected)
            self.update_sale_totals()

    def update_sale_totals(self):
        subtotal = 0.0
        for row in range(self.sale_items_table.rowCount()):
            price_text = self.sale_items_table.item(row, 4).text().replace('$', '')
            subtotal += float(price_text)
        
        iva = subtotal * 0.16
        total = subtotal + iva
        
        # Calcular puntos (1 punto por cada $100 de compra)
        points = int(total // 100)
        
        self.sale_subtotal.setText(f"{subtotal:.2f}")
        self.sale_iva.setText(f"{iva:.2f}")
        self.sale_total.setText(f"{total:.2f}")
        self.sale_points.setText(str(points))

    def process_sale(self):
        if self.sale_items_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "Agregue productos a la venta")
            return

        if not self.sale_client.currentData():
            QMessageBox.warning(self, "Error", "Seleccione un cliente")
            return

        if not self.sale_employee.currentData():
            QMessageBox.warning(self, "Error", "Seleccione un empleado")
            return

        # Obtener datos de la venta
        client_id = self.sale_client.currentData()
        employee_id = self.sale_employee.currentData()
        payment_method = self.sale_payment.currentText()
        sale_date = self.sale_date.date().toString("yyyy-MM-dd")
        subtotal = float(self.sale_subtotal.text())
        iva = float(self.sale_iva.text())
        total = float(self.sale_total.text())
        points = int(self.sale_points.text())

        # Procesar en transacción
        cursor = self.db.connection.cursor()
        try:
            # Insertar venta
            query = """
            INSERT INTO ventas (id_cliente, id_empleado, fecha_venta, subtotal, iva, total, metodo_pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (client_id, employee_id, sale_date, subtotal, iva, total, payment_method))
            sale_id = cursor.lastrowid

            # Insertar detalles de venta y actualizar inventario
            for row in range(self.sale_items_table.rowCount()):
                product_id = int(self.sale_items_table.item(row, 0).text())
                quantity = int(self.sale_items_table.item(row, 2).text())
                unit_price = float(self.sale_items_table.item(row, 3).text().replace('$', ''))
                amount = float(self.sale_items_table.item(row, 4).text().replace('$', ''))

                # Insertar detalle
                query = """
                INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, importe)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (sale_id, product_id, quantity, unit_price, amount))

                # Registrar salida de inventario
                query = """
                INSERT INTO inventario (id_producto, tipo_movimiento, cantidad, motivo, id_referencia)
                VALUES (%s, 'Salida', %s, 'Venta ID %s', %s)
                """
                cursor.execute(query, (product_id, quantity, sale_id, sale_id))

            # Actualizar puntos del cliente si es una venta registrada
            if client_id and points > 0:
                query = "UPDATE clientes SET puntos_acumulados = puntos_acumulados + %s WHERE id_cliente = %s"
                cursor.execute(query, (points, client_id))

            self.db.connection.commit()
            
            # Mostrar resumen
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Venta procesada correctamente")
            msg.setInformativeText(f"ID Venta: {sale_id}\nTotal: ${total:.2f}\nPuntos acumulados: {points}")
            msg.setWindowTitle("Éxito")
            msg.exec_()
            
            # Limpiar formulario
            self.cancel_sale()
            
            # Actualizar datos
            self.load_products_data()
            self.load_inventory_data()
            self.load_reports_data()
            self.load_clients_data()
            self.load_clients_for_sale()
            
        except mysql.connector.Error as e:
            self.db.connection.rollback()
            QMessageBox.critical(self, "Error", f"Error al procesar venta: {e}")
        finally:
            cursor.close()

    def cancel_sale(self):
        self.sale_items_table.setRowCount(0)
        self.sale_client.setCurrentIndex(0)
        self.sale_employee.setCurrentIndex(0)
        self.sale_payment.setCurrentIndex(0)
        self.sale_date.setDate(QDate.currentDate())
        self.sale_product.setCurrentIndex(0)
        self.sale_quantity.setText("1")
        self.sale_price.clear()
        self.sale_stock.clear()
        self.sale_subtotal.setText("0.00")
        self.sale_iva.setText("0.00")
        self.sale_total.setText("0.00")
        self.sale_points.setText("0")

    def print_sale(self):
        # Esta función simularía la impresión del ticket
        if self.sale_items_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No hay productos en la venta para imprimir")
            return

        ticket = "=== TICKET DE VENTA ===\n"
        ticket += f"Fecha: {self.sale_date.date().toString('dd/MM/yyyy')}\n"
        
        if self.sale_client.currentData():
            ticket += f"Cliente: {self.sale_client.currentText()}\n"
        
        ticket += "\nProductos:\n"
        
        for row in range(self.sale_items_table.rowCount()):
            product = self.sale_items_table.item(row, 1).text()
            quantity = self.sale_items_table.item(row, 2).text()
            price = self.sale_items_table.item(row, 4).text()
            ticket += f"{product} x{quantity} {price}\n"
        
        ticket += "\n"
        ticket += f"Subtotal: {self.sale_subtotal.text()}\n"
        ticket += f"IVA (16%): {self.sale_iva.text()}\n"
        ticket += f"TOTAL: {self.sale_total.text()}\n"
        ticket += f"Puntos: {self.sale_points.text()}\n"
        ticket += "======================="

        # Mostrar ticket en un diálogo
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Ticket de Venta")
        msg.setInformativeText(ticket)
        msg.setWindowTitle("Ticket")
        msg.exec_()

    def add_inventory_movement(self):
        if not self.inventory_product.currentData():
            QMessageBox.warning(self, "Error", "Seleccione un producto")
            return

        try:
            quantity = int(self.inventory_quantity.text())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "La cantidad debe ser un número positivo")
            return

        data = {
            'id_producto': self.inventory_product.currentData(),
            'tipo_movimiento': self.inventory_type.currentText(),
            'cantidad': quantity,
            'motivo': self.inventory_reason.text() or None,
            'fecha_movimiento': self.inventory_date.date().toString("yyyy-MM-dd")
        }

        query = """
        INSERT INTO inventario (id_producto, tipo_movimiento, cantidad, motivo, fecha_movimiento)
        VALUES (%(id_producto)s, %(tipo_movimiento)s, %(cantidad)s, %(motivo)s, %(fecha_movimiento)s)
        """
        if self.db.execute_query(query, data):
            QMessageBox.information(self, "Éxito", "Movimiento de inventario registrado")
            self.clear_inventory_form()
            self.load_inventory_data()
            self.load_products_data()
            self.load_products_for_sale()
            self.load_reports_data()

    def clear_inventory_form(self):
        self.inventory_id.clear()
        self.inventory_product.setCurrentIndex(0)
        self.inventory_type.setCurrentIndex(0)
        self.inventory_quantity.setText("1")
        self.inventory_reason.clear()
        self.inventory_date.setDate(QDate.currentDate())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Verificar conexión antes de mostrar la ventana principal
    db = DatabaseManager()
    if not db.connection:
        sys.exit(1)
    
    window = MainApp()
    window.show()
    sys.exit(app.exec_())