# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import random
import string
from math import e
from statistics import mode
import time




Frase='he primavera bro'.capitalize()
epocas=0
numPoblacion=10
generaciones=10000
pMutacion=0.05
resumen=generaciones/50
muestra=generaciones/20



#Genes posibles
asci=string.ascii_uppercase + ' '
letras=[]
for i in range(len(asci)):
    letras.append(asci[i])


# %%

#(e**(1 - 15) - e**(-15))/ (e**( 1 - 15 ) - e**( -15 ) )
random.choice(letras)


# %%

def coincidencias(cadena,original):
    num=0
    for i in range(len(original)):
        if cadena[i]==original[i]:
            num+=1
    return num


def CalculoFitness(original, coincidencias):
    return e**(coincidencias - len(original)) - e**(-len(original))
    
def CalculoProbSelec (fitness,coincide):
    x=fitness / (e**( max(coincide) - len(Frase) ) - e**( -len(Frase) ) )
    return x

def MonteCarloSimple(lista):#Creamos la ruleta por sectores y elegimos un numero al azar max 100
    #print(lista)
    ruleta=[]
    lista=[int(round(x*100)) for x in lista]
    for i in range(len(lista)):
        for j in range(lista[i]):
            ruleta.append(i)
    #print(max(ruleta))
    elegido=random.randint(0,len(ruleta)-1)
    return ruleta[elegido] # Esta funcion devuelve un 1 si solo son 2 valores (1 positivo, 0 negativo)

def Mutacion(padre):#a traves de la frase del padre evaluamos uno a uno si los caracteres cambian
    sustituto=''
    #print("\n\n", padre)
    nueva=[]
    for j in range(len(Frase)):
        if MonteCarloSimple([1-pMutacion,pMutacion]) == 1:
        #if random.random()<pMutacion:
            sustituto=random.choice(letras)
   #         print('Letra al azar:    ',sustituto)
            #nueva=nueva.replace(nueva[j],sustituto)
            nueva.append(sustituto)
        else:
            nueva.append(padre[j])
                        
    #print(nueva)        
    return nueva




# %%
primera=True
poblacion=[]
probabilidadP=[]
fitnes=[]
coincide=[]

print("Sentencia Target: ", Frase, ". Longitud: ", len(Frase))
print("Poblacion total: ", numPoblacion, ". Generaciones máximas: ", generaciones, )
print("Probabilidad de Mutacion: ", pMutacion, "\n\n")


while True:
    
    while primera and epocas == 0:
        poblacion=[]
        coincide=[]
        #Poblacion aleatoria
        for i in range(numPoblacion):
            frase=[]
            
            for j in range(len(Frase)):
                frase.append(random.choice(letras))
            poblacion.append(frase)
            coincide.append(coincidencias(poblacion[i], Frase))
        if max(coincide)!=0:
            primera=False
    #print(poblacion)
    #Calculamos el fitness
    if epocas==0:
        for i in range(numPoblacion):
            resul=CalculoFitness(Frase, coincide[i])#calculamos el fitnes de cada individuo
            fitnes.append(resul)
        

    
        
    #Seleccion del padre
    aleatorio=random.randint(0,numPoblacion-1)
    Padre=empieza=aleatorio
    Flag=False#False = aleatorioa --> final, True --> 0 --> aleatorio
    numero=0
    #print("Padre",Padre, "Probs: ", len(probabilidadP))
    while Flag==False or Padre<=(empieza-1):
        
        #if Padre!=empieza:
        #    
        #    probabilidadP[aleatorio]=CalculoProbSelec(fitnes[aleatorio],coincide)
            #[CalculoProbSelec(x,coincide) for x in fitnes]#Probabilidad de ser padre
            #if max(probabilidadP)==0:
            #    Padre=random.randrange(numPoblacion-1)
            #else:
            #Padre=MonteCarloSimple(1-probabilidadP[aleatorio])#Elegimos al padre
        #coincide[Padre]=coincidencias(poblacion[Padre],Frase)
        #fitnes[Padre]=CalculoFitness(Frase,coincide[Padre])
        if fitnes[Padre]!=0:
            #numero=random.random()

            prb=CalculoProbSelec(fitnes[Padre],coincide)
            #print(prb)
            if   MonteCarloSimple([1-prb,prb]):#si es menor, se replica
            #if MonteCarloSimple([1-probabilidadP[Padre], probabilidadP[Padre]])==1:
                #Sustituimos uno aleatorio
                aleatorio=random.randint(0,numPoblacion-1)
                #Mutamos al cromosoma del padre
                poblacion[aleatorio]=Mutacion(poblacion[Padre])
                #calculamos su fitnes
                coincide[aleatorio]=coincidencias(poblacion[aleatorio],Frase)
                fitnes[aleatorio]=CalculoFitness(Frase,coincide[aleatorio])
                #probabilidadP[aleatorio]=CalculoProbSelec(fitnes[aleatorio],coincide)

        

        if Padre==numPoblacion-1:
            Padre=0
            Flag=True
        Padre+=1

        
    if epocas%resumen == 0 or epocas%muestra==0:
        mejor=''
        aparece=0
        for i in range(numPoblacion):
            if max(coincide)==coincide[i]:
                mejor=poblacion[i]
                aparece+=1
        #individuo de consenso
        consenso='prueba'
        #for i in range(len(Frase)):
        #    posicion=[]
        #    for j in range(numPoblacion):
        #        posicion.append(poblacion[j][i])
        #    consenso.append(mode(posicion))
        
        print("Generacion nº: ", epocas)
        b=''
        for i in range(len(Frase)):
                    b+=mejor[i]
        
        print("Mejor individuo: ", b, ". Coincidencias: ", max(coincide), "NTAR: ", aparece, " %NTAR (",(aparece/numPoblacion)*100, "%)")
        if epocas%muestra==0:
            print('Individuo de consenso: ', consenso, '. Coincidencias de media: ', sum(coincide)/numPoblacion) 
            print("Muestreo de la poblacion: ")
            mostrados=[]
            
            for i in range(int(round(numPoblacion/5))):
                a=''
                for j in range(len(Frase)):
                    a+=poblacion[i][j]
                mostrados.append(a)
            print(mostrados)
        else:
            print('Individuo de consenso: ', consenso, '. Coincidencias de media: ', sum(coincide)/numPoblacion, "\n\n") 

    if max(coincide)==len(Frase):
        print("solucion encontrada: ", poblacion)
        print(coincide)
        break
    if epocas == generaciones:
        break
    epocas+=1
    




# %%
for i in range(int(round(numPoblacion))):
                a=''
                for j in range(len(Frase)):
                    a+=poblacion[i][j]
                print(a)


# %%
sustituto=''
print("\n\n",poblacion[4])
nueva=[]
for j in range(len(Frase)):
    #if MonteCarloSimple([1-pMutacion,pMutacion]) == 1:
    if random.random()<pMutacion:
        sustituto=random.choice(letras)
        print('Letra al azar:    ',sustituto)
        #nueva=nueva.replace(nueva[j],sustituto)
        nueva.append(sustituto)
    else:
        nueva.append(poblacion[4][j])
print(nueva)


# %%
num=0
for i in range(100):
    if random.random()<0.26894142136999516:
        num+=1
print(num)


