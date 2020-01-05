"""Analyze stock market data."""

import math

import click
import matplotlib.pyplot as plt
import pandas as pd


@click.command()
@click.option("-f", "--file", "filepath", required=True)
def main(filepath):
    """
    Download data via
    https://www.fondscheck.de/quotes/historic?boerse_id=5&secu=123822833&page=23
    """
    df = pd.read_csv(filepath, sep=";", thousands=".", decimal=",")
    df["Datum"] = pd.to_datetime(df["Datum"], format="%Y-%m-%d")
    df = df.sort_values(by="Datum").reset_index()
    print(df)
    print("Cummulative Volume: {}".format(df.Volumen.sum()))

    data = df.set_index("Datum")

    data["year"] = data.index.year
    data["month"] = data.index.month
    data["week"] = data.index.week
    data["weekday"] = data.index.weekday
    data = data[["year", "month", "week", "weekday", "Schlusskurs"]].to_records(
        index=False
    )

    # Group into weeks:
    week_data = {}
    for el in data:
        year_month_week = "{}-{}-{}".format(el[0], el[1], el[2])
        weekday = el[3]
        if year_month_week not in week_data:
            week_data[year_month_week] = {}
        week_data[year_month_week][weekday] = el[4]

    # Normalize
    for year_month_week, weekday_value_dict in week_data.items():
        for i in range(6):
            if i not in weekday_value_dict:
                # print("Could not find weekday {}".format(i))
                weekday_value_dict[i] = float("nan")
        weekday_values = sorted(weekday_value_dict.items())

        # Take the first non-nan value
        i = 0
        v0 = weekday_values[i][1]
        while math.isnan(v0) and i < len(weekday_values):
            v0 = weekday_values[i][1]
            i += 1
        weekday_values = [value - v0 for key, value in weekday_values if key < 5]
        week_data[year_month_week] = weekday_values

    # Convert it back to a dataframe
    data = []
    for year_month_week, weekday_values in week_data.items():
        assert len(weekday_values) == 5, len(weekday_values)
        row = [str(year_month_week)] + weekday_values
        data.append(row)

    df = pd.DataFrame(data)
    df.columns = ["week", 0, 1, 2, 3, 4]
    # df = df.set_index('week')
    # df = df.T.reset_index()
    print(df)
    # data_by_day = data.resample('d').mean()  #.set_index(['year', 'week', 'day']).unstack(['year', 'week'])
    # data_by_day['hash_rate'].plot()
    # data_by_day['Schlusskurs'].plot()

    # multiple line plot
    for data in df.to_records(index=False).tolist():
        key = data[0]
        values = data[1:]
        try:
            plt.plot(values, marker="", linewidth=1, alpha=0.9)
        except TypeError:
            pass

    # Add legend
    plt.legend(loc=2, ncol=2)

    # Add titles
    plt.title(
        "A (bad) Spaghetti plot", loc="left", fontsize=12, fontweight=0, color="orange"
    )
    plt.xlabel("Weekday")
    plt.ylabel("Value")
    plt.show()

    for i in range(5):
        df.hist(column=i)
        print(df[i].mean())
        plt.show()


main()
