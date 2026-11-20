import re
import math
import time

class Variable:
    def __init__(self, factors: dict[str, int] | None = None):
        self.factors = {k: v for k, v in (factors or {}).items() if v != 0}

    @classmethod
    def parse(cls, s: str) -> object:
        factors = {}
        for letter, exp in re.findall(r"([A-Za-z])(?:\^(-?\d+))?", s):
            factors[letter] = factors.get(letter, 0) + (int(exp) if exp else 1)
        return cls(factors)
    
    def __str__(self) -> str:
        return "".join(f"{letter}^{exp}" if exp != 1 else letter for letter, exp in sorted(self.factors.items()))
    
    def __repr__(self) -> str:
        return f"Variable({self.factors})"
    
    def __hash__(self) -> int:
        return hash(frozenset(self.factors.items()))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Variable):
            return self.factors == other.factors
        return False
    
    def __mul__(self, other: object) -> object:
        if isinstance(other, Variable):
            new_factors = self.factors.copy()
            for letter, exp in other.factors.items():
                new_factors[letter] = new_factors.get(letter, 0) + exp
            return Variable(new_factors)
        else:
            return NotImplemented
    
    def __floordiv__(self, other: object) -> object:
        if isinstance(other, Variable):
            new_factors = self.factors.copy()
            for letter, exp in other.factors.items():
                new_factors[letter] = new_factors.get(letter, 0) - exp
            return Variable(new_factors)
        else:
            return NotImplemented
    

