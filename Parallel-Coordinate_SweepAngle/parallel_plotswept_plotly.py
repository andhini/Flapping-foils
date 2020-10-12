## This is interactive graph for PNAS manuscript.
## The sweep angle variations are visualized using plotly Parcoord  graph.
## Data in CSV. The interactive graph can be played in HTML (internet browser)

import plotly.graph_objects as go
import numpy as np
import plotly
import itertools
import array
import pandas as pd


def main():
    dir='C:\\Users\\andhini\\Documents\\github\\github\\Parallel-Coordinate_SweepAngle\\'

    # reading collected  data from csv files
    df = pd.read_csv(dir+'SweepAngleData.csv',delim_whitespace = False,\
        names=["Cases","Sweep Angle","Aspect Ratio","St","k",\
        "Mean CT","Mean CL","Mean CPo","Efficiency","A/l*",\
        "CT_RMS","CL_RMS","CPo_RMS"])
    df.drop(df.index[0], inplace=True)

    # convert data to number from column 1
    df.iloc[:, 1:]=df.iloc[:, 1:].apply(pd.to_numeric, errors = 'coerce')

    # associate case name with number
    mapping={"Pitch-Heave":1,"Pitch":2,"Heave":3,"Twist-Roll":4,"Roll":5}
    df["Motion"]=[mapping[i] for i in df["Cases"]]

    #normalized each set of CT,CL,CPo by std (results not good)
    df["Mean CT_norm"]= df["Mean CT"]/df["Mean CT"].std()
    df["Mean CL_norm"]= df["Mean CL"]/df["Mean CL"].std()
    df["Mean CPo_norm"]= df["Mean CPo"]/df["Mean CPo"].std()

    # layout coloring
    layout = go.Layout(
    autosize=False,
    width=1500,
    height=700,
    plot_bgcolor = '#FFFFFF',
    paper_bgcolor = '#E5E5E5',
    title='Sweep angle variation')
    layout.font.size=30

    casenum=df.shape[0]/3 #no of cases

    #condition to define blue/red for tail/flipper and which sweep angle for opacity
    df["col_df"]=df['Motion']
    df.loc[(df['Motion'] <= 3) & (df["Sweep Angle"] == 20), "col_df"] = 0.3 #red
    df.loc[(df['Motion'] <= 3) & (df["Sweep Angle"] == 30), "col_df"] = 0.2
    df.loc[(df['Motion'] <= 3) & (df["Sweep Angle"] == 40), "col_df"] = 0.1
    df.loc[(df['Motion'] > 3) & (df["Sweep Angle"] == 20), "col_df"] = 0.8
    df.loc[(df['Motion'] > 3) & (df["Sweep Angle"] == 30), "col_df"] = 0.9
    df.loc[(df['Motion'] > 3) & (df["Sweep Angle"] == 40), "col_df"] = 1.0 #blue
    colors=df["col_df"].values.tolist()

    fig = go.Figure(data=
        go.Parcoords(line = dict(color=colors,colorscale='rdylbu',cmin=0,cmax=1),
            dimensions = list([
                dict(range = [1,5],tickvals = np.arange(1,casenum+1),
                     constraintrange = [1], # change this range by dragging the pink line
                     label = "Motion", values = df["Motion"],
                     ticktext = ['P & H','P','H','T & R','R',]),
                dict(range = [0.13,0.5],tickvals = [0.13,0.5],
                     label = "Amp(A/l*)", values = df["A/l*"] ),
                dict(range = [2,8],tickvals = [2,4,8],
                     label = "AR", values = df["Aspect Ratio"] ),
                dict(range = [20,40],tickvals = [20,30,40],
                     label = "SweepAngle(deg)", values= df["Sweep Angle"] ),
                dict(range = [-0.5,1.],
                     tickvals = np.round(np.linspace(-0.5,1,7),2),
                     label = "Mean_CT", values = df["Mean CT"] ),
                dict(range = [0,7.0],
                     tickvals = np.round(np.linspace(0,7.0,8),2),
                     label = "CL_RMS", values = df["CL_RMS"] ),
                dict(range = [0.0,6],
                     tickvals = np.round(np.linspace(0.,6.,7),2),
                     label = "Mean C_Pow", values = df["Mean CPo"] ),
                dict(range = [0,50],
                     tickvals = np.round(np.linspace(0,50,6),2),
                     label = "Efficiency(%)", values = df["Efficiency"] )
            ])
        ),layout = layout
    )
    fig.update_traces(labelside='top')
    fig.show()
    fig.write_html(dir+"parallel_plotly.html")
if __name__ == '__main__':
    main()
