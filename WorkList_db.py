import sqlite3
import sys
import datetime
import os
import shutil
import sys
import csv

db_con = "C:\\WorkList\\WorkList.db"  ## 경로 수정


class Singleton(type):  # Type을 상속받음
    __instances = {}  # 클래스의 인스턴스를 저장할 속성

    def __call__(cls, *args, **kwargs):  # 클래스로 인스턴스를 만들 때 호출되는 메서드
        if cls not in cls.__instances:  # 클래스로 인스턴스를 생성하지 않았는지 확인
            cls.__instances[cls] = super().__call__(*args, **kwargs)  # 생성하지 않았으면 인스턴스를 생성하여 해당 클래스 사전에 저장
            # print("인스턴스 생성 확인")
        # print("인스턴스 활용중 ~")
        # print(cls)
        return cls.__instances[cls]  # 클래스로 인스턴스를 생성했으면 인스턴스 반환


class WorkList_db_class(metaclass=Singleton):
    bcd_file_path = "C:\\TCW"  # 기본 백업 폴더(없을 경우 생성)

    # Info_plrn 테이블에 plrn 데이터 입력 후 ID 생성
    def Input_plrn_data(self, date, protocol_name, smp_num, plate_type, cap_type, ctrl_seq, pcr_bcd, bcd_list,
                        pcr_plate, dwp, extraction_bcd):
        self.date = date
        self.protocol_name = protocol_name
        self.smp_num = smp_num
        self.plate_type = plate_type
        self.cap_type = cap_type
        self.ctrl_seq = ctrl_seq
        self.pcr_bcd = pcr_bcd
        self.bcd_list = bcd_list
        self.pcr_plate = pcr_plate
        self.dwp = dwp
        self.extraction_bcd = extraction_bcd

        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute('''
                    insert into Info_plrn(Date, Protocol_Name, Smp_Num, Plate_Type, Cap_Type, Ctrl_Seq, PCR_bcd, BarcodeList, PCRplate_bcd, DWP_bcd, Extraction_bcd)
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                    , (self.date, self.protocol_name, self.smp_num, self.plate_type, self.cap_type, self.ctrl_seq,
                       self.pcr_bcd, self.bcd_list, self.pcr_plate, self.dwp, self.extraction_bcd))
        conn.commit()
        cur.execute("select ID from Info_plrn where Date = (%s)" % ("'" + self.date + "'"))
        id_plrn = cur.fetchall()

        cur.execute("update check_plrn set plrn_id = (%d)" % id_plrn[0][0])
        conn.commit()

        cur.close()
        conn.close()
        return id_plrn[0][0]

    # Info_smp 테이블에 샘플 바코드 정보 입력
    def Input_sample_data(self, smp_bcd, id_plrn):
        self.smp_bcd = smp_bcd
        self.id_plrn = id_plrn

        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        for i in range(len(self.smp_bcd)):
            cur.execute("insert into Info_smp(ID, Smp_bcd) values(?, ?)", (self.id_plrn, str(self.smp_bcd[i])))
        conn.commit()
        cur.close()
        conn.close()

    def encrypt(self, raw):
        temp = 10
        ret = ''
        for char in raw:
            ret += chr(ord(char) + temp)
        return ret

    def decrypt(self, raw):
        ret = ''
        temp = 10
        for char in raw:
            ret += chr(ord(char) - temp)
        return ret

    # Info_PCR 테이블에 PCR 바코드 정보 입력
    def PCR_test_count(self, pcr_bcd, test_cnt, pcr_cnt):
        self.pcr_bcd = pcr_bcd
        if self.pcr_bcd == "Hidden Barcode":
            return str(100)
        else:
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()
            try:
                cur.execute("select CH from Info_PCR where LJ = (%s)" % ("'" + self.pcr_bcd + "'"))
                test_count = cur.fetchall()
                if test_count == []:  # 새 PCR 시약 바코드인 경우 데이터 insert
                    cur.execute("insert into Info_PCR(LJ, CH, Tommy) values(?, ?, ?)",
                                (self.pcr_bcd, test_cnt, pcr_cnt))
                    conn.commit()
                    cur.execute("select CH from Info_PCR where LJ = (%s)" % ("'" + self.pcr_bcd + "'"))
                    test_count = cur.fetchall()
            except:
                pass
            test_pcr_cnt = self.decrypt(test_count[0][0])
            cur.close()
            conn.close()
            return str(test_pcr_cnt)

    # Info_Extraction 테이블에 추출시약 바코드 정보 입력
    def PCR_Extraction_count(self, Extraction_bcd, extraction_cnt, pcr_cnt):
        self.Extraction_bcd = Extraction_bcd
        if self.Extraction_bcd == "Hidden Barcode":
            return str(96)
        else:
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()
            try:
                cur.execute("select CH from Info_Extraction where LJ = (%s)" % ("'" + self.Extraction_bcd + "'"))
                test_count = cur.fetchall()
                if test_count == []:
                    cur.execute("insert into Info_Extraction(LJ, CH, Tommy) values(?, ?, ?)",
                                (self.Extraction_bcd, extraction_cnt, pcr_cnt))
                    conn.commit()
                    cur.execute("select CH from Info_Extraction where LJ = (%s)" % ("'" + self.Extraction_bcd + "'"))
                    test_count = cur.fetchall()
            except:
                pass
            test_pcr_cnt = self.decrypt(test_count[0][0])
            cur.close()
            conn.close()
            return str(test_pcr_cnt)

    # PCR 시약 사용시 test count 차감
    def Use_PCR(self, pcr_bcd, test_count):
        self.pcr_bcd = pcr_bcd
        self.test_count = str(test_count)
        if self.pcr_bcd == "Hidden Barcode":
            return
        else:
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()
            pcr_cnt = self.Sel_test_cnt(pcr_bcd)
            self.test_count = int(pcr_cnt) - int(test_count)
            test_count = self.encrypt(str(self.test_count))
            cur.execute("update Info_PCR set CH = (%s) where LJ = (%s)" % (
                "'" + test_count + "'", "'" + self.pcr_bcd + "'"))
            conn.commit()

            pcr_cnt = self.Sel_PCR_cnt(pcr_bcd)
            pcr_cnt = int(pcr_cnt) - 1
            pcr_cnt = self.encrypt(str(pcr_cnt))
            cur.execute("update Info_PCR set Tommy = (%s) where LJ = (%s)" % (
                "'" + pcr_cnt + "'", "'" + self.pcr_bcd + "'"))
            conn.commit()
            cur.close()
            conn.close()

    # 추출시약 사용시 Extraction count 차감
    def Use_Extraction_Reagent(self, Extraction_bcd, test_count):
        self.Extraction_bcd = Extraction_bcd
        self.test_count = str(test_count)
        if self.Extraction_bcd == "Hidden Barcode":
            return
        else:
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()
            extraction_cnt = self.Sel_Extraction_cnt(Extraction_bcd)
            self.test_count = int(extraction_cnt) - int(test_count)
            test_count = self.encrypt(str(self.test_count))
            cur.execute("update Info_Extraction set CH = (%s) where LJ = (%s)" % (
                "'" + test_count + "'", "'" + self.Extraction_bcd + "'"))
            conn.commit()

            extraction_use = self.Sel_Extraction_Use(Extraction_bcd)
            extraction_use = int(extraction_use) - 1
            extraction_use = self.encrypt(str(extraction_use))
            cur.execute("update Info_Extraction set Tommy = (%s) where LJ = (%s)" % (
                "'" + extraction_use + "'", "'" + self.Extraction_bcd + "'"))
            conn.commit()
            cur.close()
            conn.close()

    # Pre-Nat ll 장비 DataBase 초기세팅 Flag / 0 : 초기세팅 1 : 세팅완료
    def Show_Flag(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("SELECT DB_Setup_Flag FROM Monitor")
        DB_info = cur.fetchall()
        cur.close()
        conn.close()
        return DB_info[0][0]

    # Pre-Nat ll 장비 DataBase 초기세팅 Flag 완료후 업데이트
    def Update_Flag(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("update Monitor set DB_Setup_Flag = 1")
        cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

    # 현재 감시하고 있는 파일 경로를 데이터베이스에서 가져옴
    def show_path(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("SELECT Path_monitor FROM Monitor")
        b_info = cur.fetchall()
        cur.close()
        conn.close()
        return b_info

    # 현 바코드 파일경로를 데이터베이스에서 가져옴
    def Sel_Bcd(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("SELECT Inst_bcd FROM Monitor")
        b_info = cur.fetchall()
        cur.close()
        conn.close()
        return b_info

    # 해당 PCR Reagent PCR 정보를 받아옴
    def Sel_Protocol_Num(self, Protocol_Name):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("select Protocol_Num from Temp where Protocol_Name = (%s)" % ("'" + Protocol_Name + "'"))
        b_info = cur.fetchall()
        cur.close()
        conn.close()
        return b_info

    # 해당 PCR Reagent 사용 횟수를 가져옴.
    def Sel_PCR_cnt(self, PCR_bcd):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("SELECT Tommy FROM Info_PCR where LJ = (%s)" % ("'" + PCR_bcd + "'"))
        b_info = cur.fetchall()
        if b_info == []:
            return -1
        cur.close()
        conn.close()
        pcr_cnt = self.decrypt(b_info[0][0])
        return pcr_cnt

    # 해당 PCR Reagent 사용 갯수를 가져옴.
    def Sel_test_cnt(self, PCR_bcd):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("SELECT CH FROM Info_PCR where LJ = (%s)" % ("'" + PCR_bcd + "'"))
        b_info = cur.fetchall()
        cur.close()
        conn.close()
        test_cnt = self.decrypt(b_info[0][0])
        return test_cnt

    # 해당 Extraction Reagent 사용 갯수를 가져옴.
    def Sel_Extraction_Use(self, Extraction_bcd):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("SELECT Tommy FROM Info_Extraction where LJ = (%s)" % ("'" + Extraction_bcd + "'"))
        b_info = cur.fetchall()
        cur.close()
        conn.close()
        pcr_cnt = self.decrypt(b_info[0][0])
        return pcr_cnt

    # 해당 Extraction Reagent 사용 횟수를 가져옴.
    def Sel_Extraction_cnt(self, Extraction_bcd):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("SELECT CH FROM Info_Extraction where LJ = (%s)" % ("'" + Extraction_bcd + "'"))
        b_info = cur.fetchall()
        cur.close()
        conn.close()
        test_cnt = self.decrypt(b_info[0][0])
        return test_cnt

    # 현 바코드 파일경로를 실시간으로 변경시켜줌
    def update(self, Barcod_List):
        self.bcd_list = Barcod_List
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("update Monitor set Inst_bcd = (%s)" % ("'" + self.bcd_list + "'"))
        cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return 1

    # plrn 파일 생성
    def make_plrn(self, id_plrn, Control_Count):
        try:
            self.id_plrn = str(id_plrn)
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()

            # plrn 파일 생성에 필요한 프로토콜 및 샘플 정보를 불러온다.
            cur.execute("select * from Info_plrn where ID = (%s)" % ("'" + self.id_plrn + "'"))
            info_plrn = cur.fetchall()

            assay_name = info_plrn[0][2]  # item(assay) 이름
            inst_name = "PreNATII"  # 장비 이름(PreNATII 고정)
            date = info_plrn[0][1]  # 날짜
            plate_type = info_plrn[0][4]  # Plate 종류
            cap_type = info_plrn[0][5]  # Cap 종류
            plate_bcd = info_plrn[0][9]  # PCR Plate 바코드
            pcr_bcd = info_plrn[0][7]  # PCR 시약 바코드
            dwp_bcd = info_plrn[0][10]  # DWP 바코드
            extract_bcd = info_plrn[0][11]  # Extraction 시약 바코드
            patient_list = []  # patient 리스트
            separate = 1  # separate 수

            # 해당 프로토콜의 .prcl 파일 경로, 형광값 불러오기
            cur.execute(
                "select Protocol_Path, Light from Info_protocol where Protocol_Name = (%s)" % (
                            "'" + assay_name + "'"))
            info_protocol = cur.fetchall()

            # Channel 값에 맞게 fluorophores 설정
            fluorophores = [""] * 5  # fluorophores 리스트
            list_fluorophores = info_protocol[0][1].split(",")
            for value in list_fluorophores:
                temp = self.get_channel(value)
                fluorophores[temp[0][0] - 1] = temp[0][1]

            cur.execute("select Smp_bcd from Info_smp where ID = (%s)" % ("'" + self.id_plrn + "'"))
            info_smp = cur.fetchall()

            smp_num = info_plrn[0][3]  # 샘플 개수
            control = info_plrn[0][6]  # NC, PC 순서
            ctrl_cnt = Control_Count - 1  # control 개수(NC 1개 + PC n개)

            smp_list = []
            for i in range(smp_num):
                smp_list.append(info_smp[i][0])
            if control == "NC, PC":
                smp_list.append("NC")
                for j in range(ctrl_cnt):  # PC count만큼 추가
                    smp_list.append(f"PC{j + 1}")
            elif control == "PC, NC":
                for j in range(ctrl_cnt):  # PC count만큼 추가
                    smp_list.append(f"PC{j + 1}")
                smp_list.append("NC")

            # patient_name 정보
            for sep in range(separate):
                for i in range(len(smp_list)):
                    if "NC" not in smp_list[i] and "PC" not in smp_list[i]:
                        patient_list.append(f"'{smp_list[i]}'")
            patient_name = ",".join(map(str, patient_list))

            # plrn 파일 이름
            file_name = ""
            if dwp_bcd == "" and plate_bcd == "":  # DWP, PCR Plate 바코드 스캔 안 한 경우
                file_name = f"plrn, {inst_name}, {date}, {assay_name}.plrn"
            elif dwp_bcd != "" and plate_bcd == "":  # DWP 바코드만 스캔
                file_name = f"plrn, {inst_name}, {date}, {assay_name}, {dwp_bcd}.plrn"
            elif dwp_bcd == "" and plate_bcd != "":  # PCR Plate 바코드만 스캔
                file_name = f"plrn, {inst_name}, {date}, {assay_name}, {plate_bcd}.plrn"
            elif dwp_bcd != "" and plate_bcd != "":  # DWP, PCR Plate 바코드 스캔
                file_name = f"plrn, {inst_name}, {date}, {assay_name}, {dwp_bcd}, {plate_bcd}.plrn"

            cur.execute("select * from Path_plrn")  # Option에서 설정한 plrn 경로
            dir_plrn = cur.fetchall()
            dir_plrn_1 = dir_plrn[0][0].replace("/", "\\") + f"\\{assay_name}\\" + file_name
            self.make_dir(dir_plrn[0][0] + f"\\{assay_name}")  # 설정한 경로에 {프로토콜 이름} 폴더 생성

            plrn_data = [
                ['Plate Header', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', ''],
                ['Field', 'Data', '', 'Instructions', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', ''],
                ['Version', '1', '', 'Do not modify this field.', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['Plate Size', '96', '', 'Do not modify this field.', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['Plate Type', 'BR White', '', 'Allowed values (BR White BR Clear)', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['Scan Mode', 'All Channels', '', 'Allowed values (SYBR/FAM Only All Channels FRET)', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['Units', 'micromoles', '',
                 'Allowed values (copy number fold dilution micromoles nanomoles picomoles femtomoles attomoles milligrams micrograms nanograms picograms femtograms attograms percent)',
                 '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 ''],
                ['Run ID', '', '', 'Short description or bar code with no new line or commas', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['Run Notes',
                 f"'runNoteVersion':('1.1'),'plateBarcode':('{plate_bcd}'),'plateType':('{plate_type}'),'capFilm':('{cap_type}'),'ExtractBarcode':('{extract_bcd}'),'PCRBarcodeList':('{pcr_bcd}'),'PatientNameList':({patient_name}),'userId':(''),'userName':(''),'ClotSampleWell':(),'dwpBarcode':('{dwp_bcd}')",
                 '', 'Run description with no new line or commas', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['Run Protocol', f'C:\\Seegene\\Protocol\\{info_protocol[0][0]}', '', 'Protocol File Name', '', '', '',
                 '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['Data File', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', ''],
                ['TBD', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', ''],
                ['Plate Data', '', 'Do not modify this field.', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['Well', 'Ch1 Dye', 'Ch2 Dye', 'Ch3 Dye', 'Ch4 Dye', 'Ch5 Dye', 'FRET', 'Sample Type', 'Sample Name',
                 'Ch1 Target Name', 'Ch2 Target Name', 'Ch3 Target Name', 'Ch4 Target Name', 'Ch5 Target Name',
                 'FRET Target Name', 'Biological Set Name', 'Replicate', 'Ch1 Quantity', 'Ch2 Quantity', 'Ch3 Quantity',
                 'Ch4 Quantity', 'Ch5 Quantity', 'FRET Quantity', 'Well Note', 'Ch1 Well Color', 'Ch2 Well Color',
                 'Ch3 Well Color', 'Ch4 Well Color', 'Ch5 Well Color', 'FRET Well Color']
            ]

            #  sample 및 control Position 정보
            pos = 1
            if separate == 2:
                pos = 6
            elif separate == 3:
                pos = 4
            plt_pos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            for sep in range(separate):
                for i in range(len(smp_list)):
                    if "NC" not in smp_list[i] and "PC" not in smp_list[i]:
                        plrn_data.append(
                            [f'{str(plt_pos[i % 8]) + str((i // 8) + 1 + (sep * pos)).zfill(2)}', f'{fluorophores[0]}',
                             f'{fluorophores[1]}', f'{fluorophores[2]}', f'{fluorophores[3]}', f'{fluorophores[4]}', '',
                             'Unknown', f'\'{smp_list[i]}\'', '', '', '', '', '', '0_1_0', '', '', '', '', '', '', '',
                             '', f'{assay_name}', '', '', '', '', '', ''])
                    elif "NC" in smp_list[i]:
                        plrn_data.append(
                            [f'{str(plt_pos[i % 8]) + str((i // 8) + 1 + (sep * pos)).zfill(2)}', f'{fluorophores[0]}',
                             f'{fluorophores[1]}', f'{fluorophores[2]}', f'{fluorophores[3]}', f'{fluorophores[4]}', '',
                             'Negative Control', f'\'{smp_list[i]}\'', '', '', '', '', '', '0_1_0', '', '', '', '', '',
                             '', '', '', f'{assay_name}', '', '', '', '', '', ''])
                    elif "PC" in smp_list[i]:
                        plrn_data.append(
                            [f'{str(plt_pos[i % 8]) + str((i // 8) + 1 + (sep * pos)).zfill(2)}', f'{fluorophores[0]}',
                             f'{fluorophores[1]}', f'{fluorophores[2]}', f'{fluorophores[3]}', f'{fluorophores[4]}', '',
                             'Positive Control', f'\'{smp_list[i]}\'', '', '', '', '', '', '0_1_0', '', '', '', '', '',
                             '', '', '', f'{assay_name}', '', '', '', '', '', ''])

            f_plrn = open(dir_plrn_1, "w", newline='')
            writer = csv.writer(f_plrn)
            writer.writerows(plrn_data)
            f_plrn.close()

            # plrn 파일 생성 경로 2
            add_path_2 = dir_plrn[0][1]
            if add_path_2 != "":
                add_path_2 = add_path_2.replace("/", "\\") + f"\\{assay_name}"
                self.make_dir(add_path_2)
                add_path_2 = add_path_2 + f"\\" + file_name
                shutil.copy(dir_plrn_1, add_path_2)

            # plrn 파일 생성 경로 3
            add_path_3 = dir_plrn[0][2]
            if add_path_3 != "":
                add_path_3 = add_path_3.replace("/", "\\") + f"\\{assay_name}"
                self.make_dir(add_path_3)
                add_path_3 = add_path_3 + f"\\" + file_name
                shutil.copy(dir_plrn_1, add_path_3)

            cur.execute("update Monitor set (Path_plrn, Use_plrn) = ((%s), (%d))" % ("'" + dir_plrn_1 + "'", 0))
            conn.commit()
            cur.execute("select Path_plrn from Monitor")
            cur.close()
            conn.close()

        except Exception as err:
            print(err)
            print("make_plrn 에러")

    # plrn 파일이 생성되는 경로를 DB에 update
    def set_dir(self, path, i):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        self.path = path
        if i == 1:
            cur.execute("update Path_plrn set Path_1 = (%s)" % ("'" + self.path + "'"))
        elif i == 2:
            cur.execute("update Path_plrn set Path_2 = (%s)" % ("'" + self.path + "'"))
        elif i == 3:
            cur.execute("update Path_plrn set Path_3 = (%s)" % ("'" + self.path + "'"))
        elif i == 4:
            cur.execute("update Monitor set Path_worklist = (%s)" % ("'" + self.path + "'"))
        elif i == 5:
            cur.execute("update Monitor set Path_inst = (%s)" % ("'" + self.path + "'"))
        conn.commit()
        cur.close()
        conn.close()

    # 생성된 Inst 바코드 파일을 불러오면서 프로토콜 이름과 기본 setting값을 Temp 테이블에 입력
    def Inst_bcd_path(self, bcd_path):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("update Monitor set Inst_bcd = (%s)" % ("'" + bcd_path + "'"))
        conn.commit()

        temp = bcd_path.split("\\")
        protocol_name = temp[-2].split("_", 1)

        if len(protocol_name) == 1:
            cur.execute("select Protocol_Name from Temp where Protocol_Name = (%s)" % ("'" + protocol_name[0] + "'"))
        else:
            cur.execute("select Protocol_Name from Temp where Protocol_Name = (%s)" % ("'" + protocol_name[1] + "'"))

        name = cur.fetchall()
        if name == []:
            if len(protocol_name) == 1:
                cur.execute(
                    "insert into Temp(Protocol_Name, Plate_Type, Cap_Type, Control, Use_bcd) values(?, ?, ?, ?, ?)",
                    (protocol_name[0], "Plate", "Cap", "NC, PC", "PCR Plate and DWP"))
            else:
                cur.execute(
                    "insert into Temp(Protocol_Name, Plate_Type, Cap_Type, Control, Use_bcd) values(?, ?, ?, ?, ?)",
                    (protocol_name[1], "Plate", "Cap", "NC, PC", "PCR Plate and DWP"))

            conn.commit()
        cur.close()
        conn.close()

    # Make 클릭시 Temp 테이블에 setting값 저장
    def save_Temp(self, protocol, plate_type, cap_type, ctrl_seq, use_bcd):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute(
            "update Temp set (Plate_Type, Cap_Type, Control, Use_bcd) = ((%s), (%s), (%s), (%s)) where Protocol_Name = (%s)" % (
                "'" + plate_type + "'", "'" + cap_type + "'", "'" + ctrl_seq + "'", "'" + use_bcd + "'",
                "'" + protocol + "'"))
        conn.commit()
        cur.close()
        conn.close()

    # 프로토콜 기본 setting값 불러오기
    def load_setting(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("select Inst_bcd from Monitor")
        inst_bcd_path = cur.fetchall()
        temp = inst_bcd_path[0][0].split("\\")
        protocol_name = temp[-2].split("_", 1)
        if len(protocol_name) == 1:
            cur.execute("select * from Temp where Protocol_Name = (%s)" % ("'" + protocol_name[0] + "'"))
        else:
            cur.execute("select * from Temp where Protocol_Name = (%s)" % ("'" + protocol_name[1] + "'"))
        setting_data = cur.fetchall()
        cur.execute("select Protocol_Name from Temp")
        protocol_list = cur.fetchall()
        cur.close()
        conn.close()
        return setting_data[0][0], setting_data[0][1], setting_data[0][2], setting_data[0][3], setting_data[0][4], protocol_list

    # 이전에 설정한 plrn 파일 생성 경로를 불러온다.
    def display_path(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("select * from Path_plrn")
        path = cur.fetchall()
        cur.execute("select Path_worklist, Path_inst from Monitor")
        bcd_path = cur.fetchall()
        cur.close()
        conn.close()
        return path, bcd_path

    # PerkinElmer 실행경로를 데이터베이스에서 가져옴
    def show_PE_path(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("SELECT PE_path FROM Monitor")
        b_info = cur.fetchall()
        cur.close()
        conn.close()
        return b_info

    def Sel_Protocol(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("select Protocol_Name from Temp")
        protocol_list = cur.fetchall()
        cur.close()
        conn.close()
        return protocol_list

    # WorkList, Instrument 바코드 파일을 생성한다.
    def Create_barcode(self, id_plrn, bcd_list, dir_csv, worklist_name, csv_signal):
        worklist_dir = self.bcd_file_path + "\\WorkList"
        Inst_dir = self.bcd_file_path + "\\Instrument Barcode"
        Plrn_dlr = self.bcd_file_path + "\\WorkList\\Plrn"
        self.make_dir(worklist_dir)
        self.make_dir(Inst_dir)
        self.make_dir(Plrn_dlr)

        self.id_plrn = str(id_plrn)
        date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("select Path_plrn, Inst_bcd, Path_worklist, Path_inst from Monitor")
        info = cur.fetchall()
        temp = info[0][0].split("\\")
        protocol_name = temp[-2]
        temp_worklist = info[0][2]
        temp_worklist = temp_worklist.replace("/", "\\")
        temp_inst = info[0][3]
        temp_inst = temp_inst.replace("/", "\\")

        shutil.copy(info[0][1], Inst_dir + f"\\{self.id_plrn}_{date}_{protocol_name}.txt")  # Instrument 바코드 파일 복사
        if temp_inst != self.bcd_file_path:
            self.make_dir(temp_inst + "\\Instrument Barcode")
            shutil.copy(info[0][1],
                        temp_inst + "\\Instrument Barcode" + f"\\{self.id_plrn}_{date}_{protocol_name}.txt")

        if bcd_list != [] and csv_signal == 0:  # WorkList 파일이 없는 경우 .txt 파일 생성
            pos_1 = ['A', 'B', 'C', 'D', 'E', 'F']
            f = open(worklist_dir + f"\\{self.id_plrn}_{date}_{protocol_name}.txt", 'w')
            header = "SEQ\tPOS\tCODE\n"
            f.write(header)
            for seq in range(len(bcd_list)):
                pos = str(pos_1[(seq) // 16]) + str(seq - (pos_1.index(pos_1[(seq) // 16]) * 16) + 1)
                code = bcd_list[seq]
                data = f"{seq + 1}\t{pos}\t{code}\n"
                f.write(data)
            f.close()
            cur.close()
            conn.close()
            if temp_worklist != self.bcd_file_path:
                self.make_dir(temp_worklist + "\\WorkList")
                shutil.copy(worklist_dir + f"\\{self.id_plrn}_{date}_{protocol_name}.txt",
                            temp_worklist + "\\WorkList" + f"\\{self.id_plrn}_{date}_{protocol_name}.txt")

        elif bcd_list != [] and csv_signal == 1:  # WorkList 파일이 있는 경우 파일 복사
            shutil.copy(dir_csv, worklist_dir + f"\\{self.id_plrn}_{date}_{protocol_name}_{worklist_name}.csv")
            if temp_worklist != self.bcd_file_path:
                self.make_dir(temp_worklist + "\\WorkList")
                shutil.copy(dir_csv,
                            temp_worklist + "\\WorkList" + f"\\{self.id_plrn}_{date}_{protocol_name}_{worklist_name}.csv")

    # 샘플 정보 사용 후 삭제
    def delete_bcd(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("delete from Info_smp")
        conn.commit()
        cur.close()
        conn.close()

    # 디렉터리 없으면 생성
    def make_dir(self, dir):
        try:
            if not (os.path.isdir(dir)):
                os.makedirs(os.path.join(dir))
        except OSError as e:
            print(e)

    # csv load하면 해당 경로 저장
    def save_dir_csv(self, path_csv):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("update Monitor set Path_csv = (%s)" % ("'" + path_csv + "'"))
        conn.commit()
        cur.close()
        conn.close()

    # csv load 버튼누르면 저장한 경로를 불러온다.
    def open_dir_csv(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("select Path_csv from Monitor")
        dir_csv = cur.fetchall()
        cur.close()
        conn.close()
        return dir_csv[0][0]

    # 설명 : Fluorophores Channel 값 불러오기
    # 작성자 : 황채환
    # 날짜 : 2022/03/14
    def get_channel(self, fluorophores):
        try:
            self.fluorophores = fluorophores

            conn = sqlite3.connect(db_con)
            cur = conn.cursor()

            cur.execute("select * from Fluorophores_Info where Fluorophores = (%s)" % ("'" + fluorophores + "'"))
            fluorophores_info = cur.fetchall()

            cur.close()
            conn.close()
            return fluorophores_info

        except Exception as err:
            print(err)
            print("db.get_channel 에러")

    # 설명 : plrn 파일 생성 여부 flag 값 get(1이면 plrn 생성 가능)
    # 작성자 : 황채환
    # 날짜 : 2022/03/15
    def get_plrn_flag(self):
        try:
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()

            cur.execute("select Plrn_Flag from Monitor")
            plrn_flag = cur.fetchall()

            cur.close()
            conn.close()
            return plrn_flag[0][0]

        except Exception as err:
            print(err)
            print("db.get_plrn_flag 에러")

    # 설명 : Control Count set
    # 작성자 : 황채환
    # 날짜 : 2022/03/15
    def set_control_count(self, control_count):
        try:
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()

            cur.execute("update check_plrn set control_count = (%d)" % control_count)
            conn.commit()

            cur.close()
            conn.close()

        except Exception as err:
            print(err)
            print("db.set_control_count 에러")

    # 설명 : plrn ID, Control Count get
    # 작성자 : 황채환
    # 날짜 : 2022/03/15
    def get_check_plrn(self):
        try:
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()

            cur.execute("select plrn_id from check_plrn")
            check_plrn = cur.fetchall()

            cur.close()
            conn.close()
            return check_plrn[0][0]

        except Exception as err:
            print(err)
            print("db.get_check_plrn 에러")

    # 현 One Step인지, PCR Setup인지 실시간으로 변경시켜줌
    def Protocol_State(self, State):
        State = int(State)
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("update Monitor set Plrn_Flag = (%d)" % (State))
        conn.commit()
        cur.close()
        conn.close()

    # 이전 바코드 파일경로를 업데이트
    def Previous_bcd_path(self, bcd_path):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("update Monitor set Previous_Path = (%s)" % ("'" + bcd_path + "'"))
        conn.commit()
        cur.close()
        conn.close()

    # 이전 바코드 파일경로를 데이터베이스에서 가져옴
    def Previous_Sel_Bcd(self):
        conn = sqlite3.connect(db_con)
        cur = conn.cursor()
        cur.execute("SELECT Previous_Path FROM Monitor")
        b_info = cur.fetchall()
        cur.close()
        conn.close()
        return b_info[0][0]
