#Parallel plt with mathplotlib - static graph
import numpy as np
from scipy import stats, interpolate, ndimage
import csv
import itertools
from math import ceil,floor,sqrt,isnan,pi
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker,colors
from matplotlib.legend import Legend
import matplotlib.pylab as pl

def main():
    dir='C:\\Users\\andhini\\Documents\\github\\github\\Parallel-Coordinate_SweepAngle\\'

    # reading collected  data from csv files
    df = pd.read_csv(dir+'SweepAngleData.csv',delim_whitespace = False,\
        names=["Cases",r"$\Lambda$",r"$\it{AR}$",r"$\it{St}$",r"$\it{k}$",\
        r"$\overline{C_T}$",r"$\overline{C_L}$",r"$\overline{C_{Pow}}$",\
        r"$\eta$(%)",r"$\it{A/l^*}$",r"$\sigma_0 C_T$",r"$\sigma_0 C_L$",\
        r"$\sigma_0 C_{Pow}$"])
    df.drop(df.index[0], inplace=True)

    # convert data to number from column 1
    df.iloc[:, 1:]=df.iloc[:, 1:].apply(pd.to_numeric, errors = 'coerce')

    # associate case name with number
    mapping={'Pitch-Heave':1,'Pitch':2,'Heave':3,'Twist-Roll':4,'Roll':5}
    df["Motion"]=[mapping[i] for i in df["Cases"]]

    #condition to define blue/red for tail/flipper and which sweep angle for opacity
    df["col_df"]=df["Motion"]
    df.loc[(df["Motion"] <= 3) & (df[r"$\Lambda$"] == 20), "col_df"] = 0.1 #red
    df.loc[(df["Motion"] <= 3) & (df[r"$\Lambda$"] == 30), "col_df"] = 0.2
    df.loc[(df["Motion"] <= 3) & (df[r"$\Lambda$"] == 40), "col_df"] = 0.3
    df.loc[(df["Motion"] > 3) & (df[r"$\Lambda$"] == 20), "col_df"] = 0.8
    df.loc[(df["Motion"] > 3) & (df[r"$\Lambda$"] == 30), "col_df"] = 0.9
    df.loc[(df["Motion"] > 3) & (df[r"$\Lambda$"] == 40), "col_df"] = 1.0 #blue
    #colors=df["col_df"].values.tolist()

    #normalized each set of CT,CL,CPo by values @sweep 20 deg
    df["Mean CT/std"]= df[r"$\overline{C_T}$"]/df[r"$\overline{C_T}$"].std()
    df["Mean CL/std"]= df[r"$\overline{C_L}$"]/df[r"$\overline{C_L}$"].std()
    df["Mean CPo/std"]= df[r"$\overline{C_{Pow}}$"]/df[r"$\overline{C_{Pow}}$"].std()

    # associate case name with number


    #----------------parallel coordinate starts here-------------------#
    cols = ["Motion",r"$\it{A/l^*}$",r"$\it{AR}$",r"$\Lambda$",r"$\overline{C_T}$",\
            r"$\sigma_0 C_L$",r"$\overline{C_{Pow}}$",r"$\eta$(%)"]
    x = [i for i, _ in enumerate(cols)]

    # providing array colours from red to blue in html format
    red=pl.cm.Reds(np.linspace(.4,1,3))
    blue=pl.cm.Blues(np.linspace(.4,1,3))
    colours = np.concatenate((red, blue), axis=0) #in RGB
    colours = [colors.to_hex(colours[c]) for c in range(len(colours))] #in html

    #create category based on Sweep angle .and. Motion type of flipper/tail
    df["Sweep"] = df["col_df"].astype('category')
    # create dict of categories: colours
    colours = {df["Sweep"].cat.categories[i]: colours[i] \
        for i, _ in enumerate(df["Sweep"].cat.categories)}

    #create line category based on Motion
    Lines = ['-','-','-',':',':']
    df["CaseCat"] = df["Motion"].astype('category')
    LineType = {df["CaseCat"].cat.categories[j]: Lines[j] \
        for j, _ in enumerate(df["CaseCat"].cat.categories)}


    # Create (X-1) sublots along x axis
    fig, axes = plt.subplots(1, len(x)-1, sharey=False, figsize=(18,6))
    font=14; plt.rcParams.update({'font.size': font})

    min_max = {"Motion": [1, 5], \
    r"$\it{A/l^*}$": [0.13,0.5],\
    r"$\it{AR}$": [2,8],\
    r"$\Lambda$": [20.0, 40.0],\
    r"$\overline{C_T}$": [-0.5, 1],\
    r"$\sigma_0 C_L$": [0, 7.0],\
    r"$\overline{C_{Pow}}$": [0,6],\
    r"$\eta$(%)": [0,50]}

    min_max_range = {}; min_max_label = {}
    for col in cols:
        min_max_range[col] = [min_max[col][0], min_max[col][1], min_max[col][1]-min_max[col][0]]
        min_max_label[col] = [df[col].min(), df[col].max(), np.ptp(df[col])]
        df[col] = np.true_divide(df[col]-min_max[col][0],min_max[col][1]-min_max[col][0])

    #
    # Plot each row
    for i, ax in enumerate(axes):
        for idx in df.index:
            category = df.loc[idx, "Sweep"]
            category_line = df.loc[idx, "CaseCat"]
            ax.plot(x, df.loc[idx, cols], colours[category], \
                    linestyle=LineType[category_line])
        ax.set_xlim([x[i], x[i+1]])

        #shading column 1- .. for showing input variables
        if(i<3):ax.set_facecolor("#CBCBCB")

    # Set the tick positions and labels on y axis for each plot
    # Tick positions based on normalised data,Tick labels are based on original data
    def set_ticks_for_axis(dim, ax, ticks):
        min_range, max_range, yrange = min_max_range[cols[dim]]
        min_val, max_val, val_range = min_max_label[cols[dim]]
        # print ( min_max_label[cols[dim]],min_max_range[cols[dim]])
        step = yrange / float(ticks-1)
        norm_min = df[cols[dim]].min()-(min_val-min_range)*np.ptp(df[cols[dim]])/val_range
        norm_range = np.ptp(df[cols[dim]])/val_range*yrange
        norm_step = norm_range / float(ticks-1)
        # print (norm_min,norm_range,norm_step)
        # print ('ylim',ax.get_ylim())

        #combine commented #1 and #2 to manually set ticks
        tick_labels = []; new_ticks=[];n=0
        for i in range(ticks):
            if (dim==0):#first axis now string
                tick_labels.append(list(mapping)[n]);n=n+1;
            elif (dim==2 or dim==3 or dim==7):# 2nd, 3rd, 7th axis now without decimal
                tick_labels.append('%.f' %round(min_range + step * i, 2))
            else :
                tick_labels.append(round(min_range + step * i, 2)) #original
            new_ticks.append(round(norm_min + norm_step * i, 2))

        ax.yaxis.set_ticks(new_ticks)
        ax.set_yticklabels(tick_labels,fontsize=font)


    ticknum=[5,2,4,3,7,6,7,6] #manual varying tick based on variables
    for dim, ax in enumerate(axes):
        ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
        set_ticks_for_axis(dim, ax, ticks=ticknum[dim])
        ax.set_xticklabels([cols[dim]],fontsize=font)

    y1,y2=ax.get_ylim() #get +- 5% from automatic lower and upper ylim

    # Move the final axis' ticks to the right-hand side
    ax = plt.twinx(axes[-1])
    ax.set_ylim(y1, y2)
    dim = len(axes)

    ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
    set_ticks_for_axis(dim, ax, ticks=6)
    ax.set_xticklabels([cols[-2], cols[-1]],fontsize=font)


    # Remove space between subplots
    plt.subplots_adjust(wspace=0)
    #
    # Add legend to plot
    plt.legend(
        [plt.Line2D((0,1),(0,0), color=colours[cat]) for cat in df["Sweep"].cat.categories],
        [20,30,40],bbox_to_anchor=(-6.6, .96), loc=1, borderaxespad=0.)
    #
    #second legend for motion type
    style=["-",":"]; lcolours=[colours[0.3],colours[1]] #darkest colors
    leg = Legend(ax,
        [plt.Line2D((0,1),(0,0), linestyle=style[lt],color=lcolours[lt]) \
        for lt in range(2)],["Tail","Flipper"],\
        bbox_to_anchor=(-6.39, 1.1), loc=1, borderaxespad=0.)
    ax.add_artist(leg);

    plt.title("Sweep Angle Variation")
    # plt.show()
    plt.savefig(dir+'/ParallelPlot_MatplotlibVersion.png', dpi=100)

if __name__ == '__main__':
    main()
