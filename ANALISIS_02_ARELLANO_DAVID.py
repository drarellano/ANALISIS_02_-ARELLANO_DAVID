# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 16:33:03 2021

@author: David
"""

import csv


    
"""Analisis de Exportaciones e Importaciones"""    
lst_datos=[] 
   
with open ("synergy_logistics_database.csv","r") as archivo:
    datos=csv.reader(archivo)
    for dato in datos:
        lst_datos.append(dato)
    

def imp_exp(tipo):
    lst_origen=[]
    lst_destino=[]
    lst_valor=[]
    lst_tipo=[]
    lst_origen_destino_valor=[]
    #Se obtinenen las rutas y su valor de acuerdo a si es exportacion
    #o importacion.
    for dato in lst_datos:
        if dato[1]==tipo:
            lst_origen.append(dato[2])
            lst_destino.append(dato[3])
            lst_valor.append(int(dato[9]))
            lst_tipo.append([dato[2],dato[3],dato[9]])
    #se analizan las rutas para no tener repetidas
    lst_ruta=[]
    for dato in lst_tipo:
        if [dato[0],dato[1]] not in lst_ruta:
            lst_ruta.append([dato[0],dato[1]])
    lst_ruta_cont_valor=[]
    #se analizan las operaciones y el valor total de la ruta.
    for ruta in lst_ruta:
        contador=0
        suma=0
        origen=""
        destino=""
        for valor in lst_tipo:
            origen=ruta[0]
            destino=ruta[1]
            if [valor[0],valor[1]] == [origen,destino]:
                contador+=1
                suma+=int(valor[2])
        lst_ruta_cont_valor.append([origen,destino,contador,suma]) 
    suma_total=0
    cont_total=0
    for valor in lst_ruta_cont_valor:
        suma_total+=valor[3]
        cont_total+=valor[2]
    #se calculan el procentaje de cada ruta en base a su valor total  
    lst_ruta_cont_valor_promedio=[]
    promedio=0.0
    promedio_total=0.0
    for rutas in lst_ruta_cont_valor:
        promedio=round(100*rutas[3]/suma_total,2)
        promedio_total+=promedio;
        lst_ruta_cont_valor_promedio.append([rutas[0],rutas[1],rutas[2],rutas[3],promedio])
    lst_ruta_cont_valor_promedio.sort(reverse=True, key=lambda ruta:ruta[3])
    return [cont_total,suma_total,promedio_total,lst_ruta_cont_valor_promedio]

#Se le da formato y se imprime la informacion de las rutas en una tabla,
#mostrando solo las 10 primeras        
def imprimir_datos(impresion,tipo):
    print(tipo+"\n")
    total_imp_exp=[]
    total_valor=[]
    total_prom=[]
    print("{0:21} {1:28} {2:11} {3:8}    {4:12}".format("ORIGEN","DESTINO","TOTALES","VALOR TOTAL","PROMEDIO\n"))
    i=0
    for imprimir in impresion:
        print("{0:21} {1:24} {2:10} {3:15} {4:12}".format(
            imprimir[0],
            imprimir[1],
            imprimir[2],
            imprimir[3],
            imprimir[4]
            ))
        total_imp_exp.append(imprimir[2])
        total_valor.append(imprimir[3])
        total_prom.append(imprimir[4])
        i+=1
        if i>=10:
            break
    print("\n{0:21} {1:24} {2:10} {3:15} {4:12}".format("","",sum(total_imp_exp),sum(total_valor),round(sum(total_prom),2)))
    input("pulsa enter")
    borrarPantalla()

[cont_total,sum_total,prom_total,importaciones]=imp_exp("Imports")
print("\n A continuacion se muestran las 10 rutas mas importantes de importaciones")
print("ordenados de acuerdo a su valor total")
imprimir_datos(importaciones,"Importaciones")
[cont_total,sum_total,prom_total,exportaciones]=imp_exp("Exports") 
print("\n A continuacion se muestran las 10 rutas mas importantes de exportaciones")
print("ordenados de acuerdo a su valor total")
imprimir_datos(exportaciones,"Exportaciones")      



"""Analisis de transportes"""
#Se analizan los medios de transporte que se utilizan
def transporte():
    lst_transportes=[]
    lst_transportes.append(lst_datos[0][7])
    for transporte in lst_datos:
        if transporte[7] not in lst_transportes:
            lst_transportes.append(transporte[7])
    lst_transportes.pop(0)  
    return lst_transportes

#Se analizan las operaciones y el valor total de cada medio de transporte
def datos_transportes(tipo):
    cont_total=0
    suma_total=0
    cont_im=0
    cont_ex=0
    suma_t_ex=0
    suma_t_im=0
    for dato in lst_datos:
        if dato[7]==tipo:
            cont_total+=1
            suma_total+=int(dato[9])
            if dato[1]=="Imports":
                cont_im+=1
                suma_t_im+=int(dato[9])
            else:
                cont_ex+=1
                suma_t_ex+=int(dato[9])
    resultado=[tipo,cont_ex,suma_t_ex,cont_im,suma_t_im,cont_total,suma_total]
    return resultado

#se crea una lista con la informacion de cada medio de transporte
def enviar_transporte(medio):
    datos_transporte=[]
    for transporte in medio:
        datos_transporte.append(datos_transportes(transporte))
    return datos_transporte    

#Se muestra en pantalla la información de cada medio de trasnporte como una 
#tabla.
def imprimir_datos_transporte(transportes):
    os.system("cls")
    print("\n{0:12} {1:9} {2:13} {3:9} {4:13} {5:8}   {6:10}       {7:5}".format(
            "Transporte",
            "Exports",
            "Valor Exp",
            "Imports",
            "Valor Imp",
            "Totales",
            "Valor Total",
            "Promedio"
            ))
    exp_tot=0
    val_exp_tot=0
    im_tot=0
    val_imp_tot=0
    oper_tot=0
    tot_val_tot=0
    tot_prom=0.0
    prom=0.0
    imprimir=[]
    for transporte in transportes:
        exp_tot+=transporte[1]
        val_exp_tot+=transporte[2]
        im_tot+=transporte[3]
        val_imp_tot+=transporte[4]
        oper_tot+=transporte[5]
        tot_val_tot+=transporte[6]
    for transporte in transportes:  
        prom=round(100*transporte[6]/tot_val_tot,2)
        imprimir.append([
            transporte[0],
            transporte[1],
            transporte[2],
            transporte[3],
            transporte[4],
            transporte[5],
            transporte[6],
            prom
            ])
        tot_prom+=prom
    for transporte in imprimir:
        print("   {0:9s}{1:6d}   {2:10d}   {3:8d}   {4:11d} {5:10d}   {6:13d} {7:10}".format(
            transporte[0],
            int(transporte[1]),
            int(transporte[2]),
            int(transporte[3]),
            int(transporte[4]),
            int(transporte[5]),
            int(transporte[6]),
            transporte[7],
            ))
        
    print("\n   {0:9s}{1:6d}  {2:10d}   {3:8d}   {4:11d} {5:10d}   {6:13d} {7:9}".format(
            "Totales",
            exp_tot,
            val_exp_tot,
            im_tot,
            val_imp_tot,
            oper_tot,
            tot_val_tot,
            round(tot_prom,2)-0.01
            ))
        
    input("pulsa enter")
    

tipo_transporte=transporte();
lst_transprte_datos=enviar_transporte(tipo_transporte)
lst_transprte_datos.sort(reverse=True, key=lambda x:x[6])
print("\nA continuación se muestra la informacion referente a los medios de transporte")
print("ordenados de acuerdo a su valor total")
imprimir_datos_transporte(lst_transprte_datos)

"""Analisis del 80% de las exportaciones e imprtaciones"""

def analisis_paises(lista):
    #se analizan los paises distintos con los que se realizan operaciones
    lst_pais=[]
    lst_pais_cont_val=[]
    for pais in lista:
        if not pais[0] in lst_pais:
            lst_pais.append(pais[0])
    #se aanaliza la cantidad total de operaciones y el valor total por pais        
    cont_total=0
    val_total=0
    for pais in lst_pais:
        cont=0
        valor=0
        for pais1 in lista:
            if pais1[0]==pais:
                cont+=pais1[2]
                valor+=pais1[3]
        cont_total+=cont;
        val_total+=valor
        lst_pais_cont_val.append([pais,cont,valor])
    lst_pais_cont_promCont_val_promVal=[]
    #se calculan porcentajes por pais
    con=0.0
    val=0.0
    prom_oper=0.0
    prom_val=0.0
    for pais in lst_pais_cont_val:
        con=float(pais[1])*1.0
        val=float(pais[2])*1.0
        prom_oper=round(100*con/cont_total,2)
        prom_val=round(100*val/val_total,2)
        lst_pais_cont_promCont_val_promVal.append([
            pais[0],
            pais[1],
            prom_oper,
            pais[2],
            prom_val
            ])
        
    return [cont_total,val_total,lst_pais_cont_promCont_val_promVal]
def impresion_paises(paises,oper,valor,tipo,i):
    #se imprime la informacion de los paises, tanto para importaciones como
    #exportaciones
    print("\n"+tipo)
    paises.sort(reverse=True, key=lambda x:x[i])
    print("{0:20}   {1:12}    {2:12}     {3:13}{4:7}".format("PAIS","OPERACIONES","PROM_OPER","VALOR","PROM_VALOR"))
    promedio=0.0
    for pais in paises:
        print("{0:20}{1:12}{2:12}{3:20}{4:10}".format(pais[0],pais[1],pais[2],pais[3],pais[4]))
        promedio+=pais[i+1]
        #Si el porcentaje acumulado de los paises mostrados es mayor o igual
        #al 80% se detiene la impresion
        if promedio>=80:
           break 
    input("pulsa enter")
   
    
[oper,valor,paises_datos]=analisis_paises(importaciones)
print("\nA continuación se muestra la informacion referente a los paises con el")
print("80% de las importaciones, ordenados de acuerdo a su valor total")
impresion_paises(paises_datos,oper,valor,"Importaciones",3)

[oper,valor,paises_datos]=analisis_paises(exportaciones)
print("\nA continuación se muestra la informacion referente a los paises con el")
print("80% de las exportaciones, ordenados de acuerdo a su valor total")
impresion_paises(paises_datos,oper,valor,"Exportaciones",3)



