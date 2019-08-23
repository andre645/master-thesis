import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import numpy as np
import pandas as pd
import time
from sklearn.linear_model import LinearRegression as lr

timestr = time.strftime("%Y%m%d-%H%M%S")


main_win = tkinter.Tk()
main_win.title("Select data")
main_win.geometry("1000x500")
main_win.sourceFile = ''


def get():
    global s 
    s = stepsentry.get()
    return s


def getthat():
    global d
    d=datapointsentry.get()
    return d
    


def chooseFile():
    main_win.sourceFile = filedialog.askopenfilename(parent=main_win, initialdir= "/", title='Select data file')

b_chooseFile = tkinter.Button(main_win, text = "Chose File", width = 10, height = 2, command = chooseFile)
b_chooseFile.grid(row=1, column=0)

def done():
    main_win.destroy()

#Labels
Label (main_win, text='How many Vg sweep steps').grid(row=2, column=0)
Label (main_win, text='How many datapoints per step').grid(row=3, column=0)

#Text entries
stepsentry= Entry(main_win, width=5)
stepsentry.grid(row=2,column=1)

datapointsentry=Entry(main_win,width=5)
datapointsentry.grid(row=3, column=1)

# buttons
button_1=Button(main_win, text='Submit', width= 10, command=get).grid(row=2, column=2)
button_2=Button(main_win, text='Submit', width= 10, command=getthat).grid(row=3, column=2)
done_button=Button(main_win, text='Done', width=10, command=done).grid(row=4, column=0)

main_win.mainloop() 


#---------------------------------------------READ SELECTED DATA-------------------------------------#

df = pd.read_csv(main_win.sourceFile, sep=";")
df.drop(df.tail(1).index,inplace=True)
df['Vads'] = pd.to_numeric(df['Vads'],errors='coerce')
df['Time'] = pd.to_numeric(df['Time'],errors='coerce')

l = len(df)
#d = 10; #datapoints per step
#s= 25; #how many steps
d=int(d)
s=int(s)
pointspercurve = d*s # number of points per curve 
curves=(l/pointspercurve) #number of curves   
#---------------------------------------------------------------------

#---------------------------------CURVE SEPARATOR-------------------------#

a = np.split(df,curves) #separa o dataframe para as diferentes curvas
 # selecionar a curva a imprimir de 0 até curves+1 p.ex a[0]  a[2] ou para o final a[270]

def curva(numerodacurva):
    return a[numerodacurva]    
#--------------------------------------------------------------------------#

#---------------------------------SINGLE CURVE AVERAGING----------------------------#

def averagecurve(x, param):
    vadc = curva(x)['Vads']
    vg = curva(x)['Vg']
    time = curva(x)['Time']
    avgadc = [sum(vadc[i:i+d])/d for i in range(0,len(vadc),d)]
    avgtime = [sum(time[i:i+d])/d for i in range(0,len(time),d)]
    avgVg = [sum(vg[i:i+d])/d for i in range(0,len(vg),d)]

    errorAdc = [np.std(vadc[i:i+d]) for i in range(0,len(vadc),d)]
    errorVg = [np.std(vg[i:i+d]) for i in range(0,len(vg),d)]
    
    dfaveragetime = pd.DataFrame(np.column_stack([avgtime,avgadc, errorAdc, errorVg]),columns=['Average time','Average Vadc','Vadc standard deviation','Vg standard deviation'])
    dfaverageVg = pd.DataFrame(np.column_stack([avgVg,avgadc, errorAdc, errorVg]),columns=['Average Vg','Average Vadc','Vadc standard deviation','Vg standard deviation'])
    #             FAZER ESCOLHA SE QUEREMOS OS DADOS EM FUNÇAO DO TEMPO OU EM FUNÇAO DE VG
    if (param == 'time'):
        return dfaveragetime 
    if (param == 'vg'):
        return dfaverageVg

    


