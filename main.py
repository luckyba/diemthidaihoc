# This is a sample Python script.
import subprocess
from threading import Thread
import re
import csv
from pynput import keyboard


class AsyncGet(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        data = []
        for sbd in range(2000001, 2000006):
            dir_row = {}
            #print("sbd: ", sbd)
            _title = _name = _birth_day_ = _scores = ""
            #print("title ", _title, " name ", _name, " birth day ", _birth_day_, " scores ", _scores)

            with open("student.txt", "w", encoding="utf-8") as f:
                student = self.get_data(sbd)
                _data = self.clean_data(student)
                f.write(_data)

            with open("student.txt", "r", encoding="utf-8") as f:
                count = 0
                for line in f:
                    count = count + 1
                    if count == 6:
                        _title = line
                    if count == 109:
                        _name = line
                    if count == 115:
                        _birth_day_ = line
                    if count == 121:
                        _scores = line

                #print("SBD :{} \n".format(sbd), "title ", _title, " name ", _name, " birth day ", _birth_day_, "scores ", _scores)
                dir_row['SBD'] = sbd
                _name = _name.strip().replace("\n", "")
                _birth_day_ = _birth_day_.strip().replace("\n", "")
                dir_row['Họ và tên'] = _name.split()
                dir_row['Năm Sinh'] = _birth_day_

                dir_row |= self.convert_score_to_value(score=_scores)

                print(dir_row)
            data.append(dir_row)
        print(" data ", len(data))
        self.save_to_csv_file(data)


    def get_data(self, sbd):
        cmd = "curl --data " + '"SoBaoDanh=0{}"'.format(sbd) + " http://diemthi.hcm.edu.vn/Home/Show"
        #print(cmd)
        student = subprocess.check_output(cmd)
        if not student:
            print("student none")
        return student.decode("utf-8")

    def clean_data(self, _data):
        cleaner = re.compile('<.*?>')
        _clean_data = re.sub(cleaner, '', _data)
        _clean_data = _clean_data.replace('&#192;', 'À')
        _clean_data = _clean_data.replace('&#193;', 'Á')
        _clean_data = _clean_data.replace('&#194;', 'Â')

        _clean_data = _clean_data.replace('&#200;', 'È')
        _clean_data = _clean_data.replace('&#201;', 'É')
        _clean_data = _clean_data.replace('&#202;', 'Ê')

        _clean_data = _clean_data.replace("&#204;", "Ì")
        _clean_data = _clean_data.replace("&#205;", "Í")

        _clean_data = _clean_data.replace("&#210;", "Ò")
        _clean_data = _clean_data.replace("&#211;", "Ó")
        _clean_data = _clean_data.replace("&#212;", "Ô")

        _clean_data = _clean_data.replace("&#217;", "Ù")
        _clean_data = _clean_data.replace("&#218;", "Ú")

        _clean_data = _clean_data.replace("&#221;", "Ý")

        _clean_data = _clean_data.replace("&#224;", "à")
        _clean_data = _clean_data.replace("&#225;", "á")
        _clean_data = _clean_data.replace("&#226;", "â")

        _clean_data = _clean_data.replace("&#232;", "è")
        _clean_data = _clean_data.replace("&#233;", "é")
        _clean_data = _clean_data.replace("&#234;", "ê")

        _clean_data = _clean_data.replace("&#236;", "ì")
        _clean_data = _clean_data.replace("&#237;", "í")

        _clean_data = _clean_data.replace("&#242;", "ò")
        _clean_data = _clean_data.replace("&#243;", "ó")
        _clean_data = _clean_data.replace("&#244;", "ô")

        _clean_data = _clean_data.replace("&#249;", "ù")
        _clean_data = _clean_data.replace("&#250;", "ú")

        _clean_data = _clean_data.replace("&#253;", "ý")

        # print("clean data ", _clean_data, test)
        return _clean_data


    def convert_score_to_value(self, score):
        toan = ngu_van = vat_ly = hoa_hoc = sinh_hoc = khtn = tieng_anh = gdcd = \
            lich_su = dia_ly = khxh = -1
        # print("score: ", score)
        _temp1 = list(score.split(" "))
        # print(" temp ", _temp1)
        _temp2 = []
        for v in _temp1:
            if v:
                _temp2.append(v)
                #print(v)
        # print("temp2 ", _temp2)
        leng = len(_temp2)
        for i in range(leng):
            #print("i ", i, " c[i] ", _temp2[i])
            if _temp2[i] == 'Toán:':
                toan = float(_temp2[i + 1])
                continue
            if _temp2[i] == 'Ngữ':
                ngu_van = float(_temp2[i + 2])
                continue
            if _temp2[i] == 'Vật':
                vat_ly = float(_temp2[i + 2])
                continue
            if _temp2[i] == 'Hóa':
                hoa_hoc = float(_temp2[i + 2])
                continue
            if _temp2[i] == 'Sinh':
                sinh_hoc = float(_temp2[i + 2])
                continue
            if _temp2[i] == 'KHTN:':
                khtn = float(_temp2[i + 1])
                continue
            if _temp2[i] == 'Anh:':
                tieng_anh = float(_temp2[i + 1])
                continue
            if _temp2[i] == 'Lịch':
                lich_su = float(_temp2[i + 2])
                continue
            if _temp2[i] == 'Địa':
                dia_ly = float(_temp2[i + 2])
                continue
            if _temp2[i] == 'GDCD':
                gdcd = float(_temp2[i + 1])
                continue
            if _temp2[i] == 'KHXH':
                khxh = float(_temp2[i + 1])
                continue

        # print("toan ", toan, " ngu van ", ngu_van, " Lich su ", lich_su, " dia ly ", dia_ly,
        #       " gdcd ", gdcd, " khxh ", khxh, " tieng anh ", tieng_anh, " vat ly ", vat_ly,
        #       " hoa hoc ", hoa_hoc, " sinh hoc ", sinh_hoc, " khtn ", khxh)

        score_dict = {'Toán': toan, 'Ngữ Văn': ngu_van, 'Vật lý': vat_ly, 'Hóa Học': hoa_hoc
            , 'Sinh Học': sinh_hoc, 'KHTN': khtn, 'Tiếng Anh': tieng_anh, 'Lịch Sử': lich_su
            , 'Địa Lý': dia_ly, 'GDCD': gdcd, 'KHXH': khxh}
        #print(score_dict)
        return score_dict

    def save_to_csv_file (self, data):
        print(data)
        # field name
        fields = ['SBD', 'Họ và tên', 'Năm Sinh', 'Toán', 'Ngữ Văn', 'Vật lý', 'Hóa Học', 'Sinh Học', 'KHTN', 'Tiếng Anh'
                  , 'Lịch Sử', 'Địa Lý', 'GDCD', 'KHXH']

        file_name = "list_hs.csv"

        # writing to csv file
        with open(file_name, 'w', encoding="utf-8") as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            writer.writerows(data)

        # def get_facebook ():
#     fb = subprocess.check_output("curl https://www.facebook.com/")
#     fb = fb.decode("utf-8")
#     cleaner = re.compile('<.*?>')
#     _clean_data = re.sub(cleaner, '', fb)
#     print(_clean_data)


if __name__ == '__main__':
    data = AsyncGet()
    data.start()
    print("run in foreground")
    data.join()

    #get_facebook()
