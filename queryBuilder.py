from datetime import datetime, timedelta
import time

class QueryBuilder:
    def __init__(self):
        self.data = []

    def buildSqlQuery(self, configuration, configurationRows):
        baseQuery = 'SELECT Count(*) FROM Logs WHERE{}'
        conditionalQuery = ''
        cutOffArray = configuration[:-4]
        dataArray = configuration[-4:-2]
        isPositive = configuration[-2] == '1'
        count = int(configuration[-1])
        for i, conditions in enumerate(cutOffArray):
            if conditions != '-':
                equal = '' if isPositive else 'NOT '
                orOrAnd = 'OR ' if isPositive else 'AND '
                conditionsSplit = conditions.split(';')
                if len(conditionsSplit) > 1 and isPositive:
                    conditionalQuery += ' ('
                for condition in conditionsSplit:
                    conditionString = " {}{}='{}' {}".format(equal, configurationRows[i], condition, orOrAnd)
                    conditionalQuery += conditionString
                if len(conditionsSplit) > 1 and isPositive:
                    conditionalQuery += ')'
            if conditionalQuery[-4:] == 'OR )':
                conditionalQuery = ') AND '.join(conditionalQuery.rsplit('OR )', 1))
            elif conditionalQuery[-3:] == 'OR ':
                conditionalQuery = ' AND '.join(conditionalQuery.rsplit('OR ', 1))

        if ((dataArray[0] != '-') and (dataArray[1] != '-')):
            splitDates = dataArray[0].split(';')
            if len(splitDates) > 1:
                conditionalQuery += '('
            for date in splitDates:
                datetime_object = datetime.strptime(date, '%d/%b/%Y:%I:%M:%S%z')
                time_change = self.getTimeDeltaFor(dataArray[1])
                new_time = datetime_object + time_change
                new_time_string = new_time.strftime('%d/%b/%Y:%I:%M:%S%z')
                conditionalQuery += " date BETWEEN '{}' AND '{}' OR".format(date, new_time_string)
        else:
            conditionalQuery = conditionalQuery[:-4]

        conditionalQuery = conditionalQuery[:-3]
        if len(splitDates) > 1:
            conditionalQuery += ')'

        finalQueryString = baseQuery.format(conditionalQuery)
        finalQueryString += ';'
        return (finalQueryString, count)

    def getTimeDeltaFor(self, text):
        if text == 's':
            return timedelta(seconds=1)
        elif text == 'm':
            return timedelta(minutes=1)
        elif text == 'h':
            return timedelta(hours=1)
        elif text == 'd':
            return timedelta(days=1)
        elif text == 'w':
            return timedelta(weeks=1)


