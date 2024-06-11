# 🏡 ML Model - House Price Data with SKLearn

This project demonstrates a machine learning model to predict house prices in Bangalore using the API in SKLearn. It includes the following: data processing, feature engineering, and model training for different libraries in Python. The project has a Streamlit application that gives better working provision to the model.

## 📂 Files Description

1. **🏷 bengaluru_house_prices.csv**: Dataset containing the house prices in Bangalore with various features.
2. **📦 feature_names.pkl**: The pickle file that stores the feature names of the model.
3. **📦 house_price_model.pkl**: A pickle file containing the developed model of machine learning.
4. **📦 unique_locations.pkl**: PThis pickle file contains the unique locations data.
5. **🐍 model_training.py**: Python code containing the complete implementation of data processing, feature engineering, and model training.
6. **🐍 model_training_with_prints.py**: A Python file with the same code as in model_training.py but improved by using more print.
7. **🐍 app.py**: Python script to run the trained model and make predictions with Streamlit.

## 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LuciferAsh98/AI-ML-Learning-Path/
   ```

2. **Train the model:**
Run model_training.py or model_training_with_prints.py to train the model.

   ```bash
python model_training.py
   ```

💻 Execute App Locally on WebApp

```bash
streamlit run app.py
```

Enter House Details to get the PRICE. Enjoy !! 🎉


# 🏡 Real Estate Price Prediction - Technical Description

## 📊 Data Preprocessing and Model Training

The statistics preprocessing and version training process includes the subsequent steps:

1. **Dropping Unnecessary Columns:** Columns like `society` and `availability` are dropped as they do now not contribute to the rate prediction.

2. **Handling Missing Values:** Missing values are dealt with as it should be to ensure the facts is smooth for education.

3. **Feature Engineering:**
    - **BHK Extraction:** Extracting the quantity of bedrooms from the `size` column.
    - **Converting Total Square Feet:** Converting the `total_sqft` column to numerical values.
    - **Removing Outliers:** Removing outliers based totally at the square ft in keeping with BHK and charge in keeping with square toes.
    - **Location Preprocessing:** Grouping much less frequent places under `different`.
    - **Removing BHK Outliers:** Removing outliers unique to BHK and location.
    - **Encoding Categorical Variables:** Encoding place and location kind columns the usage of one-hot encoding.

4. **Model Training:** Using a pipeline with Polynomial Features and Ridge Regression to train the version.

## 🖼 Data Visualizations

The script `model_training_with_prints.Py` consists of print statements and visualizations for better know-how:

- **Initial Data:** Displays the initial few rows of the dataset.
- **Data after Dropping Unnecessary Columns:** Shows facts after dropping columns.
- **Handling Missing Values:** Displays facts after coping with lacking values and adding BHK.
- **Converting Total Square Feet:** Shows facts after changing `total_sqft` to numerical values.
- **Removing Outliers and Adding `price_per_sqft`:** Displays information after outlier elimination and including `price_per_sqft`.
- **Location Preprocessing:** Shows information after location preprocessing.
- **Removing Price according to Sqft Outliers:** Displays statistics after putting off outliers based on fee in step with square ft.
- **Removing BHK Outliers:** Shows data after disposing of BHK-particular outliers.
- **Final Cleaned Data:** Displays the very last cleaned dataset.
- **Data after Encoding Categorical Variables:** Shows statistics after encoding categorical variables.
- **Training and Testing Data Shapes:** Displays the shapes of schooling and checking out datasets.
- **R2 Score:** Prints the R2 rating of the trained model.
- **Actual vs Predicted Prices Plot:** A scatter plot comparing actual vs expected charges.

## 💻 Technologies Used

- **Python:** Programming language used for growing the version and the app.
- **Pandas:** For statistics manipulation and analysis.
- **Numpy:** For numerical computations.
- **Scikit-learn:** For building the gadget mastering model.
- **Joblib:** For model serialization.
- **Streamlit:** For developing the interactive web app.
- **Matplotlib:** For statistics visualization.