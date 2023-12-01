import pandas as pd
import numpy as np
import fastf1
import time

fastf1.Cache.enable_cache("./cache")


def timer(func):
    def wrapper():
        timeStart = time.time()
        func()
        timeEnd = time.time() - timeStart
        print(f"{timeEnd} seconds")

    return wrapper()


'''Retreives all info for a driver that can be stored into a pandas dataframe'''


def buildDataFrame(session, driver):
    """
    session is a tuple (year, race, sessionType)
    driver is their 3-lettered name
    """
    driver = driver.upper()
    try:
        assert isinstance(session, tuple)
        year, race, sessionType = session
        sessionInfo = fastf1.get_session(year, race, sessionType)
        sessionInfo.load()
        LapCategories = sessionInfo.laps.columns.array
    except(TypeError):
        raise AssertionError(
            "session is set incorrectly please ensure it is in the format \"(year, race, sessionType)\"")

    Time = sessionInfo.laps.pick_driver(driver).Time
    DriverNumber = sessionInfo.laps.pick_driver(driver).DriverNumber
    LapTime = sessionInfo.laps.pick_driver(driver).LapTime
    LapNumber = sessionInfo.laps.pick_driver(driver).LapNumber
    PitOutTime = sessionInfo.laps.pick_driver(driver).PitOutTime
    PitInTime = sessionInfo.laps.pick_driver(driver).PitInTime
    Sector1Time = sessionInfo.laps.pick_driver(driver).Sector1Time
    Sector2Time = sessionInfo.laps.pick_driver(driver).Sector2Time
    Sector3Time = sessionInfo.laps.pick_driver(driver).Sector3Time
    Sector1SessionTime = sessionInfo.laps.pick_driver(driver).Sector1SessionTime
    Sector2SessionTime = sessionInfo.laps.pick_driver(driver).Sector2SessionTime
    Sector3SessionTime = sessionInfo.laps.pick_driver(driver).Sector3SessionTime
    SpeedI1 = sessionInfo.laps.pick_driver(driver).SpeedI1
    SpeedI2 = sessionInfo.laps.pick_driver(driver).SpeedI2
    SpeedFL = sessionInfo.laps.pick_driver(driver).SpeedFL
    SpeedST = sessionInfo.laps.pick_driver(driver).SpeedST
    IsPersonalBest = sessionInfo.laps.pick_driver(driver).IsPersonalBest
    Compound = sessionInfo.laps.pick_driver(driver).Compound
    TyreLife = sessionInfo.laps.pick_driver(driver).TyreLife
    FreshTyre = sessionInfo.laps.pick_driver(driver).FreshTyre
    Stint = sessionInfo.laps.pick_driver(driver).Stint
    LapStartTime = sessionInfo.laps.pick_driver(driver).LapStartTime
    Team = sessionInfo.laps.pick_driver(driver).Team
    Driver = sessionInfo.laps.pick_driver(driver).Driver
    TrackStatus = sessionInfo.laps.pick_driver(driver).TrackStatus
    IsAccurate = sessionInfo.laps.pick_driver(driver).IsAccurate
    LapStartDate = sessionInfo.laps.pick_driver(driver).LapStartDate

    availableColumns = sessionInfo.laps.columns
    df = pd.DataFrame([Time, DriverNumber, LapTime, LapNumber, PitOutTime,
                       PitInTime, Sector1Time, Sector2Time, Sector3Time, Sector1SessionTime,
                       Sector2SessionTime, Sector3SessionTime, SpeedI1,
                       SpeedI2, SpeedFL, SpeedST, IsPersonalBest, Compound,
                       TyreLife, FreshTyre, Stint, LapStartTime,
                       Team, Driver, TrackStatus, IsAccurate, LapStartDate]).T

    if len(availableColumns) != len(df.columns):
        if len(availableColumns) > len(df.columns):
            print("unused columns exists that are not in the dataframe")
    return df


# if we provide the list of drivers we can create a dict with all pit stop laps

def pitstopLap(session, driver):
    lapCat, sessionInfo = getInfo(session, driver)

    stops = []
    try:
        Compound = sessionInfo.laps.pick_driver(driver).Compound
        TyreLife = sessionInfo.laps.pick_driver(driver).TyreLife
        prevTyreAge = 0
        if Compound.array:

            prevCompound = Compound.array
            for lap in range(Compound.size):

                if TyreLife.array[lap] < prevTyreAge or Compound.array[lap] != prevCompound:
                    if lap == 0:
                        lap = 1
                    stops.append(lap)
                prevCompound = Compound.array[lap]
                prevTyreAge = TyreLife.array[lap]
    except:
        print(f"Data Not Available for {driver}")
    return stops


'''used to retrieve all information to be used in a non-permanent state or other defined functions'''


def getInfo(session, driver):
    driver = driver.upper()
    try:
        assert isinstance(session, tuple)
        year, race, sessionType = session
        sessionInfo = fastf1.get_session(year, race, sessionType)
        sessionInfo.load()
        LapCategories = sessionInfo.laps.columns.array
    except(TypeError):
        raise AssertionError(
            "session is set incorrectly please ensure it is in the format \"(year, race, sessionType)\"")
    return LapCategories, sessionInfo


# print(buildDataFrame((2022, 'Abu Dhabi', 'R'), "NOR"))
# print(pitstopLap((2022, 'Abu Dhabi', 'R'), "NOR"))

def getResults(session):
    try:
        assert isinstance(session, tuple)
        year, race, sessionType = session
        sessionInfo = fastf1.get_session(year, race, sessionType)
        sessionInfo.load()
        resultCategories = sessionInfo.results.columns.array
    except(TypeError):
        raise AssertionError(
            "session is set incorrectly please ensure it is in the format \"(year, race, sessionType)\"")

    driverAbbreviations = sessionInfo.results.Abbreviation.array
    grandPrixName = []
    for i in range(len(driverAbbreviations)):
        grandPrixName.append(race)

    endPosition = sessionInfo.results.Position.array
    startPosition = sessionInfo.results.GridPosition.array
    finished = sessionInfo.results.Status.array
    availableColumns = sessionInfo.laps.columns

    df = pd.DataFrame([driverAbbreviations, grandPrixName, finished, startPosition, endPosition]).T
    df.columns = ["Driver", "Race","Status", "Start", "End"]
    if len(availableColumns) != len(df.columns):
        if len(availableColumns) > len(df.columns):
            print("unused columns exists that are not in the dataframe")
    return df

# x = getResults((2022, 'Bahrain', 'R'))
#
#
# driverAbbreviations = ["ALB", "ALO", "BOT", "DEV", "FIT", "GAS", "HAM", "HUL", "KUB", "KVY", "LAT", "LEC", "MAG", "NOR",
#                        "OCO", "PER", "RIC", "RUS", "SAI", "SCH", "STR", "TSU", "VER", "VET", "ZHO"]
# pitstops = {}

# for driver in driverAbbreviations:
#     pitstops[driver] = pitstopLap((2021, 'Hungary', 'R'),driver)
#     print(pitstops)
