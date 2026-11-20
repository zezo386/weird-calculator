import re

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
            


class Polynomial:
    def __init__(self, polynomial):
        terms = [Term(term) for term in polynomial.replace("-", "+-").replace(" ","").split("+") if term]

        self.terms = terms
    
    def __str__(self) -> str:
        result = " + ".join([str(term) for term in self.terms])
        result = result.replace("+-", "-").replace("+ -", "- ")
        
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
    
    def __floordiv__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Term):
            new_terms = [term // other for term in self.terms]
            return Polynomial(" + ".join([str(term) for term in new_terms]))


class PolyProduct:
    def __init__(self, factors: list[Polynomial]):
        self.factors = factors
    
    def __str__(self) -> str:
        return " * ".join([f"({str(factor)})" for factor in self.factors])

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
    if len(poly.terms) != 3:
        raise ValueError("Polynomial must have 3 terms to factorize as trinomial")

    b = poly.terms[1].coefficient
    c = poly.terms[0].coefficient * poly.terms[2].coefficient

    

    for factor in get_factors(c):
        for factor2 in get_factors(c):
            if factor * factor2 == c:
                if factor + factor2 == b:
                    return PolyProduct([Polynomial(f"{poly.terms[0].sqrt()} + {factor}"), Polynomial(f"{poly.terms[0].sqrt()} + {factor2}")])



    

def factorize_polynomial(poly: Polynomial):
    gcf_term = get_polynomial_gcf(poly)

    remaining_poly = poly // gcf_term

    current_result = PolyProduct([Polynomial(str(gcf_term)), remaining_poly])

    return current_result



p1 = Polynomial("-x+ x^2 - 12")

print(factorize_trinomial(p1))






