# App 4: Home Energy Profile Calculator

This app is designed to match the clean structure of App 1 while adding a homeowner kWh usage profile.

## Features

- Current monthly electric bill slider
- Locked annual utility increase rate of 5.5%
- Projection period slider
- Monthly kWh usage slider
- Future bill projection
- kWh per day calculation
- kWh per hour calculation
- Estimated effective price per kWh
- Usage profile classification

## Locked Rate

The annual rate is locked in the code here:

```python
LOCKED_ANNUAL_RATE_INCREASE = 5.5
```

To change the default rate later, edit that value.

## Run

```bash
streamlit run app_4_home_energy_profile_calculator.py
```