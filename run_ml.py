import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import os

wd = os.getcwd()
wd = wd + '/companies/ml_files/'
for filename in os.listdir(wd):
    if filename.endswith("_ml.csv"):

        file_name = filename
        df = pd.read_csv(wd+file_name)
        df= df.fillna(0)


        X = df.drop(['price_change'], axis=1)
        # X = df.drop(['Datetime'], axis=1)
        # X = df.drop(['Search'], axis=1)
        y = df['price_change']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        lr = LinearRegression()
        lr.fit(X_train, y_train)

        y_lr_train_pred = lr.predict(X_train)
        y_lr_test_pred = lr.predict(X_test)

        lr_train_mse = mean_squared_error(y_train, y_lr_train_pred)
        lr_train_r2 = r2_score(y_train, y_lr_train_pred)
        lr_test_mse = mean_squared_error(y_test, y_lr_test_pred)
        lr_test_r2 = r2_score(y_test, y_lr_test_pred)

        lr_results = pd.DataFrame(['Linear regression',lr_train_mse, lr_train_r2, lr_test_mse, lr_test_r2]).transpose()
        lr_results.columns = ['Method','Training MSE','Training R2','Test MSE','Test R2']


        rf = RandomForestRegressor(max_depth=10, random_state=42)
        rf.fit(X_train, y_train)

        y_rf_train_pred = rf.predict(X_train)
        y_rf_test_pred = rf.predict(X_test)

        rf_train_mse = mean_squared_error(y_train, y_rf_train_pred)
        rf_train_r2 = r2_score(y_train, y_rf_train_pred)
        rf_test_mse = mean_squared_error(y_test, y_rf_test_pred)
        rf_test_r2 = r2_score(y_test, y_rf_test_pred)

        rf_results = pd.DataFrame(['Random forest',rf_train_mse, rf_train_r2, rf_test_mse, rf_test_r2]).transpose()
        rf_results.columns = ['Method','Training MSE','Training R2','Test MSE','Test R2']

        # print(pd.concat([lr_results, rf_results]))


        company = file_name.split("_")[0]
        cwd = os.getcwd()
        output_file = open(cwd+ '/outputs/testing_'+str(company)+'_10.csv',"w+")

        lr_prediction = lr.predict(X)
        rf_prediction = rf.predict(X)
        output_file.write("value,lr,rf\n")
        for i in range(len(lr_prediction)):
            output_file.write( str(df['price_change'][i]) + "," + str(lr_prediction[i]) + "," + str(rf_prediction[i]) + "\n")
        output_file.close()