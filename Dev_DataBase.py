import sqlite3
import sys
import datetime
import os
import shutil
import sys

db_con = "C:\\WorkList\\PreNATII_Devs.db3" ## 경로 수정

class Singleton(type):  # Type을 상속받음
    __instances = {}  # 클래스의 인스턴스를 저장할 속성

    def __call__(cls, *args, **kwargs):  # 클래스로 인스턴스를 만들 때 호출되는 메서드
        if cls not in cls.__instances:  # 클래스로 인스턴스를 생성하지 않았는지 확인
            cls.__instances[cls] = super().__call__(*args, **kwargs)  # 생성하지 않았으면 인스턴스를 생성하여 해당 클래스 사전에 저장
            # print("인스턴스 생성 확인")
        # print("인스턴스 활용중 ~")
        # print(cls)
        return cls.__instances[cls]  # 클래스로 인스턴스를 생성했으면 인스턴스 반환

class Dev_DataBase_class(metaclass=Singleton):

        # Dev DbCalibration 값 추가
        def DbCalibration(self):
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()
            cur.execute("SELECT * FROM DbCalibration WHERE CoeffVolume = 10.7")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 0:
                cur.execute('''
                            INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                            VALUES (3, 0, 0,0, 10.7, 10.0)
                            ''')
                cur.execute('''
                                INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                VALUES (3, 1, 0,0, 10.7, 10.0)
                            ''')
                cur.execute('''
                                INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                VALUES (3, 2, 0,0, 10.7, 10.0)
                            ''')
                cur.execute('''
                                INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                VALUES (3, 3, 0,0, 10.7, 10.0)
                            ''')
                conn.commit()

            cur.execute("SELECT * FROM DbCalibration WHERE CoeffVolume = 16.0")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 0:
                cur.execute('''
                                            INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                            VALUES (3, 0, 0,0, 16.0, 14.9)
                            ''')
                cur.execute('''
                                            INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                            VALUES (3, 1, 0,0, 16.0, 14.9)
                            ''')
                cur.execute('''
                                            INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                            VALUES (3, 2, 0,0, 16.0, 14.9)
                            ''')
                cur.execute('''
                                            INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                            VALUES (3, 3, 0,0, 16.0, 14.9)
                            ''')
                conn.commit()

            cur.execute("SELECT * FROM DbCalibration WHERE CoeffVolume = 16.8")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 0:
                cur.execute('''
                                            INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                            VALUES (3, 0, 0,0, 16.8, 15.0)
                            ''')
                cur.execute('''
                                            INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                            VALUES (3, 1, 0,0, 16.8, 15.0)
                            ''')
                cur.execute('''
                                            INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                            VALUES (3, 2, 0,0, 16.8, 15.0)
                            ''')
                cur.execute('''
                                            INSERT INTO "main"."DbCalibration" ("TipIdx", "AdpIndex", "DisTimes", "DisIdx", "CoeffVolume", "DisVolume") 
                                            VALUES (3, 3, 0,0, 16.8, 15.0)
                            ''')
                conn.commit()
            Dev_Info = cur.fetchall()
            cur.close()
            conn.close()
            return Dev_Info

        # Dev_DbFreeDispenses 값 추가
        def DbFreeDispenses(self):
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()
            Dev_Info = cur.execute("DELETE FROM DbFreeDispenses")
            cur.execute('''
                                        INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                        VALUES (4.0, 0, 1, 2, 0, 200, 300, 0, 0, 0.0, 0, 200, 160, 300, 0, 0)
                        ''')
            cur.execute('''
                                        INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                        VALUES (5.0, 0, 2, 3, 0, 60, 300, 2, 0, 0.0, 0, 30, 20, 300, 0, 0)
                        ''')
            cur.execute('''
                                        INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                        VALUES (5.0, 0, 1, 4, 0, 300, 300, 15, 10, 0.0, 0, 440, 160, 300, 0, 0)
                        ''')
            cur.execute('''
                                        INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                        VALUES (5.0, 0, 1, 2, 0, 200, 300, 0, 0, 0.0, 0, 200, 160, 300, 0, 0)
                        ''')
            cur.execute('''
                                        INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                        VALUES (5.0, 0, 5, 1, 0, 180, 300, 2, 0, 0.0, 0, 450, 160, 3000, 0, 0)
                       ''')
            cur.execute('''
                                        INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                        VALUES (10.0, 0, 1, 2, 1, 200, 300, 15, 10, 0.0, 15, 200, 160, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (10.0, 0, 1, 2, 0, 120, 300, 40, 10, 0.0, 0, 875, 600, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (10.0, 0, 1, 1, 0, 120, 300, 40, 5, 0.0, 0, 875, 160, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (10.0, 0, 1, 1, 1, 300, 300, 15, 10, 0.0, 25, 440, 160, 300, 0, 0)
                        ''')

            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (10.0, 0, 3, 2, 0, 300, 300, 15, 0, 0.0, 15, 440, 160, 300, 0, 10)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (14.0, 0, 2, 3, 0, 60, 300, 2, 0, 0.0, 0, 30, 20, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (20.0, 0, 1, 2, 1, 200, 300, 10, 10, 0.0, 15, 200, 200, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (20.0, 0, 1, 2, 0, 120, 300, 20, 20, 0.0, 0, 200, 200, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (25.0, 0, 1, 1, 0, 120, 300, 40, 5, 0.0, 0, 875, 200, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (25.0, 0, 1, 1, 1, 120, 300, 20, 5, 0.0, 25, 875, 240, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (50.0, 0, 1, 1, 0, 120, 300, 10, 10, 0.0, 0, 875, 200, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (50.0, 0, 1, 1, 1, 120, 300, 20, 5, 0.0, 25, 875, 200, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (60.0, 0, 1, 2, 1, 550, 300, 20, 20, 0.0, 25, 440, 200, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (60.0, 0, 1, 2, 0, 80, 300, 20, 20, 0.0, 0, 300, 200, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (80.0, 0, 1, 1, 1, 300, 300, 20, 10, 0.0, 25, 875, 240, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (100.0, 0, 1, 2, 0, 80, 300, 20, 10, 0.0, 0, 300, 200, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (100.0, 0, 1, 1, 0, 300, 300, 15, 20, 0.0, 0, 875, 240, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (100.0, 0, 2, 1, 0, 100, 300, 15, 10, 0.0, 0, 300, 160, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (200.0, 0, 1, 1, 0, 300, 300, 15, 20, 0.0, 0, 440, 240, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (400.0, 0, 1, 1, 0, 300, 300, 15, 20, 0.0, 0, 300, 160, 300, 0, 0)
                        ''')
            cur.execute('''
                                         INSERT INTO "main"."DbFreeDispenses" ("DisVolume", "DisTimes", "LiquidType", "TipIdx", "PipettingType", "AspiratingSpeed", "DelayAsp", "LeadingAirgap", "TrailingAirgap", "ExcessVolume", "ConditioningVolume", "DispenseSpeed", "BreakOffSpeed", "DelayDis", "AspiratingZSpeed", "ExtraVol") 
                                         VALUES (800.0, 0, 1, 1, 0, 300, 300, 15, 20, 0.0, 0, 240, 240, 300, 0, 0)
                        ''')
            conn.commit()
            cur.close()
            conn.close()

        # Dev_LiquidContainer 값 추가
        def LiquidContainer(self):
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()
            cur.execute("SELECT * FROM DbLiquidContainer WHERE name = 'Vial Tube(1.5ml) Sample'")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 0:
                cur.execute('''
                                        INSERT INTO "main"."DbLiquidContainer" ("Name", "EnglishName", "Volume", "UnitVolume", "Height", "ExcessVolume", "Enabled", "ContainerTypeValue", "IsWide", "Shape", "IdentifyFlag", "Width", "ConeR", "ConeHeight", "ConeVol", "HeightDiff", "ExtraVolume", "OverLiquidLevel", "DetectLiquidLevelErr", "OffsetX", "ContainerHeight", "AspirateCount", "CoeffA", "CoeffB", "GroupTypeValue", "ExcessHeight", "ColCount") 
                                        VALUES ('Vial Tube(1.5ml) Sample', 'Vial Tube(1.5ml) Sample', 2000.0, 52.63, 2739, 10.0, 1, 17, 0, 2, '', 815, 0.0, 0.0, 0.0, 0.0, 20.0, 0.6, 1.0, 0.0, 0.0, 1, 0.0, 0.0, 0, 0.0, 1)
                            ''')
                conn.commit()
            cur.execute("SELECT * FROM DbLiquidContainer WHERE name = 'Primary Tube(12mm) Sample'")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 0:
                cur.execute('''
                                        INSERT INTO "main"."DbLiquidContainer" ("Name", "EnglishName", "Volume", "UnitVolume", "Height", "ExcessVolume", "Enabled", "ContainerTypeValue", "IsWide", "Shape", "IdentifyFlag", "Width", "ConeR", "ConeHeight", "ConeVol", "HeightDiff", "ExtraVolume", "OverLiquidLevel", "DetectLiquidLevelErr", "OffsetX", "ContainerHeight", "AspirateCount", "CoeffA", "CoeffB", "GroupTypeValue", "ExcessHeight", "ColCount") 
                                        VALUES ('Primary Tube(12mm) Sample', 'Primary Tube(12mm) Sample', 6500.0, 113.0, 8134, 50.0, 1, 19, 0, 0, '', 3200, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 1.0, 0.0, 0.0, 1, 0.0, 0.0, 0, 0.0, 1)
                                            ''')
                conn.commit()

            cur.execute("SELECT * FROM DbLiquidContainer WHERE name = 'Primary Tube(16mm) Sample'")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 0:
                cur.execute('''
                                        INSERT INTO "main"."DbLiquidContainer" ("Name", "EnglishName", "Volume", "UnitVolume", "Height", "ExcessVolume", "Enabled", "ContainerTypeValue", "IsWide", "Shape", "IdentifyFlag", "Width", "ConeR", "ConeHeight", "ConeVol", "HeightDiff", "ExtraVolume", "OverLiquidLevel", "DetectLiquidLevelErr", "OffsetX", "ContainerHeight", "AspirateCount", "CoeffA", "CoeffB", "GroupTypeValue", "ExcessHeight", "ColCount") 
                                        VALUES ('Primary Tube(16mm) Sample', 'Primary Tube(16mm) Sample', 9000.0, 206.0, 8134, 50.0, 1, 20, 0, 0, '', 3200, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 1.0, 0.0, 0.0, 1, 0.0, 0.0, 0, 0.0, 1)
                                                        ''')
                conn.commit()

            cur.execute("SELECT * FROM DbLiquidContainer WHERE name = 'SG Micro Tube 2.0mL'")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 0:
                cur.execute('''
                                                   INSERT INTO "main"."DbLiquidContainer" ("Name", "EnglishName", "Volume", "UnitVolume", "Height", "ExcessVolume", "Enabled", "ContainerTypeValue", "IsWide", "Shape", "IdentifyFlag", "Width", "ConeR", "ConeHeight", "ConeVol", "HeightDiff", "ExtraVolume", "OverLiquidLevel", "DetectLiquidLevelErr", "OffsetX", "ContainerHeight", "AspirateCount", "CoeffA", "CoeffB", "GroupTypeValue", "ExcessHeight", "ColCount") 
                                                   VALUES ('SG Micro Tube 2.0mL', 'SG Micro Tube 2.0mL', 2000.0, 56.75, 2500, 20.0, 1, 51, 0, 1, '', 830, 0.0, 0.0, 0.0, 16.0, 130.0, 0.6, 1.0, 0.0, 0.0, 1, 0.0, 0.0, 2, 0.0, 1)
                                                                   ''')
                conn.commit()

            cur.execute("SELECT * FROM DbLiquidContainer WHERE name = '试管 (100mm)'")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 1:
                cur.execute("UPDATE DbLiquidContainer SET GroupTypeValue = 5 WHERE name = '试管 (100mm)'")
                conn.commit()

            cur.execute("SELECT * FROM DbLiquidContainer WHERE name = '标准品(1.5ml可立管)'")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 1:
                cur.execute("UPDATE DbLiquidContainer SET GroupTypeValue = 5 WHERE name = '标准品(1.5ml可立管)'")
                conn.commit()

            cur.execute("SELECT * FROM DbLiquidContainer WHERE name = '标准品(2.0ml可立管)'")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 1:
                cur.execute("UPDATE DbLiquidContainer SET GroupTypeValue = 5 WHERE name = '标准品(2.0ml可立管)'")
                conn.commit()

            cur.execute("SELECT * FROM DbLiquidContainer WHERE name = '磁珠（2.0ml可立管）'")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 1:
                cur.execute("UPDATE DbLiquidContainer SET ExcessVolume = 10.0 WHERE name = '磁珠（2.0ml可立管）'")
                conn.commit()

            cur.execute("SELECT * FROM DbLiquidContainer WHERE name = 'EP管(1.5ml)'")
            Dev_Info = cur.fetchall()
            if Dev_Info.__len__() == 1:
                cur.execute("UPDATE DbLiquidContainer SET Height = 1000 WHERE name = 'EP管(1.5ml)'")
                conn.commit()

            conn.commit()
            cur.close()
            conn.close()

        def DbTipInfo(self):
            conn = sqlite3.connect(db_con)
            cur = conn.cursor()
            cur.execute("Delete from DbTipInfo WHERE Volume = 50.0")
            cur.execute('''
                                INSERT INTO "main"."DbTipInfo" ("TipType", "Volume", "Height", "Vender", "PLLDValue", "AdThread", "Des", "ThresholdDuration", "AbsPos", "MaxRelativePlunger", "PerformMode", "Interval", "SmpNumber", "MaxDuration") 
                                VALUES (3, 50.0, 30.0, '', 140, 130, 50, 5, 3000, 3000, 1, 20, 3, 300);
                        ''')
            conn.commit()
            cur.close()
            conn.close()



