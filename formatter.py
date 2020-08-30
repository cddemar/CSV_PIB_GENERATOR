import sys
import math
import numpy as np
import pandas as pd
import datetime as dt


def main():
    result_headers = ['FECHA', 'HORA', 'PIB_REGIONAL', 'REGION']
    year_start = 2017
    year_end = 2020

    df = load_xlsx_as_df()

    output_df = pd.DataFrame(columns=result_headers)

    print(f'generate among {year_start} - {year_end}')

    dfs = generate_records_in_range(df, year_start, year_end, output_df)

    print('<---->')
    # print(len(dfs))

    for df_idx in range(0, len(dfs)):
     #   print(dfs[df_idx])
     #   print(len(dfs[df_idx]))
        output_df.append(dfs[df_idx])

    output_df.to_csv(
        f'output.{year_start}-{year_end}.csv', index=False, encoding='utf-8')


def load_xlsx_as_df():
    file = r'data/input_prediction.xlsx'
    print(f'loading {file}')
    df = pd.read_excel(file, sheet_name=0, encoding='utf-8')
    return df


def generate_records_in_range(df, start, end, output_df):
    dfs = [generate_records_for_year_days(df, year, output_df)
           for year in range(start, end + 1, 1)]
    print(dfs)
    print(len(dfs))
    return dfs


def generate_records_for_year_days(df, year, output_df):
    print(f'Processing year: {year}')
    records = [get_regions_from_year_day(df, year, day) for day in range(
        1, 365 + 1 + is_leap_year(year), 1)]
    year = np.array(records)
    year = year.reshape(year.shape[0] * year.shape[1], -1)
    print(year.shape)
    print(year)
    output_df = output_df.append(year, ignore_index=True)
    print('<---->')
    print(output_df)
    print(output_df.shape)
    return output_df


def is_leap_year(year):
    return 1 if year % 4 == 0 else 0


def get_regions_from_year_day(df, year, day):
    print(f'\tProcessing day: {day}')
    date = get_date_from_year_and_day(year, day)
    records = get_regions_records(df, date, day)
    return np.array(records)


def get_date_from_year_and_day(year, day):
    date = dt.datetime(year, 1, 1) + dt.timedelta(day - 1)
    return date


def get_regions_records(df, date, day):
    records = np.array([np.array([date.strftime('%Y-%m-%d'), day,  get_dependencies_pib(df, date, region[1:]), region[0]])
                        for region in get_regions_with_dependencies()])
    hours = np.transpose([np.array(range(1, 25, 1))] * len(records)).ravel()
    repeated = np.repeat(records[np.newaxis, ...], 24, axis=0)
    repeated = repeated.reshape(repeated.shape[0] * repeated.shape[1], -1)

    repeated[:, 1] = hours
    return repeated


def get_dependencies_pib(df, date, dependencies):
    pibs = [get_prediction_by_date_and_department(
        df, date, dep) for dep in dependencies]
    return sum(pibs)


def get_prediction_by_date_and_department(df, date, department):
    match = df[(df['FECHA'] == date) & (df['DEPARTAMENTO'] == department)]
    return match['PIB_DEPARTAMENTAL_TRIMESTRAL_PRED'].iloc[0]


def get_regions_with_dependencies():
    return [
        ['Antioquia', 'antioquia'],
        ['Arauca', 'arauca'],
        ['Atlantico', 'atlántico'],
        ['BajoPutumayo', 'putumayo'],
        ['Bolivar',	'bolívar'],
        ['Boyaca', 'boyacá'],
        ['Caldas', 'caldas'],
        ['Cali', 'valle del cauca'],
        ['Caqueta',	'caquetá'],
        ['Cartago',	'valle del cauca'],
        ['Casanare', 'casanare'],
        ['Cauca',	'cauca'],
        ['Celsia',	'valle del cauca', 'tolima'],
        ['Cerromatoso',	'córdoba'],
        ['Choco', 'chocó'],
        ['CiraInfanta',	'santander'],
        ['Codensa',	'bogotá d.c.'],
        ['cundinamarca', 'cundinamarca'],
        ['Drummond', 'cesar'],
        ['Emec', 'nariño'],
        ['GCM',	'la guajira',  'cesar', 'magdalena'],
        ['Guaviare', 'guaviare'],
        ['Huila', 'huila'],
        ['Intercor', 'la guajira'],
        ['Meta', 'meta'],
        ['Nariño', 'nariño'],
        ['NorSantander', 'norte de santander'],
        ['Oxy',	'caquetá'],
        ['Pereira', 'risaralda'],
        ['Planeta',	'córdoba'],
        ['Putumayo', 'putumayo'],
        ['Quindio', 'quindío'],
        ['Rubiales', 'meta'],
        ['Santander', 'santander'],
        ['CordobaSucre', 'córdoba'],
        ['Tolima', 'tolima'],
        ['TubosCaribe',	'bolívar'],
        ['Tulua',	'valle del cauca'],
    ]


if __name__ == '__main__':
    main()
