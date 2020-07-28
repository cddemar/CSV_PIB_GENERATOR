import pandas as pd

# csv file info
file = 'data/input.csv'
encoding = 'utf-16'
separator = '\t'
header = 0
cols = [0, 1, 2, 3, 4, 5, 6, 7, 8]
nrows = 1848
df = pd.read_csv(file, encoding=encoding, sep=separator,
                 header=header, usecols=cols, nrows=nrows)

# Metadata
column_headers = ['FECHA', 'Row Labels', 'TRIMESTRE', 'PIB_COLOMBIA_ANUAL', 'PIB_SUBAREA_ANUAL',
                  'APORTE', 'PIB_COLOMBIA_TRIMESTRAL', 'PIB_SUBAREA_TRIMESTRAL', 'SUBAREA']
year_start = 2005
year_end = 2018
months = 12
days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
leap_year_increment = 0

sub_areas = [
    'SUBAREA ANTIOQUIA',
    'SUBAREA ARAUCA',
    'SUBAREA ATLANTICO',
    'SUBAREA BOGOTA',
    'SUBAREA BOLIVAR',
    'SUBAREA BOYACA-CASANARE',
    'SUBAREA CAQUETA',
    'SUBAREA CAUCA-NARINO',
    'SUBAREA CERROMATOSO',
    'SUBAREA CORDOBA_SUCRE',
    'SUBAREA CQR',
    'SUBAREA GCM',
    'SUBAREA HUILA-TOLIMA',
    'SUBAREA META',
    'SUBAREA NO DEFINIDA (OTROS)',
    'SUBAREA NORTE DE SANTANDER',
    'SUBAREA PUTUMAYO',
    'SUBAREA SANTANDER',
    'SUBAREA VALLE'
]

department_subarea_map = [
    ['amazonas', 'SUBAREA NO DEFINIDA (OTROS)', ''],
    ['antioquia', 'SUBAREA ANTIOQUIA', ''],
    ['arauca', 'SUBAREA ARAUCA', ''],
    ['atlántico', 'SUBAREA ATLANTICO', ''],
    ['bogotá d.c.', 'SUBAREA BOGOTA', ''],
    ['bolívar', 'SUBAREA BOLIVAR', ''],
    ['boyacá', 'SUBAREA BOYACA-CASANARE', ''],
    ['caldas', 'SUBAREA CQR', ''],
    ['caquetá', 'SUBAREA CAQUETA', ''],
    ['casanare', 'SUBAREA BOYACA-CASANARE', ''],
    ['cauca', 'SUBAREA CAUCA-NARINO', ''],
    ['cesar', 'SUBAREA GCM', ''],
    ['chocó', 'SUBAREA NO DEFINIDA (OTROS)', ''],
    ['córdoba', 'SUBAREA CERROMATOSO', 'SUBAREA CORDOBA_SUCRE'],
    ['cundinamarca', 'SUBAREA NO DEFINIDA (OTROS)', ''],
    ['guainía', 'SUBAREA NO DEFINIDA (OTROS)', ''],
    ['guaviare', 'SUBAREA NO DEFINIDA (OTROS)', ''],
    ['huila', 'SUBAREA HUILA-TOLIMA', ''],
    ['la guajira', 'SUBAREA GCM', ''],
    ['magdalena', 'SUBAREA GCM', ''],
    ['meta', 'SUBAREA META', ''],
    ['nariño', 'SUBAREA CAUCA-NARINO', ''],
    ['norte de santander', 'SUBAREA NORTE DE SANTANDER', ''],
    ['putumayo', 'SUBAREA PUTUMAYO', ''],
    ['quindío', 'SUBAREA CQR', ''],
    ['risaralda', 'SUBAREA CQR', ''],
    ['san andrés, providencia y santa catalina (archipiélago)',
     'SUBAREA NO DEFINIDA (OTROS)', ''],
    ['santander', 'SUBAREA SANTANDER', ''],
    ['sucre', 'SUBAREA CORDOBA_SUCRE', ''],
    ['tolima', 'SUBAREA HUILA-TOLIMA', ''],
    ['valle del cauca', 'SUBAREA VALLE', ''],
    ['vaupés', 'SUBAREA NO DEFINIDA (OTROS)', ''],
    ['vichada', 'SUBAREA NO DEFINIDA (OTROS)', '']
]


def get_departments_by_subarea(sub_area):
    match = [index for index, row in enumerate(
        department_subarea_map) if sub_area in row]
    result = []
    for value in match:
        result.append(department_subarea_map[value][0])
    return result


def get_record_from_dataframe(year, trimester, department):
    row = df[(df['AÑO'] == year) & (df['TRIMESTRE'] ==
                                    trimester) & (df['DEPARTAMENTO'] == department)]
    return row.to_numpy()[0].tolist()


def get_departments_as_dataframe_records(year, trimester, departments):
    result = []
    for department in departments:
        result.append(get_record_from_dataframe(year, trimester, department))
    return result


def get_records_as_formatted_record(date, row_label, trimester, records, subarea):
    subarea_total = sum(record[-2] for record in records)
    country_total = records[0][-1]
    country_trimester = records[0][5]
    percentage = subarea_total/country_total
    subarea_trimester = country_trimester * percentage
    formatted_record = [date, row_label, trimester, country_total, subarea_total,
                        percentage, country_trimester, subarea_trimester, subarea]
    return formatted_record


def generate_formatted_record(year, date, row_label, trimester, subarea):
    department_dependencies = get_departments_by_subarea(subarea)
    records = get_departments_as_dataframe_records(
        year, trimester, department_dependencies)
    formatted_record = get_records_as_formatted_record(
        date, row_label, trimester, records, subarea)
    return formatted_record


def find_previous_record(year, trimester, sub_area):
    return_value = None
    for x in trimestal_pibs:
        if x[0] == year and x[1] == trimester and x[2] == sub_area:
            return_value = x[-1]
    return return_value


trimestal_pibs = []

output_df = pd.DataFrame(columns=column_headers)

for year in range(year_start, year_end + 1, 1):
    for month in range(1, months + 1, 1):
        print(
            f'year {year}, month {month:02d} - Is being processed')
        leap_year_increment = 1 if year % 4 == 0 and month == 2 else 0
        trimester = 1 if month < 4 else (
            2 if month < 7 else (3 if month < 10 else 4))

        for day in range(1, days_per_month[month - 1] + 1 + leap_year_increment, 1):
            for hour in range(24):
                for sub_area in sub_areas:
                    existing_record = find_previous_record(
                        year, trimester, sub_area)
                    formatted_record = []
                    if(existing_record):
                        formatted_record = [f'{year}-{month:02d}-{day:02d}', hour, trimester, existing_record[3],
                                            existing_record[4], existing_record[5], existing_record[6], existing_record[7], sub_area]
                    else:
                        formatted_record = generate_formatted_record(
                            year, f'{year}-{month:02d}-{day:02d}', hour, trimester, sub_area)
                        trimestal_pibs.append(
                            [year, trimester, sub_area, formatted_record])

                    record = pd.DataFrame(
                        [formatted_record], columns=column_headers)

                    output_df = output_df.append(record)

print('writing file!')
output_df.to_csv('output.csv', index=False, encoding='utf-8')
print('file created sucesfully!')
