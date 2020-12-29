import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import yaml
from pydantic import BaseModel, Field


class Config(BaseModel):
    common_names: List[str] = [
        "aldi",
        "amazon",
        "aws",
        "c&a",
        "db bahn",
        "decathlon",
        "dm",
        "edeka",
        "ergo",
        "exxpozed",
        "finanzamt",
        "google",
        "ikea",
        "lidl",
        "media markt",
        "netflix",
        "netlight",
        "netto",
        "paypal",
        "penny",
        "rewe",
        "rossmann",
        "stripe",
        "telekom",
        "thalia",
    ]
    book_stores: List[str] = ["schmitt & hahn", "hugendubel", "thalia"]
    cloth_stores: List[str] = ["c&a"]
    food_stores: List[str] = [
        "aldi",
        "backstube wuensche",
        "baeckerei riedmair",
        "edeka",
        "hit pasing",
        "lidl",
        "my-asia-shop",
        "netto",
        "orient master gmbh",
        "penny",
        "rewe",
    ]
    grocery_stores: List[str] = ["dm", "rossmann"]
    DATE_COLUMN: str = "Date"
    CATEGORY_COLUMN: str = "Category"
    ACCOUNT_NR_COLUMN: str = "Account number"
    AMOUNT_COLUMN: str = "Amount (EUR)"
    PAYEE_COLUMN: str = "Payee"
    REFERENCE_COLUMN: str = "Payment reference"
    TRANSACTION_TYPE_COLUMN: str = "Transaction type"
    FOREIGN_CURRENCY_COLUMN: str = "Type Foreign Currency"
    RENT_CAT: str = "Rent, Electricity, Water"
    FOOD_CAT: str = "Food"
    GROCERY_CAT: str = "Groceries"
    MANUAL_CAT: str = "MANUAL_CAT"
    amazon_payee_exclude: List[str] = [
        "telekom",
        "boulderwelt",
        "allgaeu skyline park",
        "deutsche post ag",
        "hotel am kuhbogen",
        "hotel augustin",
        "hotel koenigssee",
        "büdingen med",
        "koenigsseeschifffahrt",
        "wallbergbahnen",
        "westbad",
        "paypal",
    ]
    employer_name: str = ""
    employment_min_salary: float = 500  # net (what arrives on your account)
    # The payee field sometimes has weird names. The following config
    # replaces it by a more telling name. The code tries to find the name (e.g. "amzn mktp")
    # within the payee string and replaces it with the string on the right-hand side
    payee_like_mapping: List[List[str]] = [
        ["amzn mktp", "amazon"],
        ["bm muenchen/neuaub", "toom baumarkt"],
        ["spc*kletterwelt gmbh", "boulderwelt"],
        ["finanzamt", "finanzamt"],
        ["sparkasse", "sparkasse"],
        ["reisebank", "reisebank"],
    ]
    investment_accounts: List[str] = Field(default_factory=list)
    landlord_recipient_names: List[str] = Field(default_factory=list)
    delete_transaction_by_reference_substring: List[str] = Field(default_factory=list)


def load_config(filepath: Path = Path("private.config.yaml")) -> Config:
    if not filepath.is_file():
        cfg = Config()
        with open(filepath, "w") as fp:
            fp.write(yaml.dump(cfg.dict()))
    with open(filepath) as fp:
        data = yaml.safe_load(fp.read())
    return Config.parse_obj(data)


config = load_config()
DATE_COLUMN = config.DATE_COLUMN
CATEGORY_COLUMN = config.CATEGORY_COLUMN
ACCOUNT_NR_COLUMN = config.ACCOUNT_NR_COLUMN
AMOUNT_COLUMN = config.AMOUNT_COLUMN
PAYEE_COLUMN = config.PAYEE_COLUMN
REFERENCE_COLUMN = config.REFERENCE_COLUMN
TRANSACTION_TYPE_COLUMN = config.TRANSACTION_TYPE_COLUMN
FOREIGN_CURRENCY_COLUMN = config.FOREIGN_CURRENCY_COLUMN
MANUAL_CAT = config.MANUAL_CAT


