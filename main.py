import etl.extract as extract
import etl.transform as transform
import etl.load as load

df = extract.query()
df = transform.transform(df)
load.load(df)

