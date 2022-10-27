import pandas as pd

df = pd.read_csv("./data/QA_sugarFire.csv")

df.OriginalImageUrl = df.OriginalImageUrl.astype('str')
df["OriginalImageUrl"] = df.OriginalImageUrl.apply(lambda x: x.split("?", 1)[0])
df.OriginalImageUrl = df.OriginalImageUrl.str.replace("d50be0c6-9bd0-4159-aebb-240382a58f94","6c65128a-fa4a-4252-b507-e686323cd0bb")
df = df[["Category","X1","X2","Y1","Y2","FileName","OriginalImageUrl"]].rename(columns={"OriginalImageUrl":"Url"})

df.to_csv("./mod-d50be0c6-9bd0-4159-aebb-240382a58f94_categories_15-08-22.csv",index=False)
