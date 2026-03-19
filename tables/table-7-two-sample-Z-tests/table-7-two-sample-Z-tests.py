###
title: "table-7-two-sample-Z-tests"
author: "Uyen 'Rachel' Lai and Paul Sheridan"
###



from statsmodels.stats.proportion import proportions_ztest

count = np.array([420951, 904344])
nobs  = np.array([810829, 1213606])

stat, p_value = proportions_ztest(count=count,
                                  nobs=nobs,
                                  alternative='two-sided')

print("z-stat:", stat)
print("p-value:", p_value)