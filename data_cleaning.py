import pandas as pd

# Load data
df = pd.read_csv("data/raw_data.csv")

print("Original Data:")
print(df.head())

# Remove Timestamp
if "Timestamp" in df.columns:
    df.drop(columns=["Timestamp"], inplace=True)

# Clean column names
df.columns = [col.strip().replace(" ", "_").replace("/", "_") for col in df.columns]

# Convert YES/NO (case insensitive)
df = df.replace({
    "Yes": 1, "No": 0,
    "YES": 1, "NO": 0,
    "yes": 1, "no": 0
})

# Fix Placement Readiness
if "Placement_Readiness" in df.columns:
    df["Placement_Readiness"] = df["Placement_Readiness"].replace({
        "Ready": 1,
        "Not Ready": 0
    })

# Fix CGPA ranges (handle all variations)
cgpa_map = {
    "Below 6": 5,
    "Below_6": 5,
    "6-7": 6.5,
    "6–7": 6.5,
    "7-8": 7.5,
    "7–8": 7.5,
    "8-9": 8.5,
    "8–9": 8.5,
    "9+": 9.5
}

if "CGPA" in df.columns:
    df["CGPA"] = df["CGPA"].replace(cgpa_map)

# Convert numeric columns safely
df = df.apply(pd.to_numeric, errors='ignore')

# 👉 SELECT ONLY NUMERIC COLUMNS FOR SkillScore
numeric_df = df.select_dtypes(include=['number'])

# Fix Projects Completed column
if "Projects_Completed" in df.columns:
    df["Projects_Completed"] = df["Projects_Completed"].astype(str)

    # Handle date-like values (extract number safely)
    df["Projects_Completed"] = df["Projects_Completed"].str.extract(r'(\d+)')

    # Convert to numeric
    df["Projects_Completed"] = pd.to_numeric(df["Projects_Completed"], errors='coerce')

    # Fill missing values
    df["Projects_Completed"] = df["Projects_Completed"].fillna(0)


# # Add SkillScore
# df["SkillScore"] = numeric_df.sum(axis=1)

numeric_df = df.select_dtypes(include=['number'])
df["SkillScore"] = numeric_df.sum(axis=1)

# Save cleaned data
df.to_csv("data/cleaned_data.csv", index=False)

print("✅ Cleaned data saved successfully!")