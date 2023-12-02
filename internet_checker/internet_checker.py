import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import subprocess
import chardet

class AboutDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About")
        self.geometry("300x200")
        self.configure(bg='black')
        about_text = "Internet Checker App\nVersion 1.0\n(c) 2023 RAREREQUIEM"
        label = tk.Label(self, text=about_text, padx=10, pady=10, bg='black', fg='red')
        label.pack()

class InternetCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.wm_iconbitmap(default=r'C:\Users\POSTAL\internet.ico')

        self.root.title("Internet Checker")
        self.root.geometry("400x650")
        self.root.configure(bg='black')

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="info", menu=help_menu)
        help_menu.add_command(label="about program", command=self.show_about)

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=30)
        self.output_text.pack(pady=10, expand=True, fill="both")
        self.output_text.configure(bg='black', fg='red')

        self.output_text.tk_setPalette(background='black', foreground='black', selectBackground='black', selectForeground='red')

        self.output_text.tag_configure("sel", background="green")


        self.label = tk.Label(root, text="Enter IP Address:")
        self.label.pack(pady=10)
        self.label.configure(bg='black', fg='red')

        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack(pady=5)
        self.ip_entry.configure(bg='black', fg='red')

        self.ping_button = tk.Button(root, text="Check Ping", command=self.check_ping)
        self.ping_button.pack(pady=5)
        self.ping_button.configure(bg='black', fg='red')

        self.trace_button = tk.Button(root, text="Check Traceroute", command=self.check_trace)
        self.trace_button.pack(pady=5)
        self.trace_button.configure(bg='black', fg='red')

        self.copy_button = tk.Button(root, text="Copy", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)
        self.copy_button.configure(bg='black', fg='red')

        self.output_text.tag_configure("sel", background="green")

    def run_command(self, command):
        ip_address = self.ip_entry.get()
        if not ip_address:
            messagebox.showerror("Error", "Enter IP Address")
            return

        try:
            result_bytes = subprocess.check_output(command)
            encoding_result = chardet.detect(result_bytes)
            encoding = encoding_result['encoding']

            if encoding:
                result = result_bytes.decode(encoding, errors='ignore')
            else:
                result = result_bytes.decode('utf-8', errors='ignore')

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Command Output for {ip_address}:\n{result}\n")
            self.output_text.config(state=tk.DISABLED)

            if self.output_text.tag_ranges("sel"):
                self.output_text.tag_remove("sel", tk.SEL_FIRST, tk.SEL_LAST)
                self.output_text.tag_add("sel", tk.SEL_FIRST, tk.SEL_LAST)

        except subprocess.CalledProcessError as e:
            error_message = (
                f"Error during command execution: {e}\n"
                f"Command returned non-zero exit code: {e.returncode}\n"
                f"Error output: {e.output.decode('utf-8', errors='ignore')}\n"
            )
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, error_message)
            self.output_text.config(state=tk.DISABLED)

    def show_about(self):
        about_dialog = AboutDialog(self.root)
        about_dialog.grab_set()

    def check_ping(self):
        self.output_text.delete(1.0, tk.END)
        self.run_command(["ping", "-n", "4", self.ip_entry.get()])

    def check_trace(self):
        self.output_text.delete(1.0, tk.END)
        self.run_command(["tracert", self.ip_entry.get()])

    def copy_to_clipboard(self):
        selected_text = self.output_text.get(1.0, tk.END).strip()

        if not selected_text:
            messagebox.showinfo("Copy", "No text to copy!")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)
        self.root.update()
        messagebox.showinfo("Copy", "Text copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetCheckerApp(root)
    root.mainloop()