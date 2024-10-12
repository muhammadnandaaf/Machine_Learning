## 1. File Sructures

Submission Analisis Data 1.1 (Bike Dataset)
├───Dashboard
| ├───Processed_day_df.csv
| ├───Processed_hour_df.csv
| └───dashboard.py
├───Data
| ├───Bike-sharing-dataset.zip
| ├───day.csv
| ├───hour.csv
| └───Readme.txt
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt

## 2. Project Work Cycle
1. Prepare the Library
2. Data Wrangling
   - Data Gathering
   - Assesing Data
   - Data Cleaning
2. Exploratory Data Analysis (EDA) & Clustering Analysis
   - Defined business question 
   - clustering the data to a group that have the character from business question
4. Data Visualization
   - Create data visualization to answer the business question
6. Conclusion
   - Conclude the answer from business question
8. Making Dashboard
   - Set up the DataFrame which will be used
   - Make filter components on the dashboard
   - Complete the dashboard with various data visualizations
  
## 3. Getting Started
### `notebook.ipynb`
1. Download this project.
2. Open your favorite IDE like Jupyter Notebook or Google Colaboratory.
   - Jupyter lab :
     - Open your terminal
     - Go to the path where you downloaded this file
     - Ex : cd D:this/file/to/your/path
     - Type 'jupyter lab .'
   - Google Colaboratory :
     - Create a New Notebook.
     - Upload and select the file with .ipynb extension.
     - Connect to hosted runtime.
     - Lastly, run the code cells.

### `dashboard.py`
1. Download this project.
2. Install the Streamlit in your terminal or command prompt using `pip install streamlit`.
3. Install another libraries like pandas, numpy, scipy, matplotlib, and seaborn if you haven't.
4. Please note, don't move the csv file because it acts a data source. keep it in one folder as dashboard.py
5. Open your VSCode and run the file by clicking the terminal and write it `streamlit run dashboard.py`.
