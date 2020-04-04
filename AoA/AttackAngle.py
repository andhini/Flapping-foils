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
    head_dir = "C:\\Users\\andhini\\Documents\\github\\AoA\\" #directory
    filepdf=PdfPages(head_dir+'/AoA'+'.pdf')
    plt.tight_layout()
    plt.rcParams.update({'font.size': 25})

    dt=np.linspace(0., 1.0, num=100)
    C=1 # chord length, C=0.16D where D=0.16C is foil thickness
    freq=0.3/(0.16*C)/1.875 # f=kD where k
    AD=[0,0.0625,0.125,0.25,0.5,1.0,1.5,2.0,3.0,3.75] #AD=2A/D
    zs= [z/3.75 for z in AD] #z/S is spanwise sectional
    Amp=[ad*0.16*C/2. for ad in AD ]
    Ymin=-.6;Ymax=.6
    Pamp=[asin(A/(0.75*C)) for A in Amp] # pitch amplitude
    colors = pl.cm.Blues(np.linspace(.4,1.,len(AD)))
    max_alpha_C=[];max_alpha_H=[]
    d_max_alpha_C=[];d_max_alpha_H=[]

    ## time tracing alpha max for 1 cycle ##
    fig,[ax1,ax2]=plt.subplots(2,1,figsize=(11,16))
    for i in range(len(AD)):
        ### Coupled twist-roll motion ###
        dH_t=[2.*pi*freq*Amp[i]*cos(2.*pi*freq*dt[j]) for j in range(len(dt))]
        theta_t=[Pamp[i]*cos(2*pi*freq*dt[k])+(pi/18) for k in range(len(dt))]
        alpha_t=[-(atan(dH_t[l])-theta_t[l])/pi for l in range(len(dt))]
        max_alpha_C.append(max(max(alpha_t),abs(min(alpha_t))))
        d_alpha_dt=[2*pi*freq*sin(2*pi*freq*dt[o])*(Pamp[i]-2*pi*freq*Amp[i]/(4.*pi**2*\
            freq**2*Amp[i]**2*(cos(2*pi*freq*dt[o]))**2+1))/pi for o in range(len(dt))]
        d_max_alpha_C.append(max(max(d_alpha_dt),abs(min(d_alpha_dt))))

        ### Pure roll motion ###
        alpha_t_H=[-(atan(dH_t[n])-(pi/18))/pi for n in range(len(dt))]
        max_alpha_H.append(max(max(alpha_t_H),abs(min(alpha_t_H))))
        d_alpha_H_dt=[4*pi**2*Amp[i]*freq**2*sin(2*pi*freq*dt[p])/(4*pi**2*Amp[i]**2\
            *freq**2*(cos(2*pi*freq*dt[p]))**2+1)/pi for p in range(len(dt))]
        d_max_alpha_H.append(max(max(d_alpha_H_dt),abs(min(d_alpha_H_dt))))

        ## Plot roll alpha(t) evolution ##
        Plot_graph(ax1,filepdf,dt,alpha_t,'','','',\
            color=colors[i],linestyle='--')
        ## Plot roll d/dt_alpha(t) evolution ##
        Plot_graph(ax2,filepdf,dt,d_alpha_dt,'','','',\
            color=colors[i],linestyle='--')

        ## Plot twist-roll alpha(t) evolution ##
        Plot_graph(ax1,filepdf,dt,alpha_t_H,'','','',\
            label=str('%.2f'% zs[i])+'z/S',color=colors[i],linestyle='-')
        ## Plot twist-roll d/dt alpha(t) evolution ##
        Plot_graph(ax2,filepdf,dt,d_alpha_H_dt,'','','',\
            label=str('%.2f'% zs[i])+'z/S',color=colors[i],linestyle='-')

    ## Roll kinematic (tip position in y direction or tip lateral movement) ##
    H_t=[Ymax*sin(2.*pi*freq*dt[m]) for m in range(len(dt))]
    Plot_graph(ax1,filepdf,dt,H_t,r'$\alpha$(t) in $\pi$ rad','',r'$\alpha$(t)',\
        Min_ylim=Ymin,Max_ylim=Ymax,label='Roll Kinematic',color='k',width=2.5)

    ## Only for legend ##
    ax2.set_ylim([-4,4])
    Plot_graph(ax2,filepdf,[],[],'','','',color='k',linestyle='-',label='Roll')
    Plot_graph(ax2,filepdf,[],[],r'$\dot{\alpha}$(t) in $\pi$ rad/t','t/T',\
        r'$\dot{\alpha}$(t)',color='k',linestyle='--',label='Twist-Roll')

    plt.legend(fontsize=12)
    plt.savefig(head_dir+'AoA_t.png', dpi=1000)
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
        Min_ylim2=0,Max_ylim2=4,Yaxes_Name2=r'$\dot{\alpha}_{max}$',\
        label=r'$\dot{\alpha}_{max}$ Twist-Roll',color='blue',ax2labelcoord=1)

    Plot_graph(ax,filepdf,zs,d_max_alpha_H,\
        r'$\alpha_{max}$ ($\pi$ rad) & $\dot{\alpha}_{max}$ ($\pi$ rad/t)',\
        'z/S',r'$\alpha_{max}$', ax2=1,Min_ylim2=0,Max_ylim2=4,linestyle='-',\
        Yaxes_Name2=r'$\dot{\alpha}_{max}$',label=r'$\dot{\alpha}_{max}$ Roll',\
        color='blue',ax2labelcoord=1)

    plt.savefig(head_dir+'AoAmax.png', dpi=1000)
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
        if not (ax2labelcoord==None):ax2.yaxis.set_label_coords(1.08,.4)
        ax2.set_yticks(np.arange(0, 4.1, 1.))

#
if __name__=='__main__':
    main()
    print('finished')
