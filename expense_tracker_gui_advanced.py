import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import json
import matplotlib.pyplot as plt

expenses = []

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("900x600")
root.configure(bg="#f5f7fa")

style = ttk.Style()
style.theme_use("default")
style.configure("TButton", font=("Segoe UI", 10), padding=8)
style.configure("TLabel", font=("Segoe UI", 10), background="#ffffff")
style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#f5f7fa")
style.configure("Card.TFrame", background="#ffffff", relief="flat")

def add_expense():
    try:
        expense = {
            "date": date_entry.get(),
            "category": category_var.get(),
            "description": desc_entry.get(),
            "amount": float(amount_entry.get())
        }
        expenses.append(expense)
        refresh_list()
        clear_fields()
    except ValueError:
        messagebox.showerror("Error", "Invalid amount")

def delete_expense():
    selected = listbox.curselection()
    if selected:
        expenses.pop(selected[0])
        refresh_list()

def edit_expense():
    selected = listbox.curselection()
    if selected:
        i = selected[0]
        expenses[i]["date"] = date_entry.get()
        expenses[i]["category"] = category_var.get()
        expenses[i]["description"] = desc_entry.get()
        expenses[i]["amount"] = float(amount_entry.get())
        refresh_list()

def refresh_list():
    listbox.delete(0, tk.END)
    for e in expenses:
        listbox.insert(
            tk.END,
            f"{e['date']}  |  {e['category']}  |  {e['description']}  |  ₹{e['amount']}"
        )

def clear_fields():
    desc_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def save_csv():
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "category", "description", "amount"])
        writer.writeheader()
        writer.writerows(expenses)
    messagebox.showinfo("Saved", "Saved to CSV")

def save_json():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)
    messagebox.showinfo("Saved", "Saved to JSON")

def load_csv():
    global expenses
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.DictReader(file)
            expenses = []
            for row in reader:
                row["amount"] = float(row["amount"])
                expenses.append(row)
        refresh_list()
    except FileNotFoundError:
        messagebox.showerror("Error", "CSV not found")

def show_chart():
    category_total = {}
    for e in expenses:
        category_total[e["category"]] = category_total.get(e["category"], 0) + e["amount"]
    plt.figure(figsize=(7, 4))
    plt.bar(category_total.keys(), category_total.values())
    plt.title("Category-wise Expense")
    plt.show()

header = ttk.Label(root, text="Expense Tracker", style="Header.TLabel")
header.pack(pady=20)

main_frame = ttk.Frame(root, style="Card.TFrame")
main_frame.pack(padx=30, pady=10, fill="x")

form = ttk.Frame(main_frame, style="Card.TFrame")
form.grid(row=0, column=0, padx=20, pady=20)

ttk.Label(form, text="Date").grid(row=0, column=0, sticky="w")
date_entry = DateEntry(form, width=18)
date_entry.grid(row=0, column=1, pady=5)

ttk.Label(form, text="Category").grid(row=1, column=0, sticky="w")
category_var = tk.StringVar()
category_box = ttk.Combobox(
    form,
    textvariable=category_var,
    values=["Food", "Academic", "Travel", "Shopping", "Makeup", "Other"],
    state="readonly",
    width=16
)
category_box.grid(row=1, column=1, pady=5)
category_box.current(0)

ttk.Label(form, text="Description").grid(row=2, column=0, sticky="w")
desc_entry = ttk.Entry(form, width=20)
desc_entry.grid(row=2, column=1, pady=5)

ttk.Label(form, text="Amount").grid(row=3, column=0, sticky="w")
amount_entry = ttk.Entry(form, width=20)
amount_entry.grid(row=3, column=1, pady=5)

buttons = ttk.Frame(main_frame, style="Card.TFrame")
buttons.grid(row=0, column=1, padx=20)

ttk.Button(buttons, text="Add", command=add_expense).pack(fill="x", pady=4)
ttk.Button(buttons, text="Edit", command=edit_expense).pack(fill="x", pady=4)
ttk.Button(buttons, text="Delete", command=delete_expense).pack(fill="x", pady=4)
ttk.Button(buttons, text="Save CSV", command=save_csv).pack(fill="x", pady=4)
ttk.Button(buttons, text="Save JSON", command=save_json).pack(fill="x", pady=4)
ttk.Button(buttons, text="Load CSV", command=load_csv).pack(fill="x", pady=4)
ttk.Button(buttons, text="Show Chart", command=show_chart).pack(fill="x", pady=4)

list_frame = ttk.Frame(root, style="Card.TFrame")
list_frame.pack(padx=30, pady=20, fill="both", expand=True)

listbox = tk.Listbox(
    list_frame,
    font=("Segoe UI", 10),
    bg="#ffffff",
    relief="flat",
    height=12
)
listbox.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()