import datetime

from classes.read_file import ReaderTxt

input_filename = 'E1_2023-08-31_11-19-13.mp4.txt'  # Входной файл
output_filename = 'TM1_2023-08-31_11-19-13.mp4.txt'  # Выходной файл
new_start_time = datetime.datetime(year=2023, month=9, day=1, hour=11, minute=36, second=10, microsecond=149806)


# Функция time_change меняет начальный момент времени файла
def time_change(input_filename, output_filename, new_start_time):
    reader_txt = ReaderTxt(f'data/{input_filename}')
    data = reader_txt.read_all()
    data_split = data[0].split('\t')
    old_start_time = data_split[0][0:26]
    old_start_time = datetime.datetime.strptime(old_start_time, '%Y-%m-%d %H:%M:%S.%f')
    time_delta = old_start_time - new_start_time
    data_list = []
    for line in data:
        line_split = line.split('\t')
        line_split[0] = line_split[0][0:26]
        time_line = datetime.datetime.strptime(line_split[0], '%Y-%m-%d %H:%M:%S.%f')
        time_line = time_line - time_delta

        now_string = time_line.strftime("%Y-%m-%d %H:%M:%S.%f")
        line_split[0] = now_string

        data_list.append(line_split)

    new_string_data = ''
    for string in data_list:
        new_string_data += string[0]+'\t'+string[1]+'\t'+string[2]

    with open(f'data/{output_filename}', 'w+') as file:
        file.writelines(new_string_data)


time_change(input_filename, output_filename, new_start_time)
