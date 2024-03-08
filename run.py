if __name__ == "__main__":
    from app.general_def import (
        selectClient,
        selectTimestamp,
        selectLogtype,
        printProcessing,
        generateCSV,
        showResults,
        setCSVFileName,
        checkForDuplicatesAndAddToDection,
        populateClientListFromCSV,
    )
    from data.config import StaticConfig
    from app.trend_def import requestLogs

    # RUN
    if StaticConfig.DEBUG == False:
        populateClientListFromCSV()
        selectClient()
        selectTimestamp()
        selectLogtype()
        printProcessing()
        requestLogs()
        checkForDuplicatesAndAddToDection()
        setCSVFileName()
        generateCSV()
        showResults()

    # RUN DEBUG
    if StaticConfig.DEBUG == True:
        selectClient()
        selectTimestamp()
        selectLogtype()
        printProcessing()
        requestLogs()
