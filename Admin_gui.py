import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import Tables_gui as Tables
class AdminApp:
    def __init__(self):
        self.mydb = mysql.connector.connect(host="127.0.0.1", user="root", passwd="taolao", database="Library")
        self.mycursor = self.mydb.cursor()

    def displayAdmin(self):
        win = tk.Toplevel()
        win.title("Display Admin Records")
        win.geometry("400x400")

        tree = ttk.Treeview(win, columns=("AdminID", "Password"), show="headings")
        tree.heading("AdminID", text="AdminID")
        tree.heading("Password", text="Password")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("SELECT * FROM AdminRecord")
        records = self.mycursor.fetchall()
        for i, row in enumerate(records, 1):
            tree.insert("", "end", values=(row[0], row[1]))

        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def insertAdmin(self):
        win = tk.Toplevel()
        win.title("Add Admin Record")
        win.geometry("300x200")

        tk.Label(win, text="Add Admin", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="AdminID:").pack()
        admin_id_entry = tk.Entry(win)
        admin_id_entry.pack()

        tk.Label(win, text="Password:").pack()
        password_entry = tk.Entry(win, show="*")
        password_entry.pack()

        def add_admin():
            admin_id = admin_id_entry.get()
            password = password_entry.get()
            if admin_id and password:
                query = "INSERT INTO AdminRecord VALUES (%s, %s)"
                self.mycursor.execute(query, (admin_id, password))
                self.mydb.commit()
                messagebox.showinfo("Success", "Admin added successfully")
                if not messagebox.askyesno("Continue", "Do you wish to add more Administrators?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        tk.Button(win, text="Add", command=add_admin).pack(pady=10)

    def deleteAdmin(self):
        win = tk.Toplevel()
        win.title("Delete Admin Record")
        win.geometry("300x150")

        tk.Label(win, text="Delete Admin", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="AdminID:").pack()
        admin_id_entry = tk.Entry(win)
        admin_id_entry.pack()

        def delete_admin():
            admin_id = admin_id_entry.get()
            if admin_id:
                self.mycursor.execute("DELETE FROM AdminRecord WHERE AdminID=%s", (admin_id,))
                self.mydb.commit()
                messagebox.showinfo("Success", "Admin deleted successfully")
                if not messagebox.askyesno("Continue", "Do you wish to delete more Administrators?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please enter AdminID")

        tk.Button(win, text="Delete", command=delete_admin).pack(pady=10)

    def searchAdmin(self):
        win = tk.Toplevel()
        win.title("Search Admin Record")
        win.geometry("300x200")

        tk.Label(win, text="Search Admin", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="AdminID:").pack()
        admin_id_entry = tk.Entry(win)
        admin_id_entry.pack()

        def search_admin():
            admin_id = admin_id_entry.get()
            if admin_id:
                self.mycursor.execute("SELECT * FROM AdminRecord WHERE AdminID=%s", (admin_id,))
                records = self.mycursor.fetchall()
                if records:
                    result_win = tk.Toplevel()
                    result_win.title("Search Result")
                    result_win.geometry("300x150")
                    for row in records:
                        tk.Label(result_win, text=f"AdminID: {row[0]}").pack()
                        tk.Label(result_win, text=f"Password: {row[1]}").pack()
                    tk.Button(result_win, text="Close", command=result_win.destroy).pack(pady=10)
                else:
                    messagebox.showinfo("Result", "Search Unsuccessful")
                if not messagebox.askyesno("Continue", "Do you wish to search more Administrators?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please enter AdminID")

        tk.Button(win, text="Search", command=search_admin).pack(pady=10)

    def updateAdmin(self):
        win = tk.Toplevel()
        win.title("Update Admin Record")
        win.geometry("300x200")

        tk.Label(win, text="Update Admin", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="AdminID:").pack()
        admin_id_entry = tk.Entry(win)
        admin_id_entry.pack()

        tk.Label(win, text="New Password:").pack()
        password_entry = tk.Entry(win, show="*")
        password_entry.pack()

        def update_admin():
            admin_id = admin_id_entry.get()
            password = password_entry.get()
            if admin_id and password:
                query = "UPDATE AdminRecord SET Password=%s WHERE AdminID=%s"
                self.mycursor.execute(query, (password, admin_id))
                self.mydb.commit()
                messagebox.showinfo("Success", "Admin updated successfully")
                if not messagebox.askyesno("Continue", "Do you wish to update more Administrators?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        tk.Button(win, text="Update", command=update_admin).pack(pady=10)