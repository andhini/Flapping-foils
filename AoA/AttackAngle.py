# This script traces angle of attack (AoA) of 3D rolling & twisting foils
# for both time- and max- AOA evolution.
# Each cross section of rolling foil experiences a heaving (h(t)) motion,
# and so twisting to pitching (theta(t)).

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from math import sqrt,pi,cos,sin,asin,atan,degrees
import matplotlib.pylab as pl

def main():
    head_dir = "C:\\Users\\andhini\\Documents\\research_data\\angle of attack _twistroll\\"
    filepdf=PdfPages(head_dir+'/AoA'+'.pdf')
    plt.tight_layout()
    plt.rcParams.update({'font.size': 25})

    dt=np.linspace(0., 1.0, num=100)

    ## input data: Strouhal & pitching amplitude ##
    St=0.3
    ASin=0.403385 #pamp
    Amp=[ad*St/2. for ad in np.linspace(0., 1.0, num=11)]
    Freq=1
    zs=np.linspace(0., 1.0, num=len(Amp))
    Pamp=[ad*asin(ASin) for ad in np.linspace(0., 1.0, num=11)]
    print ('Pitching Amp=',[ad*math.asin(ASin)/math.pi*180. for ad in np.linspace(0., 1.0, num=10)])
    Ymin=-.5;Ymax=.5

    colors = pl.cm.Blues(np.linspace(.4,1.,len(Amp)))
    max_alpha_C=[];max_alpha_H=[]
    d_max_alpha_C=[];d_max_alpha_H=[];mid_alpha_C=[]

    ## time tracing alpha max for 1 cycle ##
    fig,[ax1,ax2]=plt.subplots(2,1,figsize=(11,16))
    for i in range(len(Amp)):
        ### Coupled twist-roll motion ###

        H=[];dH_dt=[];theta_t=[];alpha_t=[];d_alpha_dt=[]
        for j in range(len(dt)):
            twistroll=Coupled(Amp[i],Freq,dt[j],Pamp[i])
            dH_dt.append(twistroll[1])
            theta_t.append(twistroll[2])
            alpha_t.append(twistroll[3])
            d_alpha_dt.append(twistroll[4])
        max_alpha_C.append(max(max(alpha_t),abs(min(alpha_t))))
        max_alpha=max(max(d_alpha_dt),abs(min(d_alpha_dt)));
        mid_alpha=alpha_t[int(len(dt)/2)]
        d_max_alpha_C.append(max_alpha)
        mid_alpha_C.append(mid_alpha) #alpha at 0.5t/T (to calculate dip)


        ### Pure roll motion ###
        alpha_t_H=[];d_alpha_H_dt=[]
        for k in range(len(dt)):
            roll=Heave(Amp[i],Freq,dt[k])
            alpha_t_H.append(roll[2])
            d_alpha_H_dt.append(roll[3])
        max_alpha_H.append(max(max(alpha_t_H),abs(min(alpha_t_H))))
        d_max_alpha_H.append(max(max(d_alpha_H_dt),abs(min(d_alpha_H_dt))))

        ## Plot twistroll alpha(t) evolution ##
        Plot_graph(ax1,filepdf,dt,alpha_t,'','','',\
            color=colors[i],linestyle='--')
        ## Plot roll d/dt_alpha(t) evolution ##
        Plot_graph(ax2,filepdf,dt,d_alpha_dt,'','','',\
            color=colors[i],linestyle='--')

        ## Plot roll alpha(t) evolution ##
        Plot_graph(ax1,filepdf,dt,alpha_t_H,'','','',\
            label=str('%.2f'% zs[i])+'z/S',color=colors[i],linestyle='-')
        ## Plot twist-roll d/dt alpha(t) evolution ##
        Plot_graph(ax2,filepdf,dt,d_alpha_H_dt,'','','',\
            label=str('%.2f'% zs[i])+'z/S',color=colors[i],linestyle='-')

    ## Roll kinematic (tip position in y direction or tip lateral movement) ##
    H_t=[Ymax*sin(2.*pi*Freq*dt[m]) for m in range(len(dt))]
    Plot_graph(ax1,filepdf,dt,H_t,r'$\alpha$(t) in $\pi$ rad','',r'$\alpha$(t)',Min_ylim=Ymin,\
        Max_ylim=Ymax,label='Roll Kinematic',color='k',width=2.5)

    ## Only for legend ##
    ax2.set_ylim([-7.,7.])
    Plot_graph(ax2,filepdf,[],[],'','','',color='k',linestyle='-',label='Roll')
    Plot_graph(ax2,filepdf,[],[],r'$\dot{\alpha}$(t) in $\pi$ rad/t','t/T',\
        r'$\dot{\alpha}$(t)',color='k',linestyle='--',label='Twist-Roll')


    plt.legend(fontsize=12)
    plt.text(.75, 13., r'$\theta_{twist}$='+str(round(Pamp[-1]/math.pi*180,1))+r'$^\circ$', fontsize=25)
    plt.text(.75, 12.4, 'St='+str(St), fontsize=25)
    plt.text(.75, 11.8, 'St0.3 @z/s='+str("{:.2f}".format(0.3/St)), fontsize=20)
    plt.savefig(head_dir+'AoA_'+str("{:.2f}".format(St))+'.png', dpi=100)
        filepdf.savefig()

    ## alpha max graph ##
    plt.clf()
    fig,ax=plt.subplots(figsize=(10,7))
    Plot_graph(ax,filepdf,zs,max_alpha_H,'','','', Min_ylim=0,Max_ylim=Ymax,
        linestyle='-',label='Roll',color='k')
    Plot_graph(ax,filepdf,zs,max_alpha_C,'','','',Min_ylim=0,Max_ylim=Ymax,\
        linestyle='--',label='Twist-Roll',color='k',axlabelcoord=1)
    plt.legend(loc=2)

    ## derivative of alpha max graph ##
    Plot_graph(ax,filepdf,zs,d_max_alpha_C,'','','',linestyle='--',ax2=1,\
        Min_ylim2=0,Max_ylim2=7.5,Yaxes_Name2=r'$\dot{\alpha}_{max}$',\
        label=r'$\dot{\alpha}_{max}$ Twist-Roll',color='blue',ax2labelcoord=1)

    Plot_graph(ax,filepdf,zs,d_max_alpha_H,r'$\alpha_{max}$ ($\pi$ rad) & $\dot{\alpha}_{max}$ ($\pi$ rad/t)',\
        'z/S',r'$\alpha_{max}$', ax2=1,Min_ylim2=0,Max_ylim2=7.5,linestyle='-',\
        Yaxes_Name2=r'$\dot{\alpha}_{max}$',label=r'$\dot{\alpha}_{max}$ Roll',\
        color='blue',ax2labelcoord=1)

    ## Printing z/S location, alpha max, quarter alpha, and percentage of dip at
    ## quarter cycle compared to max alpha ##
    print ('z/s=',zs)
    print ('max_alpha_C=',[max_alpha_C[maxa]*180 for maxa in range(len(max_alpha_C))])
    print ('mid_alpha_C=',[mid_alpha_C[mida]*180 for mida in range(len(mid_alpha_C))])
    dip_alpha_C=(max_alpha_C[-1]-mid_alpha_C[-1])/max_alpha_C[-1];
    print ('dip_alpha_C @ tip=',dip_alpha_C)


    plt.text(.6, 3.7, r'$\theta_{twist}$='+str(round(Pamp[-1]/math.pi*180,1))+r'$^\circ$', fontsize=25)
    plt.text(.6, 3.4, 'St='+str(St), fontsize=25)
    plt.savefig(head_dir+'AoAmax_'+str("{:.2f}".format(St))+'.png', dpi=100)
    filepdf.savefig()

