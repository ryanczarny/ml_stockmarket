
import os

wd = os.getcwd()

for filename in os.listdir(wd):
    if not filename.endswith(".py") and filename.endswith(".csv"):
        file_name = filename

        output_file = open('ml_files/' + str(file_name.split(".")[0]) + "_ml.csv","w+")
        output_file.write('Article_Count,Stock_value,Pos_Words,Neg_Words,YouTube_Vids,YT_Pos_Words,YT_Neg_Words,price_change\n')

        d=[]
        file_name = open(file_name)
        for line in file_name:
            line = line.split(",")
            if len(line) == 9 and not 'Date' in line[0] and line[len(line)-1] != None:
                d.append(line)
        for i in range(len(d)):
            line = d[i]
            line[6] = line[6].replace("\n","")
            line[len(line)-1] = line[6].replace("\n","")
            if i == 0:
                line.append(0)
            else:
                line.append(int(d[i][3]) - int(d[i-1][3]))
            for j in range(len(line)):
                if j > 1:
                    output_file.write(str(line[j]))
                    output_file.write(",")
            output_file.write("\n")
        output_file.close()