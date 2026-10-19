import math
import tkinter as tk
from tkinter import messagebox, ttk


class MegaCalculator:

  def __init__(self, root):
    self.root = root
    self.root.title("Мега Калькулятор 3000")
    self.root.geometry("450x600")
    self.root.resizable(False, False)

    # Настройка стиля
    self.style = ttk.Style()
    self.style.theme_use("clam")

    # Создание вкладки (Notebook)
    self.notebook = ttk.Notebook(root)
    self.notebook.pack(fill="both", expand=True)

    # Инициализация вкладок
    self.create_calc_tab()
    self.create_converter_tab()
    self.create_equation_tab()

  # ==================== ВКЛАДКА 1: ОСНОВНОЙ И ИНЖЕНЕРНЫЙ КАЛЬКУЛЯТОР ====================
  def create_calc_tab(self):
    calc_frame = ttk.Frame(self.notebook)
    self.notebook.add(calc_frame, text="Калькулятор")

    # Поле ввода
    self.calc_entry = ttk.Entry(
        calc_frame, font=("Arial", 20), justify="right"
    )
    self.calc_entry.pack(fill="x", padx=10, pady=10, ipady=10)

    # Сетка кнопок
    buttons_frame = ttk.Frame(calc_frame)
    buttons_frame.pack(fill="both", expand=True, padx=10, pady=5)

    buttons = [
        ("C", 0, 0),
        ("(", 0, 1),
        (")", 0, 2),
        ("/", 0, 3),
        ("sin", 0, 4),
        ("7", 1, 0),
        ("8", 1, 1),
        ("9", 1, 2),
        ("*", 1, 3),
        ("cos", 1, 4),
        ("4", 2, 0),
        ("5", 2, 1),
        ("6", 2, 2),
        ("-", 2, 3),
        ("tan", 2, 4),
        ("1", 3, 0),
        ("2", 3, 1),
        ("3", 3, 2),
        ("+", 3, 3),
        ("x^y", 3, 4),
        ("0", 4, 0),
        (".", 4, 1),
        ("√", 4, 2),
        ("π", 4, 3),
        ("=", 4, 4),
    ]

    for (text, row, col) in buttons:
      btn = ttk.Button(
          buttons_frame, text=text, command=lambda t=text: self.on_calc_click(t)
      )
      btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    # Настройка пропорций сетки
    for i in range(5):
      buttons_frame.rowconfigure(i, weight=1)
    for j in range(5):
      buttons_frame.columnconfigure(j, weight=1)

  def on_calc_click(self, char):
    current = self.calc_entry.get()

    if char == "C":
      self.calc_entry.delete(0, tk.END)
    elif char == "=":
      try:
        # Заменяем визуальные символы на программные
        expression = (
            current.replace("√", "math.sqrt")
            .replace("π", str(math.pi))
            .replace("^", "**")
        )
        expression = (
            expression.replace("sin", "math.sin")
            .replace("cos", "math.cos")
            .replace("tan", "math.tan")
        )
        # Безопасное вычисление выражения
        result = eval(expression)
        self.calc_entry.delete(0, tk.END)
        self.calc_entry.insert(0, str(result))
      except Exception:
        messagebox.showerror("Ошибка", "Неверное выражение!")
    elif char == "x^y":
      self.calc_entry.insert(tk.END, "**")
    elif char in ["sin", "cos", "tan", "√"]:
      self.calc_entry.insert(tk.END, f"{char}(")
    else:
      self.calc_entry.insert(tk.END, char)

  # ==================== ВКЛАДКА 2: КОНВЕРТЕР ВЕЛИЧИН ====================
  def create_converter_tab(self):
    conv_frame = ttk.Frame(self.notebook)
    self.notebook.add(conv_frame, text="Конвертер")

    ttk.Label(
        conv_frame,
        text="Конвертер единиц измерения (КБ в МБ, Километры в Мили)",
        font=("Arial", 10),
    ).pack(pady=10)

    # Выбор типа конвертации
    self.conv_type = ttk.Combobox(
        conv_frame,
        values=["Километры -> Мили", "Мили -> Километры", "МБ -> ГБ", "ГБ -> МБ"],
        state="readonly",
        font=("Arial", 12),
    )
    self.conv_type.pack(pady=10)
    self.conv_type.current(0)

    # Поле ввода значения
    self.conv_input = ttk.Entry(conv_frame, font=("Arial", 14))
    self.conv_input.pack(pady=10, padx=20, fill="x")

    # Кнопка перевода
    ttk.Button(
        conv_frame, text="Конвертировать", command=self.convert_units
    ).pack(pady=10)

    # Результат
    self.conv_result = ttk.Label(
        conv_frame, text="Результат: ", font=("Arial", 14, "bold")
    )
    self.conv_result.pack(pady=20)

  def convert_units(self):
    try:
      val = float(self.conv_input.get())
      choice = self.conv_type.get()

      if choice == "Километры -> Мили":
        res = val * 0.621371
      elif choice == "Мили -> Километры":
        res = val / 0.621371
      elif choice == "МБ -> ГБ":
        res = val / 1024
      elif choice == "ГБ -> МБ":
        res = val * 1024

      self.conv_result.config(text=f"Результат: {res:.4f}")
    except ValueError:
      messagebox.showerror("Ошибка", "Введите число!")

  # ==================== ВКЛАДКА 3: РЕШЕНИЕ УРАВНЕНИЙ ====================
  def create_equation_tab(self):
    eq_frame = ttk.Frame(self.notebook)
    self.notebook.add(eq_frame, text="Уравнения")

    ttk.Label(
        eq_frame,
        text="Решение квадратного уравнения: ax² + bx + c = 0",
        font=("Arial", 11, "bold"),
    ).pack(pady=15)

    # Поля для коэффициентов a, b, c
    fields_frame = ttk.Frame(eq_frame)
    fields_frame.pack(pady=10)

    ttk.Label(fields_frame, text="a:", font=("Arial", 12)).grid(
        row=0, column=0, padx=5
    )
    self.entry_a = ttk.Entry(fields_frame, width=8, font=("Arial", 12))
    self.entry_a.grid(row=0, column=1, padx=5)

    ttk.Label(fields_frame, text="b:", font=("Arial", 12)).grid(
        row=0, column=2, padx=5
    )
    self.entry_b = ttk.Entry(fields_frame, width=8, font=("Arial", 12))
    self.entry_b.grid(row=0, column=3, padx=5)

    ttk.Label(fields_frame, text="c:", font=("Arial", 12)).grid(
        row=0, column=4, padx=5
    )
    self.entry_c = ttk.Entry(fields_frame, width=8, font=("Arial", 12))
    self.entry_c.grid(row=0, column=5, padx=5)

    ttk.Button(
        eq_frame, text="Решить уравнение", command=self.solve_quadratic
    ).pack(pady=15)

    self.eq_result = ttk.Label(
        eq_frame, text="Корни появятся здесь", font=("Arial", 12)
    )
    self.eq_result.pack(pady=10)

  def solve_quadratic(self):
    try:
      a = float(self.entry_a.get())
      b = float(self.entry_b.get())
      c = float(self.entry_c.get())

      if a == 0:
        self.eq_result.config(text="Коэффициент 'a' не должен быть равен 0!")
        return

      discriminant = b**2 - 4 * a * c

      if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        self.eq_result.config(text=(f"Два корня:\nx1 = {x1:.2f}\nx2 = {x2:.2f}"))
      elif discriminant == 0:
        x = -b / (2 * a)
        self.eq_result.config(text=f"Один корень:\nx = {x:.2f}")
      else:
        self.eq_result.config(
            text="Дискриминант меньше нуля.\nНет действительных корней."
        )
    except ValueError:
      messagebox.showerror(
          "Ошибка", "Пожалуйста, заполните все поля числами!"
      )


if __name__ == "__main__":
  root = tk.Tk()
  app = MegaCalculator(root)
  root.mainloop()