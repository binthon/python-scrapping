# Ponowne zdefiniowanie warunków
import sympy as sp
f = 50 * 10**3  # 50 kHz
R1 = R2 = 1 * 10**3  # 1 kOhm
C1 = C2 = 100 * 10**-9  # 100 nF

# Pulsacja
omega = 2 * sp.pi * f

# Impedancje
Z_C = 1 / (sp.I * omega * C1)
Z_R = R1

# Całkowita impedancja dla szeregowego połączenia R i C
Z_total = Z_R + Z_C

# Napięcie na kondensatorze jako stosunek impedancji
U_C = Z_C / Z_total

# Napięcie na rezystorze
U_R = Z_R / Z_total

# Obliczenie argumentu (fazy) dla napięcia na kondensatorze i rezystorze
arg_U_C = sp.arg(U_C)
arg_U_R = sp.arg(U_R)

# Przesunięcie fazowe to różnica między argumentami napięcia na C i R
przesuniecie_fazowe = sp.simplify(arg_U_R - arg_U_C)

# Obliczenie wartości przesunięcia fazowego w radianach i stopniach
przesuniecie_fazowe_rad = przesuniecie_fazowe.evalf()
przesuniecie_fazowe_deg = sp.deg(przesuniecie_fazowe).evalf()


print(arg_U_C, arg_U_R, przesuniecie_fazowe_rad, przesuniecie_fazowe_deg)
