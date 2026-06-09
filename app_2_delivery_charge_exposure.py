import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Delivery Charge Exposure Calculator", layout="centered")

st.title("Delivery Charge Exposure Calculator")
st.write("Analyze how much of an electric bill comes from delivery charges and how those charges may grow.")

supply_charge = st.slider("Current supply charge ($)", 0.0, 500.0, 138.11, 1.0)
delivery_charge = st.slider("Current delivery charge ($)", 0.0, 700.0, 254.40, 1.0)
delivery_growth = st.slider("Annual delivery charge increase (%)", 0.0, 25.0, 15.0, 0.5)
supply_growth = st.slider("Annual supply charge increase (%)", 0.0, 25.0, 5.0, 0.5)
years = st.slider("Projection period (years)", 1, 30, 5, 1)

total_bill = supply_charge + delivery_charge
delivery_share = delivery_charge / total_bill if total_bill else 0

rows = []
for year in range(0, years + 1):
    projected_supply = supply_charge * ((1 + supply_growth / 100) ** year)
    projected_delivery = delivery_charge * ((1 + delivery_growth / 100) ** year)
    projected_total = projected_supply + projected_delivery
    rows.append({
        "Year": year,
        "Supply Charge": round(projected_supply, 2),
        "Delivery Charge": round(projected_delivery, 2),
        "Total Bill": round(projected_total, 2),
        "Delivery Share": f"{(projected_delivery / projected_total * 100):.1f}%" if projected_total else "0.0%"
    })

df = pd.DataFrame(rows)

st.subheader("Current Bill Breakdown")
st.metric("Current Total Bill", f"${total_bill:,.2f}")
st.metric("Delivery Share of Bill", f"{delivery_share * 100:.1f}%")
st.metric("Supply Share of Bill", f"{(1 - delivery_share) * 100:.1f}%")

st.subheader("Projected Future Bill")
st.metric(f"Projected Total Bill in {years} Years", f"${df.iloc[-1]['Total Bill']:,.2f}")
st.metric(f"Projected Delivery Charges in {years} Years", f"${df.iloc[-1]['Delivery Charge']:,.2f}")

st.write("""
Analyst interpretation:

If delivery charges make up most of the bill, the homeowner's concern is not only how much electricity they use.
It is also how much they are exposed to utility-side infrastructure and delivery costs over time.
""")

fig, ax = plt.subplots()
ax.plot(df["Year"], df["Supply Charge"], marker="o", label="Supply")
ax.plot(df["Year"], df["Delivery Charge"], marker="o", label="Delivery")
ax.plot(df["Year"], df["Total Bill"], marker="o", label="Total")
ax.set_xlabel("Year")
ax.set_ylabel("Monthly Cost ($)")
ax.set_title("Supply vs Delivery Charge Projection")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.dataframe(df, use_container_width=True)