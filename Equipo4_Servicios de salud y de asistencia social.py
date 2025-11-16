import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox

# Define la conexión
server = 'localhost\\SQLEXPRESS'
database = 'servicios_de_salud'
username = 'sa'
password = 'Kaleb2024'
driver = 'ODBC Driver 17 for SQL Server'

# Intenta la conexión
try:
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    print("Conexión exitosa!")
except Exception as e:
    print("Error al conectar:", e)

# Función para validar el inicio de sesión
def validar_credenciales(usuario, contraseña):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print("Error al validar credenciales:", e)
        return None
    finally:
        cursor.close()


# Funciones para interactuar con la base de datos
def insertar_estab(id_estab, clee, nombre_estab, raz_social, telefono, correoelec, www, fecha_alta, id_uniEco, codigo_act, id_per_ocu):
    try:
        cursor = conn.cursor()
        cursor.execute("{CALL InsertarEstab (?,?,?,?,?,?,?,?,?,?,?)}", (id_estab, clee, nombre_estab, raz_social, telefono, correoelec, www, fecha_alta, id_uniEco, codigo_act, id_per_ocu))
        conn.commit()
        messagebox.showinfo("Éxito", "La inserción fue exitosa")
    except Exception as e:
        messagebox.showerror("Error", f"Error al insertar, es posible que sea porque hay datos en blanco que son necesarios: {e}")
    finally:
        cursor.close()

def eliminar_estab(id_estab):
    try:
        cursor = conn.cursor()
        cursor.execute("{CALL BorrarEstab (?)}", (id_estab,))
        conn.commit()
        messagebox.showinfo("Éxito", "El borrado fue exitoso")
    except Exception as e:
        messagebox.showerror("Error", f"Error al borrar, es posible que sea porque hay datos en blanco que son necesarios: {e}")
    finally:
        cursor.close()

def actualizar_estab(id_estab, clee, nombre_estab, raz_social, telefono, correoelec, www):
    try:
        cursor = conn.cursor()
        cursor.execute("{CALL ActualizarEstab (?,?,?,?,?,?,?)}", (id_estab, clee, nombre_estab, raz_social, telefono, correoelec, www))
        conn.commit()
        messagebox.showinfo("Éxito", "La actualización fue exitosa")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar, es posible que sea porque hay datos en blanco que son necesarios: {e}")
    finally:
        cursor.close()

def modificar_estab(id_estab, columna, nuevodato):
    try:
        cursor = conn.cursor()
        cursor.execute("{CALL ModificarEstab (?,?,?)}", (id_estab, columna, nuevodato))
        conn.commit()
        messagebox.showinfo("Éxito", "La modificación fue exitosa")
    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar, es posible que sea porque hay datos en blanco que son necesarios: {e}")
    finally:
        cursor.close()

def obtener_datos_establecimiento():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_establecimiento")
        datos = cursor.fetchall()  # Obtener todos los registros
        columnas = [column[0] for column in cursor.description]  # Obtener los nombres de las columnas
        
        # Limpieza de datos (reemplazar None por una cadena vacía y quitar comillas)
        datos_limpios = []
        for fila in datos:
            datos_limpios.append(tuple("" if valor is None else str(valor).strip("'") for valor in fila))
        
        return columnas, datos_limpios
    except Exception as e:
        messagebox.showerror("Error al obtener datos:", e)
        return [], []
    finally:
        cursor.close()

#Funcion que llama a un procedimiento almacenado que toma los datos de la consulta de busqueda con el id_estab
def ConsultaID(id_estab):
    try:
        cursor = conn.cursor()
        cursor.execute("{CALL ConsultaID (?)}", (id_estab,))
        datos = cursor.fetchall()  # Obtener todos los registros
        columnas = [column[0] for column in cursor.description]  # Nombres de columnas
        
        # Limpieza de datos (reemplaza None con una cadena vacía)
        datos_limpios = [
            tuple("" if valor is None else str(valor).strip("'") for valor in fila)
            for fila in datos
        ]
        print("Consulta ejecutada correctamente.")
        return columnas, datos_limpios
    except Exception as e:
        messagebox.showerror("Error al consultar:", e)
        return [], []
    finally:
        cursor.close()