#-------------------------------------ALL CURVE AVERAGING AND Vadc normalization(?)-------------------------#
allcurveAvg=[]
for n in range (0, int (curves) ,1):
    ndf=averagecurve(n,'vg') ##DEFINIR PARA VG OU TIME   
    allcurveAvg.append(ndf)  
    maxval=allcurveAvg[n].loc[:,['Average Vadc']].max()
    normalize=allcurveAvg[n].loc[:,['Average Vadc']]/maxval
    ndf['Normalized Vadc']=normalize
    

#---------------------------------------------------------------------------------------#
def vg(x):
    return allcurveAvg[x].loc[:,['Average Vg']]

def adc(x):
    return allcurveAvg[x].loc[:,['Average Vadc']]

def stdErrorVadc(x):
    return allcurveAvg[x].loc[:,['Vadc standard deviation']]

def stdErrorVg(x):
    return allcurveAvg[x].loc[:,['Vg standard deviation']]

def normalized(x):
    return allcurveAvg[x].loc[:,['Normalized Vadc']]
#------------------------------------------------------------------------------------#

#-------------------------------------PLOT EACH CURVE---------------------------------#
  
def grafico(*nums):
    def func(*nums):
        return nums
    
    a=func(*nums)
    
    stringx=[]
    stringy=[]
    stringe=[]
    for x in a:
        txt=vg(x)
        txt1=adc(x)
        txt2=stdErrorVadc(x)
        stringx.append(txt)
        stringy.append(txt1)
        stringe.append(txt2)
        valueX=np.concatenate(stringx)
        valueY=np.concatenate(stringy)
        valueE=np.concatenate(stringe)

       
    ty=np.hstack((valueX,valueY,valueE))
    
   
   

    fig1, ax = plt.subplots()
    ax.errorbar(ty[:,0],ty[:,1],ty[:,2],linestyle='None', marker='.', ecolor='red',elinewidth=1, capsize=3)
    ax.set(xlabel='Vg (V)', ylabel='Vadc (V)', title='Response')
    ax.grid()
    
    
    plt.show()



#----------------------------------ALL CURVES PLOT--------------------------#
def plotAllCurves():
    o=np.concatenate(allcurveAvg)
    fig2, ax = plt.subplots()
    ax.errorbar(o[:,0], o[:,1], o[:,2], linestyle='None', marker='.', ecolor='red',elinewidth=1, capsize=3)
    ax.set(xlabel='Vg (V)', ylabel='Vadc (V)', title='Response')
    ax.grid()
    plt.show()
#------------------------------------------------------------------------------------#      


def plotAllnormCurves():
    o=np.concatenate(allcurveAvg)
    fig2, ax = plt.subplots()
    ax.scatter(o[:,0], o[:,4], s=1,cmap='winter')
    ax.set(xlabel='Vg (V)', ylabel='Normalized values', title='Response')
    ax.grid()
    plt.show()



#-------------------------------------PLOT EACH NORMALIZED CURVE---------------------------------#
  
def graficoNORMAL(*nums):
    def func(*nums):
        return nums
    
    a=func(*nums)
    
    stringx=[]
    stringy=[]
    for x in a:
        txt=vg(x)
        txt1=normalized(x)
        stringx.append(txt)
        stringy.append(txt1)
        valueX=np.concatenate(stringx)
        valueY=np.concatenate(stringy)

       
     
    fig3, ax = plt.subplots()
    ax.scatter(valueX,valueY, s=2)
    ax.set(xlabel='Vg (V)', ylabel='Normalized Value', title='Response')
    ax.grid()
    
    timef = curva(x)['Time']    
    avgtimef = [sum(timef[i:i+d])/d for i in range(0,len(timef),d)]
    label = str (avgtimef[-1])+' ms'
    plt.text(2.5,3,label)
    plt.show()
#---------------------------------------------------------------------------------------------------#


