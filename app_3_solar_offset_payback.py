import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Solar Offset and Payback Calculator", layout="centered")

st.title("Solar Offset and Payback Calculator")
st.write("Estimate whether solar may financially offset utility costs over time.")

monthly_bill = st.slider("Current monthly electric bill ($)", 50.0, 1000.0, 392.51, 1.0)
annual_rate_growth = st.slider("Annual utility cost increase (%)", 0.0, 25.0, 8.0, 0.5)
solar_offset = st.slider("Estimated solar offset of current bill (%)", 0.0, 100.0, 80.0, 1.0)
system_cost_before_credit = st.slider("Solar system cost before incentives ($)", 5000.0, 80000.0, 34059.0, 500.0)
federal_tax_credit = st.slider("Federal tax credit / incentive percentage (%)", 0.0, 30.0, 30.0, 1.0)
years = st.slider("Analysis period (years)", 1, 30, 25, 1)

net_system_cost = system_cost_before_credit * (1 - federal_tax_credit / 100)

rows = []
cumulative_savings = 0
payback_year = None

for year in range(1, years + 1):
    annual_utility_cost = monthly_bill * 12 * ((1 + annual_rate_growth / 100) ** (year - 1))
    annual_solar_savings = annual_utility_cost * (solar_offset / 100)
    cumulative_savings += annual_solar_savings

    if payback_year is None and cumulative_savings >= net_system_cost:
        payback_year = year

    rows.append({
        "Year": year,
        "Projected Utility Cost Without Solar": round(annual_utility_cost, 2),
        "Estimated Solar Savings": round(annual_solar_savings, 2),
        "Cumulative Savings": round(cumulative_savings, 2),
        "Net Position After System Cost": round(cumulative_savings - net_system_cost, 2)
    })

df = pd.DataFrame(rows)

st.subheader("Key Results")
st.metric("Estimated Net System Cost After Incentives", f"${net_system_cost:,.2f}")
st.metric("Estimated 25-Year / Selected-Period Savings", f"${cumulative_savings:,.2f}")
st.metric("Estimated Net Gain After System Cost", f"${cumulative_savings - net_system_cost:,.2f}")

if payback_year:
    st.metric("Estimated Payback Year", f"Year {payback_year}")
else:
    st.metric("Estimated Payback Year", "Not reached in selected period")

st.write("""
Important analyst note:

This calculator does not prove that solar is right for a home.
It estimates whether the financial profile may justify a deeper assessment.
Actual results depend on roof condition, shading, utility rules, system design, financing terms, incentives, and household usage.
""")

fig, ax = plt.subplots()
ax.plot(df["Year"], df["Cumulative Savings"], marker="o", label="Cumulative Savings")
ax.axhline(net_system_cost, linestyle="--", label="Net System Cost")
ax.set_xlabel("Year")
ax.set_ylabel("Dollars ($)")
ax.set_title("Solar Payback Projection")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.dataframe(df, use_container_width=True)