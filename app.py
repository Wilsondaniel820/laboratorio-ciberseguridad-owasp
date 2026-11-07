from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'

# Función auxiliar para registrar eventos de seguridad en el archivo eventos.log
def registrar_evento(tipo, descripcion):
    tiempo_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("eventos.log", "a") as archivo_log:
        archivo_log.write(f"[{tiempo_actual}] [{tipo.upper()}] {descripcion}\n")

# Ruta de bienvenida / Inicio
@app.route("/")
def inicio():
    return render_template("login.html")

# Ruta de Registro de Usuario
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        correo = request.form["correo"]
        password_plana = request.form["password"]
        
        # Encriptar contraseña (OWASP)
        password_hash = generate_password_hash(password_plana)
        
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        
        try:
            # Consultas parametrizadas contra Inyección SQL (OWASP)
            cursor.execute("INSERT INTO usuarios (usuario, correo, password) VALUES (?, ?, ?)", 
                           (usuario, correo, password_hash))
            conexion.commit()
            
            # Registrar evento exitoso en los logs
            registrar_evento("INFO", f"Nuevo usuario registrado exitosamente: {usuario}")
        except Exception as e:
            registrar_evento("ERROR", f"Fallo al registrar usuario {usuario}: {str_error}")
        finally:
            conexion.close()
        
        return redirect(url_for("login"))
        
    return render_template("registro.html")

# Ruta de Inicio de Sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password_plana = request.form["password"]
        
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        user = cursor.fetchone()
        conexion.close()
        
        # Verificar credenciales
        if user and check_password_hash(user[3], password_plana):
            # Registrar evento de éxito en login
            registrar_evento("INFO", f"Inicio de sesión exitoso para el usuario: {usuario}")
            return f"¡Bienvenido al sistema, {usuario}! Inicio de sesión exitoso."
        else:
            # Registrar evento de alerta de seguridad por login fallido
            registrar_evento("WARNING", f"Intento de inicio de sesión fallido para el usuario: {usuario}")
            return "Credenciales incorrectas. Inténtalo de nuevo."
            
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)