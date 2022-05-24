import sqlite3

db_job = "C:\\WorkList\\PreNATII_Jobs.db3"

class Singleton(type):  # Type을 상속받음
    __instances = {}  # 클래스의 인스턴스를 저장할 속성

    def __call__(cls, *args, **kwargs):  # 클래스로 인스턴스를 만들 때 호출되는 메서드
        if cls not in cls.__instances:  # 클래스로 인스턴스를 생성하지 않았는지 확인
            cls.__instances[cls] = super().__call__(*args, **kwargs)  # 생성하지 않았으면 인스턴스를 생성하여 해당 클래스 사전에 저장
            # print("인스턴스 생성 확인")
        # print("인스턴스 활용중 ~")
        # print(cls)
        return cls.__instances[cls]  # 클래스로 인스턴스를 생성했으면 인스턴스 반환

class Job_DataBase_class(metaclass=Singleton):
    job_name = ""
    job_Id = 0
    MOM_Id = 0
    EM_Id = 0
    Water_Id = 0
    MM_Id = 0
    LB_Id = 0
    BB_Id = 0
    WA_Id = 0
    WB_Id = 0
    WE_Id = 0
    WH_Id = 0
    EB_Id = 0
    PK_Id = 0
    Bead_Id = 0
    IC_Id = 0
    Std_Id = 0
    Smp_Id = 0

    # Jobs.db3 테이블 데이터 삭제
    def delete_protocol(self):
        conn = sqlite3.connect(db_job)
        cur = conn.cursor()

        conn.execute('DELETE FROM "main"."Job"')
        conn.execute('DELETE FROM "main"."DbCarrier"')
        conn.execute('DELETE FROM "main"."JobReaInfo"')
        conn.execute('DELETE FROM "main"."JobReaBlendProportion"')
        conn.execute('DELETE FROM "main"."JobReaInfoLoc"')
        conn.execute('DELETE FROM "main"."JobSmpItem"')
        conn.execute('DELETE FROM "main"."JobStep"')

        conn.commit()
        cur.close()
        conn.close()
        return

    # Job 추가
    def Job(self):
        conn = sqlite3.connect(db_job)
        cur = conn.cursor()

        cur.execute('''
        INSERT INTO "main"."Job" ("Name", "Description", "Ver", "HeadType", "VoltageMagnet", "RefCount", "QcCount", "TestItemCount", "StdContainerType", 
        "QcContainerType", "ReagentLotNumber", "QcLotNumber", "QcSource", "PcrPlateCount", "HeaterTypeValue", "HeaterContainerType", "OutputQcBarcode", "MixedTestCount", 
        "MixedTestVolume", "SharePcrPlateItemCount", "IsShareSampleTemplate", "IsNeedCooling", "IsNeedCheckReagent", "RefPosition", "ControlPosition", "IsStdDirectToPCR", 
        "IsShareControl", "IsReagentHeating") 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        , (self.job_name, None, '1', '2', '0.0', '2', '0', '1', '3', '3', None, None, None, '1', '2', '0', '0', '0', '0.0', '0', '0', '0', '0', '1', '1', '1', '0', '0'))
        conn.commit()

        cur.execute("select * from Job where Name = (%s)" % ("'" + self.job_name + "'"))
        protocol_Info = cur.fetchall()
        cur.close()
        conn.close()
        self.job_Id = protocol_Info[0][0]
        return

    # DbCarrier 추가
    def DbCarrier(self):
        conn = sqlite3.connect(db_job)
        cur = conn.cursor()

        tuple_carrier = (
            ('TipCarrier', '0', '0', '2', '0', self.job_Id),
            ('TipCarrier', '1', '0', '2', '0', self.job_Id),
            ('TipCarrier', '2', '0', '1', '0', self.job_Id),
            ('TipCarrier', '3', '0', '1', '0', self.job_Id),
            ('NewWshCarrier', '4', '10', '0', '0', self.job_Id),
            ('ReaCarrier', '5', '8', '0', '0', self.job_Id),
            ('TipCarrier', '6', '0', '3', '0', self.job_Id),
            ('StdCarrier', '7', '1', '0', '0', self.job_Id),
            ('HotCarrier', '8', '6', '2', '0', self.job_Id),
            ('EmpCarrier', '9', '4', '0', '1', self.job_Id),
            ('EmpCarrier', '10', '4', '0', '0', self.job_Id),
            ('PcrCarrier', '11', '2', '0', '0', self.job_Id),
            ('EmpCarrier', '12', '4', '0', '0', self.job_Id),
            ('SmpCarrier', '13', '5', '0', '0', self.job_Id)
        )
        cur.executemany('''
        INSERT INTO "main"."DbCarrier" ("Name", "LayoutIdx", "CarrierTyp", "SubType", "Disabled", "Job_Id")
        VALUES(?, ?, ?, ?, ?, ?)''', tuple_carrier)

        conn.commit()
        cur.close()
        conn.close()
        return

    # JobReaInfo 추가
    def JobReaInfo(self):
        conn = sqlite3.connect(db_job)
        cur = conn.cursor()

        tuple_reainfo = (
            ('2', '1', '0.0', 'Lysis/Binding Buffer', '0.0', '0.0', '0.0', '96', '0', '0', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('2', '1', '0.0', 'Wash Buffer A', '0.0', '0.0', '0.0', '96', '0', '0', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('2', '1', '0.0', 'Wash Buffer B', '0.0', '0.0', '0.0', '96', '0', '0', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('6', '2', '0.0', 'Internal Control', '0.0', '0.0', '0.0', '96', '0', '10', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('6', '2', '0.0', 'PK', '0.0', '0.0', '0.0', '96', '0', '10', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('8', '1', '0.0', 'Elution Buffer', '0.0', '0.0', '0.0', '96', '0', '0', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('11', '2', '0.0', 'Magnetic Bead', '0.0', '0.0', '0.0', '48', '0', '15', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('14', '1', '0.0', 'MOM', '0.0', '0.0', '0.0', '96', '0', '0', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('14', '1', '0.0', 'RNaseFreeWater', '0.0', '0.0', '0.0', '96', '0', '0', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('14', '1', '0.0', 'EM8', '0.0', '0.0', '0.0', '96', '0', '0', '5', '', '0', '1', self.job_Id, '2', '1.1'),
            ('14', '2', '0.0', 'Standard', '0.0', '0.0', '0.0', '96', '0', '0', '1', '', '0', '1', self.job_Id, '2', '1.1'),
            ('51', '3', '0.0', 'Master Mix', '0.0', '0.0', '0.0', '96', '0', '10', '2', '', '0', '1', self.job_Id, '2', '1.1')
        )
        cur.executemany('''
        INSERT INTO "main"."JobReaInfo" ("ReaContainerType", "TipType", "Ratio", "ReaName", "AspirateDepth", "DispenseDepth", "Capatity", 
        "SingleSmpCount", "Channel", "MixCount", "LiquidType", "Code", "Validity", "MixAdpCount", "Job_Id", "AdditionalCount", "Multiplier")
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple_reainfo)

        # Reagent Id 저장
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "Lysis/Binding Buffer" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.LB_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "Wash Buffer A" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.WA_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "Wash Buffer B" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.WB_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "Elution Buffer" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.EB_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "PK" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.PK_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "Magnetic Bead" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.Bead_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "Internal Control" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.IC_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName like (%s) and Job_Id = (%d)" % ("'" + "EM%" + "'", self.job_Id)) # EM 문자열 포함
        rea_Id = cur.fetchall()
        self.EM_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "MOM" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.MOM_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "RNaseFreeWater" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.Water_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "Master Mix" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.MM_Id = rea_Id[0][0]
        cur.execute("select Id from JobReaInfo where ReaName = (%s) and Job_Id = (%d)" % ("'" + "Standard" + "'", self.job_Id))
        rea_Id = cur.fetchall()
        self.Std_Id = rea_Id[0][0]

        if self.job_name.find("RV-EA") != -1:
            cur.execute("update JobReaInfo set ReaName = (%s) where Job_Id = (%s) and ReaName = (%s)" % ("'" + "EM5 Buffer" + "'", self.job_Id, "'" + "RNaseFreeWater" + "'"))
            cur.execute("update JobReaInfo set ReaName = (%s) where Job_Id = (%s) and ReaName = (%s)" % ("'" + "EM5" + "'", self.job_Id, "'" + "EM8" + "'"))

        conn.commit()
        cur.close()
        conn.close()
        return

    # JobReaBlendProportion 추가 (PCR 시약 수에 따라 데이터 행 수 다름)
    def JobReaBlendProportion(self):
        conn = sqlite3.connect(db_job)
        cur = conn.cursor()

        if self.job_name.find("Extraction") != -1:
            cur.close()
            conn.close()
            return

        elif self.job_name.find("SARS-CoV-2") != -1 or self.job_name.find("RV-EA") != -1: # SARS-CoV-2(C형) or RV-EA이면 PCR시약 3개
            tuple_reablendproportion = (
                (self.MOM_Id, '1.0', '0.0', '0.0', self.MM_Id),
                (self.Water_Id, '1.0', '0.0', '0.0', self.MM_Id),
                (self.EM_Id, '1.0', '0.0', '0.0', self.MM_Id)
            )

        elif self.job_name.find("SC2FabR") != -1: # SC2FabR(D형)이면 PCR시약 2개
            tuple_reablendproportion = (
                (self.MOM_Id, '1.0', '0.0', '0.0', self.MM_Id),
                (self.EM_Id, '1.0', '0.0', '0.0', self.MM_Id)
            )
        cur.executemany('''
        INSERT INTO "main"."JobReaBlendProportion"("ChildJobReaInfoId", "BlendProportion", "AspirateDepth", "DispenseDepth", "ParentJobReaInfoId")
        VALUES(?, ?, ?, ?, ?)''', tuple_reablendproportion)

        conn.commit()
        cur.close()
        conn.close()
        return

    # JobReaInfoLoc 추가
    def JobReaInfoLoc(self):
        conn = sqlite3.connect(db_job)
        cur = conn.cursor()

        tuple_reainfoloc = (
            ('7', '4', self.Bead_Id),
            ('7', '8', self.Bead_Id),
            ('7', '5', self.IC_Id),
            ('7', '9', self.PK_Id),
            ('5', '0', self.EB_Id),
            ('4', '0', self.WA_Id),
            ('4', '1', self.WB_Id),
            ('7', '20', self.Std_Id),
            ('7', '21', self.Std_Id),
            ('5', '3', self.LB_Id),
            ('5', '4', self.LB_Id),
            ('5', '5', self.LB_Id)
        )
        cur.executemany('''
        INSERT INTO "main"."JobReaInfoLoc" ("LayoutIdx", "SlaveIdx", "JobReaInfo_Id")
        VALUES(?, ?, ?)''', tuple_reainfoloc)

        if self.job_name.find("SARS-CoV-2") != -1 or self.job_name.find("RV-EA") != -1: # SARS-CoV-2(C형) or RV-EA일 때 시약 위치
            tuple_reainfoloc = (
                ('7', '7', self.MOM_Id),
                ('7', '11', self.Water_Id),
                ('7', '15', self.EM_Id),
                ('7', '19', self.MM_Id)
            )
            cur.executemany('''
            INSERT INTO "main"."JobReaInfoLoc" ("LayoutIdx", "SlaveIdx", "JobReaInfo_Id")
            VALUES(?, ?, ?)''', tuple_reainfoloc)

        elif self.job_name.find("SC2FabR") != -1: # SC2FabR(D형)일 때 시약 위치
            tuple_reainfoloc = (
                ('7', '11', self.MOM_Id),
                ('7', '7', self.Water_Id),
                ('7', '15', self.EM_Id),
                ('7', '19', self.MM_Id)
            )
            cur.executemany('''
            INSERT INTO "main"."JobReaInfoLoc" ("LayoutIdx", "SlaveIdx", "JobReaInfo_Id")
            VALUES(?, ?, ?)''', tuple_reainfoloc)

        conn.commit()
        cur.close()
        conn.close()
        return

    # JobSmpItem 추가
    def JobSmpItem(self):
        conn = sqlite3.connect(db_job)
        cur = conn.cursor()

        cur.execute('''
        INSERT INTO "main"."JobSmpItem"("Des", "ColorValue", "RefCount", "QcCount", "StdContainerType", "QcContainerType", "Job_Id")
        VALUES(?, ?, ?, ?, ?, ?, ?)''', ('std', '#FF0000FF', '2', '0', '10', '10', self.job_Id))
        conn.commit()

        cur.execute("select * from JobSmpItem where Job_Id = (%d)" % (self.job_Id))
        smp_id = cur.fetchall()
        cur.close()
        conn.close()
        self.Smp_Id = smp_id[0][0]
        return

    # JobStep 추가
    def JobStep(self):
        conn = sqlite3.connect(db_job)
        cur = conn.cursor()

        if self.job_name.find("PCRSetup") == -1: # PCRSetup 아니면 Extraction Procedure 추가

            # Extraction Procedure
            tuple_step = (
                ('0', '4099', '3', '0.0', '0.0', '', '0', '1', '400.0', '0', '0', '0', '0.0', '37.0', '0', '0', '1', '1', '0',
                 '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '3', '1', '0', '0', None, self.job_Id, self.LB_Id, None),
                ('1', '4098', '3', '0.0', '0.0', '', '0', '2', '15.0', '0', '0', '0', '27.5', '34.0', '0', '0', '6', '1',
                 '1', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '3', '1', '0', '0', None, self.job_Id, self.Bead_Id, None),
                ('2', '4098', '3', '0.0', '0.0', '', '0', '2', '10.0', '0', '0', '0', '27.5', '34.0', '0', '0', '8', '1',
                 '1', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '3', '1', '0', '0', None, self.job_Id, self.IC_Id, None),
                ('3', '4098', '3', '0.0', '0.0', '', '0', '2', '10.0', '0', '0', '0', '27.5', '34.0', '0', '0', '8', '1',
                 '1', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '3', '1', '0', '0', None, self.job_Id, self.PK_Id, None),
                ('4', '4097', '3', '0.0', '0.0', '', '0', '1', '200.0', '0', '0', '0', '0.0', '34.0', '0', '0', '1', '1',
                 '1', '0', '0.0', '0.0', '0.0', '0.0', '0', '0', '3', '1', '0', '0', None, self.job_Id, None, None),
                ('5', '0', '0', '0.0', '0.0', 'TakeupTips.che', '0', '1', '400.0', '0', '0', '0', '0.0', '27.0', '60', '0', '8',
                 '1', '0', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '0', '1', '0', '0', None, self.job_Id, None, None),
                ('6', '2', '3', '0.0', '0.0', 'SY659BeadBinding01_0205.che', '0', '1', '400.0', '0', '0', '0', '0.0', '27.0',
                 '1320', '0', '8', '1', '0', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '3', '1', '0', '0', None, self.job_Id, None, None),
                ('7', '4099', '6', '0.0', '0.0', '', '0', '1', '800.0', '0', '0', '0', '0.0', '27.0', '1321', '0', '1', '1', '0',
                '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '6', '1', '0', '0', None, self.job_Id, self.WA_Id, None),
                ('8', '3', '6', '0.0', '0.0', 'BeadWashing_0205.che', '0', '1', '800.0', '0', '0', '0', '0.0', '27.0', '420',
                 '0', '8', '1', '0', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '6', '1', '0', '0', None, self.job_Id, None, None),
                ('9', '4099', '1', '0.0', '0.0', '', '0', '1', '800.0', '0', '0', '0', '0.0', '27.0', '420', '0', '1', '1', '0',
                 '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '1', '1', '0', '0', None, self.job_Id, self.WB_Id, None),
                ('10', '3', '1', '0.0', '0.0', 'BeadWashing_0205.che', '0', '1', '800.0', '0', '0', '0', '0.0', '27.0', '420',
                 '0', '8', '1', '0', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '1', '1', '0', '0', None, self.job_Id, None, None),
                ('11', '4099', '4', '0.0', '0.0', '', '0', '1', '60.0', '0', '0', '0', '0.0', '40.0', '420', '0', '6', '1', '0',
                 '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '4', '1', '0', '0', None, self.job_Id, self.EB_Id, None),
                ('12', '9', '4', '0.0', '0.0', 'BeadDrying.che', '0', '1', '80.0', '0', '0', '0', '0.0', '40.0', '300', '0', '8',
                '1', '0', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '4', '1', '0', '0', None, self.job_Id, None, None),
                ('14', '7', '4', '0.0', '0.0', 'BeadElution_0205.che', '0', '4', '15.0', '1', '0', '0', '0.0', '11.5', '840',
                 '0', '1', '1', '0', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '4', '1', '0', '0', None, self.job_Id, None, None),
                ('15', '11', '1', '0.0', '0.0', 'StripTips.che', '0', '1', '10.0', '0', '0', '0', '0.0', '11.5', '60', '2', '8',
                 '1', '0', '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '1', '1', '0', '0', None, self.job_Id, None, None)
            )
            cur.executemany('''
            INSERT INTO "main"."JobStep"("StepNbr", "StepType", "TransportSlot", "VoltageMagnet", "VoltageRotation", "AuxFileName",
                      "ColorArgb", "TipsType", "Volume", "TargetPos", "SourcePos", "MixTime", "AspirateDepth",
                      "DispenseDepth", "EstimatedTime", "ItemId", "DispenseCount", "IsNeedDetectLiquildLevel",
                      "IsNeedChangeTip", "HeatingTime", "Temperature", "MixAspDepth", "MixDisDepth", "MixVolume",
                      "MixAfterDispense", "MixBeforeAspirate", "TransportSlots", "MixAdpCount", "SrcPlatformId",
                      "TargetPlatformId", "StdAspirateDepth", "Job_Id", "JobReaInfo_Id", "JobSmpItem_Id")
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            , tuple_step)

            if self.job_name.find("Extraction") != -1: # Extraction이면 StepNbr 수정
                cur.execute("update JobStep set StepNbr = 13 where Job_Id = (%d) and StepNbr = 14" % self.job_Id)
                cur.execute("update JobStep set StepNbr = 14 where Job_Id = (%d) and StepNbr = 15" % self.job_Id)
                conn.commit()
                cur.close()
                conn.close()
                return

            elif self.job_name.find("SARS-CoV-2") != -1: # SARS-CoV-2(C형)이면 MM, Retrans Procedure 추가
                tuple_step = (
                    ('13', '4101', '-1', '0.0', '0.0', '', '0', '3', '14.9', '1', '0', '0', '0.0', '13.0', '840', '0', '1', '1', '0',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '-1', '1', '0', '0', None, self.job_Id, self.MM_Id, None),
                    ('16', '4100', '4', '0.0', '0.0', '', '0', '2', '5.0', '1', '0', '0', '42.0', '10.0', '840', '0', '1', '0', '1',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '4', '1', '0', '0', None, self.job_Id, None, self.Smp_Id)
                )

            elif self.job_name.find("RV-EA") != -1: # RV-EA이면 MM, Retrans Procedure 추가
                tuple_step = (
                    ('13', '4101', '-1', '0.0', '0.0', '', '0', '3', '15.0', '1', '0', '0', '0.0', '13.0', '840', '0', '1', '1', '0',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '-1', '1', '0', '0', None, self.job_Id, self.MM_Id, None),
                    ('16', '4100', '4', '0.0', '0.0', '', '0', '2', '5.0', '1', '0', '0', '42.0', '10.0', '840', '0', '1', '0', '1',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '4', '1', '0', '0', None, self.job_Id, None, self.Smp_Id)
                )

            elif self.job_name.find("SC2FabR") != -1: # SC2FabR(D형)이면 MM, Retrans Procedure 추가
                tuple_step = (
                    ('13', '4101', '-1', '0.0', '0.0', '', '0', '3', '10.0', '1', '0', '0', '0.0', '13.0', '840', '0', '1', '1', '0',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '-1', '1', '0', '0', None, self.job_Id, self.MM_Id, None),
                    ('16', '4100', '4', '0.0', '0.0', '', '0', '2', '10.0', '1', '0', '0', '42.0', '10.0', '840', '0', '1', '0', '1',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '4', '1', '0', '0', None, self.job_Id, None, self.Smp_Id)
                )
            cur.executemany('''
            INSERT INTO "main"."JobStep"("StepNbr", "StepType", "TransportSlot", "VoltageMagnet", "VoltageRotation", "AuxFileName",
                        "ColorArgb", "TipsType", "Volume", "TargetPos", "SourcePos", "MixTime", "AspirateDepth",
                        "DispenseDepth", "EstimatedTime", "ItemId", "DispenseCount", "IsNeedDetectLiquildLevel",
                        "IsNeedChangeTip", "HeatingTime", "Temperature", "MixAspDepth", "MixDisDepth", "MixVolume",
                        "MixAfterDispense", "MixBeforeAspirate", "TransportSlots", "MixAdpCount", "SrcPlatformId",
                        "TargetPlatformId", "StdAspirateDepth", "Job_Id", "JobReaInfo_Id", "JobSmpItem_Id")
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            , tuple_step)

        elif self.job_name.find("PCRSetup") != -1: # PCRSetup이면
            if self.job_name.find("SARS-CoV-2") != -1: # SARS-CoV-2(C형)이면 MM, Retrans Procedure 추가
                tuple_step = (
                    ('0', '4101', '-1', '0.0', '0.0', '', '0', '3', '14.9', '1', '0', '0', '0.0', '13.0', '840', '0', '1', '1', '0',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '-1', '1', '0', '0', None, self.job_Id, self.MM_Id, None),
                    ('1', '4100', '4', '0.0', '0.0', '', '0', '2', '5.0', '1', '0', '0', '42.0', '10.0', '840', '0', '1', '0', '1',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '4', '1', '0', '0', None, self.job_Id, None, self.Smp_Id)
                )

            elif self.job_name.find("RV-EA") != -1: # RV-EA이면 MM, Retrans Procedure 추가
                tuple_step = (
                    ('0', '4101', '-1', '0.0', '0.0', '', '0', '3', '15.0', '1', '0', '0', '0.0', '13.0', '840', '0', '1', '1', '0',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '-1', '1', '0', '0', None, self.job_Id, self.MM_Id, None),
                    ('1', '4100', '4', '0.0', '0.0', '', '0', '2', '5.0', '1', '0', '0', '42.0', '10.0', '840', '0', '1', '0', '1',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '4', '1', '0', '0', None, self.job_Id, None, self.Smp_Id)
                )

            elif self.job_name.find("SC2FabR") != -1: # SC2FabR(D형)이면 MM, Retrans Procedure 추가
                tuple_step = (
                    ('0', '4101', '-1', '0.0', '0.0', '', '0', '3', '10.0', '1', '0', '0', '0.0', '13.0', '840', '0', '1', '1', '0',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '-1', '1', '0', '0', None, self.job_Id, self.MM_Id, None),
                    ('1', '4100', '4', '0.0', '0.0', '', '0', '2', '10.0', '1', '0', '0', '42.0', '10.0', '840', '0', '1', '0', '1',
                     '0', '0.0', '0.0', '0.0', '10.0', '0', '0', '4', '1', '0', '0', None, self.job_Id, None, self.Smp_Id)
                )
            cur.executemany('''
            INSERT INTO "main"."JobStep"("StepNbr", "StepType", "TransportSlot", "VoltageMagnet", "VoltageRotation", "AuxFileName",
                        "ColorArgb", "TipsType", "Volume", "TargetPos", "SourcePos", "MixTime", "AspirateDepth",
                        "DispenseDepth", "EstimatedTime", "ItemId", "DispenseCount", "IsNeedDetectLiquildLevel",
                        "IsNeedChangeTip", "HeatingTime", "Temperature", "MixAspDepth", "MixDisDepth", "MixVolume",
                        "MixAfterDispense", "MixBeforeAspirate", "TransportSlots", "MixAdpCount", "SrcPlatformId",
                        "TargetPlatformId", "StdAspirateDepth", "Job_Id", "JobReaInfo_Id", "JobSmpItem_Id")
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            , tuple_step)

        conn.commit()
        cur.close()
        conn.close()
        return

    def make_protocol(self, job_name):
        self.job_name = job_name

        self.Job()
        self.DbCarrier()
        self.JobReaInfo()
        self.JobReaBlendProportion()
        self.JobReaInfoLoc()
        self.JobSmpItem()
        self.JobStep()
        return



DB = Job_DataBase_class()
DB.delete_protocol()

DB.make_protocol("Extraction_Seegene")
DB.make_protocol("OneStep_RV-EA")
DB.make_protocol("OneStep_SARS-CoV-2")
DB.make_protocol("OneStep_SC2FabR")
DB.make_protocol("PCRSetup_RV-EA")
DB.make_protocol("PCRSetup_SARS-CoV-2")
DB.make_protocol("PCRSetup_SC2FabR")
