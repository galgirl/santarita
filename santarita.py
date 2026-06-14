import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import os

# --- Constantes de Estilo Win2000 ---
BG_COLOR = "#D4D0C8"
FG_COLOR = "#000000"
FONT_DEFAULT = ("MS Sans Serif", 9)
FONT_BOLD = ("MS Sans Serif", 9, "bold")
FONT_TITLE = ("MS Sans Serif", 12, "bold")

class Database:
    """Capa de datos aislada y simplificada."""
    def __init__(self, db_name="registro_estudiantes.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dob TEXT DEFAULT '',
                parent_name TEXT DEFAULT '',
                phone TEXT DEFAULT '',
                mass_absences INTEGER DEFAULT 0,
                class_absences INTEGER DEFAULT 0,
                grade_book REAL DEFAULT 0.0,
                grade_extra REAL DEFAULT 0.0,
                grade_exam REAL DEFAULT 0.0,
                observations TEXT DEFAULT ''
            )
        ''')
        self.conn.commit()

    def get_all(self, search=""):
        self.cursor.execute("SELECT id, name FROM students WHERE name LIKE ? ORDER BY name", (f"%{search}%",))
        return self.cursor.fetchall()

    def get_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        return self.cursor.fetchone()

    def insert(self, name):
        self.cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, student_id, data):
        query = '''UPDATE students SET 
                   name=?, dob=?, parent_name=?, phone=?, 
                   mass_absences=?, class_absences=?, 
                   grade_book=?, grade_extra=?, grade_exam=?, observations=?
                   WHERE id=?'''
        self.cursor.execute(query, (*data, student_id))
        self.conn.commit()

    def delete(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.conn.commit()

class SplashScreen(tk.Toplevel):
    """Ventana de carga brutalista inmune a fallos de archivo."""
    def __init__(self, parent, delay=2500):
        super().__init__(parent)
        self.overrideredirect(True) # Elimina los bordes de ventana de Windows
        self.configure(bg=BG_COLOR)
        
        # Dimensiones y centrado absoluto en pantalla
        width, height = 400, 250
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Intentar cargar "logo.png" de forma nativa
        archivo_imagen = "logo.png"
        if os.path.exists(archivo_imagen):
            try:
                self.img = tk.PhotoImage(file=archivo_imagen)
                lbl = tk.Label(self, image=self.img, bg=BG_COLOR, relief=tk.RAISED, borderwidth=3)
            except Exception:
                lbl = self._get_fallback_label()
        else:
            lbl = self._get_fallback_label()
            
        lbl.pack(fill=tk.BOTH, expand=True)
        
        # Programar la transición al programa principal
        self.after(delay, self.on_finish)

    def _get_fallback_label(self):
        return tk.Label(
            self, 
            text="[ SANTA RITA ]\n\nSistema de Gestión Académica\nCargando base de datos...", 
            font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR, relief=tk.RAISED, borderwidth=3
        )

    def on_finish(self):
        self.destroy() # Destruye el splash
        self.master.deiconify() # Muestra la ventana principal

class RegistroApp:
    """Capa de presentación e interfaz gráfica."""
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Académico - Notas y Asistencia")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_COLOR)
        
        style = ttk.Style()
        style.theme_use('classic')
        
        self.db = Database()
        self.current_id = None
        
        self._init_vars()
        self._build_ui()
        self.refresh_list()

    def _init_vars(self):
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_list())
        
        self.v_name = tk.StringVar()
        self.v_dob = tk.StringVar()
        self.v_parent = tk.StringVar()
        self.v_phone = tk.StringVar()
        
        self.v_mass_abs = tk.IntVar()
        self.v_class_abs = tk.IntVar()
        
        self.v_gr_book = tk.DoubleVar()
        self.v_gr_extra = tk.DoubleVar()
        self.v_gr_exam = tk.DoubleVar()

    def _build_ui(self):
        main_frame = tk.Frame(self.root, bg=BG_COLOR, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- PANEL IZQUIERDO: Lista y Búsqueda ---
        left_frame = tk.Frame(main_frame, bg=BG_COLOR, relief=tk.SUNKEN, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        tk.Label(left_frame, text="Buscar Estudiante:", bg=BG_COLOR, font=FONT_BOLD).pack(anchor=tk.W, padx=5, pady=5)
        tk.Entry(left_frame, textvariable=self.search_var, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=2)

        self.listbox = tk.Listbox(left_frame, width=35, relief=tk.SUNKEN, font=FONT_DEFAULT, exportselection=False)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.load_selected)

        btn_frame = tk.Frame(left_frame, bg=BG_COLOR)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(btn_frame, text="Nuevo", command=self.add_student, relief=tk.RAISED, width=12).pack(side=tk.LEFT, expand=True)
        tk.Button(btn_frame, text="Eliminar", command=self.delete_student, relief=tk.RAISED, width=12).pack(side=tk.RIGHT, expand=True)

        # --- PANEL DERECHO: Formulario de Datos ---
        right_frame = tk.Frame(main_frame, bg=BG_COLOR, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        top_bar = tk.Frame(right_frame, bg=BG_COLOR)
        top_bar.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(top_bar, text="Estudiante:", bg=BG_COLOR, font=FONT_BOLD).pack(side=tk.LEFT)
        tk.Entry(top_bar, textvariable=self.v_name, width=40, font=FONT_TITLE, relief=tk.SUNKEN).pack(side=tk.LEFT, padx=10)
        tk.Button(top_bar, text="💾 GUARDAR CAMBIOS", command=self.save_student, font=FONT_BOLD, relief=tk.RAISED).pack(side=tk.RIGHT)

        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pestaña 1: Datos Personales
        tab_personal = tk.Frame(notebook, bg=BG_COLOR)
        notebook.add(tab_personal, text=" Datos Personales ")
        
        tk.Label(tab_personal, text="Fecha de Nac.:", bg=BG_COLOR).grid(row=0, column=0, sticky=tk.W, padx=10, pady=15)
        tk.Entry(tab_personal, textvariable=self.v_dob, relief=tk.SUNKEN, width=20).grid(row=0, column=1, sticky=tk.W)
        
        tk.Label(tab_personal, text="Representante:", bg=BG_COLOR).grid(row=1, column=0, sticky=tk.W, padx=10, pady=15)
        tk.Entry(tab_personal, textvariable=self.v_parent, relief=tk.SUNKEN, width=40).grid(row=1, column=1, sticky=tk.W)
        
        tk.Label(tab_personal, text="Teléfono:", bg=BG_COLOR).grid(row=2, column=0, sticky=tk.W, padx=10, pady=15)
        tk.Entry(tab_personal, textvariable=self.v_phone, relief=tk.SUNKEN, width=20).grid(row=2, column=1, sticky=tk.W)

        # Pestaña 2: Notas y Faltas
        tab_academic = tk.Frame(notebook, bg=BG_COLOR)
        notebook.add(tab_academic, text=" Control Académico ")

        frame_faltas = tk.LabelFrame(tab_academic, text=" Inasistencias ", bg=BG_COLOR, font=FONT_BOLD)
        frame_faltas.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(frame_faltas, text="Faltas Misa:", bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(frame_faltas, textvariable=self.v_mass_abs, width=8, relief=tk.SUNKEN).grid(row=0, column=1)
        tk.Label(frame_faltas, text="Faltas Clase:", bg=BG_COLOR).grid(row=0, column=2, padx=20, pady=10)
        tk.Entry(frame_faltas, textvariable=self.v_class_abs, width=8, relief=tk.SUNKEN).grid(row=0, column=3)

        frame_notas = tk.LabelFrame(tab_academic, text=" Calificaciones ", bg=BG_COLOR, font=FONT_BOLD)
        frame_notas.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(frame_notas, text="Nota Libro:", bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(frame_notas, textvariable=self.v_gr_book, width=8, relief=tk.SUNKEN).grid(row=0, column=1)
        tk.Label(frame_notas, text="Nota Extra:", bg=BG_COLOR).grid(row=0, column=2, padx=20, pady=10)
        tk.Entry(frame_notas, textvariable=self.v_gr_extra, width=8, relief=tk.SUNKEN).grid(row=0, column=3)
        tk.Label(frame_notas, text="Examen:", bg=BG_COLOR).grid(row=0, column=4, padx=20, pady=10)
        tk.Entry(frame_notas, textvariable=self.v_gr_exam, width=8, relief=tk.SUNKEN).grid(row=0, column=5)

        tk.Label(tab_academic, text="Observaciones:", bg=BG_COLOR, font=FONT_BOLD).pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.txt_obs = tk.Text(tab_academic, height=4, relief=tk.SUNKEN)
        self.txt_obs.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for s in self.db.get_all(self.search_var.get()):
            self.listbox.insert(tk.END, f"{s[0]} | {s[1]}")

    def add_student(self):
        name = simpledialog.askstring("Nuevo Estudiante", "Ingrese nombre y apellido del estudiante:", parent=self.root)
        if name and name.strip():
            new_id = self.db.insert(name.strip())
            self.refresh_list()
            
            for i in range(self.listbox.size()):
                if self.listbox.get(i).startswith(f"{new_id} |"):
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(i)
                    self.listbox.event_generate('<<ListboxSelect>>')
                    break

    def load_selected(self, event):
        sel = self.listbox.curselection()
        if not sel: return
        
        self.current_id = int(self.listbox.get(sel[0]).split(" | ")[0])
        data = self.db.get_by_id(self.current_id)
        
        if data:
            self.v_name.set(data[1])
            self.v_dob.set(data[2])
            self.v_parent.set(data[3])
            self.v_phone.set(data[4])
            self.v_mass_abs.set(data[5])
            self.v_class_abs.set(data[6])
            self.v_gr_book.set(data[7])
            self.v_gr_extra.set(data[8])
            self.v_gr_exam.set(data[9])
            
            self.txt_obs.delete("1.0", tk.END)
            self.txt_obs.insert(tk.END, data[10])

    def save_student(self):
        if not self.current_id:
            messagebox.showwarning("Atención", "Seleccione un estudiante primero.")
            return
            
        try:
            data = (
                self.v_name.get(), self.v_dob.get(), self.v_parent.get(), self.v_phone.get(),
                self.v_mass_abs.get(), self.v_class_abs.get(),
                self.v_gr_book.get(), self.v_gr_extra.get(), self.v_gr_exam.get(),
                self.txt_obs.get("1.0", tk.END).strip()
            )
            self.db.update(self.current_id, data)
            self.refresh_list()
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        except tk.TclError:
            messagebox.showerror("Error", "Por favor, verifique que las notas y faltas sean valores numéricos válidos.")

    def delete_student(self):
        if not self.current_id: return
        if messagebox.askyesno("Confirmar", "¿Eliminar permanentemente este registro?"):
            self.db.delete(self.current_id)
            self.current_id = None
            self.refresh_list()
            self._clear_form()

    def _clear_form(self):
        self.v_name.set("")
        self.v_dob.set("")
        self.v_parent.set("")
        self.v_phone.set("")
        self.v_mass_abs.set(0)
        self.v_class_abs.set(0)
        self.v_gr_book.set(0.0)
        self.v_gr_extra.set(0.0)
        self.v_gr_exam.set(0.0)
        self.txt_obs.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Mantiene oculta la ventana principal al inicio
    
    # Lanza el Splash Screen de forma asíncrona por 2.5 segundos
    splash = SplashScreen(root, delay=2500) 
    app = RegistroApp(root)
    
    root.mainloop()