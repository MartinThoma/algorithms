from typing import NamedTuple

class Base:
    years = 30  # How long do you expect the solar panels to last?
    electricity_price = 0.27  # [€/kWh] at the beginning of the 30 years
    yearly_price_increase = 0.03  # [percent] yearly increase in electricity price
    yearly_consumption = 6924  # [kWh/year] electricity consumption
    starting_capital = 22_000  # [€] money you have in the beginning
    feed_in_tariff = 0.0851  # [€/kWh] money you get for feeding in electricity

    # yearly interest on your capital after taxes
    # (if you have to pay taxes on it even without realizing gains)
    german_tax_rate = 0.25 * (1 + 0.055)  # 25% + 5.5% solidarity tax
    yearly_capital_gains = 0.03 * (1-german_tax_rate)


def electricity_payment(Base, yearly_consumption, year):
    """
    What will you pay in year `year` for electricity?

    Starting with year=0.
    """
    inflation = (1 + Base.yearly_price_increase) ** year
    price_per_kwh = Base.electricity_price * inflation
    return price_per_kwh * yearly_consumption

def calculate_final_money(
    Base,
    solar_investment,
    saved_yearly_consumption,
    feed_in_amount,
):
    # You start with your starting capital,
    # but if you buy solar panels you start with less.
    investment = Base.starting_capital - solar_investment
    remaining_yearly_consumption = Base.yearly_consumption - saved_yearly_consumption
    for current_year in range(Base.years):
        investment *= 1 + Base.yearly_capital_gains
        # If you have a surplus, you can sell it. You don't spend it,
        # but keep investing it:
        investment += Base.feed_in_tariff * feed_in_amount

        # If you save on electricity, you can invest that too:
        investment += electricity_payment(Base, saved_yearly_consumption, current_year)
    
    electricy = sum(-electricity_payment(Base, remaining_yearly_consumption, year) for year in range(Base.years))
    return investment + electricy


class Scenario(NamedTuple):
    solar_price: int
    saved_yearly_consumption: int
    feed_in_amount: int

scenarios = [
    Scenario(solar_price=0, saved_yearly_consumption=0, feed_in_amount=0),  # no solar
    Scenario(solar_price=16_500, saved_yearly_consumption=2746, feed_in_amount=7317), # solar without battery
    Scenario(solar_price=22_000, saved_yearly_consumption=5197, feed_in_amount=4866)  # solar with battery
]

for scenario in scenarios:
    v = calculate_final_money(
        Base,
        solar_investment=scenario.solar_price,
        saved_yearly_consumption=scenario.saved_yearly_consumption,
        feed_in_amount=scenario.feed_in_amount,
    )
    print(f"{str(scenario):<80}: {v:>12,.2f}€")
