import numpy.random


class clCapacityReleasePolicy(object):
    __maxCapacity = 10
    __lstDayTypes = [4, 7]
    __planningHorizonLength = 4
    __policyDict = {}

    def __init__(self, avgRate=5.5, theta=7 / 5, policyType=2):
        # this is to run multiple tests
        if theta == 1:
            self.__lstDayTypes[0] = avgRate
            self.__lstDayTypes[1] = avgRate
        else:
            self.__lstDayTypes[0] = (2 - theta) * avgRate
            self.__lstDayTypes[1] = theta * avgRate
        # enter capacity release policy for each day type
        for dayType in self.__lstDayTypes:
            self.__policyDict[dayType] = {}
            # initally release nothing
            self.__addCapacity(dayType, self.__planningHorizonLength + 1, 0)
            # on the last day release maximum
            self.__addCapacity(dayType, 0, self.__maxCapacity)

        # call proper policy function
        print policyType
        policy = getattr(self, "add_policy_"+str(policyType), None)
        if policy is not None:
            policy()
        else:
            print "Policy not found, defaulting to policy 1"
            self.add_policy_1()

        # now add sorted lists of capacity adjustments
        for dayType in self.__lstDayTypes:
            tempSortedList = sorted(list(self.__policyDict[dayType].keys()))
            print dayType, self.__policyDict[dayType]
            numKeys = len(tempSortedList) - 1
            # and check that the capacity released is not increasing
            for j in range(numKeys):
                key1 = tempSortedList[j]
                key2 = tempSortedList[j + 1]
                assert self.__policyDict[dayType][key1] >= self.__policyDict[dayType][
                    key2], "capacity released must not decrease as appointment day approaches"

    # TODO: Add automated policy creation for longer horizons?

    def add_policy_1(self):
        """
        A policy object will consist of:
            a list of days until the date
            a list of the capacity to be released
        This will allow for quick creation of different policies and easy
        implementation.
        :return:
        """

        days_from_today = [self.__planningHorizonLength]
        cap_released = [[self.__maxCapacity]] * len(self.__lstDayTypes)

        self.add_capacities(self.__lstDayTypes, days_from_today, cap_released)

    def add_policy_2(self):
        #### adding policy for the first day type

        days_from_today =  [4, 3, 2, 1]
        cap_released =    [[6, 7, 8, 9]]*len(self.__lstDayTypes)

        self.add_capacities(self.__lstDayTypes, days_from_today, cap_released)

    def add_policy_3(self):
        #### adding policy for the first day type

        days_from_today =  [4, 3, 2, 1]
        cap_released =    [[2, 4, 6, 8]]*len(self.__lstDayTypes)

        self.add_capacities(self.__lstDayTypes, days_from_today, cap_released)


    def add_policy_4(self):
        #### adding policy for the first day type

        days_from_today =  [4, 3, 2, 1]
        cap_released =    [[0, 1, 4, 7]]*len(self.__lstDayTypes)

        self.add_capacities(self.__lstDayTypes, days_from_today, cap_released)

    def add_policy_5(self):
        # get low and high day types
        dayTypeLow, dayTypeHigh = self.__lstDayTypes[0], self.__lstDayTypes[1]

        days_from_today =  [4, 3, 2, 1]
        cap_released    = [[6, 7, 8, 9],  # LOW
                           [2, 4, 6, 8]]  # HIGH

        self.add_capacities([dayTypeLow, dayTypeHigh], days_from_today, cap_released)

    def add_policy_6(self):

        dayTypeLow = self.__lstDayTypes[0]
        dayTypeHigh = self.__lstDayTypes[1]

        # list of days from today
        daysFromToday =  [4, 3, 2, 1]
        capReleased    = [[2, 4, 6, 8],    # LOW
                           [6, 7, 8, 9]]    # HIGH

        self.add_capacities([dayTypeLow, dayTypeHigh], daysFromToday, capReleased)

    def add_capacities(self, lstDayTypes, lstDaysFromToday, lstCapacityReleased):
        """
        Apply the capacity policy to the simulation.
        :param lstDayTypes: list of day types
        :param lstDaysFromToday: list of days from today, has corresponding capacity to be released
        :param lstCapacityReleased: list of capacities to be released
        :return:
        """

        assert len(lstDayTypes) == len(lstCapacityReleased), "too many capacity release schedules"
        assert len(lstDaysFromToday) == len(lstCapacityReleased[0]), "day must have corresponding capacity"
        # add capacities for each day type
        for i, dayType in enumerate(lstDayTypes):
            for j, daysUntil in enumerate(lstDaysFromToday):

                # perform error checking
                assert lstCapacityReleased[i][j] <= self.__maxCapacity, "cannot release more than " + self.__maxCapacity + " slots"
                assert daysUntil <= self.__planningHorizonLength + 1, "days ahead cannot be greater than " + self.__planningHorizonLength + 1
                if j > 0:
                    assert self.__policyDict[dayType][daysUntil+1] <= max(0, lstCapacityReleased[i][j]), "capacity cannot decrease as time goes on"

                self.__policyDict[dayType][daysUntil] = max(0, lstCapacityReleased[i][j])



    def getCapToRelease(self, dayTypeKey, daysTilTodayKey):
        if dayTypeKey in self.__policyDict.keys():
            if daysTilTodayKey in self.__policyDict[dayTypeKey].keys():
                return self.__policyDict[dayTypeKey][daysTilTodayKey]
        return 0

    def getLenPlanningHorizon(self):
        return self.__planningHorizonLength

    def getNumDayTypes(self):
        return len(self.__lstDayTypes)

    def getLstDayTypes(self):
        return self.__lstDayTypes


