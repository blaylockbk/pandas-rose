import pandas as pd
import rose

def test_rose_sampledata():
    df = pd.read_csv("sample_data/WBB.csv", skiprows=lambda x: x in [0, 1, 2, 3, 4, 5, 7])

    df.rose.table()

    df.rose.plot()


