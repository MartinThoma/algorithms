# core modules
from math import pi

# 3rd party modules
import matplotlib.pyplot as plt
import pandas as pd

# internal modules
import analysis


def main(path):
    df = analysis.parse_file(path)
    df = prepare_df(df, grouping=(df['date'].dt.hour))
    print(df.reset_index().to_dict(orient='list'))
    df = pd.DataFrame({'date': [209, 13, 1, 2, 1, 25, 809, 3571, 1952, 1448, 942, 1007, 1531, 1132, 981, 864, 975, 2502, 2786, 2717, 3985, 4991, 2872, 761]},
                      index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    print(df)
    create_radar_chart(df,
                       # cat_names=['Monday',
                       #            'Tuesday',
                       #            'Wednesday',
                       #            'Thursday',
                       #            'Friday',
                       #            'Saturday',
                       #            'Sunday']
                       )


def prepare_df(df, grouping):
    df = df['date'].groupby(grouping).count().to_frame().reset_index(drop=True)
    return df


def create_radar_chart(df, cat_names=None):
    """

    Parameters
    ----------
    df : pandas.DataFrame
        Has a column 'date'
    """

    values = df['date'].tolist()

    df = df.T.reset_index(drop=True)
    df.insert(0, 'group', 'A')

    # number of variable
    categories = list(df)[1:]
    if cat_names is None:
        cat_names = categories
    assert len(cat_names) == len(categories)
    N = len(categories)

    # What will be the angle of each axis in the plot?
    # (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], cat_names, color='grey', size=8)

    # Draw ylabels
    # ax.set_rlabel_position(0)
    ticks = get_ticks(values)
    # plt.yticks(ticks, [str(tick) for tick in ticks], color="grey", size=7)
    # plt.ylim(0, 40)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    values

    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')

    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
    plt.show()


def get_ticks(values):
    return sorted(values)


if __name__ == '__main__':
    args = analysis.get_parser().parse_args()
    main(args.filename)
