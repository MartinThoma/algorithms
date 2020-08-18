# Core Library modules
import datetime
import math
from typing import List

# Third party modules
import matplotlib
import matplotlib.pyplot as plt

# First party modules
from regression import LogitRegressor, get_data

matplotlib.use("TKAgg", warn=False, force=True)


simulation_day_start = 0
switching_day = 100
simulation_day_end = 360
critical_care_percentage = 0.05
intensive_care_beds = 28_000


model = LogitRegressor(beta=0.2060, c=14.5360, d=1.0, max_population=262400000.0)
model_flat = LogitRegressor(
    beta=0.05, c=13.4600, d=1.0000, max_population=20_000_000.0, shift_x=120
)


def get_new_infections(model, simulation_day_start, simulation_day_end) -> List[float]:
    new_infected_list = []
    for day in range(simulation_day_start, simulation_day_end):
        if day == 0:
            new_infected_list.append(0)
        else:
            new_infected = model.predict([day])[0] - model.predict([day - 1])[0]
            new_infected_list.append(new_infected)
    return new_infected_list


with plt.xkcd():
    fig, ax = plt.subplots(1, 1, figsize=(15, 6))
    y_max = model.max_population
    total_infected = model.predict(range(simulation_day_start, simulation_day_end))
    new_infected_list = get_new_infections(
        model, simulation_day_start, simulation_day_end
    )

    day = datetime.datetime.strptime("2020-02-24", "%Y-%m-%d")
    print("date, predicted accummulated sick, new sick")
    for sick_people, new_infected in zip(total_infected, new_infected_list):
        print(f"{day:%Y-%m-%d}: {sick_people:,.0f} (+{new_infected:,.0f})")
        day += datetime.timedelta(seconds=24 * 60 * 60)
    # plt.plot(
    #     list(range(simulation_day_start, simulation_day_end)),
    #     total_infected,
    # )
    plt.plot(list(range(simulation_day_start, simulation_day_end)), new_infected_list)

    flat_infected = []
    flat_infected = get_new_infections(model, simulation_day_start, switching_day)

    if len(flat_infected) == 0:
        x = 0
    else:
        x = model.get_x(flat_infected[-1])
    print(f"Switch day: {x}")
    print("-" * 80)
    delta = x - switching_day
    add = len(range(int(simulation_day_start + delta), int(simulation_day_end + delta)))
    delta_list = len(new_infected_list) - add
    flat_infected += get_new_infections(
        model_flat,
        int(simulation_day_start + delta) - delta_list,
        int(simulation_day_end + delta),
    )
    flat_infected = get_new_infections(
        model_flat, simulation_day_start, simulation_day_end
    )
    plt.plot(
        list(range(simulation_day_start, simulation_day_start + len(flat_infected))),
        flat_infected,
    )
    plt.plot(
        list(range(simulation_day_start, simulation_day_start + len(flat_infected))),
        [intensive_care_beds for _ in range(simulation_day_start, simulation_day_end)],
        "--",
    )
    plt.plot(
        list(range(simulation_day_start, simulation_day_start + len(flat_infected))),
        [
            intensive_care_beds / critical_care_percentage
            for _ in range(simulation_day_start, simulation_day_end)
        ],
        "--",
    )
    plt.xlabel("Days after first infection")
    plt.ylabel("New infections per day")
    plt.text(250, intensive_care_beds + 30_000, "Intensive Care Beds", color="green")
    plt.text(
        250,
        intensive_care_beds + intensive_care_beds / critical_care_percentage,
        "Healthcare carrying capacity",
        color="red",
    )
    plt.legend(["new infected", "new infected (lower growth)"])  # "sick (accumulated)",

    def formatter(x, pos):
        prefixes = [("m", 10 ** 6), ("k", 10 ** 3)]
        for prefix, amount in prefixes:
            if x >= amount:
                return f"{x / amount}{prefix}"
        return f"{x:,}"

    plt.gca().yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(formatter))
    plt.show()
