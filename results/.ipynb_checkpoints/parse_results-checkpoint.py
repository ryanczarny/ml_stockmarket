import pandas as pd
import os

wd = os.getcwd()
output_file = open('parsed_results.csv',"w+")
output_file.write("Company,LR_Acc,LR_Wrong,RF_Acc,RF_Wrong\n")
for filename in os.listdir(wd):
    if filename.endswith(".xlsx"):
        company = filename.split("_")[1]
        df = pd.read_excel(filename,engine='openpyxl')

        lr_perc = df['lr.1'][6]
        lr_wrong = df['lr.1'][8]
        rf_perc = df['rf.1'][6]
        rf_wrong = df['rf.1'][8]

        output_file.write(str(company) + "," + str(lr_perc) + "," + str(lr_wrong) + "," + str(rf_perc) + "," + str(rf_wrong) + "\n" )
output_file.close()