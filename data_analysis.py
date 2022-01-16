import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.neighbors import KernelDensity
import matplotlib as mpl
import matplotlib.gridspec as grid_spec

def Q1(x):
    return np.percentile(x, 25)

def Q3(x):
    return np.percentile(x, 75)

if __name__ == "__main__":
    # Load Spotify data
    sp_df = pd.read_csv('data/processed_spotify_songs_duration.csv', index_col=0)
    sp_df = sp_df.drop(columns=['playlist_url', 'track_uri', 'title'])

    '''
    Plot song duration line graph 
    '''

    # Record statistical data
    sp_graphing_df = sp_df.groupby('release year')['duration'].agg(Median='median', Q1=Q1, Q3=Q3)
    sp_graphing_df['release year'] = sp_graphing_df.index

    # Plot line graph
    fig1, ax = plt.subplots()

    # Plot data
    ax.plot(sp_graphing_df['release year'], sp_graphing_df['Median'], label='Median',
             color='#40A84E', marker='o')
    ax.fill_between(sp_graphing_df['release year'], sp_graphing_df['Q1'], sp_graphing_df['Q3'], alpha=0.2,
                    label='Interquartile Range', color='#40A84E', edgecolor=None)

    # Create legend
    plt.legend(loc='upper left', fontsize=12)

    # Label axis
    plt.xlabel('Release Year', fontdict={'fontsize': 13}, horizontalalignment="center")
    plt.ylabel('Duration (s)', fontdict={'fontsize': 13}, horizontalalignment="center")

    # Set line graph title
    plt.title('Duration of Hit Songs by Release Year', fontdict={'fontsize': 16, 'fontweight': 'semibold'},
              horizontalalignment="center")

    # Customize x axis ticks
    plt.xticks(np.arange(1990, 2023, 2))

    # Add gridlines
    plt.grid(axis='y', color='#7C7C7C', linestyle='-', alpha=0.25)

    plt.show()

    '''
    Plot song duration density scatter plot 
    '''

    fig2, ax = plt.subplots()

    for year in range(1991, 2022):

        x = sp_df.loc[sp_df['release year'] == year, 'release year'].to_numpy()
        y = sp_df.loc[sp_df['release year'] == year, 'duration'].to_numpy()

        # Calculate the point density
        z = gaussian_kde(y)(y)
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

        plt.scatter(x, y, c=z, s=20)

    plt.colorbar()
    plt.show()

    '''
    Plot song duration ridgeplot
    '''
    years = [x for x in np.unique(sp_df['release year']) if x >= 2006 and x <= 2021]
    colours = ['#40A84E', '#40A89B']

    gs = (grid_spec.GridSpec(len(years), 1))

    fig = plt.figure(figsize=(16,9))

    i = 0

    # creating empty list
    ax_objs = []

    gs.update(hspace=-0.75)

    for year in years:
        # creating new axes object and appending to ax_objs
        ax_objs.append(fig.add_subplot(gs[i:i + 1, 0:]))

        # plotting the distribution
        plot = (sp_df.loc[sp_df['release year'] == year, 'duration'].plot.kde(ax=ax_objs[-1], color="#f0f0f0", lw=0.5)
                )

        # grabbing x and y data from the kde plot
        x = plot.get_children()[0]._x
        y = plot.get_children()[0]._y

        # filling the space beneath the distribution
        ax_objs[-1].fill_between(x, y, color=colours[i%2])

        # setting uniform x and y lims
        ax_objs[-1].set_xlim(90, 330)
        ax_objs[-1].set_ylim(0, 0.03)

        # make background transparent
        rect = ax_objs[-1].patch
        rect.set_alpha(0)

        # remove borders, axis ticks, and labels
        ax_objs[-1].axes.get_yaxis().set_visible(False)
        ax_objs[-1].set_frame_on(False)

        if i == len(years) - 1:
            ax_objs[-1].set_xlabel("Duration (s)", fontsize=12,fontweight="normal")
        else:
            ax_objs[-1].set_xticklabels([])

        spines = ["top", "right", "left", "bottom"]
        for s in spines:
            ax_objs[-1].spines[s].set_visible(False)

        ax_objs[-1].text(70, 0, year, fontweight="semibold", fontsize=12, ha="center")

        i += 1

    plt.show()