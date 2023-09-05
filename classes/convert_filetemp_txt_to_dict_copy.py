from classes.read_file import ReaderTxt


class ConverterTxtToDict:
    def __init__(self):
        self.list_dicts = []
        self.raw_data_list: list = []
        self.data_list: list = []

    def convert(self, data):
        temp_list = []
        long_string = ''
        for id, val in enumerate(data):
            line_list: list = val.split('\t')
            if line_list[2] == 'IRP_MJ_READ' and line_list[4] == 'STATUS_SUCCESS' and len(line_list[6]) > 2 and line_list[6].find('.') != 0:
                if line_list[6].rfind('.') == len(line_list[6]) - 1:
                    line_list[6] = line_list[6].rstrip(line_list[6][-1])

                try:
                    date_time = line_list[1]
                    temperature = float(line_list[6])
                    # print(date_time, temperature, '\n' , line_list[6], 'len = ', len(line_list[6]))
                    long_string += str(temperature)

                    # self.raw_data_list.append([date_time, temperature])
                except Exception as e:
                    # print(line_list, e)
                    pass
        print(long_string)
        for i in range(0,len(long_string),4):
            print(long_string[i:i+4])

        summ = [0]
        counter = 1
        for id, val in enumerate(self.raw_data_list):
            if len(self.raw_data_list) - 1 > id:
                val_next = self.raw_data_list[id + 1]
            if val_next[0] == val[0]:
                counter += 1
                summ = [summ[0] + val_next[1]]
            else:
                date_time = val[0]
                self.data_list.append([date_time, summ[0] / counter])
                counter = 1
                summ = [val[1]]
        result_dict = {}
        for id, val in enumerate(self.data_list):
            result_dict[val[0].replace("/", "-")] = {"T": val[1]}
        return result_dict