# NYC Crash Data Visualization

---

## Streamlit App link
[Click here to view the Streamlit app](https://nyc-crashdata.streamlit.app) 

---

## Introduction
This project aims to visualize and analyze traffic accident data in New York City. The main goal is to highlight the areas with the highest incidence of traffic-related injuries and fatalities, providing a clear and interactive interface for users to explore and understand the patterns in crash data. Through this analysis, we can identify dangerous streets and intersections, thereby informing policy decisions and public awareness efforts aimed at improving road safety.

---

## Data/Operation Abstraction Design
The data for this project is sourced from the [Motor Vehicle Collisions - Crashes dataset](https://catalog.data.gov/dataset/motor-vehicle-collisions-crashes) provided by the NYC Open Data portal. This comprehensive dataset compiles details on every motor vehicle collision in NYC as reported by the NYPD through the Traffic Accident Management System.

The dataset was meticulously prepared with the following procedures to enhance its clarity and utility for the app:

- **Filtering by Year**: To manage the dataset size and focus the analysis on recent trends, only collision data from the year 2022 was included.
- **Removing Null Boroughs**: Entries lacking borough specifications were excluded to ensure that the analysis would be based on geographically identifiable data.
- **Correcting Location Data**: Records with incorrect or ambiguous location details were removed, guaranteeing the geospatial accuracy necessary for the app's mapping features.
- **Ensuring Borough Linkage**: Data cleaning processes were implemented to verify that each entry contained precise information required to link it to a specific borough, which is critical for the borough-centric visualizations presented in the app.

These data preparation steps were critical in constructing a robust and reliable dataset, enabling the app to provide users with meaningful and current insights into traffic-related incidents within NYC.

---

## Future Work
The Streamlit app is an ongoing project with the following future enhancements planned:

- **Integration with Real-Time Data**: Implementing a feature to pull and display real-time accident data as it becomes available.
- **Extended Analysis**: Expanding the analysis to include factors such as weather, visibility, and road conditions.
- **User Interaction**: Allowing users to filter data by date range, time of day, or type of accident.
- **Geospatial Analysis**: Further development of geospatial visualizations to identify hotspots and trends over time.

---

## How to Use the App
Upon accessing the app, users can interact with the following features:

- **Borough Selection**: Choose a borough from the dropdown menu to highlight it on the map and load the relevent data for that specific borough in each tab.
- **Data Visualization**: View bar charts and maps that dynamically update based on the selected borough.
- **Tabs for Different Categories**: Explore categorized data on pedestrians, cyclists, and motorists.

---

## References
For further reading and context on traffic safety and the challenges faced by cyclists and pedestrians in New York City, the following resources provide valuable insights:

- [The Challenges of Bicycle Safety in New York City](https://www.bikelegalfirm.com/the-challenges-of-bicycle-safety-in-new-york-city): This article discusses the various aspects of bicycle safety in NYC, including the infrastructure and legal framework that impact cyclists.
- [New York Dangerous for Pedestrians](https://www.cellinolaw.com/blogs/new-york-dangerous-for-pedestrians/#:~:text=New%20York%20Ranks%20No.,-19%20for%20Pedestrian&text=According%20to%20the%202022%20%E2%80%9CDangerous,was%201.35%2C%20which%20is%2031st.): A blog post that examines the dangers pedestrians face in New York, backed by data and statistics that highlight the risks and the need for better safety measures.

These references were instrumental in shaping the narrative and focus of the app, underlining the importance of visualizing collision data to promote awareness and inform safer streets initiatives.



