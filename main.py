import numpy as np
import pandas as pd
import logAnalysis as la

# Считываем A и B из файла
stratData = pd.read_csv("strat_data.csv", index_col=0)  # "index_col=0" нужен для "stratData.index"
A_jun = stratData['Aj'].tolist()
A_adult = stratData['Aa'].tolist() 
B_jun = stratData['Bj'].tolist()
B_adult = stratData['Ba'].tolist() 
stratIndexes = stratData.index
# Считываем заданные оптимальные A и B из файла
optStratData = pd.read_csv("opt_strat_data.csv", index_col=0)
A_jun_opt = optStratData['Aj'].tolist()
A_adult_opt = optStratData['Aa'].tolist()
B_jun_opt = optStratData['Bj'].tolist()
B_adult_opt = optStratData['Ba'].tolist() 
optStratIndexes = optStratData.index

depth = 140
optimal_depth = 80

log = []

def genParam():
    mt = np.random.Generator(np.random.MT19937())

    s1 = mt.random()
    s2 = mt.random()

    # # для генерации коэф-ов примерно одного порядка для взрослых/молодых особей
    # exp1 = np.power(10, -mt.integers(0, 6), dtype = float)
    # exp2 = np.power(10, -mt.integers(0, 6), dtype = float)
    # exp3 = np.power(10, -mt.integers(0, 6), dtype = float)
    # exp4 = np.power(10, -mt.integers(0, 6), dtype = float)

    a_j = mt.uniform(0, 1) * np.power(10, -mt.integers(0, 6), dtype = float)
    b_j = mt.uniform(0, 1) * np.power(10, -mt.integers(0, 6), dtype = float)
    d_j = mt.uniform(0, 1) * np.power(10, -mt.integers(0, 6), dtype = float)
    g_j = mt.uniform(-1, 1) * np.power(10, -mt.integers(0, 6), dtype = float)

    a_a = mt.uniform(0, 1) * np.power(10, -mt.integers(0, 6), dtype = float)
    b_a = mt.uniform(0, 1) * np.power(10, -mt.integers(0, 6), dtype = float)
    d_a = mt.uniform(0, 1) * np.power(10, -mt.integers(0, 6), dtype = float)
    g_a = mt.uniform(-1, 1) * np.power(10, -mt.integers(0, 6), dtype = float)

    return s1, s2, a_j, b_j, d_j, g_j, a_a, b_a, d_a, g_a


def checkParam(s1, s2, a_j, b_j, d_j, g_j, a_a, b_a, d_a, g_a):
    def calcFitness(A_jun, B_jun, A_adult, B_adult, stratIndexes):
        Fitness = []
        fitIndexes = []
        for i in range(len(A_jun)):
            M1 = s1 * (A_jun[i] + depth)
            M2 = -s2 * (A_jun[i] + depth + B_jun[i]/2)
            M3 = -2*(np.pi*B_jun[i])**2
            M4 = -((A_jun[i]+optimal_depth)**2 + (B_jun[i]**2)/2)
            M5 = s1 * (A_adult[i] + depth)
            M6 = -s2 * (A_adult[i] + depth + B_adult[i]/2)
            M7 = -2*(np.pi*B_adult[i])**2
            M8 = -((A_adult[i]+optimal_depth)**2 + (B_adult[i]**2)/2)

            p = a_j*M1 + b_j*M3 + d_j*M4
            r = a_a*M5 + b_a*M7 + d_a*M8
            q = g_j*M2  # !!!
            s = g_a*M6  # !!!

            if(4*r*p+np.square(p+q-s)>=0):
                fit = -s-p-q+(np.sqrt((4*r*p+(p+q-s)**2)))

                Fitness.append(fit)
                fitIndexes.append(stratIndexes[i])

        return Fitness, fitIndexes

    Fitness, fitIndxs = calcFitness(A_jun, B_jun, A_adult, B_adult, stratIndexes)
    optFitness, optFitIndxs = calcFitness(A_jun_opt, B_jun_opt, A_adult_opt, B_adult_opt, optStratIndexes)

    optFit = -1
    errs = 0
    errIndxs = []
    errFits = []
    orderErrs = -1
    if (len(optFitness)):
        # из всех заданных в файле оптимальных стратегий рассматриваем только "самую оптимальную" при данных параметрах
        optFit = np.max(optFitness)
        # либо конкретную
        # # optFit = optFitness[0]

        for i in range(len(Fitness)):
            if (Fitness[i] > optFit):
                errs += 1
                errIndxs.append(fitIndxs[i])
                errFits.append(Fitness[i])
        
        # проверяем корректность на всех абсолютных значениях
        """стратегии для каждого абс.значения должны быть проиндексированы в порядке: 0:(?,?),1:(?,?),2:(?,?),3:(-,-)"""
        orderErrs = 0
        for i in range(len(Fitness)):
            if (fitIndxs[i] % 4 == 3):
                orderErr = 0
                for j in range(1, 4):
                    if (i-j < 0):
                        break
                    for k in range(j, 4):
                        if (fitIndxs[i-j] == fitIndxs[i] - k):
                            if (Fitness[i-j] > Fitness[i]):
                                orderErr = 1
                orderErrs+=orderErr
    else:
        # если ни одна из заданных оптимальных стратегий при данных параметрах не вычисляется
        errs = -1

    print(s1, s2, a_j, b_j, d_j, g_j, a_a, b_a, d_a, g_a, errs, orderErrs)
    log.append([s1, s2, a_j, b_j, d_j, g_j, a_a, b_a, d_a, g_a, optFitIndxs, optFitness, optFit, errs, errIndxs, errFits, fitIndxs, Fitness, orderErrs])


checkParam(1, 1, 0.0016, 0.0000007, 0.000016, 0.00008, 0.006, 0.000000075, 0.00006, 0.004)
checkParam(1, 1, 0.0016, 0.0000007, 0.000016, -0.00008, 0.006, 0.000000075, 0.00006, -0.004)
checkParam(0.25, 0.003, 0.0016, 0.0000007, 0.000016, 0.00008, 0.006, 0.000000075, 0.00006, 0.004)
checkParam(0.25, 0.003, 0.098, 0.0000006, 0.0003, 0.003, 0.616, 0.000035, 0.0003, 0.006)
checkParam(0.25, 0.003, 0.098, 0.0000006, 0.00003, 0.003, 0.012, 0.000035, 0.00003, 0.006)
checkParam(0.25, 0.003, 0.0245, 0.0000006, 0.00003, 0.003, 0.012, 0.000035, 0.00003, 0.006)

# i = 0
# for i in range(100000):
#     s1, s2, a_j, b_j, d_j, g_j, a_a, b_a, d_a, g_a = genParam()
#     checkParam(s1, s2, a_j, b_j, d_j, g_j, a_a, b_a, d_a, g_a)

logData = pd.DataFrame(log, columns=["s1", "s2", "a_j", "b_j", "d_j", "g_j", "a_a", "b_a", "d_a", "g_a", "optFitIndxs", "optFitness", "optFit", "errs", "errIndxs", "errFits", "allFitIndxs", "allFitness", "orderErrs"])
logData.to_csv("out/log.csv")

la.dropStratFitData(0)
la.dropFitDataByAbsVals(0)
la.dropStratFitData(1)
la.dropFitDataByAbsVals(1)