#------------------------------------------------------------PLOT CONSTANT Vg------------------------------------# 
def VgCTE(*nums):
    def func(*nums):
        return nums
    
    a=func(*nums)
    
    vgctexvalue=[]
    vgcteyvalue=[]
    vgcteevalue=[]
    for curveregion in a:
        
        for n in range (0, int (curves), 1):
            xvalue = int(n)
            yvalue = float(adc(n).iloc[curveregion])
            evalue = float(stdErrorVadc(n).iloc[curveregion])
            vgctexvalue.append(xvalue)
            vgcteyvalue.append(yvalue)
            vgcteevalue.append(evalue)
            
           
         
    fig3, ax = plt.subplots()
    ax.errorbar(vgctexvalue,vgcteyvalue,vgcteevalue, linestyle='None', marker='.', ecolor='red',elinewidth=1, capsize=3)
    ax.set(xlabel='Cycle', ylabel='Vadc(V)', title='Response')
    ax.grid()
    
    plt.show()

#---------------------------------------------------PLOT CONSTANT VADC------------------------------------#
def VadcCTE(*nums):
    def func(*nums):
        return nums
    
    a=func(*nums)
    
    vadctexvalue=[]
    vadcteyvalue=[]
    vadcteevalue=[]
    for curveregion in a:
        
        for n in range (0, int (curves), 1):
            xvalue = int(n)
            yvalue = float(vg(n).iloc[curveregion])
            evalue = float(stdErrorVg(n).iloc[curveregion])
            vadctexvalue.append(xvalue)
            vadcteyvalue.append(yvalue)
            vadcteevalue.append(evalue)
            
                 

    fig3, ax = plt.subplots()
    ax.errorbar(vadctexvalue,vadcteyvalue, vadcteevalue, linestyle='None', marker='.', ecolor='red',elinewidth=1, capsize=3)
    ax.set(xlabel='Cycle', ylabel='Vg(V)', title='Response')
    ax.grid()
    
    plt.show()


#-----------------------------PLOT ALL RELEVANT DATA----------------------#
def easy():
    #plotAllCurves()
    grafico(0,10,255)
    vgCte(15)
    vadCte(15)
    graficoNORMAL(0,284)
    plt.show()

#----------------------- Linear Regression ------------------------------------------------#
def linreg(curva,min,max):
    x=vg(curva).loc[min:max,:]
    y=adc(curva).loc[min:max,:]
    model=lr().fit(x,y)

    r_sq = model.score(x, y)
    intercept= float (model.intercept_)
    slope= float(model.coef_)
    xintercept=float (-intercept/slope)

    xmodel=np.linspace(xintercept+0.1,vg(curva).loc[max,:])
    ymodel=(slope*xmodel)+intercept
    
    label = str("Cycle "+str(curva)+"\n"+"m="+str(slope)+"\n"+"b="+str(intercept)+"\n"+"r2="+str(r_sq)+"\n"+"x axis intercept = "+str(xintercept))
    plt.plot (xmodel,ymodel, '-r', label = label )
    plt.scatter (vg(curva),adc(curva))
    plt.legend(loc='upper left')
    plt.xlabel('Vg(V)')
    plt.ylabel('Vadc(V)')
    plt.show()
    
#----------------------------------Save Averaged curves---------------------------------#
def saveAvgCurves():
    
    directory=tkinter.filedialog.askdirectory()
    filestr=("/"+timestr+"AVGcurves.csv")
    savestr=str(directory+filestr)
    dfallcurveAvg=pd.DataFrame(allcurveAvg)
    print(dfallcurveAvg)
    dfallcurveAvg.to_csv(savestr)

#---------------------------------Plot window---------------------------#

plot_win = tkinter.Tk()
plot_win.title("Process the data for me")
plot_win.geometry("1000x500")

def get_curveregion():
    global curveregion
    curveregion = regionentry.get()
    return 


def get_curves():
    global response
    response = curvesentry.get()
    return 

def graph():
   global response
   response=str(response)
   response=response.split(',')
   response=list(map(int,response))
   response=tuple(response)
   grafico(*response)
   return

def VadcCte():
    global curveregion
    curveregion=str(curveregion)
    curveregion=curveregion.split(',')
    curveregion=list(map(int,curveregion))
    curveregion=tuple(curveregion)
    VadcCTE(*curveregion)
    return

def VgCte():
    global curveregion
    curveregion=str(curveregion)
    curveregion=curveregion.split(',')
    curveregion=list(map(int,curveregion))
    curveregion=tuple(curveregion)
    VgCTE(*curveregion)
    return

