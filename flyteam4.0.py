from BeautifulSoup import BeautifulSoup
import requests
import csv
from datetime import datetime
from datetime import timedelta
import time
import random
import os

def findflight(Num):
    Number = str(Num)
    while True:
        try:
            r = requests.get(urlHead + Number)
            soup = BeautifulSoup(r.content)
            if len(soup) == 0:
                time.sleep(5)
            else:
                print "Successed"
                return soup
        except ConnectionError:
            print "Connection Failed"
            print Num

def dayconvert(s):
    if s == "Daily":
        return range(0,7)
    else:
        s = s.replace("Mon","0")
        s = s.replace("Tue","1")
        s = s.replace("Wed","2")
        s = s.replace("Thu","3")
        s = s.replace("Fri","4")
        s = s.replace("Sat","5")
        s = s.replace("Sun","6")
        converted = []
        while True:
            if s.find('-') == 1:
                converted += range(int(s[0]),int(s[2])+1)
                s = s[4:]
            elif s.find(',') == 1:
                converted += [int(s[0])]
                s = s[2:]
            else:
                if len(s) != 0:
                    converted += [int(s[0])]
                else:
                    pass
                break
        return converted
    
def getdate(strdate):
    year = int(strdate[0:4])
    month = int(strdate[5:7])
    date = int(strdate[8:10])
    return datetime(year, month, date)

def getrightone(strtable, setdate):
    #print strtable
    effectfromdate = strtable.find("Effective from")
    if effectfromdate == -1:
        effectdate = strtable.find("Effective")
        if effectdate == -1:
            operatedate = strtable.find("Operates")
            if operatedate == -1:
                validdate = strtable.find("Valid")
                if validdate == -1:
                    return 0
                else:
                    date = getdate(strtable[validdate+12:validdate+22])
                    #print date
                    if setdate <= date:
                        #print "Gotchya!"
                        return strtable
                    else:
                        return 0
            else:
                date = getdate(strtable[operatedate+17:operatedate+27])
                #print date
                if setdate == date:
                    #print "Got it"
                    return strtable
                else:
                    return 0
        else:
            date1 = getdate(strtable[effectdate+10:effectdate+20])
            date2 = getdate(strtable[effectdate+29:effectdate+39])
            #print date1
            #print date2
            if (setdate >= date1) and (setdate <= date2):
                #print "Got it Here!"
                return strtable
            else:
                return 0
    else:
        date = getdate(strtable[effectfromdate+15:effectfromdate+25])
        #print date
        if setdate >= date:
            #print "Quite future!"
            return strtable
        else:
            return 0
    
def getinfo(lists):
    length = len(lists)
    target = "\n"
    info = []
    for i in lists:
        for num in range(0,9):
            if num == 0:
                i = i[i.find(target)+1:]
            elif num == 1:
                temp = i[:i.find(target)-1]
                day = temp[temp.find(">")+1:]
                i = i[i.find(target)+1:]
            elif num == 2:
                departTime = i[0:5]
                i = i[i.find(target)+1:]
            elif num == 3:
                departCity = i[i.find("/airport")+9:i.find("/airport")+12]
                i = i[i.find(target)+1:]
            elif num == 4:
                arriveTime = i[0:5]
                i = i[i.find(target)+1:]
            elif num == 5:
                arriveCity = i[i.find("/airport")+9:i.find("/airport")+12]
                i = i[i.find(target)+1:]
            elif num == 6:
                flightNum = i[:i.find(target)]
                i = i[i.find(target)+1:]
            elif num == 7:
                durationTime = i[i.find(target)-5:i.find(target)]
                i = i[i.find(target)+1:]
            elif num == 8:
                if i.find('The flight arrives') == -1:
                    ArriveDate = 0
                else:
                    ArriveDate = i[i.find('The flight arrives')+19]
            else:
                pass
        info += [[flightNum, departCity, arriveCity, departTime, arriveTime, durationTime, day, ArriveDate]]
    return info
                

#Gotit_odd = 0;
# "No flights found" when there is no flight number
# Japan : 7**
# China : 8**
# Europe, MEA, Africa : 9**
# America : 0** -> **
# Oceania : 1**
# SEA : 6**, 4**

#Flights
FlightJapan = range(701,800) + [2725, 2726, 2727, 2728, 1, 2, 2707, 2708, 2709, 2710, 2711, 2712]
FlightChina = range(801,900) + [2851, 2852, 8865, 8866, 2815, 2816, 8881, 8882, 8843, 8844]
FlightSEA = range(601,700) + [463, 464, 479, 480, 467, 468, 473, 474, 471, 472]
FlightAmerica = [35, 36, 37, 38, 31, 32, 51, 52, 53, 54, 29, 30, 5, 6, 11, 12, 17, 18, 61, 62, 81, 82, 85, 86, 23, 24, 19, 20, 71, 72, 73, 74, 93, 94]
FlightEurope = [925, 926, 905, 906, 955, 956, 907, 908, 913, 914, 927, 928, 903, 904, 901, 902, 935, 936, 931, 932, 937, 938, 917, 918]
FlightRMC = [983, 984, 923, 924, 941, 942, 867, 8867, 868, 8868, 981, 982, 929, 930]
FlightMEA = [951, 952, 961, 962, 957, 958]
FlightOceania = [129, 130, 123, 124, 111, 112, 2115, 2116, 137, 138, 121, 122]
#FlightJeju = range(1200,1266) + range(1001,1018) + range(1812,1820) + range(1901,1909) + range(1951, 1959) + [1917, 1918, 1851, 1852, 1821, 1822, 1831, 1832, 1931, 1932]
#FlightGimpo = range(1100,1128) + range(1603, 1617) + range(1331,1339) + [1300, 1301, 1305, 1306] + range(1631,1635) + range(1411,1415) + range(1401,1409)
#Flight Numbers
Flights = FlightJapan + FlightChina + FlightSEA + FlightAmerica + FlightEurope + FlightRMC + FlightMEA + FlightOceania# + FlightJeju + FlightGimpo

