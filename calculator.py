import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", padding=5, font=('Arial', 12))
        
        # Display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display = ttk.Entry(
            root,
            textvariable=self.display_var,
            justify="right",
            font=('Arial', 20),
            state='readonly'
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        # Buttons layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('CE', 5, 1), ('√', 5, 2), ('^', 5, 3)
        ]
        
        for (text, row, col) in buttons:
            button = ttk.Button(
                root,
                text=text,
                command=lambda t=text: self.button_click(t)
            )
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # Configure grid weights
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
            
        self.current_expression = ""
        self.last_was_operator = False
        
    def button_click(self, value):
        if value == "C":
            self.current_expression = ""
            self.display_var.set("0")
        elif value == "CE":
            self.current_expression = self.current_expression[:-1]
            self.display_var.set(self.current_expression if self.current_expression else "0")
        elif value == "=":
            try:
                # Replace √ with math.sqrt and ^ with **
                expression = self.current_expression.replace("^", "**").replace("√", "math.sqrt")
                result = eval(expression)
                self.current_expression = str(result)
                self.display_var.set(self.current_expression)
            except:
                self.display_var.set("Error")
                self.current_expression = ""
        elif value == "√":
            if self.current_expression:
                try:
                    num = float(self.current_expression)
                    result = math.sqrt(num)
                    self.current_expression = str(result)
                    self.display_var.set(self.current_expression)
                except:
                    self.display_var.set("Error")
                    self.current_expression = ""
        else:
            self.current_expression += value
            self.display_var.set(self.current_expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop() 