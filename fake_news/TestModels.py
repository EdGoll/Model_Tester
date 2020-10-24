from Model_01 import exec_xgboost

mat_conf, report = exec_xgboost("datasets/datos_def.xlsx","class")

print(mat_conf)
print(report)