def Plot_graph(ax,filepdf,X,Y,title,Xaxes_Name,Yaxes_Name,curve_type='b-',\
    linestyle='-',width=1.5,Min_xlim=None,Max_xlim=None,Min_ylim=None,Max_ylim=None,\
    label=None,color=None,ax2=None,Yaxes_Name2=None,Min_ylim2=None,\
    Max_ylim2=None,axlabelcoord=None,ax2labelcoord=None):
    if (ax2==None):
        ax.plot(X,Y,curve_type,linestyle=linestyle,label=label,color=color,linewidth=width)
        ax.set_title(title)
        ax.set_xlabel(Xaxes_Name)
        ax.set_ylabel(Yaxes_Name,rotation=0)
        ax.set_xlim([Min_xlim,Max_xlim])
        if not (axlabelcoord==None):ax.yaxis.set_label_coords(-0.1,.4)
        ax.set_ylim([Min_ylim,Max_ylim])

    else :
        ##dummy 1st axis
        ax.plot([],[])
        ax.set_title(title)
        ax.set_xlabel(Xaxes_Name)
        ax.set_ylabel(Yaxes_Name,rotation=0)
        ax.set_xlim([Min_xlim,Max_xlim])

        ##2nd axis
        ax2 = ax.twinx()
        ax2.plot(X,Y,curve_type,linestyle=linestyle,color=color,linewidth=width)
        ax2.set_ylabel(Yaxes_Name2, rotation=0,color=color)
        ax2.tick_params(axis='y', color=color,labelcolor=color)
        ax2.set_ylim([Min_ylim2,Max_ylim2])
        if not (ax2labelcoord==None):ax2.yaxis.set_label_coords(1.08,.5)
        ax2.set_yticks(np.arange(0, 7.1, 1.))

