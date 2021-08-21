# Data Exploration

In the education industry, high schools prepare students for the next chapter in his or her life. Aside from GPA, SAT scores assist in measuring learned skills, knowledge and prestige in institutions. Using student data from high schools in Massachusettes and various national universities, how well prepared are high school students in Massachuesettes for universities in United States. Furthermore, is Massachuesettes' Accountability and Assistance level a reliable indicator of education quality compared to universities in Massachuesettes?

Location: Data Science Graduate Course at KU
Dates: Aug 29th, 2018 to Sep 10, 2018

## Goal
* Determine preparedness of Massachuesettes high school students for U.S. universities
* Determine reliability of  Massachuesettes' Accountability and Assistance level as an indicator of preparedness

## Data
1. [High schools in Massachusettes](https://www.kaggle.com/ndalziel/massachusetts-public-schools-data#MA_Public_Schools_2017.csv). The data viewed are SAT scores and accountability/assistance levels.
2. [Universities in the United States](https://www.kaggle.com/theriley106/university-statistics). Contains average SAT scores of the current students as well as the state.


## Process Techniques
In this project...
* I performed data rangling on the two data sets (i.e., normalized features, combined data sets, removing unrelevant entries, randomizing entries) 
* I sampled scores to reduce time complexity of calculating across the entire data set.
* Correlated SAT scores between HS and Universities as well as Accountability and Assistance Level versus SAT through box plot analysis.

## Results
Based on the SAT provided by high schools and universities, high schools are on par with universities throughout the nation, but slightly unpar with universities in Massachusettes. Comparing high schools to national universities, the medians greatly overlap. Unfortunately the schools consistently score lower than the median of universities in Massachusettes. Furthermore, the levels of accountability and assistance assigned do correlate with SAT scores such that lower median scores are ranked lower. Even with the highest high school level, the schools perform about average for universities.

## Repository Contents

| Directory | Description |
| --- | ----------- |
| Data | Contains all of the datasets used in this project. |
| Libraries | If libraries are used, the exact distribution will be located here. Includes library, library name, and library version. |
| Models | Models generated for the project such as machine learning models. |
| Notebooks | Notebooks used for visualing the data. |
| Reports | The resulting reports on this project. |
| Src | Source scripts and other helper files located here. |


