"""
Created on Sat Aug 29 16:32:11 2020

@author: Jinyin Zha
"""
import matplotlib.pyplot as plt
from utils import lr1d
from utils import cubic1d

#Hello
print("Welcome to use ReynoldsMaster! This Program is developed by Jinyin Zha.\nIt helps you to do a Reynold correction.")

while True:
    
    #1, Get Input
    str_data=input("Please input the temperatures (Celsius). Split temperatures by spaces.\nAn easier way to do it is firstly to tap temperatures into Excel (in a line) and then copy them here.\nInput 'exit' to exit.\n")
    if str_data=="exit":
        print("Bye!")
        break
    dt=input("Please input the time between two temperature.\n(Unit : s  Press Enter for 30s)\n")
    bgnum=input("Please input the number of points before burning.\n")
    
    
    #2, Numerate inputs

    
    str_data_li=str_data.split()
    data=[]
    try:
        for i in str_data_li:
            data.append(float(i))
    except:
        print("Temperature should be a number!\n'"+i+"' is not a number!\nPlease try again!")
        input("Press enter continue.")
        continue
    data_num=len(data)
    
    try:
        if dt=="":
            dt=30
        else:
            dt=float(dt)
    except:
        print("Interval time should be a number!\n'"+dt+"' is not a number!\nPlease try again!")
        input("Press enter continue.")
        continue
    time=[]
    for i in range(data_num):
        time.append(i*dt)    
    
    try:
        bgnum=int(bgnum)
    except:
        print("Number of points before burning should be an intergal!\n'"+i+"' is not an intergal!\nPlease try again!")
        input("Press enter continue.")
        continue
    if bgnum<=0:
        print("Number of points before burning should be Positive!")
        input("Press enter continue.")
        continue
    elif bgnum>data_num-1:
        print("Number of points before burning is too big!\nIt should not be bigger than the length og data - 1!\nPlease check your data!")
        input("Press enter continue.")
        continue
    if bgnum<5:
        print("Warning! Too few data before burning! (<5)")
    
    
    #3, Data Grouping
    begin_data=data[0:bgnum]
    begin_time=time[0:bgnum]
    
    i=data_num-2
    end=[data[-1]]
    end_num=1
    while i > bgnum:
        if data[i] < end[0]:
            break
        else:
            end=[data[i]]+end
            end_num+=1
            i-=1
    if end_num==1:
        print("You have no records for the temperature decreasing after burning!\nPlease check your data!")
        input("Press enter continue.")
        continue
    elif end_num < 5:
        print("Warning! Too few data for the temperature decreasing after burning! (<5)")
    end_point=data_num-end_num 
    end_data=data[end_point:data_num]
    end_time=time[end_point:data_num]
    
    # def interp1d_cubic(x, y):
    #     h = []
    #     for i in range(1, len(x)):
    #         h.append(x[i] - x[i-1])
    #     a = y

    
    #4, Interpolation for all the data
    ft=[]
    i=0
    while i<=(data_num-1)*dt:
        ft.append(i)
        i+=0.001
    # ipp=ip.interp1d(time,data,kind="cubic")
    # fi=ipp(ft)
    fi = cubic1d(time,data, ft)
    
    #5, Liner Regression of begin and end       
    # kb,bb,rb,pb,eb=st.linregress(begin_time,begin_data)
    # ke,be,re,pe,ee=st.linregress(end_time,end_data)
    kb, bb = lr1d(begin_time,begin_data)
    ke, be = lr1d(end_time,end_data)
    

    #6, Get Tm and tm
    T_bg=data[bgnum-1]
    T_ed=data[end_point]
    Tm=(T_bg+T_ed)/2
    
    tm=0
    for i in range((bgnum+1)*30000,end_point*30000):
        if fi[i]>Tm:
            if (fi[i]-Tm) < (Tm-fi[i-1]):
                tm=ft[i]
            else:
                tm=ft[i-1]
            break
        
    
    #7, Fixing temperature by line crossing
    T_bgf=round(kb*tm+bb,3)
    T_edf=round(ke*tm+be,3)
    delta_T=round(T_edf-T_bgf,3)
    
    bgline_time=[]
    bgline_data=[]
    i=0
    while i <=tm:
        bgline_time.append(i)
        bgline_data.append(kb*i+bb)
        i+=0.1
        
    edline_time=[]
    edline_data=[]
    i=tm
    while i <= (data_num-1)*dt:
        edline_time.append(i)
        edline_data.append(ke*i+be)
        i+=0.1
        
    tm_line_x=[]
    tm_line_y=[]
    i=min(data)-0.1
    edi=max(data)+0.2
    while i<=edi:
        tm_line_x.append(tm)
        tm_line_y.append(i)
        i+=0.1
        
    bx=[]
    by=[]
    i=0
    edi=end_point*dt
    while i<=edi:
        bx.append(i)
        by.append(T_ed)
        i+=0.1
        
    sx=[]
    sy=[]
    i=0
    edi=tm
    while i<=edi:
        sx.append(i)
        sy.append(T_bg)
        i+=0.1
        
    mx=[]
    my=[]
    i=0
    edi=tm
    while i<=edi:
        mx.append(i)
        my.append(Tm)
        i+=0.1
        
    
    #8,Draw pictures and output
    name=input("\n\nThe image will be saved in the running dir. Please give it a name.\n")
        
    plt.figure()
    plt.xlim(0,time[-1]+100)
    plt.plot(ft,fi,lw=5,color="black")
    plt.plot(time,data,"o",markersize=7,label="Experimental Data")
    plt.plot(tm_line_x,tm_line_y,lw=4,color="black")
    plt.plot(bx,by,"--",lw=2,color="black")
    plt.plot(sx,sy,"--",lw=2,color="black")
    plt.plot(mx,my,"--",lw=2,color="black")
    plt.plot(bgline_time,bgline_data,"--",lw=2,color="red")
    plt.plot(edline_time,edline_data,"--",lw=2,color="red")
    plt.plot([tm,tm],[T_bg,T_ed],"s",label="Raw Temperatures")
    plt.plot([tm,tm],[T_bgf,T_edf],"s",label="Fixed Temperatures")
    plt.legend(frameon=False,fontsize=13)
    plt.xlabel("Time (s)",fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("Temperature (Celsius)",fontsize=18)
    plt.yticks(fontsize=15)   
    plt.savefig(name+".png",dpi=500,bbox_inches="tight")
    #plt.show()#Can not run in idle!
    
    print("  Raw Data: Start Temperature: "+str(T_bg)+"; End Temperature: "+str(T_ed))
    print("Fixed Data: Start Temperature: "+str(T_bgf)+"; End Temperature: "+str(T_edf))
    print("            Temperature Difference: "+str(delta_T)+" (Unit: Celsius)")
    print("Image has been saved as "+name+".png!")
    print("Done! Press enter to continue.")
    