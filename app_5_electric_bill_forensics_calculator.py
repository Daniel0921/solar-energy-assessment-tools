import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Electric Bill Forensics Calculator", layout="centered")

st.title("Electric Bill Forensics Calculator")
st.write("Show homeowners how monthly kWh usage, price per kWh, and fixed delivery/program charges combine to create their electric bill.")

st.divider()

st.subheader("1. Monthly kWh Usage")
monthly_kwh = st.slider("Monthly electricity usage (kWh)", 100, 3000, 669, 25)

st.subheader("2. Electricity Price")
price_per_kwh = st.slider("Price per kWh ($)", 0.05, 0.60, 0.152, 0.001, format="%.3f")

st.subheader("3. Fixed Monthly Fees / Delivery Costs")
fixed_fees = st.slider(
    "Fixed monthly fees and delivery/program charges ($)",
    0.0, 500.0, 136.21, 1.0,
    help="Use delivery services, customer charges, program charges, or other non-supply charges."
)

st.divider()

current_energy_cost = monthly_kwh * price_per_kwh
current_total_cost = current_energy_cost + fixed_fees

high_energy_cost = high_usage_kwh * price_per_kwh
high_total_cost = high_energy_cost + fixed_fees

usage_difference = high_usage_kwh - monthly_kwh
bill_difference = high_total_cost - current_total_cost

effective_current_rate = current_total_cost / monthly_kwh if monthly_kwh else 0
effective_high_rate = high_total_cost / high_usage_kwh if high_usage_kwh else 0

st.subheader("Bill Formula")
st.latex(r"\text{Total Cost} = (\text{Monthly kWh Used} \times \text{Price per kWh}) + \text{Fixed Monthly Fees}")

st.write(f"**({monthly_kwh:,} kWh × ${price_per_kwh:.3f}/kWh) + ${fixed_fees:,.2f} = ${current_total_cost:,.2f}**")

st.subheader("Current Bill Estimate")
col1, col2 = st.columns(2)
with col1:
    st.metric("Energy Usage Cost", f"${current_energy_cost:,.2f}")
    st.metric("Fixed / Delivery Fees", f"${fixed_fees:,.2f}")
with col2:
    st.metric("Estimated Total Bill", f"${current_total_cost:,.2f}")
    st.metric("Effective All-In Rate", f"${effective_current_rate:.3f}/kWh")

st.divider()

st.subheader("High Usage Scenario")
st.write(f"If usage rises from **{monthly_kwh:,} kWh** to **{high_usage_kwh:,} kWh**, while fixed fees remain at **${fixed_fees:,.2f}**, the bill changes like this:")

col3, col4 = st.columns(2)
with col3:
    st.metric("High-Usage Energy Cost", f"${high_energy_cost:,.2f}")
    st.metric("High-Usage Total Bill", f"${high_total_cost:,.2f}")
with col4:
    st.metric("Additional kWh Used", f"{usage_difference:,} kWh")
    st.metric("Bill Increase", f"${bill_difference:,.2f}")

st.divider()

st.subheader("Bill Composition")

current_fixed_share = fixed_fees / current_total_cost if current_total_cost else 0
current_energy_share = current_energy_cost / current_total_cost if current_total_cost else 0
high_fixed_share = fixed_fees / high_total_cost if high_total_cost else 0
high_energy_share = high_energy_cost / high_total_cost if high_total_cost else 0

st.write(f"""
Current bill:
- Energy usage cost: **{current_energy_share * 100:.1f}%**
- Fixed / delivery fees: **{current_fixed_share * 100:.1f}%**

High usage bill:
- Energy usage cost: **{high_energy_share * 100:.1f}%**
- Fixed / delivery fees: **{high_fixed_share * 100:.1f}%**
""")

composition_df = pd.DataFrame({
    "Category": ["Energy Usage Cost", "Fixed / Delivery Fees"],
    "Current Bill": [current_energy_cost, fixed_fees],
    "High Usage Bill": [high_energy_cost, fixed_fees]
})

fig1, ax1 = plt.subplots()
ax1.bar(composition_df["Category"], composition_df["Current Bill"])
ax1.set_ylabel("Cost ($)")
ax1.set_title("Current Bill Composition")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.bar(composition_df["Category"], composition_df["High Usage Bill"])
ax2.set_ylabel("Cost ($)")
ax2.set_title("High Usage Bill Composition")
st.pyplot(fig2)

st.subheader("Usage Sensitivity Table")
scenario_rows = []
for kwh in range(250, 3250, 250):
    energy_cost = kwh * price_per_kwh
    total_cost = energy_cost + fixed_fees
    scenario_rows.append({
        "Monthly kWh": kwh,
        "Energy Cost": round(energy_cost, 2),
        "Fixed / Delivery Fees": round(fixed_fees, 2),
        "Estimated Total Bill": round(total_cost, 2),
        "Effective All-In Rate": round(total_cost / kwh, 3)
    })

scenario_df = pd.DataFrame(scenario_rows)
st.dataframe(scenario_df, use_container_width=True)

st.subheader("How Usage Increases Total Bill")
fig3, ax3 = plt.subplots()
ax3.plot(scenario_df["Monthly kWh"], scenario_df["Estimated Total Bill"], marker="o")
ax3.set_xlabel("Monthly kWh Usage")
ax3.set_ylabel("Estimated Total Bill ($)")
ax3.set_title("Monthly kWh Usage vs Estimated Bill")
ax3.grid(True)
st.pyplot(fig3)

st.subheader("Analyst Interpretation")
st.write(f"""
This bill is driven by two forces:

1. **Usage-based electricity costs**: the kWh the home consumes.
2. **Fixed or delivery-related costs**: charges tied to the utility system, grid, delivery services, and program fees.

At **{monthly_kwh:,} kWh**, the estimated bill is **${current_total_cost:,.2f}**.

If usage rises to **{high_usage_kwh:,} kWh**, the estimated bill becomes **${high_total_cost:,.2f}**.

That is an increase of **${bill_difference:,.2f}**.

This is why controlling energy matters. Higher kWh usage increases the energy portion of the bill while the homeowner still remains exposed to delivery and infrastructure costs.
""")

st.warning("Assessment takeaway: The more electricity a home needs from the utility, the more exposed the homeowner remains to usage charges, delivery charges, and future utility rate increases.")

st.caption("This tool is for assessment and education only. Actual bills vary by utility, rate class, supplier, taxes, credits, seasonal usage, and net metering rules.")
