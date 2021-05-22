from datetime import datetime, timedelta
import time

class QueryBuilder:
    def __init__(self):
        self.data = []

    def buildSqlQuery(self, configuration, configurationRows):
        baseQuery = 'SELECT Count(*) FROM Logs WHERE {}'
        conditionalQuery = ''

        # We are stripping the array of date,granulation,isPositive,count
        # since they do not provide and data for the basic filtering
        cutOffArray = configuration[:-4]

        # The date array with date,granulation for time frame filtering
        dataArray = configuration[-4:-2]

        # The flag which contains information about positive/negative filtering
        isPositive = configuration[-2] == '1'

        # The expected number of rows from the configuration
        count = int(configuration[-1])

        # If there are more than 1 dates specified, they are split and kept in the array
        splitDates = dataArray[0].split(';')
        for i, conditions in enumerate(cutOffArray):
            # Omit empty conditions
            if conditions != '-':
                equal = '' if isPositive else 'NOT '
                orOrAnd = 'OR ' if isPositive else 'AND '

                # Splitting multiple values if they are provided
                conditionsSplit = conditions.split(';')

                if len(conditionsSplit) > 1 and isPositive:
                    conditionalQuery += ' ('
                for condition in conditionsSplit:
                    # Inserting the proper data i.e. -> NOT PATH = '/' AND
                    # If the negative filtering is specified conditions are connected with 'AND'
                    # In the other case they are 'OR' conditions
                    conditionString = " {}{}='{}' {}".format(equal, configurationRows[i], condition, orOrAnd)
                    conditionalQuery += conditionString
                if len(conditionsSplit) > 1 and isPositive:
                    conditionalQuery += ')'
            # The last occurance of 'OR )' or 'OR ' is changed to end, since we are connecting
            # different filter values with the opoosite of different values for each filter
            if conditionalQuery[-4:] == 'OR )':
                conditionalQuery = ') AND '.join(conditionalQuery.rsplit('OR )', 1))
            elif conditionalQuery[-3:] == 'OR ':
                conditionalQuery = ' AND '.join(conditionalQuery.rsplit('OR ', 1))

        # Adding the dates if both the date and granulation is provided
        if ((dataArray[0] != '-') and (dataArray[1] != '-')):
            if len(splitDates) > 1:
                conditionalQuery += '('
            for date in splitDates:
                datetime_object = datetime.strptime(date, '%d/%b/%Y:%I:%M:%S%z')

                # Get and add the proper time delta to the object for time filtering
                time_change = self.getTimeDeltaFor(dataArray[1])
                new_time = datetime_object + time_change
                new_time_string = new_time.strftime('%d/%b/%Y:%I:%M:%S%z')

                # Format the query to SQL
                conditionalQuery += " date BETWEEN '{}' AND '{}' OR".format(date, new_time_string)
        else:
            # If dates were not specified there is a spare 'AND ' at the end o the query
            conditionalQuery = conditionalQuery[:-4]

        # If any dates were specified there is a spare ' OR' at the end of the query
        if conditionalQuery[-3:] == ' OR':
            conditionalQuery = conditionalQuery[:-3]

        # If more than one date was specified the braces must be closed
        if splitDates is not None:
            if len(splitDates) > 1:
                conditionalQuery += ')'

        # Add ';' at the end of the query and remove any excess spaces
        finalQueryString = baseQuery.format(conditionalQuery)
        finalQueryString += ';'
        finalQueryString = finalQueryString.replace("  ", " ").replace(" ;", ";")
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


