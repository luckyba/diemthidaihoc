# This is a sample Python script.
import subprocess
from threading import Thread
import re
import csv
import datetime
from pynput import keyboard


class AsyncGet(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.data = []
        for sbd in range(3000000, 3000020):
            dir_row = {}
            #print("sbd: ", sbd)
            _title = _name = _birth_day_ = _scores = ""
            #print("title ", _title, " name ", _name, " birth day ", _birth_day_, " scores ", _scores)

            student = self.get_data(sbd)
            _data = self.clean_data(student)

            dir_row['SBD'] = sbd
            _name = _name.strip().replace("\n", "")
            _birth_day_ = _birth_day_.strip().replace("\n", "")
            dir_row['Họ và tên'] = _name.split()
            dir_row['Năm Sinh'] = _birth_day_
            dir_row |= self.convert_score_to_value(data=_data)

            # print(dir_row)
            self.data.append(dir_row)
        # print(" data ", len(self.data), " data ", self.data)

    def get_data(self, sbd):
        print("before get_data", " current time ", datetime.datetime.now())

        cmd = "curl {}".format('"http://diemthi.24h.com.vn/?v_page=1&v_sbd=0{}&v_ten=&v_cum_thi=00"'.format(sbd))
        #print(cmd)
        print("before get_data 1", " current time ", datetime.datetime.now())

        student = subprocess.check_output(cmd)
        print("after get_data", " current time ", datetime.datetime.now())

        if not student:
            print("student none")
        return student

    def clean_data(self, _data):
        # print("before decode", " current time ", datetime.datetime.now())
        _data = _data.decode("utf-8")
        # print("before decode", " current time ", datetime.datetime.now())

        # print("clean to utf-8", _data)
        # print("before compile", " current time ", datetime.datetime.now())

        cleaner = re.compile('<.*?>')
        _clean_data = re.sub(cleaner, '', _data)
        # print("after compile", " current time ", datetime.datetime.now())

        _temp = list(_clean_data[9000:11000].replace(" ","").split("\n"))

        # index of sbd: 39
        # print("_temp", _temp, " len ", len(_temp))
        #_temp ['', '', '', '', '', '', '', 'KếtquảđiểmthiTHPTquốcgia2020', '', 'KHÔNGTÌMTHẤYDỮLIỆUĐIỂMTHICỦATHÍSINH',
        # 'TheoquyđịnhcủaBộGD&amp;ĐT,côngtácchấmthiTHPTquốcgianăm2020hoànthànhchậmnhấtvàongày13/7/2020đểcôngbốkếtquảthivào14/72020
        # .-->', '', '', '', '', '', '\t\tHướngdẫntracứuđiểmthiTHPT', '\t\t\tNămnay,phụhuynhvàcácemhọcsinhtrêncảnướccóthểdễdàngtracứuđiểmthiTHPTQuốcgia2020mộtcáchnhanhvàchínhxác.BộGD&amp
        # ;ĐTsẽcungcấpdữliệukếtquảđiểmthichocáccơquanbáochíđểđăngtảirộngrãi.&nbsp;', '', 'HướngdẫntracứuđiểmthiTHPTquốcgia2020theotên', '', '', 'Bước1:Truycậpvàotrangtracứuđiểmthihttp://diemthi.24h.com.vn/', 'Bước2:Tìmtheotênthísinh', 'Trêngiaodiệntìmkiếm,tạiô“Nhậphọvàtên”bạnnhậpvàoTên,haycảhọvàTên'
        # , 'Vídụcụmtừcóthểnhập:Hy,GiaHy,CaoGiaHy,NguyễnCaoGiaHy….', '', 'Bước3:Xemkếtquả',
        # 'SaukhinhậpTênvàoôcầntìmbạnnhấnvàonút“Xemkếtquả”hệthốngsẽtựđộngtìmkiếmcácthísinhthỏamãnTênđãđượcnhậpvàhiểnthịkếtquả', '', 'MộtsốchúýkhitracứuđiểmthiTHPTquốcgiabằngtên', '-Khinhậptênthìcácbạnkhôngnhậpcáckýtựđặcbiệtnhưlà:*,&amp;,%,$,@,#....Nhậpcáckýtựnàyhệthốngsẽkhôngchorakếtquảnhưmongmuốn', '-Tìmkiếmtheotêncóthểsẽranhiềuthísinhnêncóthểkếthợpvớiđiềukiệntìm“Tỉnhthành”sẽchorakếtquảchínhxáchơn', '-Tìmkiếmtheotêncóthểchoranhiềukếtquả,bạnsửdụngphântrangđểtìmkếtquảphíasauchophùhợp', '-BạnsửdụngNút“Hủytìm”đểthiếthủycácđiềukiệnTracứukhinhậpsai', '', '', '', 'HướngdẫntracứuđiểmthiTHPTqu']  len  39

        if len(_temp) > 50 and _temp[6] != '':
            # print("temp 1", _temp)
            _temp = _temp[40:52]
            # print(len(_temp), "\n", " sub data ", _temp)
            return _temp

        # print("clean data ", _clean_data)
        return ""


    def convert_score_to_value(self, data):
        if len(data) > 0:
            score_dict = {'Toán': float(data[1]) if data[1] != "" else -1
                , 'Ngữ Văn': float(data[2]) if data[2] != "" else -1
                , 'Tiếng Anh':float(data[3]) if data[3] != "" else -1
                , 'Vật lý': float(data[4]) if data[4] != "" else -1
                , 'Hóa Học': float(data[5]) if data[5] != "" else -1
                , 'Sinh Học': float(data[6]) if data[6] != "" else -1
                , 'KHTN': float(data[7]) if data[7] != "" else -1
                , 'Lịch Sử': float(data[8]) if data[8] != "" else -1
                , 'Địa Lý': float(data[9]) if data[9] != "" else -1
                , 'GDCD': float(data[10]) if data[10] != "" else -1
                , 'KHXH': float(data[11]) if data[11] != "" else -1}

            print(score_dict)
            # print("after convert_score_to_value", " current time ", datetime.datetime.now())

            return score_dict
        return ""

def save_to_csv_file (data):
    #print(data)
    # field name
    fields = ['SBD', 'Họ và tên', 'Năm Sinh', 'Toán', 'Ngữ Văn', 'Vật lý', 'Hóa Học', 'Sinh Học', 'KHTN', 'Tiếng Anh'
                  , 'Lịch Sử', 'Địa Lý', 'GDCD', 'KHXH']

    filename = "diemthi24h.csv"
    # writing to csv file
    with open(filename, 'w', encoding="utf-8") as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(data)


if __name__ == '__main__':
    asyndata = AsyncGet()
    asyndata.start()
    print("run in foreground", " current time ", datetime.datetime.now())
    asyndata.join()
    data = asyndata.data
    print( "current time after get data", datetime.datetime.now())
    save_to_csv_file(data)
    print( "current time after save to csv", datetime.datetime.now())
    #get_facebook()
