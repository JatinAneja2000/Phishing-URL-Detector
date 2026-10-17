import pandas as pd


# Load your two CSVs
df1 = pd.read_csv("data/phishing_site_urls-1.csv")
df2 = pd.read_csv("data/phishing_site_urls-2.csv")


# Combine them
df = pd.concat([df1, df2], ignore_index=True)


# Standardise column names first
if "URL" in df.columns:
    df = df.rename(columns={"URL": "url"})

if "Label" in df.columns:
    df = df.rename(columns={"Label": "label"})

if "ClassLabel" in df.columns:
    df = df.rename(columns={"ClassLabel": "label"})


# Keep only the needed columns
df = df[["url", "label"]]


# Clean URL text
df["url"] = df["url"].astype(str).str.strip().str.lower()


# Convert bad/good labels to 0/1
df["label"] = (
    df["label"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace({
        "bad": 0,
        "good": 1
    })
)


# Convert labels to numbers
df["label"] = pd.to_numeric(df["label"], errors="coerce")


# Remove invalid rows and duplicates
df = df.dropna()
df = df.drop_duplicates(subset="url")
df = df[df["label"].isin([0, 1])]
df["label"] = df["label"].astype(int)


# Label meanings:
# 0 = phishing
# 1 = legitimate
df.to_csv("data/clean_phishing_urls.csv", index=False)


print("Label counts:")
print(df["label"].value_counts())

print("\nFirst rows:")
print(df.head())