# covidTO 

This a web app backed by Flask and hosted on Firebase with custom domain name curtosy of Domain.com with a backend in Python

## Problem Tackled

Predict the counts of each Toronto neighbourhood and which neighbourhoods are expected to have outbreaks a day to days in advance.

## Approach
### Data Collection
Data was collected from publicaaly available souces listed below.

* Neighbourhood Data:
    * [https://open.toronto.ca/dataset/neighbourhoods/](https://open.toronto.ca/dataset/neighbourhoods/)
    
* Toronto Covid Data:
    * [https://open.toronto.ca/dataset/covid-19-cases-in-toronto/](https://open.toronto.ca/dataset/covid-19-cases-in-toronto/)
    
### Build Model - Neuarl Network
##### Assumptions:
1. data without a valid neighbourhood name was not considered
2. we assumed the case remained in the neighbourhood for 2 weeks 
3. if the result was fatal or the person was was ever hospitalized we assumed it lasted 1 week.

*These assumptions were made based on data of the contageous period of covid as well as if a person is in hospital or no longer alive then they cannot infect their neighbourhood this data was gathered from [CBC Covid progression](# https://www.cbc.ca/news/health/typical-covid-19-progression-1.5546949 approx 7 days after symptoms you get hospitalized]*

Using tactics from the set up of open source chess engines Leela and Maia, the data was created in "map" form to preserve spatial relations between neighbourhoods.

A map is of shape 3x45x45 with channels as follows:
1. Case counts where the counts are displayed in array indicies that would fall into the corresponding neighbourhood (image displaying point-neighbourhood correlation shown below). *Note: areas outside of the map were given a value of 0*
2. Outbreak present shown with 1s in respective neighbourhoods
3. Calendar week of prediction date to preserve timing relations

![image](https://user-images.githubusercontent.com/60823286/116826347-8d8df400-ab61-11eb-8f04-496cd95ea273.png)

Model inputs were 13x45x45 channels as follows:
* 1-3: Current map
* 3-12: Last 3 maps
* 13 array of 0s and 1s where the ones are only in indicies that overlap *Image shown above for clarity*

![image](https://user-images.githubusercontent.com/60823286/116826056-215ec080-ab60-11eb-927e-90c4799eee53.png)

The network was trained for 5 steps with a batch size of 10 for both count and outbreak modeling.

The average error on count prediction was 15.7% and the average percision and recall for prediction outbreaks is 0.88 and 0.87 respectively.

### Make Publically Accessible
The website can be access through [covidto.tech](covidto.tech)

Firebase was used for hosting. Since the code was done with python, Flask combined with Google Cloud was used as a bridging language to allow for a dynamic webpage through Firebase hosting.

The website is a work in progress as I was entirely new to Firebase, Flask and Google Cloud. The intention is to have someone be able to look at past outbreak and count trends, as well as look ahead on where trends can lead, both on graph and map views.
