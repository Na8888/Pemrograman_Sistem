import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Fungsi untuk menghubungkan ke database dan membuat tabel jika belum ada
def connect_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, 
                  title TEXT, 
                  description TEXT, 
                  category TEXT, 
                  priority TEXT, 
                  due_date TEXT)''')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan tugas
def add_task():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, category, priority, due_date) VALUES (?, ?, ?, ?, ?)",
              (title_var.get(), description_var.get(), category_var.get(), priority_var.get(), due_date_var.get()))
    conn.commit()
    conn.close()
    load_tasks()
    clear_fields()

# Fungsi untuk memuat tugas ke dalam treeview
def load_tasks():
    for i in tree.get_children():
        tree.delete(i)
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree.insert("", END, values=row)

# Fungsi untuk menghapus tugas
def delete_task():
    selected_task = tree.selection()
    if selected_task:
        task_id = tree.item(selected_task)['values'][0]
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Select a task to delete")

# Fungsi untuk mengedit tugas
def edit_task():
    selected_task = tree.selection()
    if selected_task:
        task_id = tree.item(selected_task)['values'][0]
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET title=?, description=?, category=?, priority=?, due_date=? WHERE id=?",
                  (title_var.get(), description_var.get(), category_var.get(), priority_var.get(), due_date_var.get(), task_id))
        conn.commit()
        conn.close()
        load_tasks()
        clear_fields()
    else:
        messagebox.showwarning("Warning", "Select a task to edit")

# Fungsi untuk mengisi field dengan data tugas yang dipilih
def fill_fields(event):
    selected_task = tree.selection()
    if selected_task:
        task = tree.item(selected_task)['values']
        title_var.set(task[1])
        description_var.set(task[2])
        category_var.set(task[3])
        priority_var.set(task[4])
        due_date_var.set(task[5])

# Fungsi untuk menghapus isi field
def clear_fields():
    title_var.set("")
    description_var.set("")
    category_var.set("")
    priority_var.set("")
    due_date_var.set("")

# Setup GUI menggunakan tkinter
root = Tk()
root.title("Task Managerku")

# Variabel untuk input
title_var = StringVar()
description_var = StringVar()
category_var = StringVar()
priority_var = StringVar()
due_date_var = StringVar()

# Label dan Entry untuk judul
Label(root, text="Title (masukan judul tugas)").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=title_var).grid(row=0, column=1, padx=10, pady=5)

# Label dan Entry untuk deskripsi
Label(root, text="Description (deskripsikan tugas)").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=description_var).grid(row=1, column=1, padx=10, pady=5)

# Label dan Entry untuk kategori
Label(root, text="Category (contoh: kerja/pendidikan/pribadi)").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=category_var).grid(row=2, column=1, padx=10, pady=5)

# Label dan Combobox untuk prioritas
Label(root, text="Priority (tinggi/sedang/rendah)").grid(row=3, column=0, padx=10, pady=5)
priority_combobox = ttk.Combobox(root, textvariable=priority_var, values=["Rendah", "Sedang", "Tinggi"])
priority_combobox.grid(row=3, column=1, padx=10, pady=5)

# Label dan Entry untuk tanggal batas akhir
Label(root, text="Due Date (contoh: 2004-05-19)").grid(row=4, column=0, padx=10, pady=5)
Entry(root, textvariable=due_date_var).grid(row=4, column=1, padx=10, pady=5)

# Tombol untuk menambahkan, menghapus, dan mengedit tugas
Button(root, text="Tambah Tugas", command=add_task).grid(row=5, column=0, padx=10, pady=5)
Button(root, text="Edit", command=edit_task).grid(row=5, column=1, padx=10, pady=5)
Button(root, text="Hapus", command=delete_task).grid(row=5, column=2, padx=10, pady=5)

# Treeview untuk menampilkan tugas
columns = ("ID", "Title", "Description", "Category", "Priority", "Due Date")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("ID", text="ID")
tree.heading("Title", text="Title")
tree.heading("Description", text="Description")
tree.heading("Category", text="Category")
tree.heading("Priority", text="Priority")
tree.heading("Due Date", text="Due Date")
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=5)
tree.bind('<<TreeviewSelect>>', fill_fields)

# Load tugas saat aplikasi dimulai
connect_db()
load_tasks()

root.mainloop()