#Muestra una tabla con los datos de la consulta por medio del id_estab 
def mostrar_tabla_ConsultaID(id_estab):
    """Muestra los datos de la consulta en una ventana de Tkinter."""
    columnas, datos = ConsultaID(id_estab)
    if not columnas or not datos:
        messagebox.showerror("Error", "No hay datos para mostrar o ocurrió un error.")
        return

    # Crear una nueva ventana
    ventana_tabla = tk.Tk()
    ventana_tabla.title(f"Resultados para id_estab = {id_estab}")

    # Crear el Treeview para mostrar la tabla
    tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings")

    # Configurar encabezados y columnas
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor='center', width=130)

    # Insertar datos en la tabla
    for fila in datos:
        tabla.insert("", "end", values=fila)

    # Empacar la tabla
    tabla.pack(expand=True, fill="both")

    # Iniciar el bucle principal
    ventana_tabla.mainloop()

#Funcion que llama a un procedimiento almacenado que toma los datos de la consulta de busqueda con el nombre_estab
def Consultanombre(nombre_estab):
    try:
        cursor = conn.cursor()
        cursor.execute("{CALL Consultanombre (?)}", (nombre_estab,))
        datos = cursor.fetchall()  # Obtener todos los registros
        columnas = [column[0] for column in cursor.description]  # Nombres de columnas
        
        # Limpieza de datos (reemplaza None con una cadena vacía)
        datos_limpios = [
            tuple("" if valor is None else str(valor).strip("'") for valor in fila)
            for fila in datos
        ]
        print("Consulta ejecutada correctamente.")
        return columnas, datos_limpios
    except Exception as e:
        messagebox.showerror("Error al consultar:", e)
        return [], []
    finally:
        cursor.close()
#Muestra una tabla con los datos de la consulta por medio del nombre_estab
def mostrar_tabla_Consultanombre(nombre_estab):
    """Muestra los datos de la consulta en una ventana de Tkinter."""
    columnas, datos = Consultanombre(nombre_estab)
    if not columnas or not datos:
        messagebox.showerror("Error", "No hay datos para mostrar o ocurrió un error.")
        return

    # Crear una nueva ventana
    ventana_tabla = tk.Tk()
    ventana_tabla.title(f"Resultados para nombre_estab = {nombre_estab}")

    # Crear el Treeview para mostrar la tabla
    tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings")

    # Configurar encabezados y columnas
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor='center', width=130)

    # Insertar datos en la tabla
    for fila in datos:
        tabla.insert("", "end", values=fila)

    # Empacar la tabla
    tabla.pack(expand=True, fill="both")

    # Iniciar el bucle principal
    ventana_tabla.mainloop()

def ConsultauniEco(id_uniEco):
    try:
        cursor = conn.cursor()
        cursor.execute("{CALL ConsultauniEco (?)}", (id_uniEco,))
        datos = cursor.fetchall()  # Obtener todos los registros
        columnas = [column[0] for column in cursor.description]  # Nombres de columnas
        
        # Limpieza de datos (reemplaza None con una cadena vacía)
        datos_limpios = [
            tuple("" if valor is None else str(valor).strip("'") for valor in fila)
            for fila in datos
        ]
        print("Consulta ejecutada correctamente.")
        return columnas, datos_limpios
    except Exception as e:
        messagebox.showerror("Error al consultar:", e)
        return [], []
    finally:
        cursor.close()

#Muestra una tabla con los datos de la consulta por medio del id_uniEco
def mostrar_tabla_ConsultauniEco(id_uniEco):
    """Muestra los datos de la consulta en una ventana de Tkinter."""
    columnas, datos = ConsultauniEco(id_uniEco)
    if not columnas or not datos:
        messagebox.showerror("Error", "No hay datos para mostrar o ocurrió un error.")
        return

    # Crear una nueva ventana
    ventana_tabla = tk.Tk()
    ventana_tabla.title(f"Resultados para id_estab = {id_uniEco}")

    # Crear el Treeview para mostrar la tabla
    tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings")

    # Configurar encabezados y columnas
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor='center', width=130)

    # Insertar datos en la tabla
    for fila in datos:
        tabla.insert("", "end", values=fila)

    # Empacar la tabla
    tabla.pack(expand=True, fill="both")

    # Iniciar el bucle principal
    ventana_tabla.mainloop()

