# %% [markdown]
# Step 1: Import Modules

# %%
import os
import math

from stock_universe import (
    STOCK_UNIVERSE,
    RISK_FREE_RATE,
    MARKET_RETURN
)

from investor_profiles import (
    INVESTOR_PROFILES
)

# %% [markdown]
# Step 2: Create the Tool Function

# %%
def get_stock_data(ticker):
    """
    Tool function.
    Simulates fetching stock data.
    """
    return STOCK_UNIVERSE[ticker]

# %% [markdown]
# Step 3: Define the Mandatory Allocation Rules

# %%
ALLOCATION_RULES = {

    "Conservative": [
        "PAYBOND",
        "PAYGOLD",
        "PAYRETAIL"
    ],

    "Moderate": [
        "PAYRETAIL",
        "PAYINFRA",
        "PAYGOLD"
    ],

    "Aggressive": [
        "PAYTECH",
        "PAYFIN",
        "PAYINFRA"
    ]
}

# %% [markdown]
# Step 4: CAPM Function

# %%
def capm_return(beta):

    return (
        RISK_FREE_RATE
        + beta *
        (MARKET_RETURN - RISK_FREE_RATE)
    )

# %% [markdown]
# Step 5: Portfolio Variance Function
# 
# Assignment formula:
# 
# $ Var(Rp​)=∑wi2​σi2​+2i<j∑​wi​wj​Cov(Ri​,Rj​) $ 
# 
# and
# 
# $ Cov(Ri​,Rj​)=0.3×σi​×σj​ $ 

# %%
def portfolio_variance(std_devs,
                       weights,
                       rho=0.3):

    variance = 0

    # variance terms

    for w, sigma in zip(weights, std_devs):
        variance += (w**2) * (sigma**2)

    # covariance terms

    n = len(std_devs)

    for i in range(n):

        for j in range(i + 1, n):

            covariance = (
                rho *
                std_devs[i] *
                std_devs[j]
            )

            variance += (
                2 *
                weights[i] *
                weights[j] *
                covariance
            )

    return variance

# %% [markdown]
# Step 6: Create the Think → Act → Observe Agent

# %%
def advisory_agent(profile):

    investor_id = profile["investor_id"]

    risk_tolerance = profile["risk_tolerance"]

    investment_amount = (
        profile["investment_amount_inr"]
    )

    ##################################################
    # THINK
    ##################################################

    tickers = ALLOCATION_RULES[
        risk_tolerance
    ]

    weights = [1/3, 1/3, 1/3]

    ##################################################
    # ACT (tool calls)
    ##################################################

    stock_data = []

    for ticker in tickers:

        data = get_stock_data(ticker)

        stock_data.append(data)

    ##################################################
    # OBSERVE
    ##################################################

    stock_returns = []

    std_devs = []

    for data in stock_data:

        expected_return = capm_return(
            data["beta"]
        )

        stock_returns.append(
            expected_return
        )

        std_devs.append(
            data["std_dev"]
        )

    portfolio_return = sum(
        w * r
        for w, r in zip(
            weights,
            stock_returns
        )
    )

    variance = portfolio_variance(
        std_devs,
        weights,
        rho=0.3
    )

    portfolio_std_dev = (
        variance ** 0.5
    )

    ##################################################
    # HUMAN IN LOOP
    ##################################################

    if portfolio_std_dev > 0.20:

        status = (
            "ESCALATED_TO_HUMAN_ADVISOR"
        )

    else:

        status = "APPROVED"

    ##################################################
    # MOCK LLM RESPONSE
    ##################################################

    mock_llm = (
        os.getenv(
            "MOCK_LLM",
            "1"
        )
    )

    if mock_llm == "1":

        narrative = (
            f"For {risk_tolerance} investor "
            f"{investor_id}, we recommend "
            f"an allocation across "
            f"{tickers} with an expected "
            f"portfolio return of "
            f"{portfolio_return:.1%} and "
            f"volatility of "
            f"{portfolio_std_dev:.1%}."
        )

    else:

        narrative = (
            f"For {investor_id}, the "
            f"portfolio is expected to "
            f"deliver approximately "
            f"{portfolio_return:.1%} annual "
            f"return with "
            f"{portfolio_std_dev:.1%} "
            f"volatility."
        )

    return {
        "investor_id":
            investor_id,

        "risk_tolerance":
            risk_tolerance,

        "tickers":
            tickers,

        "portfolio_return":
            portfolio_return,

        "portfolio_std_dev":
            portfolio_std_dev,

        "status":
            status,

        "narrative":
            narrative
    }

# %% [markdown]
# Step 7: Run All Five Investors

# %%
for investor in INVESTOR_PROFILES:

    result = advisory_agent(
        investor
    )

    print("\n--------------------")

    for k, v in result.items():
        print(f"{k}: {v}")


