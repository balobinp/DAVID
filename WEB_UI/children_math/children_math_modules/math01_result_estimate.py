import numpy as np
from pandas import DataFrame

# This funsction makes groups of cicles and enumerate the raws in each group
# Input is the DataFrame with columns:
# 'RES' - 1 or 0 means success or unsuccess
# 'SRES' - shist forward of 'RES'
# The output is list of lists

def math_result_make_groups(df):
    res_list = []
    i = 0
    gr = 0
    for df_list in df[['RES', 'SRES']].values:
        if df_list[0] == 1 and df_list[1] == 0:
            gr += 1
            i = 1
            res_list.append([gr, i])
        elif df_list[0] == 1 and df_list[1] == 1:
            if i == 7:
                gr += 1
                i = 1
            else:
                i += 1
            res_list.append([gr, i])
        elif df_list[0] == 0:
            res_list.append([0, 0])
    return res_list

# This function adds group number and a number within each group to the DataFrame
# Input is the original DataFrame from DataBase
# Output is the DataFt=rame with group number and a number within each group

def math_result_add_groups(df):
    df_resampled = DataFrame()
    for name in df.USER_NAME.unique():
        df_temp = df[df.USER_NAME == name].resample('D').asfreq(0).reset_index()
        df_temp.USER_NAME = name
        df_temp['RES'] = df_temp.SCORE_FIVE.apply(lambda x: 1 if int(x) >= 1 else 0)
        df_temp['SRES'] = df_temp['RES'].shift().fillna(0).astype('int64')
        df_temp[['GR', 'NUM']] = DataFrame(math_result_make_groups(df_temp))
        df_resampled = df_resampled.append(df_temp)
    return df_resampled

# This function takes the DataFrame and returns two values: today_task, solved_tasks
# Input is the original DataFrame from DataBase
# Output is today_task, solved_tasks

def math_result_estimate(df, today):
    df_resampled = math_result_add_groups(df)
    df_grouped = df_resampled.groupby(['USER_NAME', 'GR'], as_index=False).agg({'REP_DATE': max, 'NUM': 'max'})[-1:]

    if df_grouped.REP_DATE.values[0] == np.datetime64(today) and df_grouped.NUM.values[0] > 0:
        today_task = 'OK'
        solved_tasks = df_grouped.NUM.values[0]
    elif df_grouped.REP_DATE.values[0] == (np.datetime64(today) - np.timedelta64(1, 'D')) and df_grouped.NUM.values[0] > 0:
        today_task = 'NOK'
        solved_tasks = df_grouped.NUM.values[0]
    else:
        today_task = 'NOK'
        solved_tasks = 0
    return today_task, solved_tasks