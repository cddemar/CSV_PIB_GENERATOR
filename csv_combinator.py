import pandas as pd

# csv file info
files = ['output.2017-2017.csv', 'output.2018-2018.csv',
         'output.2019-2019.csv', 'output.2020-2020.csv']
encoding = 'utf-8'
separator = ','
header = 0
cols = [0, 1, 2, 3]
rows = [315630, 315630, 315630, 316224]

# Metadata
column_headers = ['FECHA', 'HORA', 'PIB_REGIONAL', 'REGION']

dfs = []
print('reading files...')
for index in range(0, len(files)):
    # print(files[index], rows[index])
    temp_df = pd.read_csv(files[index], encoding=encoding, sep=separator,
                          header=header, usecols=cols, nrows=rows[index])
    dfs.append(temp_df)

output_df = pd.concat(dfs, ignore_index=True)
output_df.to_csv(f'output.csv', index=False, encoding='utf-8')
print('done!')