def ConsultaActividad(codigo_act):
    try:
        cursor = conn.cursor()
        cursor.execute("{CALL ConsultaActividad (?)}", (codigo_act,))
        datos = cursor.fetchall()  # Obtener todos los registros
        columnas = [column[0] for column in cursor.description]  # Nombres de columnas
        
        # Limpieza de datos (reemplaza None con una cadena vacía)
        datos_limpios = [
            tuple("" if valor is None else str(valor).strip("'") for valor in fila)
            for fila in datos
        ]
        print("Consulta ejecutada correctamente.")
        return columnas, datos_limpios
    except Exception as e:
        messagebox.showerror("Error al consultar:", e)
        return [], []
    finally:
        cursor.close()

#Muestra una tabla con los datos de la consulta por medio del codigo_act
def mostrar_tabla_ConsultaActividad(codigo_act):
    """Muestra los datos de la consulta en una ventana de Tkinter."""
    columnas, datos = ConsultaActividad(codigo_act)
    if not columnas or not datos:
        messagebox.showerror("Error", "No hay datos para mostrar o ocurrió un error.")
        return

    # Crear una nueva ventana
    ventana_tabla = tk.Tk()
    ventana_tabla.title(f"Resultados para id_estab = {codigo_act}")

    # Crear el Treeview para mostrar la tabla
    tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings")

    # Configurar encabezados y columnas
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor='center', width=130)

    # Insertar datos en la tabla
    for fila in datos:
        tabla.insert("", "end", values=fila)

    # Empacar la tabla
    tabla.pack(expand=True, fill="both")

    # Iniciar el bucle principal
    ventana_tabla.mainloop()

#Funcion que llama a un procedimiento almacenado que toma los datos de la consulta de busqueda con el id_per_ocu
def Consultaper_ocu(id_per_ocu):
    try:
        cursor = conn.cursor()
        cursor.execute("{CALL Consultaper_ocu (?)}", (id_per_ocu,))
        datos = cursor.fetchall()  # Obtener todos los registros
        columnas = [column[0] for column in cursor.description]  # Nombres de columnas
        
        # Limpieza de datos (reemplaza None con una cadena vacía)
        datos_limpios = [
            tuple("" if valor is None else str(valor).strip("'") for valor in fila)
            for fila in datos
        ]
        print("Consulta ejecutada correctamente.")
        return columnas, datos_limpios
    except Exception as e:
        messagebox.showerror("Error al consultar:", e)
        return [], []
    finally:
        cursor.close()

#Muestra una tabla con los datos de la consulta por medio del id_per_ocu
def mostrar_tabla_Consultaper_ocu(id_per_ocu):
    """Muestra los datos de la consulta en una ventana de Tkinter."""
    columnas, datos = Consultaper_ocu(id_per_ocu)
    if not columnas or not datos:
        messagebox.showerror("Error", "No hay datos para mostrar o ocurrió un error.")
        return

    # Crear una nueva ventana
    ventana_tabla = tk.Tk()
    ventana_tabla.title(f"Resultados para id_estab = {id_per_ocu}")

    # Crear el Treeview para mostrar la tabla
    tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings")

    # Configurar encabezados y columnas
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor='center', width=130)

    # Insertar datos en la tabla
    for fila in datos:
        tabla.insert("", "end", values=fila)

    # Empacar la tabla
    tabla.pack(expand=True, fill="both")

    # Iniciar el bucle principal
    ventana_tabla.mainloop()

