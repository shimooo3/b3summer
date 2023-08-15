import pandas as pd
import time

year_list = ["2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014"]

for year in year_list:
    with open("data/"+year+"_url.csv") as f:
        df = pd.DataFrame()
        for line in f:
            time.sleep(2)
            url = "https://db.netkeiba.com" + line
            print(url)
            dfs = pd.read_html(url)
            df = pd.concat([df, dfs[0]])
        df.to_csv(year+"_data.csv", index=False, header=False)



