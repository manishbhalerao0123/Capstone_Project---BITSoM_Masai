# %% [markdown]
# Step 1: Create extract_disclosure.py

# %%
import os
import re

from disclosure_snippets import (
    DISCLOSURE_SNIPPETS
)

# %% [markdown]
# Step 2: Implement extract_signals()

# %%
{
    "risk_flags": [...],
    "hedging_detected": bool,
    "sentiment": f"confident | cautious | neutral"
}

# %% [markdown]
# Complete Function

# %%
def extract_signals(snippet: str) -> dict:

    text = snippet.lower()

    risk_flags = []

    #################################################
    # Risk Flags
    #################################################

    if "litigation" in text:
        risk_flags.append("litigation")

    if "regulatory" in text:
        risk_flags.append("regulatory")

    #
    # Customer concentration detection
    #
    if (
        "top three customers" in text
        or "account for" in text
        and "revenue" in text
    ):
        risk_flags.append(
            "customer concentration"
        )

    #################################################
    # Hedging Language
    #################################################

    hedging_phrases = [
        "assuming",
        "cautiously",
        "visibility"
    ]

    hedging_detected = any(
        phrase in text
        for phrase in hedging_phrases
    )

    #################################################
    # Sentiment
    #################################################

    if (
        "confident" in text
        or "approved" in text
    ):
        sentiment = "confident"

    elif hedging_detected:

        sentiment = "cautious"

    else:

        sentiment = "neutral"

    #################################################
    # Final Output
    #################################################

    return {
        "risk_flags": risk_flags,
        "hedging_detected":
            hedging_detected,
        "sentiment":
            sentiment
    }

# %% [markdown]
# Step 3: Run Against All Disclosure Snippets

# %%
for snippet in DISCLOSURE_SNIPPETS:

    result = extract_signals(
        snippet
    )

    print("\n--------------------------------")
    print(snippet)
    print(result)