def plotnormalizedCurves():
   global response
   response=str(response)
   response=response.split(',')
   response=list(map(int,response))
   response=tuple(response)
   graficoNORMAL(*response)
   return

#------------------Linear Reg functions-----------------#
def get_curva():
    global linregcurva
    linregcurva = linregCurveEntry.get()
    linregcurva=int(linregcurva)
    return 

def get_From():
    global linregfrom
    linregfrom = linregFromEntry.get()
    linregfrom=int(linregfrom)
    return 

def get_To():
    global linregto
    linregto = linregToEntry.get()
    linregto=int(linregto)
    return 

def linregplot():
    linreg(linregcurva,linregfrom,linregto)
    return
#-------------------------------------------------------------#
#-----------------Shift calc-----------------------#

def shiftcalc(curva1,curva2):
    vadc1=allcurveAvg[curva1].loc[:,'Normalized Vadc']
    vadc2=allcurveAvg[curva2].loc[:,'Normalized Vadc']
    shift = vadc2-vadc1
    shiftArray=np.column_stack((vadc1,vadc2,shift))
    curva1Str=str('Curve '+str(curva1))
    curva2Str=str('Curve '+str(curva2))
    shiftDF=pd.DataFrame(data=shiftArray, columns=[curva1Str,curva2Str,'Shift'])
    return print(shiftDF)
#----------------------------------------------------#

#Labels
Label (plot_win, text='Which curves you want to plot?').grid(row=2, column=0)
Label (plot_win, text='What is the curve region/regions you want to plot for cte. Vg?').grid(row=3, column=0)
Label (plot_win, text='Total number of curves =').grid(row=1, column=0)
Label (plot_win, text=curves).grid(row=1,column=1)

Label (plot_win, text= "Linear regression").grid(row=8, column=1)
Label (plot_win, text= "Curve number:").grid(row=9, column=0)
Label (plot_win, text= "From:").grid(row=10, column=0)
Label (plot_win, text= "To:").grid(row=11, column=0)
#Text entries
curvesentry= Entry(plot_win, width=50)
curvesentry.grid(row=2,column=1)

regionentry=Entry(plot_win,width=50)
regionentry.grid(row=3, column=1)

linregCurveEntry=Entry(plot_win, width=20)
linregCurveEntry.grid(row=9,column=1)

linregFromEntry=Entry(plot_win, width=20)
linregFromEntry.grid(row=10,column=1)

linregToEntry=Entry(plot_win, width=20)
linregToEntry.grid(row=11,column=1)

# buttons
button_PlotAll=Button(plot_win, text='Plot all', command=plotAllCurves).grid(row=4, column=0)
button_PlotAllnormalizedCurves=Button(plot_win, text='Plot all normalized curves', command=plotAllnormCurves).grid(row=5,column=0)
button_grafico=Button(plot_win, text='Plot curves', command=graph).grid(row=6,column=0)
button_Plotnormalized=Button(plot_win, text='Plot normalized curves', command=plotnormalizedCurves).grid(row=7, column=0)


button_vadCte=Button(plot_win, text='Plot curves for constant Vadc', command=VadcCte).grid(row=4, column=1)
button_vgCte=Button(plot_win, text='Plot curves for constant Vg', command=VgCte).grid(row=5, column=1)

buttonget_curves=Button(plot_win, text="Submit", command=get_curves).grid(row=2,column=2)
buttonget_curveregion=Button(plot_win, text="Submit", command=get_curveregion).grid(row=3,column=2)
button_SaveAvgCurves=Button(plot_win, text='Save averaged curves data', command=saveAvgCurves).grid(row=4,column=2)


buttonget_curva=Button(plot_win, text="Submit", command=get_curva).grid(row=9,column=2)
buttonget_from=Button(plot_win, text="Submit", command=get_From).grid(row=10,column=2)
buttonget_to=Button(plot_win, text="Submit", command=get_To).grid(row=11,column=2)
buttonget_linregPlot=Button(plot_win, text="Plot", command=linregplot).grid(row=12,column=1)


plot_win.mainloop()


  