def read_data(csv_filepath) -> pd.DataFrame:
    df = pd.read_csv(csv_filepath, parse_dates=[DATE_COLUMN])
    assert PAYEE_COLUMN in df.columns
    assert AMOUNT_COLUMN in df.columns
    assert DATE_COLUMN in df.columns
    assert REFERENCE_COLUMN in df.columns

    df[PAYEE_COLUMN] = normalize_payee_names(df[PAYEE_COLUMN])
    df[REFERENCE_COLUMN] = df[REFERENCE_COLUMN].fillna("")
    df[MANUAL_CAT] = df.apply(map_category, axis=1)
    return df


def normalize_payee_names(payee_series):
    mapping = {}
    common_names = config.common_names
    for name in common_names:
        mapping[name] = name
    receivers = sorted(list(set(payee_series.tolist())))
    for value in receivers:
        value_cmp = value.lower().strip()

        # check if a prefix is inside
        for i in range(1, len(value_cmp)):
            prefix = value_cmp[:i]
            if prefix in mapping.values():
                mapping[value] = prefix
                break
        else:
            mapping[value] = value.lower()
    for value in receivers:
        for search, replace in config.payee_like_mapping:
            if search in value.strip().lower():
                mapping[value] = replace
    return payee_series.map(mapping)


def get_spending_by_recipient(df: pd.DataFrame) -> Dict[str, float]:
    eur_by_recipient = defaultdict(float)
    for _, row in df.iterrows():
        recipient = row[PAYEE_COLUMN]
        eur_by_recipient[recipient] += row[AMOUNT_COLUMN]
    return eur_by_recipient


def get_spending_by_category(df: pd.DataFrame) -> Dict[str, float]:
    eur_by_category = defaultdict(float)
    for _, row in df.iterrows():
        category = map_category(row)
        eur_by_category[category] += row[AMOUNT_COLUMN]
    return eur_by_category


def map_category(row: Dict[str, Any]) -> str:
    recipient = row[PAYEE_COLUMN]
    comment_line = row[REFERENCE_COLUMN]
    category = row[CATEGORY_COLUMN]
    if recipient in config.food_stores or category == "Food & Groceries":
        return config.FOOD_CAT
    if recipient in config.grocery_stores:
        return config.GROCERY_CAT
    if recipient == "amazon":
        return "Amazon"
    if recipient in config.landlord_recipient_names:
        return config.RENT_CAT
    if recipient in config.book_stores:
        return "Books"
    if recipient in config.cloth_stores:
        return "Clothes"
    return category


def find_aborts(df: pd.DataFrame, verbose: bool = False) -> List[Tuple[int, int]]:
    aborts: List[Tuple[int, int]] = []
    tuple2indices = {}
    for index, row in df.iterrows():
        data_tuple = row[DATE_COLUMN], row[PAYEE_COLUMN], row[TRANSACTION_TYPE_COLUMN]
        if data_tuple not in tuple2indices:
            tuple2indices[data_tuple] = [index]
        else:
            # Check if this "undoes" one of the others
            just_added = None
            for pair_index in tuple2indices[data_tuple]:
                if does_undo(df.iloc[index], df.iloc[pair_index], verbose):
                    just_added = (index, pair_index)
                    aborts.append(just_added)
                    break
            if just_added:
                tuple2indices[data_tuple].remove(pair_index)
    return aborts


def combine_amazon_refunds(df: pd.DataFrame, verbose: bool) -> List[List[int]]:
    drop_count = 0
    # Find the refunds
    refunds: List[List[int]] = []
    reference2indices = defaultdict(list)
    for index, row in df.iterrows():
        if row[PAYEE_COLUMN].startswith("amazon"):
            reference = get_amazon_reference_code(row[REFERENCE_COLUMN])
            if reference is None:
                continue
            reference2indices[reference].append(index)

    # Combine the refunds
    indices_to_drop = []
    for index_group in reference2indices.values():
        if len(index_group) <= 1 or all(
            df.loc[idx][AMOUNT_COLUMN] < 0.0 for idx in index_group
        ):
            continue
        if len(index_group) > 2:
            st.write("Too complicated, investigate manually:")
            st.write(df.loc[index_group])
            continue
        if (
            df.loc[index_group[0]][AMOUNT_COLUMN]
            + df.loc[index_group[1]][AMOUNT_COLUMN]
            != 0.0
        ):
            st.write("Sum is not zero, investigate manually:")
            st.write(df.index[index_group])
            continue
        indices_to_drop += index_group
        drop_count += 1
    df = df.drop(df.index[indices_to_drop])
    st.write(f"Amazon orders were sent back {drop_count}×")
    return df


