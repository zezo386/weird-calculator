import tkinter as tk
from tkinter import ttk, messagebox

from terms import (
    Polynomial, Term, PolyProduct, Fraction,
    simplify_polynomial, factorize_polynomial,
)


class CalculatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Weird fraction Calculator")
        self.root.geometry("600x400")

        input_frame = ttk.Frame(root, padding=8)
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="enter your mathy thing here:").pack(side=tk.LEFT)
        self.entry = ttk.Entry(input_frame, font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.entry.bind("<Return>", lambda e: self.compute())

        op_frame = ttk.Frame(root, padding=(8, 0))
        op_frame.pack(fill=tk.X)

        ttk.Label(op_frame, text="Operation:").pack(side=tk.LEFT)
        self.operation = tk.StringVar(value="simplify")
        ops = ["simplify", "factor", "evaluate fraction", "multiply fractions", "add fractions"]
        op_combo = ttk.Combobox(
            op_frame, textvariable=self.operation, values=ops, state="readonly", width=20
        )
        op_combo.pack(side=tk.LEFT, padx=8)

        btn_frame = ttk.Frame(root, padding=8)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Compute", command=self.compute).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=8)

        ttk.Label(root, text="Result:", padding=(8, 0)).pack(anchor="w")
        self.output = tk.Text(root, height=10, font=("Consolas", 12), wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        hint = (
            "Examples:\n"
            "  simplify:  x^2 + 5x + 6\n"
            "  factor:    x^2 + 5x + 6\n"
            "  evaluate fraction:  (x^2 - 9) / (x + 3)\n"
            "  multiply fractions:  (x^2 - 9)/(x+3) * (x+3)/(x-3)\n"
            "  add fractions:       (5x-8)/(x-3) + (2x+1)/(x-3)"
        )
        self.output.insert(tk.END, hint)

    def compute(self):
        expr = self.entry.get().strip()
        if not expr:
            return

        op = self.operation.get()

        try:
            if op == "simplify":
                result = simplify_polynomial(Polynomial(expr))
            elif op == "factor":
                result = factorize_polynomial(Polynomial(expr))
            elif op == "evaluate fraction":
                result = self._parse_fraction(expr)
            elif op == "multiply fractions":
                left, right = self._split_op(expr, "*")
                result = self._parse_fraction(left) * self._parse_fraction(right)
            elif op == "add fractions":
                left, right = self._split_op(expr, "+")
                result = self._parse_fraction(left) + self._parse_fraction(right)
            else:
                raise ValueError(f"Unknown operation: {op}")

            self._show(str(result))

        except Exception as e:
            messagebox.showerror("Error", f"{type(e).__name__}: {e}")
            self._show(f"ERROR: {e}")

    def _parse_fraction(self, s: str) -> Fraction:
        s = s.strip()
        if "/" not in s:
            return Fraction(
                PolyProduct([Polynomial(s)]),
                PolyProduct([Polynomial("1")]),
            )

        num_str, den_str = s.split("/", 1)
        num_str = num_str.strip().strip("()")
        den_str = den_str.strip().strip("()")

        return Fraction(
            PolyProduct([Polynomial(num_str)]),
            PolyProduct([Polynomial(den_str)]),
        )

    def _split_op(self, s: str, op: str):
        depth = 0
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == op and depth == 0:
                return s[:i], s[i + 1:]
        raise ValueError(f"No top-level '{op}' found in {s!r}")

    def _show(self, text: str):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def clear(self):
        self.entry.delete(0, tk.END)
        self.output.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    CalculatorApp(root)
    root.mainloop()