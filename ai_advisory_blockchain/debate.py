# %% [markdown]
# Step 1: Imports

# %%
import os

from stock_universe import STOCK_UNIVERSE

# %% [markdown]
# Step 2: Choose a Ticker

# %%
TICKER = "PAYTECH"

# because PAYTECH is having good portfolio
# beta = 1.55
# analyst_expected_return = 0.19
# std_dev = 0.34

# %% [markdown]
# Step 3: Bull Agent

# %%
def bull_agent(ticker):

    data = STOCK_UNIVERSE[ticker]

    beta = data["beta"]
    expected_return = data["analyst_expected_return"]

    argument = (
        f"BULL CASE: {ticker} offers an "
        f"analyst expected return of "
        f"{expected_return:.1%}. "
        f"With a beta of {beta:.2f}, "
        f"the stock has strong market "
        f"sensitivity and may benefit "
        f"disproportionately during "
        f"bullish market conditions. "
        f"This provides attractive "
        f"upside potential for investors "
        f"seeking growth."
    )

    return argument

# %% [markdown]
# Step 4: Bear Agent

# %%
def bear_agent(ticker):

    data = STOCK_UNIVERSE[ticker]

    std_dev = data["std_dev"]
    beta = data["beta"]

    argument = (
        f"BEAR CASE: {ticker} carries "
        f"a volatility of "
        f"{std_dev:.1%} and a beta "
        f"of {beta:.2f}. "
        f"Such elevated volatility may "
        f"lead to significant price swings. "
        f"Investors should be prepared "
        f"for larger drawdowns during "
        f"unfavorable market periods."
    )

    return argument

# %% [markdown]
# Step 5: Synthesizer Agent

# %%
def synthesizer_agent(
    ticker,
    bull_argument,
    bear_argument
):

    data = STOCK_UNIVERSE[ticker]

    expected_return = (
        data["analyst_expected_return"]
    )

    std_dev = data["std_dev"]

    summary = (
        f"SYNTHESIZED VIEW: {ticker} "
        f"offers a relatively strong "
        f"expected return of "
        f"{expected_return:.1%}, which "
        f"supports the growth case. "
        f"However, its volatility of "
        f"{std_dev:.1%} indicates elevated "
        f"risk compared with more "
        f"defensive investments. "
        f"Investors should weigh the "
        f"potential upside against the "
        f"higher uncertainty before "
        f"making an allocation decision."
    )

    return summary

# %% [markdown]
# Step 6: Debate Orchestrator

# %%
def run_debate(ticker):

    bull_view = bull_agent(ticker)

    bear_view = bear_agent(ticker)

    final_view = synthesizer_agent(
        ticker,
        bull_view,
        bear_view
    )

    return {
        "ticker": ticker,
        "bull_agent": bull_view,
        "bear_agent": bear_view,
        "synthesizer": final_view
    }

# %% [markdown]
# Step 7: Execute Debate

# %%
if __name__ == "__main__":

    result = run_debate("PAYTECH")

    print("\n" + "="*70)
    print("MULTI-AGENT INVESTMENT DEBATE")
    print("="*70)

    print("\n")
    print(result["bull_agent"])

    print("\n")
    print(result["bear_agent"])

    print("\n")
    print(result["synthesizer"])


