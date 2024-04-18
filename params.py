import math

L_wire = 157E-3



L_rod = 305E-3
D_rod = 10E-3

l_M = 131E-3
w_M =  19E-3
h_M =  25E-3
m_M = 514.15E-3

d = 281E-3 / 2



p_rod = 500
m_rod = L_rod * math.pi * (D_rod/2)**2#m = pV = p*L*pi*R^2



I_ROD = 1/2 * m_rod * L_rod**2
I_M = m_M*h_M*(l_M**2 + w_M**2)/12 + m_M*(d**2)
I = I_ROD + I_M