import pandas as pd

df = pd.read_csv("n26-csv-transactions.csv", parse_dates=["Datum"])
print(df.columns)
print(df["Datum"].dtype)
print(df)
mapping = {}
common_names = [
    "edeka",
    "dm",
    "amazon",
    "netlight",
    "netto",
    "paypal",
    "rewe",
    "exxpozed",
    "ergo",
    "penny",
    "aldi",
    "lidl",
]
for name in common_names:
    mapping[name] = name
receivers = sorted(list(set(df["Empfänger"].tolist())))
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

mapping["Sidharta GmbH"] = "restaurant"
mapping["TRATTORIA AL PALADINO"] = "restaurant"
mapping["RESTARUANT VIET-HA"] = "restaurant"
mapping["THE THAI"] = "restaurant"
mapping["RED PEPPER"] = "restaurant"
mapping["HSO*Ye Wei Asia Restau"] = "restaurant"
mapping["HSO*Ye Wei Asia Restau"] = "restaurant"

mapping["Servus Heidi"] = "Gehalt"
mapping["NETLIGHT CONSULTING GMBH"] = "Gehalt"
mapping["Netlight Consulting GmbH"] = "Gehalt"

mapping["SPC*KLETTERWELT GMBH"] = "klettern"
mapping["KLETTERWELT GMBH"] = "klettern"

mapping["SPORTH. SCHUSTER GMBH"] = "nepal"
mapping["REISEBANK FRANKFURT AT"] = "nepal"
mapping["ERGO Direkt Krankenversicherung Aktiengesellschaft"] = "nepal"
mapping["ERGO Krankenversicherung AG"] = "nepal"
mapping["NABIL"] = "nepal"
mapping["REISEPRAXIS MÜNCHEN"] = "nepal"
mapping["NCELL"] = "nepal"
mapping["eXXpozed - sports & fashion AndreasOliver Bindhammer e. K."] = "nepal"
mapping["exxpozed - sports & fashion"] = "nepal"
mapping["405286999999"] = "nepal"
mapping["fx dispence-uae"] = "nepal"

mapping["LANDESBANK BERLIN"] = "amazon"

mapping["Lidl Vertriebs GmbH &"] = "essen"
mapping["ALDI SUED SAGT DANKE"] = "essen"
mapping["Penny Pasinger Mar"] = "essen"
mapping["REWE Filiale Muenchen"] = "essen"
mapping["Netto Marken-Discount"] = "essen"
mapping["Netto Marken-Discount"] = "essen"
mapping["EDEKA HOELTKEMEYER"] = "essen"
mapping["EDEKA M LANDSB. ST 869"] = "essen"
mapping["EDEKA PESCHEL"] = "essen"
mapping["HIT MUENCHEN PASING"] = "essen"
mapping["HIT MUENCHEN PASING"] = "essen"

mapping["momox GmbH"] = "books"
mapping["reBuy reCommerce Gmb"] = "books"

mapping["Von Hauptkonto nach Savings"] = "investment"
mapping["Von Savings nach Hauptkonto"] = "investment"
mapping["Martin Thoma"] = "investment"
mapping["N26 Fixed Term"] = "investment"
mapping["LBS Westdeutsche Landesbausparkasse"] = "investment"

# if value_cmp.startswith('edeka'):
#     mapping[value] = 'edeka'
# elif value_cmp.startswith('dm-drogerie'):
#     mapping[value] = 'DM-DROGERIE'
# else:
#     mapping[value] = value.lower()
df["Empfänger"] = df["Empfänger"].map(mapping)

df2 = (
    df.groupby(df["Empfänger"])
    .aggregate({"Betrag (EUR)": "sum"})
    .sort_values(["Betrag (EUR)"], ascending=False)
)
print(df2)  # [df2['Betrag (EUR)'].abs() > 50]
