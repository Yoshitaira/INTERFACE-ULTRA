import tkinter as tk

class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text='', command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.text = text
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.draw_button()

    def draw_button(self):
        self.delete("all")
        self.create_rounded_rectangle(5, 5, self.winfo_width() - 5, self.winfo_height() - 5, fill="#4CAF50", outline="")
        self.create_text(self.winfo_width() // 2, self.winfo_height() // 2, text=self.text, fill="#FFFFFF", font=("Calibri", 12))

    def create_rounded_rectangle(self, x0, y0, x1, y1, r=20, **kwargs):
        points = [
            x0 + r, y0,
            x1 - r, y0,
            x1, y0 + r,
            x1, y1 - r,
            x1 - r, y1,
            x0 + r, y1,
            x0, y1 - r,
            x0, y0 + r
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_hover(self, event):
        self.draw_button()
        self.create_rounded_rectangle(5, 5, self.winfo_width() - 5, self.winfo_height() - 5, fill="#45A049", outline="")

    def on_leave(self, event):
        self.draw_button()