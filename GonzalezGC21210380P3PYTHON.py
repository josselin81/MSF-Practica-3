"""
Práctica 2: sistema respiratorio

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Gonzalez Garcia Josselin
Número de control: C21210380
Correo institucional: l21210380@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
PRACTICA 5: SISTEMA CARDIOVASCULAR
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot
import control as ctrl

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math
import matplotlib.pyplot as plt


# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,10,5
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)
u1 = np.sin(2*math.pi*95/60*t)+0.8 #Escalon unitario

# Componentes del circuito RLC y función de transferencia
def cardio (Z,C,R,L):
    num = [L*R,R*Z]
    den = [C*L*R*Z,L*R+L*Z,R*Z]
    sys = ctrl.tf(num,den)
    return sys  

# Función de transferencia: Individuo hipotenso []
Z,C,R,L = 0.020, 0.250, 0.600, 0.005
sysHIPO = cardio(Z,C,R,L)
print('HIPOTENSO:')
print(sysHIPO)

# Función de transferencia: Individuo NOMOTENSO []
Z,C,R,L = 0.033, 1.500, 0.950, 0.010
sysNOMO = cardio(Z,C,R,L)
print('NOMOTENSO:')
print(sysNOMO)

# Función de transferencia: Individuo HIPERTENSO []
Z,C,R,L = 0.050, 2.500, 1.400, 0.020
sysHIPER = cardio(Z,C,R,L)
print('HIPERTENSO:')
print(sysHIPER)

# Respuesta del sistema en lazo abierto y en lazo cerrado
# color azul bajo[0.3,0.8,0.8]
# color azul fuerte [0.1,0.3,0.9]
# color rosa [0.8,0.3,0.6]
# Naranja [0.9,0.7,0.8]

def plotsignals(u1,sysHIPO,sysNOMO,sysHIPER,signal):
    
    fig = plt.figure() #1era figura codigo basado en page 87 Inicializa la figura
    # plt.plot(t,u,'-',color=[],label = '$P_{ao}(t)') #Grafica la entrada
    
    # P A C I E N T E     H I P O     [ F I G U R A ]
    ts,Vs =ctrl.forced_response(sysHIPO,t,u1,x0)
    plt.plot(t,Vs,'--',color = [0.8,0.3,0.6],
             label='$P_p(t): Hipotenso$')
    
    # P A C I E N T E    N O M O     [ F I G U R A ]
    ts, Ve = ctrl.forced_response(sysNOMO,t,u1,x0)
    plt.plot(t,Ve,'-',color = [0.3,0.8,0.8],
             label='$P_p(t): Nomotenso$')
    
    # C O N T R O L    H I P E   [ F I G U R A ]
    ts,pid = ctrl.forced_response(sysHIPER,t,Vs,x0)
    # plt.plot(t,u3,'-', linewidth=3, color = [0.8,0.3,0.6], label = 'Ve(t)' ) 
    plt.plot(t,pid,':', linewidth=2, color = [0.1,0.3,0.9], 
             label= '$P_p(t): Hipertenso$')
    
    plt.grid(True)
    plt.xlim(0,10)
    plt.ylim(-0.5,2)
    plt.xticks(np.arange(0, 11, 1))
    plt.yticks(np.arange(-0.5, 2.5, 0.5))
    plt.xlabel('$t$ [s]')
    plt.ylabel('$V(t)$ [V]')
    plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol=4,
               fontsize = 8, frameon = False)
    plt.show()
    
    ## Almacenamiento de figura 
    fig.set_size_inches(w,h)
    fig.tight_layout()
    namepng = 'python_' + signal + '.png'
    namepdf = 'python_' + signal + '.pdf'
    fig.savefig(namepng, dpi = 600,bbox_inches = 'tight')
    fig.savefig(namepdf, bbox_inches = 'tight')
    
plotsignals(u1,sysHIPO, sysNOMO, sysHIPER, 'Sistema Catdiovascular')



