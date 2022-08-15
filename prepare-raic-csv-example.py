import pandas as pd

df = pd.read_csv("./d50be0c6-9bd0-4159-aebb-240382a58f94_categories_15-08-22.csv")

df.OriginalImageUrl = df.OriginalImageUrl.astype('str')
df["OriginalImageUrl"] = df.OriginalImageUrl.apply(lambda x: x.split("?", 1)[0])
df.OriginalImageUrl = df.OriginalImageUrl.str.replace("d50be0c6-9bd0-4159-aebb-240382a58f94","382785e1-5dff-4998-8776-8278255f1e3a")
df = df[["Category","X1","X2","Y1","Y2","FileName","OriginalImageUrl"]].rename(columns={"OriginalImageUrl":"Url"})

df.to_csv("./mod-d50be0c6-9bd0-4159-aebb-240382a58f94_categories_15-08-22.csv",index=False)
