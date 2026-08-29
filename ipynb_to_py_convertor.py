import json
import sys

# Replace with your actual notebook filename
notebook_file = "payments_fraud_analytics\\dashboard.ipynb"  
output_file = "payments_fraud_analytics\\dashboard.py"

with open(notebook_file, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(output_file, "w", encoding="utf-8") as f:
    for cell in data.get("cells", []):
        if cell.get("cell_type") == "code":
            # Join the lines of code and write them to the file
            code = "".join(cell.get("source", []))
            f.write(code + "\n\n")

print(f"Successfully converted {notebook_file} to {output_file}")
