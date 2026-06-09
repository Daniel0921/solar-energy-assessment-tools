import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Electric Bill Inflation Calculator", layout="centered")

st.title("Electric Bill Inflation Calculator")
st.write("Estimate how a monthly electric bill may grow over time using compound growth.")

monthly_bill = st.slider("Current monthly electric bill ($)", 50.0, 1000.0, 392.51, 1.0)
annual_increase = st.slider("Annual utility increase rate (%)", 0.0, 25.0, 15.0, 0.5)
years = st.slider("Projection period (years)", 1, 30, 5, 1)

r = annual_increase / 100

rows = []
for year in range(0, years + 1):
    projected_monthly = monthly_bill * ((1 + r) ** year)
    projected_annual = projected_monthly * 12
    rows.append({
        "Year": year,
        "Projected Monthly Bill": round(projected_monthly, 2),
        "Projected Annual Cost": round(projected_annual, 2)
    })

df = pd.DataFrame(rows)

future_monthly = df.iloc[-1]["Projected Monthly Bill"]
future_annual = df.iloc[-1]["Projected Annual Cost"]
current_annual = monthly_bill * 12

st.subheader("Results")
st.metric("Current Monthly Bill", f"${monthly_bill:,.2f}")
st.metric(f"Projected Monthly Bill in {years} Years", f"${future_monthly:,.2f}")
st.metric("Projected Annual Cost Increase", f"${future_annual - current_annual:,.2f}")

st.subheader("Formula")
st.latex(r"FV = PV(1+r)^n")

st.write(f"""
Using your inputs:

- Present monthly bill: **${monthly_bill:,.2f}**
- Annual increase rate: **{annual_increase:.1f}%**
- Years projected: **{years}**

Projected future monthly bill: **${future_monthly:,.2f}**
""")

fig, ax = plt.subplots()
ax.plot(df["Year"], df["Projected Monthly Bill"], marker="o")
ax.set_xlabel("Year")
ax.set_ylabel("Projected Monthly Bill ($)")
ax.set_title("Projected Monthly Electric Bill Growth")
ax.grid(True)
st.pyplot(fig)

st.dataframe(df, use_container_width=True)