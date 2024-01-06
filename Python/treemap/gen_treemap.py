import plotly.express as px

# Data for the Treemap
income_data = {
    "Value-added tax": 284.9,  # Umsatzsteuer
    "Income tax": 343.3,  # Lohnsteuer, veranlagte Einkommensteuer, nicht veranlagte Einkommensteuer
    "Corporate tax": 46.3,  # Körperschaftsteuer
    "Tobacco tax": 14.2,
    "Energy tax": 33.6,
    "Motor vehicle tax": 9.5,  # Kraftfahrzeugsteuer
    "Electricity tax": 6.8,  # Stromsteuer
    "Real estate transfer tax": 17.1, #  Grunderwerbsteuer
    "Inheritance tax": 9.2,  # Erbschaftsteuer
    "Beer tax": 0.6,  # Biersteuer
    "Municipal trade tax": 70.2,  # Gewerbesteuer
    "Property tax": 17.0,  # Grundsteuer
    "Broadcasting fee": 8.6,  # Rundfunkbeitrag
    "Public Health insurances": 289.3,  #
    "Public pension fund": 362.98,  # https://de.statista.com/statistik/daten/studie/39054/umfrage/einnahmen-der-gesetzlichen-rentenversicherung-seit-1990/
}

# Flatten the data for plotting
flattened_data = [{"Category": category, "Value": value}
                  for category, value in income_data.items()]

# Create a DataFrame for Plotly
import pandas as pd
df = pd.DataFrame(flattened_data)

# Create a Treemap using Plotly
fig = px.treemap(df, path=['Category'], values='Value',
                 color='Value', color_continuous_scale='aggrnyl',
                 title="Income Distribution by Category",
                 custom_data=['Value'])
fig.update_traces(textinfo='label+text+value')

# Show the plot
fig.show()