urlHead = "http://info.flightmapper.net/en/flight/Korean_Air_Lines_KE_"

# Get keyboard input
TargetInput = raw_input('What month do you want to know?(YYYYMM, ex.201509)\n')
TargetYear = int(TargetInput[0:4])
TargetMonth = int(TargetInput[4:6])
if TargetMonth == 12:
    DateofMonth = 31
else:
    DateofMonth = int(str(datetime(TargetYear, TargetMonth+1, 1)-datetime(TargetYear, TargetMonth, 1))[0:2])

FlightFrom = int(raw_input('From where do you want to start?(default=0, Input other number when robot occurs)\n'))

# Make the CSV files for everyday
Directory = os.getcwd() + "\\db\\%04d%02d\\" % (TargetYear, TargetMonth)
DBRoot = os.getcwd() + '\\db\\'
if not os.path.exists(Directory):
        os.makedirs(Directory)
if FlightFrom == 0:
    for TargetDate in range(1,DateofMonth+1):
        FileName = Directory + "schedule_%04d%02d%02d.csv" %(TargetYear, TargetMonth, TargetDate)
        with open(FileName, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
    with open(DBRoot + "FlightNumbers.csv",'w') as fd:
        writer = csv.writer(fd, lineterminator='\n')
else:
    pass

# For manual input
if FlightFrom == 999:
    CharterNum = raw_input('Input charter flight number(KE****)\n')
    CharterNum = 'KE '+CharterNum
    CharterFrom = raw_input('Where is the origin airport?\n')
    CharterTo = raw_input('Where is the destination airport?\n')
    CharterDay = raw_input('What date is the charter operation on this month?(write only date, if multiple date then divide with /)\n')
    CharterDepart = raw_input('What time is the departure?\n')
    CharterArrive = raw_input('What time is the arrival?\n')
    CharterDuration = raw_input('How long is the operation time?\n')
    CharterDayPlus = raw_input('If it arrives on same day, input 0, if not, input plus day\n')
    FileNamecsv = os.getcwd() + '\\db\\FlightNumbers.csv'
    
    CharterDays = []
    while True:
        if CharterDay.find('/') != -1:
            CharterDays += [int(CharterDay[:CharterDay.find('/')])]
            CharterDay = CharterDay[CharterDay.find('/')+1:]
        else:
            CharterDays += [int(CharterDay)]
            break
    
    for TargetDate in CharterDays:   
        FileName = Directory + "schedule_%04d%02d%02d.csv" %(TargetYear, TargetMonth, TargetDate)
        Info = [[CharterNum, CharterFrom, CharterTo, CharterDepart, CharterArrive, CharterDuration, 'Charter', CharterDayPlus]]
        with open(FileName,'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(Info)
        f.close()
    print 'Charter added!'
    
else:
    # For every flight number
    for Number in Flights[FlightFrom:]:
        soup = findflight(Number)
        Robot = repr(soup).find("The website has detected requests which look like automated requests from a computer bot program.")
        Nothing = repr(soup).find("No flights found.")
        if Robot != -1:
            print Number
            print 'You should start from'
            print Flights.index(Number)
            raise NotImplementedError
        else:
            pass

        if Nothing != -1:
            print "No flights found for KE%04d." % Number
        else:
            FileNamecsv = DBRoot + 'FlightNumbers.csv'
            with open(FileNamecsv,'a') as fd:
                writers = csv.writer(fd, lineterminator='\n')
                writers.writerow([Number])
            fd.close()

        tables_odd = soup.findAll("tr", {"class" : "odd"})
        tables_even = soup.findAll("tr", {"class" : "even"})
        
        if (tables_odd == []) and (tables_even == []):
            pass

        else:
            for TargetDate in range(1,DateofMonth+1):   
                Info = []
                setdate = datetime(TargetYear, TargetMonth, TargetDate)
                targetday = setdate.weekday()
                FileName = Directory + "schedule_%04d%02d%02d.csv" %(TargetYear, TargetMonth, TargetDate)
                
                if tables_odd == []:
                    pass
                else:
                    Tables_odd = []
                    for tables in tables_odd:
                        table = repr(tables)
                        strtable = getrightone(table, setdate)
                        if strtable == 0:
                            pass
                        else:
                            Tables_odd += [strtable]
                    if Tables_odd == []:
                        pass           
                    else:
                        newInfo = getinfo(Tables_odd)
                        for i in range(0,len(newInfo)):               
                            if targetday in dayconvert(newInfo[i][6]):
                                #print "Yes"
                                Info += [newInfo[i]]
                            else:
                                pass
                                #print "No"

                if tables_even == []:
                    pass
                else:
                    Tables_even = []
                    for tables in tables_even:
                        table = repr(tables)
                        strtable = getrightone(table, setdate)
                        if strtable == 0:
                            pass
                        else:
                            Tables_even += [strtable]
                    if Tables_even == []:
                        pass
                    else:
                        newInfo = getinfo(Tables_even)
                        for i in range(0,len(newInfo)):               
                            if targetday in dayconvert(newInfo[i][6]):
                                #print "Yes"
                                Info += [newInfo[i]]
                            else:
                                pass
                                #print "No"

                with open(FileName,'a') as f:
                    writer = csv.writer(f, lineterminator='\n')
                    writer.writerows(Info)
                f.close()
            print Number
        time.sleep(random.randrange(35,60))

