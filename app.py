from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = '123456'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_DB'] = 'biblioteca'

mysql = MySQL(app)

# Rutas
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM libros")
    if result_value > 0:
        books = cur.fetchall()
        return render_template('index.html', books=books)
    return render_template('index.html')

@app.route('/consul_usuario')
def index_usuario():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM usuarios")
    if result_value > 0:
        books = cur.fetchall()
        return render_template('consulta_usuario.html', books=books)
    return render_template('consulta_usuario.html')

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_details = request.form
        title = book_details['title']
        author = book_details['author']
        editorial = book_details['editorial']
        anio = book_details['anio']
        genero = book_details['genero']
        stock = book_details['stock']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO libros(titulo, autor, editorial, anio_publicacion,genero,cantidad_disponible) VALUES(%s, %s, %s, %s, %s, %s)", (title, author, editorial, anio, genero, stock))
        mysql.connection.commit()
        cur.close()
        flash('Libro Agregado Satisfactoriamente')
        return redirect(url_for('index'))
    return render_template('libros_add.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        book_details = request.form
        ape = book_details['apellido']
        nomb = book_details['nombre']
        correo = book_details['correo']
        fono = book_details['fono']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios(nombre, apellido, correo, telefono) VALUES(%s, %s, %s, %s)", (nomb, ape, correo, fono))
        mysql.connection.commit()
        cur.close()
        flash('Usuario Agregado Satisfactoriamente')
        return redirect(url_for('index_usuario'))
    return render_template('usuarios_add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM libros WHERE id = %s", [id])
    book = cur.fetchone()
    if request.method == 'POST':
        book_details = request.form
        title = book_details['title']
        author = book_details['author']
        editorial = book_details['editorial']
        anio = book_details['anio']
        genero = book_details['genero']
        stock = book_details['stock']
        cur.execute("UPDATE libros SET titulo = %s, autor = %s, editorial = %s, anio_publicacion= %s, genero = %s , cantidad_disponible = %s WHERE id = %s", (title, author, editorial, anio, genero, stock, id))
        mysql.connection.commit()
        cur.close()
        flash('Libro actualizado satisfactoriamente')
        return redirect(url_for('index'))
    return render_template('libros_edit.html', book=book)


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s", [id])
    book = cur.fetchone()
    if request.method == 'POST':
        book_details = request.form
        ape = book_details['apellido']
        nomb = book_details['nombre']
        correo = book_details['correo']
        fono = book_details['fono']
        
        cur.execute("UPDATE usuarios SET apellido = %s, nombre = %s, correo = %s, telefono= %s WHERE id = %s", (ape, nomb, correo, fono, id))
        mysql.connection.commit()
        cur.close()
        flash('Usuario actualizado satisfactoriamente')
        return redirect(url_for('index_usuario'))
    return render_template('usuarios_edit.html', book=book)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM libros WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Libro eliminado satisfactoriamente')
    return redirect(url_for('index'))


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Usuario eliminado satisfactoriamente')
    return redirect(url_for('index_usuario'))



@app.route('/prestamos')
def prestamos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.id, l.titulo as libro_titulo, u.nombre as prestatario_nombre, p.fecha_prestamo, p.fecha_devolucion "
                "FROM prestamos p "
                "JOIN Libros l ON p.id_libro = l.id "
                "JOIN Usuarios u ON p.id_usuario = u.id")
    prestamos1 = cur.fetchall()

    cur.execute("SELECT id, titulo FROM libros")
    libros1 = cur.fetchall()

    cur.execute("SELECT id, concat(apellido,' ', nombre) as nomb FROM usuarios")
    usuarios1 = cur.fetchall()

    cur.close()
    return render_template('prestamos.html', prestamos=prestamos1, libros=libros1, usuarios=usuarios1)


@app.route('/prestamos/agregar', methods=['GET', 'POST'])
def agregar_prestamo():
    if request.method == 'POST':
        id_libro = request.form['id_libro']
        id_usuario = request.form['id_usuario']
        fecha_prestamo = request.form['fecha_prestamo']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Prestamos (id_libro, id_usuario, fecha_prestamo) VALUES (%s, %s, %s)",
                (id_libro, id_usuario, fecha_prestamo))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('prestamos'))
    return render_template('prestamos.html')



@app.route('/edit_pres/<int:id>', methods=['GET', 'POST'])
def edit_pres(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestamos WHERE id = %s", [id])
    book = cur.fetchone()

    cur.execute("SELECT id, titulo FROM libros")
    libros1 = cur.fetchall()

    cur.execute("SELECT id, concat(apellido,' ', nombre) as nomb FROM usuarios")
    usuarios1 = cur.fetchall()

    if request.method == 'POST':
        book_details = request.form
        id_libro = book_details['id_libro']
        id_usuario = book_details['id_usuario']
        fecha_prestamo = book_details['fecha_prestamo']
        f_devolucion= book_details['fecha_dev']
        
        
        cur.execute("UPDATE prestamos SET id_libro = %s, id_usuario = %s, fecha_prestamo = %s, fecha_devolucion= %s WHERE id = %s", (id_libro, id_usuario, fecha_prestamo, f_devolucion, id))
        
        
        
        mysql.connection.commit()

        cur.close()
        flash('Prestamo actualizado satisfactoriamente')
        return redirect(url_for('prestamos'))
    return render_template('edit_pres.html', book=book, libros=libros1, usuarios=usuarios1)

@app.route('/delete_pres/<int:id>', methods=['POST'])
def delete_pres(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM prestamos WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Prestamo eliminado satisfactoriamente')
    return redirect(url_for('prestamos'))

if __name__ == '__main__':
    app.run(debug=True)