class clAppointmentSimulation(object):

    def __init__(self, maxDelayAcute, probFollowUpNeeded, minDelayFollowUp, onePeriodCancelProb, probCancelAnnounced,
                 theta, policyType):

        # average demand
        averageAcuteDemand = 8.5 * (1. - probFollowUpNeeded)
        # initialize capacity release policy
        self.capReleasePolicy = clCapacityReleasePolicy(averageAcuteDemand, theta, policyType)
        # get data from capacity release policy for easy access
        self.lenPlanningHorizon = self.capReleasePolicy.getLenPlanningHorizon() + 1
        self.numDayTypes = self.capReleasePolicy.getNumDayTypes()
        self.lstDayTypes = self.capReleasePolicy.getLstDayTypes()
        # set the parameters for the simulaton
        clDay.initializeClassParameters(probFollowUpNeeded, minDelayFollowUp, maxDelayAcute, onePeriodCancelProb,
                                        probCancelAnnounced, self.capReleasePolicy, 0)

        # structure for rolling horizon scheduling
        self.planningHorizon = {}
        for i in range(self.lenPlanningHorizon):
            self.planningHorizon[i] = clDay(i)

        # structures for keep track of output
        self.lstUtilized = []
        self.lstAcuteRefused = []
        self.lstFollowupRefused = []
        self.lstAcuteRequests = []
        self.lstFollowUpRequests = []
        self.lstApptsCancelled = []
        self.lstCancelAnnounced = []
        self.lstScheduled = []
        self.lstDebugReleasedCapacity = []

        self.myResultsDict = {'probFollowUpNeeded': probFollowUpNeeded, 'onePeriodCancelProb': onePeriodCancelProb,
                              'probCancelAnnounced': probCancelAnnounced, 'theta': theta, 'policy': policyType}

    def runSimulation(self, numPeriods):
        for i in range(numPeriods):
            self.advanceDay()
        self.myResultsDict['utilization'] = sum(self.lstUtilized) / numPeriods
        self.myResultsDict['% average acute refused'] = 100 * sum(self.lstAcuteRefused) / sum(self.lstAcuteRequests)
        if sum(self.lstFollowUpRequests) > 0:
            self.myResultsDict['% average follow up refused'] = 100 * sum(self.lstFollowupRefused) / sum(
                self.lstFollowUpRequests)
        else:
            self.myResultsDict['% average follow up refused'] = "not applicable"
        self.myResultsDict['average number cancelled'] = sum(self.lstApptsCancelled) / numPeriods
        return self.myResultsDict

    def advanceDay(self):
        # what day are we on now
        currentDay = clDay.getCurrentDay()
        # keep track of total cancellations
        ttlApptCancelled = 0
        ttlCancelAnnounced = 0
        # go over all the days in the horizon and cancel some of the appointments
        for d in range(currentDay, currentDay + self.lenPlanningHorizon):
            modIndex = d % self.lenPlanningHorizon
            # release capacity
            self.planningHorizon[modIndex].releaseCapacity()
            # cancel some of the previously scheduled appointments
            (apptsCancelled, cancelAnnounced) = self.planningHorizon[modIndex].cancelScheduled()
            ttlApptCancelled = ttlApptCancelled + apptsCancelled
            ttlCancelAnnounced = ttlCancelAnnounced + cancelAnnounced
        # record total cancellations
        self.lstApptsCancelled.append(ttlApptCancelled)
        self.lstCancelAnnounced.append(ttlCancelAnnounced)
        # generate new requests for appointments
        thisDayIndex = currentDay % self.lenPlanningHorizon
        (numAcuteRequests, acuteScheduled, acuteToSchedule, followUpToSchedule) = self.planningHorizon[
            thisDayIndex].generateApptRequests()
        self.lstUtilized.append(self.planningHorizon[thisDayIndex].anticipatedUtilized)
        self.lstScheduled.append(self.planningHorizon[thisDayIndex].scheduled)
        self.lstDebugReleasedCapacity.append(self.planningHorizon[thisDayIndex].releasedCap)
        self.lstAcuteRequests.append(numAcuteRequests)
        self.lstFollowUpRequests.append(followUpToSchedule)

        # schedule the appointments over the other days
        for d in range(currentDay + 1, currentDay + self.lenPlanningHorizon):
            if acuteToSchedule == 0 and followUpToSchedule == 0:
                break
            modIndex = d % self.lenPlanningHorizon
            (acuteToSchedule, followUpToSchedule) = self.planningHorizon[modIndex].scheduleAcuteAndFollowUp(
                acuteToSchedule, followUpToSchedule)

        # after we are done record how many acute and follow-up were refused
        self.lstAcuteRefused.append(acuteToSchedule)
        self.lstFollowupRefused.append(followUpToSchedule)
        # advance the day
        clDay.advanceCurrentDay()
        # reinitialize current day to use again
        self.planningHorizon[thisDayIndex].initialize(currentDay + self.lenPlanningHorizon)
        return None

    def printMyResults(self):
        print("average last day capacity " + str(sum(self.lstDebugReleasedCapacity) / n))
        print("average appointments utilized  " + str(sum(self.lstUtilized) / n))
        print("average number cancelled  " + str(sum(self.lstApptsCancelled) / n))
        print("% average cancellations announced " + str(
            100 * sum(self.lstCancelAnnounced) / sum(self.lstApptsCancelled)) + "%")
        print("average acute requests " + str(sum(self.lstAcuteRequests) / n))
        print("% average acute refused " + str(100 * sum(self.lstAcuteRefused) / sum(self.lstAcuteRequests)) + "%")
        print("average follow up requests " + str(sum(self.lstFollowUpRequests) / n))
        print("% average follow-up refused " + str(
            100 * sum(self.lstFollowupRefused) / sum(self.lstFollowUpRequests)) + "%")


