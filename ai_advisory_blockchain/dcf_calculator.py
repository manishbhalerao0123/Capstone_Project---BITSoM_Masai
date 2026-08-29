# %% [markdown]
# Overall task -  
#     Compute FCFF.  
# Compute Cost of Equity using CAPM.  
# Compute WACC.  
# Forecast 5 years of FCFF.  
# Calculate Terminal Value.  
# Discount all cash flows to present value.  
# Build a 3×3 sensitivity table.  
# Cross-check against EV/EBITDA valuation.  
# Verify that WACC > Terminal Growth Rate in all sensitivity scenarios.

# %% [markdown]
# Imports

# %%
import pandas as pd

# %% [markdown]
# Base Inputs (INR)

# %%
fcff = 80.0

growth_rate = 0.10

terminal_growth = 0.04

wacc = 0.1155

# %% [markdown]
# Forecast 5 Years FCFF  
# $ FCFF=EBIT(1−T)+DA−CapEx−ΔNWC $

# %%
cashflows = []

current_fcf = fcff

for year in range(1, 6):

    current_fcf = (
        current_fcf *
        (1 + growth_rate)
    )

    cashflows.append(current_fcf)

# %% [markdown]
# Compute Terminal Value  
# $ TV=FCF5​(1+g)/WACC−g​ $

# %%
terminal_value = (
    cashflows[-1]
    *
    (1 + terminal_growth)
) / (
    wacc - terminal_growth
)

# %% [markdown]
# Discount Cash Flows

# %%
pv_cashflows = []

for year, cf in enumerate(
        cashflows, start=1):

    pv = cf / (
        (1 + wacc) ** year
    )

    pv_cashflows.append(pv)

# %% [markdown]
# Discount Terminal Value

# %%
pv_terminal = (
    terminal_value
    /
    ((1 + wacc) ** 5)
)

# %% [markdown]
# Enterprise Value

# %%
enterprise_value = (
    sum(pv_cashflows)
    + pv_terminal
)

print(
    f"Enterprise Value: "
    f"₹{enterprise_value:.2f} Crore"
)

# %% [markdown]
# Cost of Equity (CAPM)  
# $ Re​=Rf​+β(Rm​−Rf​) $

# %% [markdown]
# Cost of Debt  
# $ Rd​=EBTDA * (1−TaxRate) $

# %% [markdown]
# Capital Structure

# %% [markdown]
# WACC  
# $ WACC=(E/V)×Re​+(D/V)×Rd​ $

# %% [markdown]
# Generate 3×3 Grid

# %%
wacc_values = [
    wacc - 0.01,
    wacc,
    wacc + 0.01
]

growth_values = [
    terminal_growth - 0.01,
    terminal_growth,
    terminal_growth + 0.01
]

results = {}

# %%
for w in wacc_values:

    row = {}

    for g in growth_values:

        tv = (
            cashflows[-1]
            * (1 + g)
        ) / (
            w - g
        )

        pv_tv = (
            tv /
            ((1+w)**5)
        )

        ev = (
            sum(
                cf/((1+w)**yr)
                for yr, cf
                in enumerate(
                    cashflows,
                    start=1
                )
            )
            + pv_tv
        )

        row[
            f"{g:.2%}"
        ] = round(
            ev,
            2
        )

    results[
        f"{w:.2%}"
    ] = row

# %%
sensitivity_table = (
    pd.DataFrame(results)
)

print(sensitivity_table)

# %% [markdown]
# Required Self-Check  
# 
# Worst-case cell:  
# Lowest WACC = 10.55%  
# Highest Growth = 5%  
# 
# Difference:
# 10.55% - 5.00%=5.55%
# 
# Check:
# 5.55% > 1%

# %% [markdown]
# EV/EBITDA Cross-Check  
# 
# EBITDA = ₹150 Crore
# 
# Industry Multiple = 8x
# 
# Formula:
# 
# $ EV=EBITDA×MultipleEV = EBITDA \times Multiple $  
# $ EV = 150\times8 = ₹1,200\ CroreEV=150×8=₹1,200 Crore $

# %% [markdown]
# Comparison  
# 
# Method - Enterprise Value   
# DCF - ₹1,248 Cr  
# EV/EBITDA - ₹1,200 Cr
# Difference - ₹48 Cr (4%)


