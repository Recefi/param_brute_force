import pandas as pd
from ast import literal_eval


def dropStratFitData(row):
    """выводим в файл стратегии вместе с фитнесом из указанной строки лога"""

    logData = pd.read_csv("out/log.csv", index_col=0)
    stratData = pd.read_csv("strat_data.csv", index_col=0)

    indexes = logData.loc[row]['allFitIndxs']
    indexes = literal_eval(indexes)
    fits = logData.loc[row]['allFitness']
    fits = literal_eval(fits)
    fitData = pd.DataFrame({"fit": fits}, index=indexes)

    stratFitData = pd.concat([stratData, fitData], axis = 1)
    stratFitData.to_csv("out/stratFitData_" + str(row) + ".csv")


def dropFitDataByAbsVals(row):
    """выводим в файл фитнес по абсолютным значениям из указанной строки лога"""

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

        order = (absValFit[0] < absValFit[3] and absValFit[1] < absValFit[3] and absValFit[2] < absValFit[3])
        absValFit.append(order)
        fitsByAbsVals.append(absValFit)

    fitDataByAbsVals = pd.DataFrame(fitsByAbsVals, columns=["fit_pp", "fit_pm", "fits_mp", "fits_mm", "order"])
    fitDataByAbsVals.to_csv("out/fitDataByAbsVals_" + str(row) + ".csv")

    