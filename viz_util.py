import statsmodels.stats.api as sms
import pandas as pd
import os
import numpy as np


#read the file each line and split by "," to get each column
def read_data():
    with open(os.path.dirname(__file__) +"\\data\\country_page_traffic.csv", "r+") as d:
        flag = 0
        for i in d.readlines():
            if flag == 0:
                columns = i.strip("\n").strip("'ï»¿").strip('"').split(",")
                df = pd.DataFrame(columns=columns)
                flag += 1
            else:
                df.loc[flag - 1, :] = i.strip("\n").strip('"').split(",")
                flag += 1
    df["acq_weekly_traffic"] = df["acq_weekly_traffic"].astype(float)
    return df

#function to clean data
def clean_data(df) :
    #for our analysis we need traffic for both homepage and checkout
    #dropping rows with NUll
    clean_data = df.dropna()

    #clean_data = clean_data[clean_data["country_code"] != "CN"]

    #correcting typo
    clean_data["page"] = clean_data["page"].replace({"Checkoutn": "Checkout"})

    clean_data = clean_data[clean_data["country_code"] != ""]

    return clean_data

#function to get data of countries with all three pages
def get_country_all_pages(df) :
    df = df[df["country_code"].isin(df[df["page"] == 'Customer Merchant Home']["country_code"])]
    df = df.pivot_table("acq_weekly_traffic", "country_code", "page").reset_index().dropna()
    return df.sort_values("PayPal Home",ascending=False)

#function to calculate the conversion
# traffic of checkout/traffic of homepage
def get_conversions(df) :

    cd = df.pivot_table(values="acq_weekly_traffic", columns="page", index="country_code").reset_index()

    cd = cd.drop("Customer Merchant Home", axis=1)

    cd = cd.dropna()

    cd["conversion"] = cd["Checkout"] / cd["PayPal Home"]

    cd = cd[cd["conversion"] < 1]

    return cd

#function to calculate the sample size for each country given selected parameters
def get_sample_size(conversions,minimum_effect_size, alpha, beta,traffic_used) :

    conversions["sample_size"] = conversions.apply(lambda x : sample_calculator(x["conversion"]*100,minimum_effect_size,alpha,beta),axis=1)

    conversions["weeks_for_sample_size"] = conversions["sample_size"]/(conversions["PayPal Home"]*(traffic_used/100.0))

    conversions["weeks_for_sample_size"] = conversions["weeks_for_sample_size"].apply(lambda x : round(x,3))

    conversions.sort_values("weeks_for_sample_size",ascending=True,inplace=True)

#function to calculate the sample size for selected country and scale of Beta values
def get_sample_size_custom(conversions,selected_country,minimum_effect_size, alpha,):

    selected_country_df = conversions[conversions["country_code"]==selected_country]

    beta = np.linspace(0, 1, 100)[1:99]

    sample_req = [sample_calculator(selected_country_df["conversion"].values[0]*100,minimum_effect_size,alpha,i) for i in beta]

    return sample_req


#Base sample calculator
def sample_calculator(conversion_rate, minimum_effect_size, alpha, beta):
    p1 = conversion_rate / 100.0
    p2 = p1 + (p1 * ((minimum_effect_size) / 100.0))

    es = sms.proportion_effectsize(p1, p2)

    return int(sms.NormalIndPower().solve_power(es, power=1 - beta, alpha=alpha, ratio=1))
