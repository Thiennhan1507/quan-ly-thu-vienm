import tkinter as tk
from tkinter import messagebox
import mysql.connector
# NOTE: Adjust this import path if MainMenu_gui is in a package
import MainMenu_gui as MainMenu


class LoginApp:
    """Simple role‑based login screen that checks AdminRecord or UserRecord,
    then launches the appropriate main menu from MainMenu_gui.

    Usage
    -----
    >>> from login_gui import launch_login
    >>> launch_login()
    """

    def __init__(self):
        # === Build UI ===
        self.root = tk.Tk()
        self.root.title("The Book Worm – Login")
        self.root.geometry("360x250")
        self.root.resizable(False, False)

        tk.Label(self.root, text="Sign in to The Book Worm", font=("Arial", 14)).pack(pady=10)

        # --- Username ---
        tk.Label(self.root, text="Username / ID:").pack(anchor="w", padx=40)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(padx=40)

        # --- Password ---
        tk.Label(self.root, text="Password:").pack(anchor="w", padx=40, pady=(8, 0))
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(padx=40)

        # --- Role choice ---
        self.role_var = tk.StringVar(value="User")
        role_frame = tk.Frame(self.root)
        role_frame.pack(pady=10)
        tk.Label(role_frame, text="Role:").pack(side="left")
        tk.Radiobutton(role_frame, text="User", variable=self.role_var, value="User").pack(side="left", padx=5)
        tk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="Admin").pack(side="left", padx=5)

        # --- Buttons ---
        tk.Button(self.root, text="Login", width=12, command=self.check_login).pack(pady=5)
        tk.Button(self.root, text="Exit", width=12, command=self.root.destroy).pack()

        # Bind <Return> to trigger login quickly
        self.root.bind("<Return>", lambda _evt: self.check_login())

        self.root.mainloop()

    # ---------------------------------------------------------------------
    # Database helpers
    # ---------------------------------------------------------------------
    @staticmethod
    def _get_connection():
        """Edit connection params once here."""
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="taolao",
            database="Library",
        )

    # ------------------------------------------------------------------
    # Login logic
    # ------------------------------------------------------------------
    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Missing info", "Please enter both username/ID and password.")
            return

        try:
            db = self._get_connection()
            cur = db.cursor()
            if role == "Admin":
                cur.execute("SELECT Password FROM AdminRecord WHERE AdminID = %s", (username,))
            else:  # User
                cur.execute("SELECT Password FROM UserRecord WHERE UserID = %s", (username,))
            row = cur.fetchone()
        except mysql.connector.Error as err:
            messagebox.showerror("Database error", f"Could not connect/query:\n{err}")
            return
        finally:
            if "db" in locals():
                db.close()

        if row and row[0] == password:
            messagebox.showinfo("Login success", f"Welcome {username}! Logged in as {role}.")
            self.root.destroy()  # close the login window before switching
            if role == "Admin":
                MainMenu.Adminmenu()  # opens Admin main menu (creates its own Tk)
            else:
                MainMenu.Usermenu()
        else:
            messagebox.showerror("Login failed", "Incorrect credentials – please try again.")


# ----------------------------------------------------------------------
# Helper to launch directly
# ----------------------------------------------------------------------

def launch_login():
    """Entry‑point called from other modules or __main__."""
    LoginApp()


if __name__ == "__main__":
    launch_login()