class Term:
    def __init__(self,term: str) -> None:
        if term.isnumeric() or term[0] == "-" and term[1:].isnumeric():
            self.coefficient = int(term)
            self.variable = None
            return
        
        m = re.match(r"^([+-]?\d*)([A-Za-z].*)$", term)
        if not m:
            raise ValueError(f"Bad term: {term!r}")
        coeff_str, var_str = m.groups()
        self.coefficient = -1 if coeff_str == "-" else int(coeff_str) if coeff_str else 1
        self.variable = Variable.parse(var_str)
    
    def __str__(self) -> str:
        return f"{self.coefficient}{self.variable if self.variable else ''}"
    
    def __repr__(self) -> str:
        return f"Term({self.coefficient}{self.variable if self.variable else ''})"

    def __or__(self, value: object) -> bool:
        if isinstance(value, Term):
            if self.variable == value.variable:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Term):
            return self.coefficient == other.coefficient and self.variable == other.variable
        return NotImplemented

    def __add__(self, other: object) -> object:
        if isinstance(other, Term):
            if self.variable == other.variable:
                return Term(f"{self.coefficient + other.coefficient}{self.variable if self.variable else ''}")
            else:
                raise ValueError("Cannot add terms with different variables.")
        else:
            return NotImplemented
    
    def __sub__(self, other: object) -> object:
        if isinstance(other, Term):
            if self.variable == other.variable:
                return Term(f"{self.coefficient - other.coefficient}{self.variable if self.variable else ''}")
            else:
                raise ValueError("Cannot subtract terms with different variables.")
    
    def __mul__(self, other: object) -> object:
        if isinstance(other, int) or isinstance(other, float):
            coefficient = self.coefficient * other
            variable = self.variable if self.variable else None
            return Term(f"{coefficient}{variable if variable else ''}")

        if isinstance(other, Term):
            coefficient = self.coefficient * other.coefficient

            if self.variable and other.variable:
                variable = self.variable * other.variable
            elif self.variable:
                variable = self.variable
            elif other.variable:
                variable = other.variable
            else:
                variable = None
            return Term(f"{coefficient}{variable if variable else ''}")
    
    def __floordiv__(self, other: object) -> object:
        if isinstance(other, int) or isinstance(other, float):
            coefficient = self.coefficient // other
            variable = self.variable if self.variable else None
            return Term(f"{coefficient}{variable if variable else ''}")

        if isinstance(other, Term):
            coefficient = self.coefficient // other.coefficient

            if self.variable and other.variable:
                variable = self.variable // other.variable
            elif self.variable:
                variable = self.variable
            elif other.variable:
                variable = other.variable
            else:
                variable = None
            return Term(f"{coefficient}{variable if variable else ''}")
    
    def sqrt(self) -> object:
        if self.coefficient < 0:
            raise ValueError("Cannot take square root of negative term")
        
        coefficient_sqrt = int(self.coefficient ** 0.5)
        variable_sqrt = Variable({k: v // 2 for k, v in self.variable.factors.items()}) if self.variable else None

        return Term(f"{coefficient_sqrt}{variable_sqrt if variable_sqrt else ''}")
    
    def can_sqrt(self) -> bool:
        return can_sqrt(self.coefficient) and (all(exp % 2 == 0 for exp in self.variable.factors.values()) if self.variable else True)
    
    def cbrt(self) -> object:
        coefficient_cbrt = int(math.cbrt(self.coefficient))
        variable_cbrt = Variable({k: v // 3 for k, v in self.variable.factors.items()}) if self.variable else None

        return Term(f"{coefficient_cbrt}{variable_cbrt if variable_cbrt else ''}")
    
    def can_cbrt(self) -> bool:
        return can_cbrt(self.coefficient) and (all(exp % 3 == 0 for exp in self.variable.factors.values()) if self.variable else True)
    
            


class Polynomial:
    def __init__(self, polynomial):
        terms = [Term(term) for term in polynomial.replace("- -", "+ ").replace("-", "+-").replace(" ","").split("+") if term]

        self.terms = terms
    
    def __str__(self) -> str:
        result = " + ".join([str(term) for term in self.terms])
        result = result.replace("+-", "-").replace("+ -", "- ").replace("- -", "+ ")
        
        return result
    
    def __repr__(self) -> str:
        return f"Polynomial({self.terms})"
    
    def __add__(self, other: object) -> object:
        if isinstance(other, Polynomial):
            return simplify_polynomial(Polynomial(str(self) + " + " + str(other)))
        return NotImplemented
    
    def __sub__(self, other: object) -> object:
        if isinstance(other, Polynomial):
            return simplify_polynomial(Polynomial(str(self) + str(other*-1)))
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Term):
            new_terms = [term * other for term in self.terms]
            return Polynomial(" + ".join([str(term) for term in new_terms]))
        if isinstance(other, Polynomial):
            new_terms = []
            for term1 in self.terms:
                for term2 in other.terms:
                    new_terms.append(term1 * term2)
            return simplify_polynomial(Polynomial(" + ".join([str(term) for term in new_terms])))
    
    def __floordiv__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Term):
            new_terms = [term // other for term in self.terms]
            return Polynomial(" + ".join([str(term) for term in new_terms]))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Polynomial):
            return simplify_polynomial(self).terms == simplify_polynomial(other).terms
        return NotImplemented


class PolyProduct:
    def __init__(self, factors: list[Polynomial]):
        self.factors = factors
    
    def __str__(self) -> str:
        return " * ".join([f"({str(factor)})" for factor in self.factors])
    
    def __repr__(self) -> str:
        return f"PolyProduct({self.factors})"
    
    def __mul__(self, other: object) -> object:
        if isinstance(other, PolyProduct):
            return PolyProduct(self.factors + other.factors)
        if isinstance(other, Polynomial):
            return PolyProduct(self.factors + [other])
    

    def evaluate(self) -> object:
        result = self.factors[0]
        for factor in self.factors[1:]:
            result = result * factor
        return simplify_polynomial(result)

def term_sort_key(term: Term):
    if term.variable is None:
        return (0, ())
    degree = sum(term.variable.factors.values())
    letters = tuple(sorted(term.variable.factors.items()))
    return (degree, letters)

def simplify_polynomial(polynomial: Polynomial) -> Polynomial:
    existing_terms = dict()

    for term in polynomial.terms:
        if term.variable in existing_terms:
            existing_terms[term.variable] += term.coefficient
        else:
            existing_terms[term.variable] = term.coefficient

    simplified_terms = [Term(f"{coefficient}{variable if variable else ''}") for variable, coefficient in existing_terms.items() if coefficient != 0]

    simplified_terms = sorted(simplified_terms, key=term_sort_key, reverse=True)

    return Polynomial(" + ".join([str(term) for term in simplified_terms]))

def can_sqrt(a: int) -> bool:
    return a >= 0 and math.isqrt(a) ** 2 == a

def can_cbrt(a: int) -> bool:
    r = round(math.cbrt(a))
    return r ** 3 == a

def gcf_two_numbers(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return abs(a)

def get_gcf(numbers: list[int]) -> int:
    if len(numbers) < 2:
        return numbers[0] if numbers else 1
    
    gcf = numbers[0]

    for i in range(1,len(numbers)):
        gcf = gcf_two_numbers(gcf, numbers[i])    
    
    return gcf
        

def get_polynomial_gcf(polynomial: Polynomial) -> Term:
    if not polynomial.terms:
        return Term("1")
    
    coefficients = [term.coefficient for term in polynomial.terms]

    coefficient_gcf = get_gcf(coefficients)

    variable_gcf = None
    first = True
    for term in polynomial.terms:
        if first:
            variable_gcf = term.variable
            first = False
        elif term.variable is None or variable_gcf is None:
            variable_gcf = None
            break
        else:
            common = set(variable_gcf.factors) & set(term.variable.factors)
            variable_gcf = Variable({k: min(variable_gcf.factors[k], term.variable.factors[k]) for k in common})
    
    if polynomial.terms[0].coefficient < 0:
        coefficient_gcf *= -1

    return Term(f"{coefficient_gcf}{variable_gcf if variable_gcf else ''}")

def get_factors(a: int) -> list[int]:
    result = []
    for i in range(1, abs(a) + 1):
        if a % i == 0:
            result.append(i)
            result.append(-i)

    return result

def factorize_trinomial(poly: Polynomial):
    poly = simplify_polynomial(poly)
    if len(poly.terms) == 3:
        t0, t1, t2 = poly.terms
        a, b, c = t0.coefficient, t1.coefficient, t2.coefficient

        for p in get_factors(a):
            if p == 0 or a % p != 0:
                continue
            r = a // p
            for m in get_factors(c):
                if m == 0 or c % m != 0:
                    continue
                n = c // m
                if p * n + r * m != b:
                    continue
                result = PolyProduct([
                    Polynomial(f"{p}x + {m}"),
                    Polynomial(f"{r}x + {n}"),
                ])
                if result.evaluate() == poly:
                    return result


    if len(poly.terms) == 2:
        if poly.terms[0].can_sqrt() and (poly.terms[1]*-1).can_sqrt():
            result = PolyProduct([Polynomial(f"{poly.terms[0].sqrt()} + {(poly.terms[1]*-1).sqrt()}"), Polynomial(f"{poly.terms[0].sqrt()} - {(poly.terms[1]*-1).sqrt()}")])
            if result.evaluate() == poly:
                return result
        
        if poly.terms[0].can_cbrt() and poly.terms[1].can_cbrt():
            a = poly.terms[0].cbrt()
            b = poly.terms[1].cbrt()
            result = PolyProduct([Polynomial(f"{a} + {b}"), Polynomial(f"{a*a} - {a*b} + {b*b}")])
            if result.evaluate() == poly:
                return result
        
    return None

def factorize_by_grouping(poly: Polynomial):
    poly = simplify_polynomial(poly)
    for i in range(len(poly.terms) - 1):
        for j in range(i, len(poly.terms) - 1):
            group1 = Polynomial(" + ".join([str(term) for term in poly.terms[i:j+1]]))
            group2 = Polynomial(" + ".join([str(term) for term in poly.terms[:i] + poly.terms[j+1:]]))

            gcf1 = get_polynomial_gcf(group1)
            gcf2 = get_polynomial_gcf(group2)

            remaining1 = group1 // gcf1
            remaining2 = group2 // gcf2

            if (gcf1 == remaining2 or gcf2 == remaining1 or remaining1 == remaining2):
                if gcf1 == remaining2:
                    return PolyProduct([gcf1, Polynomial(f"{remaining1} + {remaining2}")])
                elif gcf2 == remaining1:
                    return PolyProduct([gcf2, Polynomial(f"{remaining1} + {remaining2}")])
                elif remaining1 == remaining2:
                    return PolyProduct([remaining1, Polynomial(f"{gcf1} + {gcf2}")])
    return None

                


def factorize_polynomial(poly: Polynomial):
    gcf_term = get_polynomial_gcf(poly)

    poly = poly // gcf_term

    factors = [Polynomial(str(gcf_term))] if gcf_term != Term("1") else []

    changed = True
    while changed:
        changed = False
        poly = simplify_polynomial(poly)

        grouped = factorize_by_grouping(poly)
        if grouped is not None:
            for f in grouped.factors:
                factors.append(f)
            return PolyProduct(factors)
        
        tri = factorize_trinomial(poly)
        if tri is not None:
            factors.extend(tri.factors)
            return PolyProduct(factors)

        break

    if str(poly) != "1":
        factors.append(poly)

    if not factors:
        factors = [Polynomial("1")]    

    return PolyProduct(factors)

