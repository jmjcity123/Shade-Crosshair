import sys
import subprocess
import tkinter as tk
from tkinter import ttk, colorchooser

# Installation der benötigten Windows-Bibliotheken
try:
    import win32gui, win32con
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    import win32gui, win32con

class CrosshairStudio:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Overlay Fenster (Immer im Vordergrund, durchsichtig)
        self.ov = tk.Toplevel(self.root)
        self.ov.overrideredirect(True)
        self.ov.attributes("-topmost", True)
        self.ov.attributes("-transparentcolor", "black")
        self.ov.config(bg="black")
        
        self.size = 200
        self.color = "#00FF00"
        self.shape = "Kreuz"
        
        self.canvas = tk.Canvas(self.ov, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Click-Through aktivieren
        hwnd = win32gui.GetParent(self.ov.winfo_id())
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        
        self.show_menu()
        
        # Sicherstellen, dass alles beim Schließen beendet wird
        self.menu.protocol("WM_DELETE_WINDOW", self.exit_app)
        
        self.draw()
        self.root.mainloop()

    def show_menu(self):
        self.menu = tk.Toplevel(self.root)
        self.menu.title("HUD Settings")
        self.menu.geometry("320x450")
        self.menu.configure(bg="#121212")
        
        # Header
        ttk.Label(self.menu, text="CROSSHAIR HUD", background="#121212", foreground="#00FF00", font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        # Container für Buttons (nach unten verschoben)
        btn_frame = tk.Frame(self.menu, bg="#121212")
        btn_frame.pack(side="bottom", pady=30, fill="x", padx=20)
        
        for s in ["Kreuz", "Kreis", "Quadrat", "Punkt"]:
            tk.Button(btn_frame, text=s, command=lambda x=s: self.change_shape(x), 
                      bg="#1f1f1f", fg="white", activebackground="#333", relief="flat", height=2).pack(fill="x", pady=2)
        
        # Slider
        ttk.Label(self.menu, text="SKALIERUNG", background="#121212", foreground="#888").pack(pady=(10, 0))
        s = ttk.Scale(self.menu, from_=50, to=400, orient="horizontal", command=self.change_size)
        s.set(200)
        s.pack(fill="x", padx=30, pady=10)
        
        tk.Button(self.menu, text="Farbe wählen", command=self.pick_color, bg="#1f1f1f", fg="white", relief="flat").pack(pady=10)

    def exit_app(self):
        self.ov.destroy()
        self.root.destroy()

    def change_shape(self, shape): self.shape = shape; self.draw()
    def change_size(self, v): self.size = int(float(v)); self.draw()
    def pick_color(self): 
        c = colorchooser.askcolor()[1]
        if c: self.color = c; self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.ov.geometry(f"{self.size}x{self.size}+{self.root.winfo_screenwidth()//2-self.size//2}+{self.root.winfo_screenheight()//2-self.size//2}")
        c = self.size // 2
        
        # Optimierte Proportionen
        L = self.size * 0.075    # 50% kürzere Striche
        G = self.size * 0.0375   # 25% kleinerer Gap
        W = max(1, self.size * 0.02)
        
        if self.shape == "Kreuz":
            self.canvas.create_line(c-G-L, c, c-G, c, fill=self.color, width=W)
            self.canvas.create_line(c+G, c, c+G+L, c, fill=self.color, width=W)
            self.canvas.create_line(c, c-G-L, c, c-G, fill=self.color, width=W)
            self.canvas.create_line(c, c+G, c, c+G+L, fill=self.color, width=W)
        elif self.shape == "Kreis": self.canvas.create_oval(c-L, c-L, c+L, c+L, outline=self.color, width=W)
        elif self.shape == "Quadrat": self.canvas.create_rectangle(c-L, c-L, c+L, c+L, outline=self.color, width=W)
        elif self.shape == "Punkt": self.canvas.create_oval(c-W*2, c-W*2, c+W*2, c+W*2, fill=self.color, outline=self.color)

if __name__ == "__main__":
    CrosshairStudio()