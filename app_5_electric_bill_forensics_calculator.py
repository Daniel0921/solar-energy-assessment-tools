import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Electric Bill Forensics Calculator", layout="centered")

st.title("Electric Bill Forensics Calculator")
st.write(
    "Show homeowners how monthly kWh usage, price per kWh, and fixed delivery/program charges "
    "combine to create their electric bill."
)

st.divider()

st.subheader("1. Monthly kWh Usage")
monthly_kwh = st.slider("Monthly electricity usage (kWh)", 100, 3000, 669, 25)

st.subheader("2. Electricity Price")
price_per_kwh = st.slider(
    "Price per kWh ($)",
    0.05,
    0.60,
    0.152,
    0.001,
    format="%.3f"
)

st.subheader("3. Fixed Monthly Fees / Delivery Costs")
fixed_fees = st.slider(
    "Fixed monthly fees and delivery/program charges ($)",
    0.0,
    500.0,
    136.21,
    1.0,
    help="Use delivery services, customer charges, program charges, or other non-supply charges."
)

st.divider()

current_energy_cost = monthly_kwh * price_per_kwh
current_total_cost = current_energy_cost + fixed_fees
effective_current_rate = current_total_cost / monthly_kwh if monthly_kwh else 0

st.subheader("Bill Formula")
st.latex(
    r"\text{Total Cost} = (\text{Monthly kWh Used} \times \text{Price per kWh}) + \text{Fixed Monthly Fees}"
)

st.write(
    f"**({monthly_kwh:,} kWh × ${price_per_kwh:.3f}/kWh) "
    f"+ ${fixed_fees:,.2f} = ${current_total_cost:,.2f}**"
)

st.subheader("Current Bill Estimate")
col1, col2 = st.columns(2)

with col1:
    st.metric("Energy Usage Cost", f"${current_energy_cost:,.2f}")
    st.metric("Fixed / Delivery Fees", f"${fixed_fees:,.2f}")

with col2:
    st.metric("Estimated Total Bill", f"${current_total_cost:,.2f}")
    st.metric("Effective All-In Rate", f"${effective_current_rate:.3f}/kWh")

st.divider()

st.subheader("Bill Composition")

current_fixed_share = fixed_fees / current_total_cost if current_total_cost else 0
current_energy_share = current_energy_cost / current_total_cost if current_total_cost else 0

st.write(
    f"""
Current bill:

- Energy usage cost: **{current_energy_share * 100:.1f}%**
- Fixed / delivery fees: **{current_fixed_share * 100:.1f}%**
"""
)

composition_df = pd.DataFrame(
    {
        "Category": ["Energy Usage Cost", "Fixed / Delivery Fees"],
        "Cost": [current_energy_cost, fixed_fees],
    }
)

fig, ax = plt.subplots()
ax.bar(composition_df["Category"], composition_df["Cost"])
ax.set_ylabel("Cost ($)")
ax.set_title("Current Bill Composition")
st.pyplot(fig)

st.subheader("Bill Breakdown Summary")

st.write(
    f"""
For this home:

- Monthly Usage: **{monthly_kwh:,} kWh**
- Electricity Cost: **${current_energy_cost:,.2f}**
- Delivery & Fixed Charges: **${fixed_fees:,.2f}**
- Total Estimated Bill: **${current_total_cost:,.2f}**
- Effective Electricity Cost: **${effective_current_rate:.3f}/kWh**
"""
)

st.divider()

st.subheader("Analyst Interpretation")

st.write(
    f"""
This bill is driven by two forces:

1. **Usage-based electricity costs**: the kWh the home consumes.
2. **Fixed or delivery-related costs**: charges tied to the utility system, grid, delivery services, and program fees.

At **{monthly_kwh:,} kWh**, the estimated bill is **${current_total_cost:,.2f}**.

Of that amount:

- **${current_energy_cost:,.2f}** comes from electricity consumption.
- **${fixed_fees:,.2f}** comes from delivery and infrastructure-related costs.

This demonstrates why understanding both energy usage and delivery charges is important when evaluating long-term electricity costs.
"""
)

st.warning(
    "Assessment takeaway: The more electricity a home needs from the utility, "
    "the more exposed the homeowner remains to usage charges, delivery charges, "
    "and future utility rate increases."
)

st.caption(
    "This tool is for assessment and education only. Actual bills vary by utility, "
    "rate class, supplier, taxes, credits, seasonal usage, and net metering rules."
)