class clDay(object):
    # one day's capacity
    # is a class variable
    # there is just one variable for the whole class
    __maxDelayAcute = None
    __minDelayFollowUp = None
    __probFollowUpNeeded = None
    __currentDay = None
    __onePeriodCancelProb = None
    __probCancelAnnounced = None
    __capReleasePolicy = None

    @classmethod
    def initializeClassParameters(cls, probFollowUpNeeded, minDelayFollowUp, maxDelayAcute, onePeriodCancelProb,
                                  probCancelAnnounced, capReleasePolicy, currentDay=0):
        cls.__probFollowUpNeeded = probFollowUpNeeded
        assert maxDelayAcute >= 0, "delay for acute must be non-negative"
        cls.__maxDelayAcute = maxDelayAcute
        assert minDelayFollowUp > 0, "delay for follow up must be at least 1 day"
        cls.__minDelayFollowUp = minDelayFollowUp
        cls.__onePeriodCancelProb = onePeriodCancelProb
        cls.__probCancelAnnounced = probCancelAnnounced
        cls.__capReleasePolicy = capReleasePolicy
        cls.__currentDay = currentDay

    @classmethod
    def advanceCurrentDay(cls):
        cls.__currentDay = cls.__currentDay + 1

    @classmethod
    def getCurrentDay(cls):
        return cls.__currentDay

    def __init__(self, simulationDay):
        self.initialize(simulationDay)

    def initialize(self, simulationDay):
        self.rateAcute = self.__capReleasePolicy.getLstDayTypes()[
            simulationDay % self.__capReleasePolicy.getNumDayTypes()]
        self.simulationDay = simulationDay
        self.scheduled = 0
        self.anticipatedUtilized = 0
        self.releaseCapacity()

    def generateApptRequests(self):
        # acute requests are random
        numAcuteRequests = numpy.random.poisson(self.rateAcute)
        # schedule acute requests
        acuteScheduled = min(self.releasedCap - self.scheduled, numAcuteRequests)
        assert acuteScheduled >= 0, "error, more scheduled then released capacity"
        # modify anticipated utilization
        self.anticipatedUtilized = self.anticipatedUtilized + acuteScheduled
        self.scheduled = self.scheduled + acuteScheduled
        # now figure out how many would need follow-up
        followUpNeeded = numpy.random.binomial(self.anticipatedUtilized, self.__probFollowUpNeeded)
        return (numAcuteRequests, acuteScheduled, numAcuteRequests - acuteScheduled, followUpNeeded)

    def scheduleAcuteAndFollowUp(self, acuteNeededToSchedule, followUpNeededToSchedule):
        acuteRemainingToSchedule = acuteNeededToSchedule
        followUpRemainingToSchedule = followUpNeededToSchedule
        daysTillAppt = self.simulationDay - self.__currentDay
        if daysTillAppt <= self.__maxDelayAcute:
            acuteScheduled = max(0, min(self.releasedCap - self.scheduled, acuteNeededToSchedule))
            assert acuteScheduled >= 0, "error, more acute scheduled then released capacity"
            self.scheduled = self.scheduled + acuteScheduled
            self.anticipatedUtilized = self.anticipatedUtilized + acuteScheduled
            acuteRemainingToSchedule = acuteNeededToSchedule - acuteScheduled
        if daysTillAppt >= self.__minDelayFollowUp:
            followUpScheduled = max(0, min(self.releasedCap - self.scheduled, followUpNeededToSchedule))
            assert followUpScheduled >= 0, "error, more follow up scheduled then released capacity"
            self.scheduled = self.scheduled + followUpScheduled
            self.anticipatedUtilized = self.anticipatedUtilized + followUpScheduled
            followUpRemainingToSchedule = followUpNeededToSchedule - followUpScheduled
        return (acuteRemainingToSchedule, followUpRemainingToSchedule)

    def cancelScheduled(self):
        # see if there is something that can be cancelled
        if self.anticipatedUtilized <= 0:
            return (0, 0)
        # only the appointments that have not yet been cancelled can be cancelled
        apptsCancelled = numpy.random.binomial(self.anticipatedUtilized, self.__onePeriodCancelProb)
        # cancellations can be announced when appointments are cancelled
        cancelAnnounced = numpy.random.binomial(apptsCancelled, self.__probCancelAnnounced)
        # cancelled appointment slots will not be utilized
        self.anticipatedUtilized = self.anticipatedUtilized - apptsCancelled
        # if cancellation is announced, the slot is available
        self.scheduled = self.scheduled - cancelAnnounced
        return (apptsCancelled, cancelAnnounced)

    def releaseCapacity(self):
        self.releasedCap = self.__capReleasePolicy.getCapToRelease(self.rateAcute,
                                                                   self.simulationDay - self.__currentDay)
        return self.releasedCap


if __name__ == "__main__":

    maxDelayAcute = 2
    minDelayFollowUp = 2
    n = 1000
    lstResults = []
    myResultDict = {}

    # TODO: Test over a range of values ?

    for probFollowUpNeeded in [0.2, 0.5]:
        for onePeriodCancelProb in [0.1, 0.25]:
            for probCancelAnnounced in [0.3, 0.7]:
                for theta in [1, 1.2, 1.5]:
                    for policyType in [1, 2, 3, 4, 5, 6]:
                        # initialize random number generator, so we can get repeatable results
                        numpy.random.seed(1234)
                        # run the test
                        test = clAppointmentSimulation(maxDelayAcute, probFollowUpNeeded, minDelayFollowUp,
                                                       onePeriodCancelProb, probCancelAnnounced, theta, policyType)
                        lstResults.append(test.runSimulation(n))

    import pandas as pd

    df = pd.DataFrame(lstResults)
    from pandas import ExcelWriter

    writer = ExcelWriter('PythonExport.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()


