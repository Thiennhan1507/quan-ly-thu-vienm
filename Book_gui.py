import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import Tables_gui as Tables
class BookApp:
    def __init__(self):
        self.mydb = mysql.connector.connect(host="localhost", user="root", passwd="200511", database="Library")
        self.mycursor = self.mydb.cursor()

    def displayBook(self):
        win = tk.Toplevel()
        win.title("Display Book Records")
        win.geometry("600x400")

        tree = ttk.Treeview(win, columns=("BookID", "BookName", "Author", "Publisher", "IssuedBy", "UserID"), show="headings")
        tree.heading("BookID", text="BookID")
        tree.heading("BookName", text="BookName")
        tree.heading("Author", text="Author")
        tree.heading("Publisher", text="Publisher")
        tree.heading("IssuedBy", text="Issued By")
        tree.heading("UserID", text="UserID")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("""SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher, 
                                UserRecord.UserName, UserRecord.UserID
                                FROM BookRecord LEFT JOIN UserRecord ON BookRecord.BookID=UserRecord.BookID""")
        records = self.mycursor.fetchall()
        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def insertBook(self):
        win = tk.Toplevel()
        win.title("Add Book Record")
        win.geometry("300x300")

        tk.Label(win, text="Add Book", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="BookID:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        tk.Label(win, text="Book Name:").pack()
        book_name_entry = tk.Entry(win)
        book_name_entry.pack()

        tk.Label(win, text="Author:").pack()
        author_entry = tk.Entry(win)
        author_entry.pack()

        tk.Label(win, text="Publisher:").pack()
        publisher_entry = tk.Entry(win)
        publisher_entry.pack()

        def add_book():
            book_id = book_id_entry.get()
            book_name = book_name_entry.get()
            author = author_entry.get()
            publisher = publisher_entry.get()
            if all([book_id, book_name, author, publisher]):
                query = "INSERT INTO BookRecord VALUES (%s, %s, %s, %s)"
                self.mycursor.execute(query, (book_id, book_name, author, publisher))
                self.mydb.commit()
                messagebox.showinfo("Success", "Book added successfully")
                if not messagebox.askyesno("Continue", "Do you wish to add more Books?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        tk.Button(win, text="Add", command=add_book).pack(pady=10)

    def deleteBook(self):
        win = tk.Toplevel()
        win.title("Delete Book Record")
        win.geometry("300x150")

        tk.Label(win, text="Delete Book", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="BookID:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        def delete_book():
            book_id = book_id_entry.get()
            if book_id:
                self.mycursor.execute("DELETE FROM BookRecord WHERE BookID=%s", (book_id,))
                self.mydb.commit()
                messagebox.showinfo("Success", "Book deleted successfully")
                if not messagebox.askyesno("Continue", "Do you wish to delete more Books?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please enter BookID")

        tk.Button(win, text="Delete", command=delete_book).pack(pady=10)

    def searchBook(self):
        win = tk.Toplevel()
        win.title("Search Book Record")
        win.geometry("300x200")

        tk.Label(win, text="Search Book", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="BookID:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        def search_book():
            book_id = book_id_entry.get()
            if book_id:
                self.mycursor.execute("""SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher,
                                        UserRecord.UserName, UserRecord.UserID
                                        FROM BookRecord LEFT JOIN UserRecord ON BookRecord.BookID=UserRecord.BookID
                                        WHERE BookRecord.BookID=%s""", (book_id,))
                records = self.mycursor.fetchall()
                if records:
                    result_win = tk.Toplevel()
                    result_win.title("Search Result")
                    result_win.geometry("400x200")
                    for row in records:
                        tk.Label(result_win, text=f"BookID: {row[0]}").pack()
                        tk.Label(result_win, text=f"BookName: {row[1]}").pack()
                        tk.Label(result_win, text=f"Author: {row[2]}").pack()
                        tk.Label(result_win, text=f"Publisher: {row[3]}").pack()
                        tk.Label(result_win, text=f"Issued By: {row[4]}").pack()
                        tk.Label(result_win, text=f"UserID: {row[5]}").pack()
                    tk.Button(result_win, text="Close", command=result_win.destroy).pack(pady=10)
                else:
                    messagebox.showinfo("Result", "Search Unsuccessful")
                if not messagebox.askyesno("Continue", "Do you wish to search more Books?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please enter BookID")

        tk.Button(win, text="Search", command=search_book).pack(pady=10)

    def updateBook(self):
        win = tk.Toplevel()
        win.title("Update Book Record")
        win.geometry("300x300")

        tk.Label(win, text="Update Book", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="BookID:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        tk.Label(win, text="Book Name:").pack()
        book_name_entry = tk.Entry(win)
        book_name_entry.pack()

        tk.Label(win, text="Author:").pack()
        author_entry = tk.Entry(win)
        author_entry.pack()

        tk.Label(win, text="Publisher:").pack()
        publisher_entry = tk.Entry(win)
        publisher_entry.pack()

        def update_book():
            book_id = book_id_entry.get()
            book_name = book_name_entry.get()
            author = author_entry.get()
            publisher = publisher_entry.get()
            if all([book_id, book_name, author, publisher]):
                query = "UPDATE BookRecord SET BookName=%s, Author=%s, Publisher=%s WHERE BookID=%s"
                self.mycursor.execute(query, (book_name, author, publisher, book_id))
                self.mydb.commit()
                messagebox.showinfo("Success", "Book updated successfully")
                if not messagebox.askyesno("Continue", "Do you wish to update more Books?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        tk.Button(win, text="Update", command=update_book).pack(pady=10)

    def BookList(self):
        win = tk.Toplevel()
        win.title("List of All Books")
        win.geometry("400x400")

        tree = ttk.Treeview(win, columns=("BookID", "BookName", "Author", "Publisher"), show="headings")
        tree.heading("BookID", text="BookID")
        tree.heading("BookName", text="BookName")
        tree.heading("Author", text="Author")
        tree.heading("Publisher", text="Publisher")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("SELECT * FROM BookRecord")
        records = self.mycursor.fetchall()
        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def IssueBook(self):
        win = tk.Toplevel()
        win.title("Issue Book")
        win.geometry("400x400")

        tk.Label(win, text="Issue Book", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="Enter your UserID:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        def check_user():
            user_id = user_id_entry.get()
            if user_id:
                self.mycursor.execute("SELECT BookID FROM UserRecord WHERE UserID=%s", (user_id,))
                checking = self.mycursor.fetchone()
                if checking and checking[0] is None:
                    tree_frame = tk.Frame(win)
                    tree_frame.pack(fill="both", expand=True)
                    
                    tree = ttk.Treeview(tree_frame, columns=("BookID", "BookName", "Author", "Publisher"), show="headings")
                    tree.heading("BookID", text="BookID")
                    tree.heading("BookName", text="BookName")
                    tree.heading("Author", text="Author")
                    tree.heading("Publisher", text="Publisher")
                    tree.pack(fill="both", expand=True)

                    self.mycursor.execute("""SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher,
                                            UserRecord.UserName, UserRecord.UserID
                                            FROM BookRecord LEFT JOIN UserRecord ON BookRecord.BookID=UserRecord.BookID""")
                    records = self.mycursor.fetchall()
                    available_books = [row for row in records if row[5] is None]
                    for row in available_books:
                        tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))

                    if not available_books:
                        messagebox.showinfo("Info", "No available books in the Library")
                        win.destroy()
                        return

                    tk.Label(win, text="Enter BookID to issue:").pack()
                    book_id_entry = tk.Entry(win)
                    book_id_entry.pack()

                    def issue_book():
                        book_id = book_id_entry.get()
                        query = "UPDATE UserRecord SET BookID=%s WHERE UserID=%s"
                        self.mycursor.execute(query, (book_id, user_id))
                        self.mydb.commit()
                        messagebox.showinfo("Success", "Book successfully issued")
                        win.destroy()

                    tk.Button(win, text="Issue", command=issue_book).pack(pady=10)
                else:
                    messagebox.showerror("Error", "Book already issued. Please return it first.")
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please enter UserID")

        tk.Button(win, text="Check", command=check_user).pack(pady=10)

    def ShowIssuedBook(self):
        win = tk.Toplevel()
        win.title("Issued Book Records")
        win.geometry("400x300")

        tk.Label(win, text="Enter your UserID:").pack(pady=10)
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        def show_issued():
            user_id = user_id_entry.get()
            if user_id:
                self.mycursor.execute("""SELECT UserRecord.UserID, UserRecord.UserName, UserRecord.BookID, BookRecord.BookName
                                        FROM UserRecord INNER JOIN BookRecord ON UserRecord.BookID=BookRecord.BookID
                                        WHERE UserID=%s""", (user_id,))
                records = self.mycursor.fetchall()
                if records:
                    result_win = tk.Toplevel()
                    result_win.title("Issued Book")
                    result_win.geometry("400x200")
                    for row in records:
                        tk.Label(result_win, text=f"UserID: {row[0]}").pack()
                        tk.Label(result_win, text=f"UserName: {row[1]}").pack()
                        tk.Label(result_win, text=f"BookID: {row[2]}").pack()
                        tk.Label(result_win, text=f"BookName: {row[3]}").pack()
                    tk.Button(result_win, text="Close", command=result_win.destroy).pack(pady=10)
                else:
                    messagebox.showinfo("Info", "No book issued")
                win.destroy()
            else:
                messagebox.showerror("Error", "Please enter UserID")

        tk.Button(win, text="Show", command=show_issued).pack(pady=10)

    def returnBook(self):
        win = tk.Toplevel()
        win.title("Return Book")
        win.geometry("300x200")

        tk.Label(win, text="Return Book", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="Enter your UserID:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        tk.Label(win, text="Enter BookID to return:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        def return_book():
            user_id = user_id_entry.get()
            book_id = book_id_entry.get()
            if user_id and book_id:
                query = "UPDATE UserRecord SET BookID=%s WHERE UserID=%s AND BookID=%s"
                self.mycursor.execute(query, (None, user_id, book_id))
                self.mydb.commit()
                messagebox.showinfo("Success", "Return successful")
                win.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        tk.Button(win, text="Return", command=return_book).pack(pady=10)