# twist roll function
def Coupled(amp,freq,time,pamp):
    H,A,f,t,Pamp = symbols('H A f t Pamp')
    H=A*sin(2*pi*f*t) #heave
    dH_dt=diff(H, t)  #velocity of heave or dH/dt
    # theta=Pamp*cos(2*pi*f*t)+(pi/18.)  #pitch, with bias
    theta=Pamp*cos(2*pi*f*t)  #pitch, without bias
    alpha=-(atan(dH_dt)-theta)/pi      #AoA normalised by pi
    dalpha=diff(alpha, t)  #d_AoA/dt normalised by pi

    H=H.subs(A, amp).subs(f,freq).subs(t,time).evalf()
    dH_dt=dH_dt.subs(A, amp).subs(f,freq).subs(t,time).evalf()
    theta=theta.subs(Pamp, pamp).subs(f,freq).subs(t,time).evalf()
    alpha=alpha.subs(A, amp).subs(Pamp, pamp).subs(f,freq).subs(t,time).evalf()
    dalpha=dalpha.subs(A, amp).subs(Pamp, pamp).subs(f,freq).subs(t,time).evalf()

    return H,dH_dt,theta,alpha,dalpha

# roll function
def Heave(amp,freq,time):
    H,A,f,t = symbols('H A f t')
    H=A*sin(2*pi*f*t) #heave
    dH_dt=diff(H, t)  #velocity of heave or dR/dt
    alpha=-(atan(dH_dt))/pi      #AoA normalised by pi, without bias
    # alpha=-(atan(dH_dt)-(pi/18.))/pi      #AoA normalised by pi, with bias
    dalpha=diff(alpha, t)  #d_AoA/dt normalised by pi

    H=H.subs(A, amp).subs(f,freq).subs(t,time).evalf()
    dH_dt=dH_dt.subs(A, amp).subs(f,freq).subs(t,time).evalf()
    alpha=alpha.subs(A, amp).subs(f,freq).subs(t,time).evalf()
    dalpha=dalpha.subs(A, amp).subs(f,freq).subs(t,time).evalf()

    return H,dH_dt,alpha,dalpha
#
if __name__=='__main__':
    main()
    print('finished')
