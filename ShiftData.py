#coding=utf-8
import datetime
import re
import calendar
import random;
class ShiftData:
    """Classe representando um ciclo clockin/clockout/break"""
    indexesByMonth = {v: k for k,v in enumerate(calendar.month_abbr)}


    def __init__(self, shiftText):

         self.parseFromText(shiftText)
    
    def parseFromText(self, txt):
        regex = r"^(?P<durationHours>(\d+h))*(, )*(?P<durationMinutes>\d+m)* (?P<startTime>\d+:\d+) (?P<endTime>\d+:\d+) (?P<month>\D+)(?P<dayOfMonth>\d+)\s+(?P<breakHours>(\d+h))*(, )*(?P<breakMinutes>\d+m)*"
        compiledPattern = re.compile(regex)
        matches = re.search(compiledPattern, txt)
        startTimeStr = matches.group("startTime")
        endTimeStr = matches.group("endTime")

        self.month = matches.group("month")
        self.dayOfMonth = matches.group("dayOfMonth")
        self.startTime = datetime.datetime.strptime(startTimeStr, '%H:%M').time()
        self.endTime = datetime.datetime.strptime(endTimeStr, '%H:%M').time()
        hours = self.getIntFromCaptureGroup(matches, "durationHours")
        minutes = self.getIntFromCaptureGroup(matches, "durationMinutes")
        self.shiftDuration = datetime.timedelta(hours=hours, minutes=minutes)

        hours = self.getIntFromCaptureGroup(matches, "breakHours")
        minutes = self.getIntFromCaptureGroup(matches, "breakMinutes")
        self.breakDuration = datetime.timedelta(hours=hours, minutes=minutes)


    def __str__(self):
        shiftDataStr = "Dia " + self.dayOfMonth + "/" + str(ShiftData.indexesByMonth[self.month.strip()]) + "\n"
        shiftDataStr += "Entrada: " + self.startTime.strftime("%H:%M") + "\n"
        shiftDataStr += "Break start: " + self.getBreakStartSpeculation().strftime("%H:%M") + "\n"
        shiftDataStr += "Duração break: " + self.getDeltaInMinutesOrHours(self.breakDuration) + "\n"
        shiftDataStr += "Saída: " + self.endTime.strftime("%H:%M") + "\n"
        shiftDataStr += "Dia da semana: " + self.getDayOfWeek() + "\n"

        return shiftDataStr

    def getIntFromCaptureGroup(self, matches, groupName):
        value = 0
        str = matches.group(groupName)
        if (str != None):
            str = str[0:-1]
            value = int(str)
        
        return value

    def getDayOfWeek(self):
        monthNumber = ShiftData.indexesByMonth[self.month.strip()]
        weekdayIndex = datetime.datetime(2018, monthNumber, int(self.dayOfMonth)).weekday()
        weekdays = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

        return weekdays[weekdayIndex]


    def isUnusual(self):
        breakMinutes = int(self.breakDuration.total_seconds()/60)
        shiftDurationHours = self.shiftDuration.total_seconds() / 3600
        unusual = ((breakMinutes > 120 or breakMinutes < 30) or
                    (shiftDurationHours < 6 or shiftDurationHours > 10))
        return unusual;
    
    def getBreakStartSpeculation(self):
        weekDay = self.getDayOfWeek()
        
        if (weekDay == "Segunda" or weekDay == "Quinta" or weekDay == "Quarta"):
            breakStartTime = datetime.datetime(hour=11, minute=50, year=2018, month=1, day=1);
        elif (weekDay == "Terça"):
            breakStartTime = datetime.datetime(hour=14, minute=15, year=2018, month=1, day=1);
        else:
            breakStartTime = datetime.datetime(hour=15, minute=50, year=2018, month=1, day=1);

        randomOscilation = random.randint(-5, 10);
        deltaToAdd = datetime.timedelta(minutes = randomOscilation);

        breakStartTime = breakStartTime + deltaToAdd

        return breakStartTime

    def getDeltaInMinutesOrHours(self, delta):
        
        minutes = int(delta.total_seconds()/60)
        if (minutes < 60):
            formattedDelta = str(minutes) + "min"
        else:
            hours = int(minutes / 60)
            minutes = int(minutes % 60)
            formattedDelta = datetime.time(hours, minutes).strftime("%H:%M")
        
        return formattedDelta

                    

    