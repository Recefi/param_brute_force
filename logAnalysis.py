import pandas as pd
from ast import literal_eval


def writeStratFitData(row):
    """
    выводим в файл стратегии вместе с фитнесом из указанной строки лога
        работает только с первым вариантом лога и только если он не слишком большой
    """

    logData = pd.read_csv("out/log.csv", index_col=0)
    stratData = pd.read_csv("strat_data.csv", index_col=0)

    indexes = logData.loc[row]['allFitIndxs']
    indexes = literal_eval(indexes)
    fits = logData.loc[row]['allFitness']
    fits = literal_eval(fits)
    fitData = pd.DataFrame({"fit": fits}, index=indexes)

    stratFitData = pd.concat([stratData, fitData], axis = 1)
    stratFitData.to_csv("out/stratFitData_" + str(row) + ".csv")


def writeFitDataByAbsVals(row):
    """
    выводим в файл фитнес по абсолютным значениям из указанной строки лога
        работает только с первым вариантом лога и только если он не слишком большой
    """

    logData = pd.read_csv("out/log.csv", index_col=0)

    indexes = logData.loc[row]['allFitIndxs']
    indexes = literal_eval(indexes)
    fits = logData.loc[row]['allFitness']
    fits = literal_eval(fits)

    i = 0
    k = 0
    fitsByAbsVals = []
    while(i < len(fits)):
        absValFit = []
        for j in range(0, 4):
            if(k % 4 == indexes[i] % 4):
                absValFit.append(fits[i])
                i+=1
                k+=1
            else:
                absValFit.append(0)
                k+=1

        best = ""
        if ((absValFit[0] != 0 and absValFit[1] != 0 and absValFit[2] != 0 and absValFit[3] != 0)):
            if ((absValFit[0] < absValFit[3] and absValFit[1] < absValFit[3] and absValFit[2] < absValFit[3])):
                best = "(-,-)"
            else: 
                if ((absValFit[0] < absValFit[2] and absValFit[1] < absValFit[2] and absValFit[3] < absValFit[2])):
                    best = "(+,-)"
                else:
                    if ((absValFit[0] < absValFit[1] and absValFit[2] < absValFit[1] and absValFit[3] < absValFit[1])):
                        best = "(-,+)"
                    else:
                        if ((absValFit[1] < absValFit[0] and absValFit[2] < absValFit[0] and absValFit[3] < absValFit[0])):
                            best = "(+,+)"

        absValFit.append(best)
        fitsByAbsVals.append(absValFit)

    fitDataByAbsVals = pd.DataFrame(fitsByAbsVals, columns=["fit(+,+)", "fit(-,+)", "fit(+,-)", "fit(-,-)", "the best"])
    fitDataByAbsVals.to_csv("out/fitDataByAbsVals_" + str(row) + ".csv")

    