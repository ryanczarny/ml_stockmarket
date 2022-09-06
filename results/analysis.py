import pandas as pd
import os

output_file = open('results.csv','w+')
output_file.write('company,lr_acc,lr_cf,rf_acc,rf_cf\n')

for filename in os.listdir('../outputs/'):
    if filename.endswith('.csv'):
        working_file = pd.read_csv('../outputs/'+filename)
        lr_tp = 0
        lr_tn = 0
        lr_fp = 0
        lr_fn = 0

        rf_tp = 0
        rf_tn = 0
        rf_fp = 0
        rf_fn = 0

        for i in range(len(working_file.value)):
            val = working_file.value[i]
            lr_val = working_file.lr[i]
            rf_val = working_file.rf[i]

            if val >= 0:
                if lr_val >= 0:
                    lr_tp += 1
                else:
                    lr_fn += 1
                if rf_val >= 0:
                    rf_tp += 1
                else:
                    rf_fn += 1
            if val < 0:
                if lr_val < 0:
                    lr_tn += 1
                else:
                    lr_fp += 1
                if rf_val < 0:
                    rf_tn += 1
                else:
                    rf_fp += 1

        total = len(working_file.value)

        lr_acc = (lr_tp + lr_tn) / total
        rf_acc = (rf_tp + rf_tn) / total

        lr_fp_perc = (lr_fp) / total
        rf_fp_perc = (rf_fp) / total

        output_file.write(str(filename.split('_')[1])+','+str(lr_acc)+','+str(lr_fp_perc)+','+str(rf_acc)+','+str(rf_fp_perc)+'\n')
                              
                              
                              