import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
''')
conn.commit()

root = tk.Tk()
root.title('Учёт расходов (простая версия)')


tk.Label(root, text='Название:').grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text='Сумма:').grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text='Дата (ГГГ-ММ-ДД):').grid(row=2, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1, padx=5, pady=5)
date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))


listbox = tk.Listbox(root, width=50)
listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


def add_expense():
    try:
        title = title_entry.get().strip()
        amount = float(amount_entry.get())
        date = date_entry.get()
        
        if not title or amount <= 0:
            messagebox.showerror('Ошибка', 'Название не может быть пустым, сумма > 0!')
            return
            
        cursor.execute('INSERT INTO expenses (title, amount, date) VALUES (?, ?, ?)',
                      (title, amount, date))
        conn.commit()
        
        refresh_list()
        messagebox.showinfo('Успех', 'Расход добавлен!')
        
    except ValueError:
        messagebox.showerror('Ошибка', 'Сумма должна быть числом!')
    except Exception as e:
        messagebox.showerror('Ошибка', f'Ошибка: {e}')

def refresh_list():
    listbox.delete(0, tk.END)
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    for row in cursor.fetchall():
        listbox.insert(tk.END, f'{row[0]} | {row[1]} | {row[2]} руб. | {row[3]}')

def delete_expense():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning('Предупреждение', 'Выберите расход для удаления!')
        return
    
    item = listbox.get(selection[0])
    expense_id = item.split(' | ')[0]
    
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    refresh_list()
    messagebox.showinfo('Успех', 'Расход удалён!')

tk.Button(root, text='Добавить', command=add_expense).grid(row=4, column=0, padx=5, pady=5)
tk.Button(root, text='Обновить', command=refresh_list).grid(row=4, column=1, padx=5, pady=5)
tk.Button(root, text='Удалить', command=delete_expense).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

refresh_list()

root.mainloop()

conn.close()
