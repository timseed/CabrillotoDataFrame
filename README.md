# CabrillotoDataFrame

# Install 

    python setup.py


# Useage 


```python
from hamcabrillo import LoadCab

if __name__ == '__main__':
    hc = LoadCab()
    df_cab = hc.convert_to_df("notebook/2022 ARRL International DX Contest CW.cbr")
    print(f"We read {len(df_cab)} records")
```