import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# APP 4: HOME ENERGY PROFILE CALCULATOR
# ============================================================
# EDITABLE LOCKED RATE
#
# The annual utility increase rate is intentionally locked
# at 5.5% for the homeowner-facing app.
#
# To change the locked rate later, edit this value:
LOCKED_ANNUAL_RATE_INCREASE = 5.5
# ============================================================

LOCKED_ANNUAL_RATE_INCREASE = 5.5

st.set_page_config(
    page_title="Home Energy Profile Calculator",
    layout="centered"
)

st.title("Home Energy Profile Calculator")

st.write(
    "Estimate how a homeowner's electric bill may grow over time using a locked "
    f"{LOCKED_ANNUAL_RATE_INCREASE:.1f}% annual utility increase rate, while also identifying average electricity usage per hour."
)

st.divider()

# ------------------------------------------------------------
# MAIN INPUTS
# ------------------------------------------------------------

monthly_bill = st.slider(
    "Current monthly electric bill ($)",
    min_value=50.0,
    max_value=1000.0,
    value=392.51,
    step=1.0
)

years = st.slider(
    "Projection period (years)",
    min_value=1,
    max_value=30,
    value=5,
    step=1
)

st.subheader("Monthly kWh Usage")

monthly_kwh = st.slider(
    "Monthly electricity usage (kWh)",
    min_value=100,
    max_value=3000,
    value=1200,
    step=25,
    help="This is usually listed on the electric bill as monthly kWh usage."
)

# ------------------------------------------------------------
# CALCULATIONS
# ------------------------------------------------------------

rate = LOCKED_ANNUAL_RATE_INCREASE / 100

future_monthly_bill = monthly_bill * ((1 + rate) ** years)
current_annual_cost = monthly_bill * 12
future_annual_cost = future_monthly_bill * 12
annual_cost_increase = future_annual_cost - current_annual_cost

kwh_per_day = monthly_kwh / 30
kwh_per_hour = monthly_kwh / (30 * 24)

estimated_price_per_kwh = monthly_bill / monthly_kwh if monthly_kwh > 0 else 0

rows = []
for year in range(0, years + 1):
    projected_monthly_bill = monthly_bill * ((1 + rate) ** year)
    projected_annual_cost = projected_monthly_bill * 12

    rows.append({
        "Year": year,
        "Projected Monthly Bill": round(projected_monthly_bill, 2),
        "Projected Annual Cost": round(projected_annual_cost, 2)
    })

df = pd.DataFrame(rows)

# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------

st.subheader("Results")

st.metric("Current Monthly Bill", f"${monthly_bill:,.2f}")
st.metric(f"Projected Monthly Bill in {years} Years", f"${future_monthly_bill:,.2f}")
st.metric("Projected Annual Cost Increase", f"${annual_cost_increase:,.2f}")

st.subheader("Formula")

st.latex(r"FV = PV(1+r)^n")

st.write(f"""
Using your inputs:

- **Present monthly bill:** ${monthly_bill:,.2f}
- **Locked annual increase rate:** {LOCKED_ANNUAL_RATE_INCREASE:.1f}%
- **Years projected:** {years}

Projected future monthly bill: **${future_monthly_bill:,.2f}**
""")

st.divider()

# ------------------------------------------------------------
# KWH USAGE SECTION
# ------------------------------------------------------------

st.subheader("kWh Usage Breakdown")

st.latex(r"\text{kWh per hour} = \frac{\text{Monthly kWh}}{30 \times 24}")

st.write(f"""
Using your monthly usage:

- **Monthly kWh usage:** {monthly_kwh:,.0f} kWh
- **Average kWh per day:** {kwh_per_day:,.2f} kWh/day
- **Average kWh per hour:** {kwh_per_hour:,.2f} kWh/hour
- **Estimated effective price per kWh:** ${estimated_price_per_kwh:,.3f}/kWh
""")

# ------------------------------------------------------------
# USAGE PROFILE
# ------------------------------------------------------------

st.subheader("Energy Usage Profile")

if monthly_kwh < 500:
    st.info("Low Usage Home: This home uses relatively little electricity. The savings opportunity may be smaller unless rates are very high.")
elif monthly_kwh < 1000:
    st.info("Moderate Usage Home: This home has a balanced electricity profile and should be reviewed for utility cost exposure, insulation, HVAC efficiency, and future energy needs.")
elif monthly_kwh < 1600:
    st.warning("High Usage Home: This home has meaningful electricity demand. Higher usage often creates more opportunity to offset utility purchases.")
else:
    st.error("Very High Usage Home: This home has very high electricity demand. The assessment should strongly review HVAC, insulation, heat pumps, EVs, pools, and solar offset potential.")

# ------------------------------------------------------------
# CHART
# ------------------------------------------------------------

st.subheader("Projected Monthly Electric Bill Growth")

fig, ax = plt.subplots()
ax.plot(df["Year"], df["Projected Monthly Bill"], marker="o")
ax.set_xlabel("Year")
ax.set_ylabel("Projected Monthly Bill ($)")
ax.set_title(f"Projected Bill Growth at {LOCKED_ANNUAL_RATE_INCREASE:.1f}% Annual Increase")
ax.grid(True)
st.pyplot(fig)

st.subheader("Projection Table")
st.dataframe(df, use_container_width=True)

st.caption(
    "This calculator is for assessment and education only. Actual utility costs depend on usage, rate class, supply charges, delivery charges, seasonal changes, and utility-specific pricing."
)