# Interfaz gráfica
class MainApp:
    def __init__(self, root,rol):
        self.root = root
        self.root.title("Gestión de Establecimientos")
        self.root.geometry("700x550")
        self.rol = rol  

        # Campos de entrada
        self.fields = {
            "ID Establecimiento": tk.StringVar(),
            "CLEE": tk.StringVar(),
            "Nombre Establecimiento": tk.StringVar(),
            "Razón Social": tk.StringVar(),
            "Teléfono": tk.StringVar(),
            "Correo Electrónico": tk.StringVar(),
            "WWW": tk.StringVar(),
            "Fecha Alta": tk.StringVar(),
            "ID Unidad Económica": tk.StringVar(),
            "Código de Actividad": tk.StringVar(),
            "ID Persona Ocupante": tk.StringVar(),
        }

        row = 0
        for field in self.fields:
            label = tk.Label(root, text=field)
            label.grid(row=row, column=0, padx=10, pady=5)
            entry = tk.Entry(root, textvariable=self.fields[field])
            entry.grid(row=row, column=1, padx=10, pady=5)
            row += 1
        
        columnas_modificables = [
            "CLEE", 
            "Nombre Establecimiento", 
            "Razón Social", 
            "Teléfono", 
            "Correo Electrónico", 
            "WWW", 
            "Fecha Alta"
        ]
        tk.Label(root, text="Columna a Modificar").grid(row=row, column=0, padx=10, pady=5)
        self.columna_modificar = ttk.Combobox(root, values=columnas_modificables, state="readonly")
        self.columna_modificar.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Campo para nuevo dato
        tk.Label(root, text="Nuevo Dato").grid(row=row, column=0, padx=10, pady=5)
        self.nuevo_dato = tk.Entry(root)
        self.nuevo_dato.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Botones
        btn_ConsultaID = tk.Button(root, text="ConsultaID", command=self.ConsultaID)
        btn_ConsultaID.grid(row=row, column=2, padx=10, pady=10)

        btn_Consultanombre = tk.Button(root, text="Consultanombre", command=self.Consultanombre)
        btn_Consultanombre.grid(row=row+1, column=2, padx=10, pady=10)

        btn_ConsultauniEco = tk.Button(root, text="ConsultauniEco", command=self.ConsultauniEco)
        btn_ConsultauniEco.grid(row=row, column=3, padx=10, pady=10)

        btn_ConsultaActividad = tk.Button(root, text="ConsultaActividad", command=self.ConsultaActividad)
        btn_ConsultaActividad.grid(row=row+1, column=3, padx=10, pady=10)

        btn_Consultaper_ocu = tk.Button(root, text="Consultaper_ocu", command=self.Consultaper_ocu)
        btn_Consultaper_ocu.grid(row=row+2, column=2,columnspan=2, padx=10, pady=10)

        btn_insert = tk.Button(root, text="Insertar", command=self.insertar)
        btn_insert.grid(row=row, column=0, padx=10, pady=10)

        btn_delete = tk.Button(root, text="Eliminar", command=self.eliminar)
        btn_delete.grid(row=row, column=1, padx=10, pady=10)

        btn_update = tk.Button(root, text="Actualizar", command=self.actualizar)
        btn_update.grid(row=row + 1, column=0, padx=10, pady=10)

        btn_modify = tk.Button(root, text="Modificar", command=self.modificar)
        btn_modify.grid(row=row + 1, column=1, padx=10, pady=10)

        btn_show = tk.Button(root, text="Mostrar Tabla", command=self.mostrar_tabla)
        btn_show.grid(row=row + 2, column=0, columnspan=2, padx=10, pady=10)
        #Selfs
        self.btn_insert = tk.Button(root, text="Insertar", command=self.insertar)
        self.btn_insert.grid(row=row, column=0, padx=10, pady=10)

        self.btn_delete = tk.Button(root, text="Eliminar", command=self.eliminar)
        self.btn_delete.grid(row=row, column=1, padx=10, pady=10)

        self.btn_update = tk.Button(root, text="Actualizar", command=self.actualizar)
        self.btn_update.grid(row=row + 1, column=0, padx=10, pady=10)

        self.btn_modify = tk.Button(root, text="Modificar", command=self.modificar)
        self.btn_modify.grid(row=row + 1, column=1, padx=10, pady=10)

        if self.rol == "Consultor":
            self.btn_insert.config(state="disabled")
            self.btn_delete.config(state="disabled")
            self.btn_update.config(state="disabled")
            self.btn_modify.config(state="disabled")

    def ConsultaID(self):
        mostrar_tabla_ConsultaID(
            self.fields["ID Establecimiento"].get()
        )

    def Consultanombre(self):
        mostrar_tabla_Consultanombre(
            self.fields["Nombre Establecimiento"].get()
        )

    def ConsultauniEco(self):
        mostrar_tabla_ConsultauniEco(
            self.fields["ID Unidad Económica"].get()
        )

    def ConsultaActividad(self):
        mostrar_tabla_ConsultaActividad(
            self.fields["Código de Actividad"].get()
        )

    def Consultaper_ocu(self):
        mostrar_tabla_Consultaper_ocu(
            self.fields["ID Persona Ocupante"].get()
        )

    def insertar(self):
        insertar_estab(
            self.fields["ID Establecimiento"].get(),
            self.fields["CLEE"].get(),
            self.fields["Nombre Establecimiento"].get(),
            self.fields["Razón Social"].get(),
            self.fields["Teléfono"].get(),
            self.fields["Correo Electrónico"].get(),
            self.fields["WWW"].get(),
            self.fields["Fecha Alta"].get(),
            self.fields["ID Unidad Económica"].get(),
            self.fields["Código de Actividad"].get(),
            self.fields["ID Persona Ocupante"].get()
        )
        

    def eliminar(self):
        eliminar_estab(self.fields["ID Establecimiento"].get())

    def actualizar(self):
        actualizar_estab(
            self.fields["ID Establecimiento"].get(),
            self.fields["CLEE"].get(),
            self.fields["Nombre Establecimiento"].get(),
            self.fields["Razón Social"].get(),
            self.fields["Teléfono"].get(),
            self.fields["Correo Electrónico"].get(),
            self.fields["WWW"].get()
        )
    
    #Hay que trabajar el modificar
    def modificar(self):
        columna_seleccionada = self.columna_modificar.get()
        if not columna_seleccionada:
            messagebox.showerror("Error", "Por favor selecciona una columna para modificar.")
            return
        
        # Traducir la columna seleccionada al formato esperado por la base de datos
        columnas_db = {
            "CLEE": "clee",
            "Nombre Establecimiento": "nombre_estab",
            "Razón Social": "raz_social",
            "Teléfono": "telefono",
            "Correo Electrónico": "correoelec",
            "WWW": "www",
            "Fecha Alta": "fecha_alta",
        }
        columna_db = columnas_db.get(columna_seleccionada)

        modificar_estab(
            self.fields["ID Establecimiento"].get(),
            columna_db,  # Columna traducida
            self.nuevo_dato.get()  # Nuevo dato
        )

    def mostrar_tabla(self):
        columnas, datos = obtener_datos_establecimiento()
        ventana_tabla = tk.Toplevel(self.root)
        ventana_tabla.title("Tabla: Establecimientos")
        tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings")

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=100, anchor='center')

        for fila in datos:
            tabla.insert("", "end", values=fila)

        tabla.pack(expand=True, fill="both")
        ventana_tabla.mainloop()

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("300x200")

        # Widgets
        tk.Label(root, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
        self.usuario_entry = tk.Entry(root)
        self.usuario_entry.grid(row=0, column=1)

        tk.Label(root, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
        self.contrasena_entry = tk.Entry(root, show="*")
        self.contrasena_entry.grid(row=1, column=1)

        btn_login = tk.Button(root, text="Iniciar Sesión", command=self.validar_credenciales)
        btn_login.grid(row=2, column=0, columnspan=2, pady=20)

    def validar_credenciales(self):
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Advertencia", "Debe ingresar ambos campos")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT rol FROM usuarios WHERE usuario=? AND contraseña=?", (usuario, contrasena))
            resultado = cursor.fetchone()
            cursor.close()

            if resultado:
                rol = resultado[0]
                messagebox.showinfo("Éxito", f"Bienvenido {usuario} ({rol})")
                self.abrir_ventana_principal(rol)
            else:
                messagebox.showerror("Error", "Credenciales inválidas")
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar credenciales: {e}")

    def abrir_ventana_principal(self,rol):
        self.root.destroy()  # Cierra la ventana de inicio de sesión
        ventana_principal = tk.Tk()
        MainApp(ventana_principal, rol)
        ventana_principal.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()