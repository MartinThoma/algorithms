import pandas as pd
import requests
import json

res = requests.get("http://api.offenesparlament.de/api/mdb")
data = json.loads(res.content)["data"]
df = pd.DataFrame(data)

df["party"] = df["party"].replace("CDU", "UNION")
df["party"] = df["party"].replace("CSU", "UNION")
parties = [
    "UNION",
    "SPD",
    "DIE LINKE",
    "DIE GRÜNEN",
]

print(f"Es gibt {len(df)} MdBs.")
for party in parties:
    print(party)
    df_party = df[df["party"] == party]
    avg_age = 1
    pct_male = len(df_party[df_party["gender"] == "male"]) / len(df_party) * 100
    print(f"* {party}\t: {pct_male:3.0f} % männlich")

del df["profile_url"]
del df["picture"]
del df["agw_id"]
del df["election_list"]
for key in df:
    if key in ["first_name", "last_name", "id"]:
        continue
    print(f"## {key}")
    print(df[key].value_counts())
    print("---------------------------")
print(df)
