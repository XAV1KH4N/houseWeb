import datetime

class Bin:
    def __init__(self):
        self.refuse = datetime.datetime(2022, 1, 10) # First day of refuse bins

    def nextBins(self):
        new_date = self.nextMonday()
        return self.calc(new_date)

    def today(self):
        return datetime.datetime.today()
        #return datetime.datetime(2022,2,7)

    def nextMonday(self):
        days_ahead = self.countDown()
        return self.today() + datetime.timedelta(days_ahead)

    def countDown(self):
        days_ahead = 0 - self.today().weekday()
        if days_ahead < 0:
            days_ahead += 7
        return days_ahead

    def calc(self, date):
        days = self.diff(date)
        weeks = days//7
        return self.bins(weeks % 2 == 0)

    def diff(self, date):
        delta = date - self.refuse
        return delta.days

    def bins(self, refuse):
        days = self.countDown()

        if refuse:
            return {"Refuse": days,
                    "Recycling": days + 7,
                    "Food Waste": days}

        return {"Refuse": days + 7,
                    "Recycling": days,
                    "Food Waste": days}


