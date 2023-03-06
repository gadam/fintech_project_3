# Sales Forecasting for Mercadolibre: Findings

### In this assignment, I applied time series analysis techniques to forecast daily sales figures for Mercadolibre using Facebook Prophet.
<br/>

## DATA: 
### Used three datasets Google Hourly search trends, Marcado daily Stock Prices and Marcado daily revenues. 
<br/>

## Method:
I uploaded the data into Pandas DataFrame and setting the "date" column as the DataFrame index. I then used hvPlot library to create a visualization of the daily sales figures.

Next, I used the Facebook Prophet algorithm to model the time series data. 

First step was to train the Prophet model on the historical sales data and used it to make predictions about future sales figures for the next quarter (90 days). Next, I created a future DataFrame and using the Prophet model generated sales forecasts for each day in the future. 

<br/>

## Results:
Prophet model generated a forecast that included best and worst case scenarios, as well as a most likely scenario. The forecast indicated that Mercado's daily sales figures were likely to range between $1.77 million and $2.12 million, with an expected daily sales figure of approximately $1.95 million