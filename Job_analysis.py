"""
to create an analysis over the applying positions
step 1: create a db and load the existing data into the db
step 2 : fetch this data from the db to find KPIs

"""
import pandas as pd

positions_df = pd.read_excel(io="../applications-flow.xlsx"
                             )
print(positions_df.shape)
print(positions_df.head)

# pandas remaining columns
positions_df.rename(mapper={"Date": "date of apply", "Position": "Job_role",
                            "company": "company", "Link": "details", "Response": "response"},
                    axis='columns', inplace=True)

print(positions_df.columns)
# original dataframe is modified by removing the null columns
modified_df = positions_df.loc[:, 'date of apply': 'response']
