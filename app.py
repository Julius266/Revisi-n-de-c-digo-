from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = '123456'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'sistema_inventario'

mysql = MySQL(app)


# Rutas
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM productos")
    if result_value > 0:
        products = cur.fetchall()
        return render_template('index.html', products=products)
    return render_template('index.html')

@app.route('/consul_usuario')
def index_usuario():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM proveedores")
    if result_value > 0:
        products = cur.fetchall()
        return render_template('consulta_usuario.html', products=products)
    return render_template('consulta_usuario.html')

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        products_details = request.form
        nombre = products_details['nombre']
        descripcion = products_details['descripcion']
        precio = products_details['precio']
        stock = products_details['stock']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos(nombre, descripcion, precio, stock) VALUES(%s, %s, %s, %s)", (nombre, descripcion, precio, stock))
        mysql.connection.commit()
        cur.close()
        flash('Producto Agregado Satisfactoriamente')
        return redirect(url_for('index'))
    return render_template('products_add.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        products_details = request.form
        nomb = products_details['nombre']
        contacto = products_details['contacto']
        telefono = products_details['telefono']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO proveedores(nombre, contacto, telefono) VALUES(%s, %s, %s)", (nomb, contacto, telefono))
        mysql.connection.commit()
        cur.close()
        flash('Proveedor Agregado Satisfactoriamente')
        return redirect(url_for('index_usuario'))
    return render_template('usuarios_add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", [id])
    product = cur.fetchone()
    if request.method == 'POST':
        products_details = request.form
        nombre = products_details['nombre']
        descripcion = products_details['descripcion']
        precio = products_details['precio']
        stock = products_details['stock']
        cur.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock= %s WHERE id = %s", (nombre, descripcion, precio, stock, id))
        mysql.connection.commit()
        cur.close()
        flash('Producto actualizado satisfactoriamente')
        return redirect(url_for('index'))
    return render_template('products_edit.html', product=product)


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM proveedores WHERE id = %s", [id])
    product = cur.fetchone()
    if request.method == 'POST':
        products_details = request.form
        nomb = products_details['nombre']
        contacto = products_details['contacto']
        telefono = products_details['telefono']
        
        cur.execute("UPDATE proveedores SET nombre = %s, contacto = %s, telefono= %s WHERE id = %s", (nomb, contacto, telefono, id))
        mysql.connection.commit()
        cur.close()
        flash('Proveedor actualizado satisfactoriamente')
        return redirect(url_for('index_usuario'))
    return render_template('usuarios_edit.html', product=product)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Producto eliminado satisfactoriamente')
    return redirect(url_for('index'))


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM proovedores WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Proveedor eliminado satisfactoriamente')
    return redirect(url_for('index_usuario'))



@app.route('/compras')
def compras():
    cur = mysql.connection.cursor()
    cur.execute("SELECT c.id, p.nombre as nombre_producto, u.nombre as proovedor_nombre, c.fecha, c.cantidad "
                "FROM Compras c "
                "JOIN Productos p ON p.id = p.id_product "
                "JOIN Proovedores u ON p.id = u.id_proovedores")
    compras1 = cur.fetchall()

    cur.execute("SELECT id, nombre FROM Productos")
    producto1 = cur.fetchall()

    cur.execute("SELECT id, nombre as nomb FROM Proovedores")
    usuarios1 = cur.fetchall()

    cur.close()
    return render_template('compras.html', compras=compras1, productos=producto1, usuarios=usuarios1)


@app.route('/compras/agregar', methods=['GET', 'POST'])
def agregar_compras():
    if request.method == 'POST':
        id_libro = request.form['id_libro']
        id_usuario = request.form['id_usuario']
        fecha_prestamo = request.form['fecha_prestamo']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Prestamos (id_libro, id_usuario, fecha_prestamo) VALUES (%s, %s, %s)",
                (id_libro, id_usuario, fecha_prestamo))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('compras'))
    return render_template('prestamos.html')



@app.route('/edit_compra/<int:id>', methods=['GET', 'POST'])
def edit_compra(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM compras WHERE id = %s", [id])
    compra = cur.fetchone()

    cur.execute("SELECT id, nombre FROM productos")
    product1 = cur.fetchall()

    cur.execute("SELECT id, nombre as nomb FROM proovedores")
    usuarios1 = cur.fetchall()

    if request.method == 'POST':
        products_details = request.form
        id_product = products_details['id_product']
        id_usuario = products_details['id_proovedor']
        fecha_compra = products_details['fecha']
        cantidad = products_details['cantidad']
        
        
        cur.execute("UPDATE compras SET id_product = %s, id_usuario = %s, fecha_compra = %s, cantidad = %s WHERE id = %s", (id_product, id_usuario, fecha_compra, cantidad, id))
        
        
        
        mysql.connection.commit()

        cur.close()
        flash('Compra actualizado satisfactoriamente')
        return redirect(url_for('compras'))
    return render_template('edit_pres.html', compra=compra, product=product1, usuarios=usuarios1)

@app.route('/delete_pres/<int:id>', methods=['POST'])
def delete_pres(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM compras WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Compra eliminado satisfactoriamente')
    return redirect(url_for('compras'))

if __name__ == '__main__':
    app.run(debug=True)
