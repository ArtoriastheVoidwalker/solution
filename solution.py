import pandas as pd
import locale
import time


locale.setlocale(locale.LC_ALL, 'ru_RU')


def binary_search(array, element, start, end):
    if start > end:
        return -1

    mid = (start + end) // 2
    if element == array[mid]['Date-time']:
        return array[mid]

    if element < array[mid]['Date-time']:
        return binary_search(array, element, start, mid - 1)
    else:
        return binary_search(array, element, mid + 1, end)


def get_sample_data(start_datetime: str, end_datetime: str, apertura: int):
    start_timer = time.time()
    custom_date_parser = lambda x: pd.to_datetime(x[:-9], format='%d %B %Y г. %H:%M:%S')
    df = pd.read_csv('786442_Ribbon1.csv',
                     encoding='Windows-1251',
                     parse_dates=['Date-time'],
                     date_parser=custom_date_parser)

    df_sorted = df.sort_values(by=['Date-time'])

    start = 0
    end = df_sorted.iloc[-1]['RecordID']

    # data-time start and end
    list_df = []
    [list_df.append(df_sorted.iloc[row]) for row in range(0, df_sorted.iloc[-1]['RecordID'])]

    # get borders
    start_datetime = pd.to_datetime(start_datetime, format='%d %B %Y г. %H:%M:%S')
    end_datetime = pd.to_datetime(end_datetime, format='%d %B %Y г. %H:%M:%S')

    left_border = binary_search(array=list_df, element=start_datetime, start=start, end=end)
    right_border = binary_search(array=list_df, element=end_datetime, start=start, end=end)

    # result csv
    df_sorted = df_sorted.set_index('Date-time')
    new_df = df_sorted[left_border['Date-time']:right_border['Date-time']]

    result_list = []
    # search for deviation for each parameter
    for column in new_df.columns[1:-1]:
        result_list.append(new_df[abs(new_df[column] - new_df[column].shift()) > apertura]) if len(
            new_df[abs(new_df[column] - new_df[column].shift()) > apertura]) > 0 else 0
    # elimination of duplicates and recording the result
    pd.concat(result_list).drop_duplicates().sort_index().to_csv('result.csv')
    return time.time() - start_timer