def get_amazon_reference_code(reference_text: str) -> Optional[str]:
    pattern = re.compile(r"[\d\w]{1}\d{2}-\d{7}-\d{7}")
    matches = pattern.search(reference_text)
    if matches is None:
        st.write(f"Could not find amazon reference for this: '{reference_text}'")
        return None
    return matches.group(0)


def does_undo(a, b, verbose: bool = False) -> bool:
    if a[AMOUNT_COLUMN] + b[AMOUNT_COLUMN] == 0:
        if verbose:
            st.write(a)
            st.write(b)
            st.write("-" * 80)
        return True
    return False


if __name__ == "__main__":
    pd.options.display.float_format = "{:6.2f}".format

    st.title("A Years Spendings")
    filename = st.sidebar.text_input(
        "Enter a file path to CSV export:", "n26-csv-transactions (1).csv"
    )
    df = read_data(filename)

    st.header("Data Cleaning")
    st.subheader("Deleted for other reasons")
    transactions = df[REFERENCE_COLUMN] == "initialize"
    for ref_substring in config.delete_transaction_by_reference_substring:
        transactions = transactions | df[REFERENCE_COLUMN].str.contains(
            ref_substring, case=False, na=False
        )
    st.write(df[transactions])
    df = df[~transactions]

    st.subheader("Non-EUR")
    other_currency = (df[FOREIGN_CURRENCY_COLUMN] != "EUR") & ~df[
        FOREIGN_CURRENCY_COLUMN
    ].isna()
    st.write(df[other_currency])
    df = df[~other_currency]
    df = df.drop(
        columns=[FOREIGN_CURRENCY_COLUMN, "Exchange Rate", "Amount (Foreign Currency)"]
    )

    st.subheader("Salary")
    transactions = (df[AMOUNT_COLUMN] > config.employment_min_salary) & (
        df[PAYEE_COLUMN].str.contains(config.employer_name, na=False, case=False)
    )
    st.write(
        f"The salary gave me an income of {df[transactions][AMOUNT_COLUMN].sum():,.2f} EUR."
    )
    st.write(df[transactions])
    df = df[~transactions]

    st.subheader("Investment")
    transactions = df[ACCOUNT_NR_COLUMN] == "placeholder"
    for investment_account in config.investment_accounts:
        transactions = transactions | (df[ACCOUNT_NR_COLUMN] == investment_account)
    st.write(df[transactions])
    df = df[~transactions]

    st.subheader("Side Hustles")
    transactions = df[PAYEE_COLUMN].fillna("").str.startswith("stripe")
    st.write(
        f"The side hustles gave me an income of {df[transactions][AMOUNT_COLUMN].sum():,.2f} EUR."
    )
    st.write(
        df[transactions][[DATE_COLUMN, PAYEE_COLUMN, AMOUNT_COLUMN, REFERENCE_COLUMN]]
    )
    df = df[~transactions]

    st.subheader("Being Smart")
    transactions = df[PAYEE_COLUMN].isin(
        ["finanzamt", "check24.de", "comdirect kontoaufloesung"]
    )
    st.write(
        f"Being smart gave me an income of {df[transactions][AMOUNT_COLUMN].sum():,.2f} EUR."
    )
    st.write(
        df[transactions][[DATE_COLUMN, PAYEE_COLUMN, AMOUNT_COLUMN, REFERENCE_COLUMN]]
    )
    df = df[~transactions]

    st.subheader("ATMs")
    transactions = df[CATEGORY_COLUMN] == "ATM"
    st.write(
        f"I've used ATMs {sum(transactions)}× and withdrew a total of {abs(df[transactions][AMOUNT_COLUMN].sum()):,.2f} EUR."
    )
    st.write(
        df[transactions][
            [DATE_COLUMN, PAYEE_COLUMN, AMOUNT_COLUMN, REFERENCE_COLUMN]
        ].sort_values(AMOUNT_COLUMN)
    )
    df = df[~transactions]

    st.subheader("Aborted Transactions")
    df = df.reset_index(drop=True)
    aborts = find_aborts(df, verbose=False)
    st.write(f"Found {len(aborts)} transactions which cancel each other. Delete them.")
    df = df.drop(df.index[[idx for ab in aborts for idx in ab]])

    df = combine_amazon_refunds(df, verbose=True)

    st.subheader("Reimbursed")
    salary = df[PAYEE_COLUMN].str.contains(config.employer_name, na=False, case=False)
    # First what I got back, then a list of what I paid before
    reference_pairs = [
        (  # Jan 17, 55.20 EUR, Fahrkarte
            "RPN4UO725G",
            [("2020-01-04", "DB AUTOMATEN", "")],
        ),
        (  # Feb 24, 2020: 120.2000, Fahrkarte
            "RPG24J1P1J",
            [("2020-01-23", "DB AUTOMATEN", "")],
        ),
        (  # Aug 10, 55.20 EUR, Fahrkarte
            "RP0K3IHL6Q",
            [("2020-07-10", "DB AUTOMATEN", "")],
        ),
        (  # Sep 4, 55.20 EUR, Fahrkarte
            "Re-Nr. rpqusyr5l5, Betrag 55,20",
            [("2020-08-10", "DB AUTOMATEN", "")],
        ),
        (  # Sep 18, 55.20 EUR, Fahrkarte
            "Re-Nr. rplms8ns8m, Betrag 55,20",
            [("2020-09-09", "DB AUTOMATEN", "")],
        ),
        (  # Oct 26, 55.20 EUR, Fahrkarte
            "Re-Nr. rpos0p0lk0, Betrag 55,20",
            [("2020-10-10", "MÜNCHNER VERKEHRSGESEL", "")],
        ),
        # (  # Jan 10, 2020: RP5G6R5CRN 45.8000, Sushi
        #     "RP5G6R5CRN",
        # ),
        # (  # Errornous payment
        #     "RPC9ULPAHT",
        #     [
        #         (
        #             "2020-07-15",
        #             "Netlight",
        #             "Pay back of double payment of Skovik expenses (Martin Thoma)",
        #         )
        #     ],
        # ),
    ]
    #
    # Feb 28, 2020: RPZCBJRSZK 50.8500
    # Jul 3, 2020: RPC9ULPAHT,T 3.3000
    # Jul 3, 2020: RPC9ULPAHT,h 9.9900
    # Jul 3, 2020: RPC9ULPAHT,T 3.3000
    # Jul 3, 2020: RPC9ULPAHT,T 2.6800
    # Aug 10, 2020: RP8A8ZLL24 16.6000
    # Nov 19, 2020: Re-Nr. rpexqnhu4u, 50.6400
    for reference_message, list_payments in reference_pairs:
        transaction = df[REFERENCE_COLUMN].str.lower() == reference_message.lower()
        assert (
            sum(transaction) == 1
        ), f"#transactions={sum(transaction)} for '{reference_message}'"
        df = df[~transaction]
        for date_str, payee, ref_msg in list_payments:
            transaction = (
                (df[DATE_COLUMN] == date_str)
                & (df[PAYEE_COLUMN].str.lower() == payee.lower())
                & (df[REFERENCE_COLUMN].str.lower() == ref_msg.lower())
            )
            if not (sum(transaction) == 1):
                st.write(
                    f"#transactions={sum(transaction)}, {date_str}, {payee}, {ref_msg}"
                )
            else:
                df = df[~transaction]

    st.write(df[salary][[DATE_COLUMN, PAYEE_COLUMN, REFERENCE_COLUMN, AMOUNT_COLUMN]])
    df = df[~salary]

    st.subheader("Other Income")
    # TODO: Add this to payback/returns!!!
    transactions = df[AMOUNT_COLUMN] > 0
    st.write(
        df[transactions][[DATE_COLUMN, PAYEE_COLUMN, AMOUNT_COLUMN, REFERENCE_COLUMN]]
    )
    df = df[~transactions]

    st.header("Univariate Analysis")
    st.write(f"{len(df)} transactions left after cleaning")
    st.write("Day with most transactions:")
    st.write(df[DATE_COLUMN].value_counts()[:5])
    st.write("Most common payees:")
    st.write(df[PAYEE_COLUMN].value_counts()[:10])
    st.write("Most common transaction types:")
    st.write(df[TRANSACTION_TYPE_COLUMN].value_counts())
    st.write("Most common reference:")
    st.write(df[REFERENCE_COLUMN].value_counts()[:5])
    st.write("Most common category:")
    st.write(df[MANUAL_CAT].value_counts()[:5])
    df2 = df[df[AMOUNT_COLUMN] <= 0]
    st.write(
        f"Amount paid: min={-df2[AMOUNT_COLUMN].max():0.2f}, median={-df2[AMOUNT_COLUMN].median():0.2f}, 25-percentile={-df2[AMOUNT_COLUMN].quantile(0.75):0.2f}, mean={-df2[AMOUNT_COLUMN].mean():0.2f}, 75-percentile={-df2[AMOUNT_COLUMN].quantile(0.25):0.2f}, max={-df2[AMOUNT_COLUMN].min():0.2f}"
    )
    st.write(df)

    st.header("Transaction Type")
    st.bar_chart(df[TRANSACTION_TYPE_COLUMN])

    st.header("Outflow")
    outflow = df[df[AMOUNT_COLUMN] < 0]
    st.write(
        f"* Sum outflow: {sum(outflow[AMOUNT_COLUMN]):,.2f} EUR in {len(outflow)} transactions"
    )
    st.write(df[df[AMOUNT_COLUMN] < 0])

    st.header("By recipient")
    spendings = get_spending_by_recipient(df)
    block = "```\n"
    for rec, volume in sorted(spendings.items(), key=lambda n: n[1], reverse=True):
        block += f"* {rec:<30}: {volume:7.2f} EUR\n"
    block += "```"
    st.write(block)

    st.header("By category")
    nb_no_category = sum(df[CATEGORY_COLUMN].isna())
    if nb_no_category > 0:
        st.write(f"Transactions without a category: {nb_no_category}")
    df2 = (
        df[[MANUAL_CAT, AMOUNT_COLUMN]]
        .groupby(df[MANUAL_CAT])
        .aggregate({AMOUNT_COLUMN: sum})
    ).sort_values(AMOUNT_COLUMN)
    st.write(df2)

    st.header("Investigate Categories")
    for cat in df2.index.tolist():
        st.subheader(cat)
        df_cat = df[df[MANUAL_CAT] == cat][
            [DATE_COLUMN, PAYEE_COLUMN, REFERENCE_COLUMN, AMOUNT_COLUMN]
        ].sort_values(AMOUNT_COLUMN)
        st.write(
            f"{len(df_cat)} transaction, totalling {sum(df_cat[AMOUNT_COLUMN]):,.2f} EUR"
        )
        st.write(df_cat)

    st.header("Amazon Usage")
    base = df[
        ~(
            df[MANUAL_CAT].isin(
                [
                    config.FOOD_CAT,
                    "Transport & Car",
                    "Insurances & Finances",
                    "Bars & Restaurants",
                    config.RENT_CAT,
                    "Family & Friends",
                ]
            )
            | (df[PAYEE_COLUMN].isin(config.amazon_payee_exclude))
        )
    ]
    money_spent = abs(base[AMOUNT_COLUMN].sum())
    money_spent_amazon = abs(base[base[PAYEE_COLUMN] == "amazon"][AMOUNT_COLUMN].sum())
    st.write(
        f"I spent {money_spent_amazon:,.2f} EUR on Amazon. "
        f"That is {money_spent_amazon / money_spent*100:.0f}% of my total money spent "
        f"on stuff that Amazon offers. Excluded are things that are not offered by Amazon such as "
        f"Hotels, Restaurants, local activities like swimming/bouldering. Also excluded are "
        f"areas where Amazon is not active in Germany (food, postal services, internet providers)"
    )
    st.write("Other spendings: ")
    st.write(
        base[base[PAYEE_COLUMN] != "amazon"][
            [DATE_COLUMN, PAYEE_COLUMN, REFERENCE_COLUMN, MANUAL_CAT, AMOUNT_COLUMN]
        ]
    )
    st.write("Competitors are: ")
    st.write(
        base[[PAYEE_COLUMN, AMOUNT_COLUMN]]
        .groupby(PAYEE_COLUMN)
        .aggregate({AMOUNT_COLUMN: sum})
    )

    st.header("Monthly spendings")
    st.write(
        f"In total, I spent {abs(df[AMOUNT_COLUMN].sum()):,.2f} EUR in 2020, "
        f"meaning in average per month {abs(df[AMOUNT_COLUMN].sum()/12):,.2f} EUR. "
        f"Typically, this means about ..."
    )
    st.write(
        "* 500 EUR/month for my 12.5m² room in Munich, Germany (including electricity, warm water, waste water, internet)."
    )
    st.write(
        f"* {abs(sum(df[df[MANUAL_CAT].isin(['Shopping', 'Clothes', 'Amazon', 'Books', 'Leisure & Entertainment', 'Media & Electronics'])][AMOUNT_COLUMN]))/12:.2f} EUR/month for leisure time activities (including clothes, books, Amazon, Netflix)"
    )
    st.write(
        f"* {abs(sum(df[df[MANUAL_CAT] ==config.FOOD_CAT][AMOUNT_COLUMN]))/12:.2f} EUR/month for food"
    )
    st.write(
        f"* {abs(sum(df[df[MANUAL_CAT] =='Transport & Car'][AMOUNT_COLUMN]))/12:.2f} EUR/month for public transportation"
    )
    st.write(
        f"* {abs(sum(df[df[MANUAL_CAT] =='Bars & Restaurants'][AMOUNT_COLUMN]))/12:.2f} EUR/month for bars & restaurants"
    )
    st.write(
        f"* {abs(sum(df[df[MANUAL_CAT] =='Travel & Holidays'][AMOUNT_COLUMN]))/12:.2f} EUR/month for travel and holiday"
    )
    st.write(
        f"* {abs(sum(df[df[MANUAL_CAT] =='Family & Friends'][AMOUNT_COLUMN]))/12:.2f} EUR/month for family and friends"
    )
    st.write(
        f"* {abs(sum(df[df[MANUAL_CAT].isin(['Healthcare & Drug Stores', 'Insurances & Finances'])][AMOUNT_COLUMN]))/12:.2f} EUR/month for health and insurances"
    )
    st.write(
        f"* {abs(sum(df[df[MANUAL_CAT].isin([config.GROCERY_CAT])][AMOUNT_COLUMN]))/12:.2f} EUR/month for hygene and cleaning stuff"
    )

    df2 = df[
        ~df["MANUAL_CAT"].isin(
            [
                config.FOOD_CAT,
                "Transport & Car",
                config.RENT_CAT,
                "Shopping",
                "Amazon",
                "Travel & Holidays",
                "Family & Friends",
                "Healthcare & Drug Stores",
                "Bars & Restaurants",
                "Insurances & Finances",
                "Books",
                config.GROCERY_CAT,
                "Leisure & Entertainment",
                "Media & Electronics",
                "Clothes",
            ]
        )
    ]
    st.write(f"* Other spendings: {abs(df2[AMOUNT_COLUMN].sum())/12:.2f} EUR/month")
    st.write(df2)
    # fig, ax = plt.subplots()
    # sns.barplot(x=RECEIVER_COLUMN, y=AMOUNT_COLUMN, data=df, orient="h")
    # st.pyplot(fig)
