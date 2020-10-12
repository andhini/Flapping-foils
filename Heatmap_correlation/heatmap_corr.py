## This is a script to produce heatmap of Pearson corelation coefficient
## and Correlation ratio. Data is taken from SweepangleData.csv in
## Parallel-Coordinate_SweepAngle folder. Check the png graph for the result!

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import matplotlib.pylab as pl


# Step 0 - Read the dataset, calculate column correlations and make a seaborn heatmap
def main():
    dir='C:\\Users\\andhini\\Documents\\github\\github\\'

    df = pd.read_csv(dir+'\\Parallel-Coordinate_SweepAngle\\SweepAngleData.csv',delim_whitespace = False,\
        names=["Cases",r"$\Lambda$",r"$\it{AR}$",r"$\it{St}$",r"$\it{k^*}$",\
        r"$\overline{C_T}$",r"$\overline{C_L}$",r"$\overline{C_{Pow}}$",\
        r"$\eta$(%)",r"$\it{A/l^*}$",r"$\sigma_0 C_T$",r"$\sigma_0 C_L$",\
        r"$\sigma_0 C_{Pow}$"])

    df.drop(df.index[0], inplace=True)

    # convert data to number from column 1
    df.iloc[:, 1:]=df.iloc[:, 1:].apply(pd.to_numeric, errors = 'coerce')

    # associate case name with number
    mapping={'Pitch-Heave':1,'Pitch':2,'Heave':3,'Twist-Roll':4,'Roll':5}
    df["Motion"]=[mapping[i] for i in df["Cases"]]

    data = df.filter(["Motion",r"$\it{A/l^*}$",r"$\it{AR}$",r"$\Lambda$",\
            r"$\overline{C_T}$",r"$\sigma_0 C_L$",r"$\overline{C_{Pow}}$",\
            r"$\eta$(%)"], axis=1)
    data=data.apply(lambda x: pd.to_numeric(x, errors='ignore'))
    corr = data.corr(method='pearson')

    #remove first column corr data because it'll be recomputed with corr ratio
    corr["Motion"] = np.NAN

    # Mask the upper half matrix
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    with sns.axes_style("white"):
        ax = sns.heatmap(corr,vmin=-1, vmax=1, center=0,cmap='bwr',
            square=True, annot=corr ,mask=mask, cbar_kws={'label': 'Pearson correlation Coefficient'})
    ax.set_xticklabels(ax.get_xticklabels(),
            rotation=45,horizontalalignment='center');
    ax.set_yticklabels(ax.get_xticklabels(),
            rotation=0,horizontalalignment='right');

    # Create a Rectangle patch
    rect = patches.Rectangle((3,4),1,3.95,linewidth=2,edgecolor='k',facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    ## --- correlation for category vs continuous data --- ##
    obs=["Cases",r"$\it{A/l^*}$",r"$\it{AR}$",r"$\Lambda$",\
            r"$\overline{C_T}$",r"$\sigma_0 C_L$",r"$\overline{C_{Pow}}$",\
            r"$\eta$(%)"]

    for i in range(len(obs)-1):
        Motion_Correlations=correlation_ratio(np.array(df[obs[0]]),np.array(df[obs[i+1]]))
        print (Motion_Correlations)
        colors=pl.cm.Greys(Motion_Correlations)
        textcolor='k' if Motion_Correlations<=0.5 else 'w'
        ax.add_patch(patches.Rectangle((0,1+i),1,i+2,linewidth=2,\
            color=colors,fill=True))
        ax.text(0.5*(1), (1.5+i), "%.2f" % round(Motion_Correlations, 2),\
            horizontalalignment='center',color=textcolor)


    #Grey colorbar
    ax = pl.imshow(np.array([[0,1]]), cmap="Greys")
    ax.set_visible(False)
    pl.colorbar(orientation="vertical",label='Correlation ratio for category')

    plt.savefig(dir+'//Heatmap_correlation//Heatmap_Correlation.png', dpi=350)

def correlation_ratio(categories, measurements):
    fcat, _ = pd.factorize(categories)
    cat_num = np.max(fcat)+1
    y_avg_array = np.zeros(cat_num)
    n_array = np.zeros(cat_num)
    for i in range(0,cat_num):
        cat_measures = measurements[np.argwhere(fcat == i).flatten()]
        n_array[i] = len(cat_measures)
        y_avg_array[i] = np.mean(cat_measures)
    y_total_avg = np.sum(np.multiply(y_avg_array,n_array))/np.sum(n_array)

    numerator = np.sum(np.multiply(n_array,np.power(np.subtract(y_avg_array,y_total_avg),2)))
    denominator = np.sum(np.power(np.subtract(measurements,y_total_avg),2))
    if numerator == 0:
        eta = 0.0
    else:
        eta = np.sqrt(numerator/denominator)
    return eta

if __name__ == '__main__':
    main()
