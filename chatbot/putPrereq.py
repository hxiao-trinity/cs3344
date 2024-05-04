import pandas as pd
import re

df = pd.read_csv('cosb.csv')

def extract_prerequisites(description):
    if not isinstance(description, str):
        print(12121)
        return None
    match = re.search(r"prerequisite[s]?: ([^.]+)\.", description, re.IGNORECASE)
    if match:
        return match.group(1).strip()  # Extract the prerequisite part and strip any extra whitespace
    return None  # Return None if no prerequisites are found

# Apply the function to create a new column with extracted prerequisites
df['prereq'] = df['description'].apply(extract_prerequisites)

# Save the modified DataFrame back to a CSV file
df.to_csv('swaaaaaaaaaaaaaaaaaaaaaaaaaaaa.csv', index=False)

# Optionally, display the DataFrame to verify changes
print(df[['course', 'coursetitle', 'prereq']])