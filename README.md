# Experimentation
The goal of this exercise is to helps marketer make an informed decision while running experimentations. Company has multiple websites across the world, localized for a specific country. All websites have homepage, consumer and business homepage and checkout page. Sample size of each experiment differs with the page/country combinations as the conversion rate changes for these combinations. 

## Getting Started
Copy the python files along with the csv file to local machine

### Prerequisites
python packages required: pandas,numpy,statsmodels,dash
```
pip install dash
pip install statsmodels
```
### Preprocessing
Data needed preprocessing before the final use. There were Nulls in country column and not all columns had all three pages. Corrected typos {'checkoutn':'checkout'}.
For our analysis we use conversion from homepage to checkout page as our metric. Countries having conversion more than 1 are considered to have data issues and removed from our analysis. conversion rate anything greater than certain threshold should be considered as outliers and further analysis is needed to validate data. As we don't have access to more data, assuming that these conversion rates are valid.

### Exploration
US is the country with highest traffic in homepage and checkout page followed by DE and GB. Only US and IN has traffic from all the three webpages. Countries like ID and EG have highest conversion rate. 

### Weeks required for Experimentation
Power analysis can be used to estimate the sample size given significance value (α), power(1-β) and effect size. As we generally don't run our experiments on all of our traffic, option to choose the percentage of traffic used is provided. Once we get the sample size, it is divided by the weekly traffic to give portion of week needed to run the experiment. As week traffic is not equally divided per day, we are not giving the final results in unit of days. 

ID being the country with high conversion rate and relatively large traffic, it come out to be top in most of combinations of parameters

### Sample size by country
This chart helps the marketers to decide the duration of experiment if they have already decided the country. Imagine a new feature needs to be rolled out in a specific country, given the effect size this plot shows the sample size needed for 90,95,99 confidence intervals. We can see that more the CI more sample is needed. This plot also helps to know the power of test if we know the sample size we experimented on.


### TODO
similar analysis can be done on pages like "customer merchant home". Based on the flow of user path we can decide the conversion rate of home page and customer merchant home and calculate the sample size needed. 
