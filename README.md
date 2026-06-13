# Solar Energy Assessment Calculator Apps

These are five Streamlit apps designed for energy assessment conversations.

## Apps

### `app_1_bill_inflation_calculator.py`

Projects electric bill growth using compound interest.  
Useful for showing what happens if utility costs increase over time.

### `app_2_delivery_charge_exposure.py`

Breaks down supply vs delivery charges.  
Useful for showing how much of a bill is delivery-related and how delivery costs may inflate.

### `app_3_solar_offset_payback.py`

Estimates solar offset, payback period, and long-term savings.  
Useful for positioning solar as an analysis, not a sales claim.

### `app_4_home_energy_profile_calculator.py`

Builds a homeowner energy profile using the monthly electric bill, monthly kWh usage, a locked 5.5% annual increase rate, and a selected projection period.  
Useful for estimating long-term utility exposure and identifying low, moderate, high, or very high electricity usage homes.

### `app_5_electric_bill_forensics_calculator.py`

Breaks down an electric bill using the formula:

`Total Cost = (Monthly kWh Used × Price per kWh) + Fixed Monthly Fees`

Useful for showing homeowners how monthly kWh usage, price per kWh, and fixed delivery/program charges combine to create the total bill. It also shows how high-usage months can increase costs while fixed delivery charges remain attached.

Run any app:

```bash
streamlit run app_1_bill_inflation_calculator.py
streamlit run app_2_delivery_charge_exposure.py
streamlit run app_3_solar_offset_payback.py
streamlit run app_4_home_energy_profile_calculator.py
streamlit run app_5_electric_bill_forensics_calculator.py
```

## Field Use

These apps are meant to support an assessment conversation, not guarantee savings.
Use them to explain scenarios, qualify interest, and help homeowners understand why a full energy assessment is worth reviewing.
