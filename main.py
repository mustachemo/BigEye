import extract
import transform
import load

df = extract.query()
df = transform.transform(df)
load.load(df)

