# Bangalore House Price Prediction with Linear and Ridge Regression

## Overview
This project involves predicting house prices in Bangalore using machine learning techniques. We start with basic linear regression and enhance the model using techniques like removing outliers, addressing multicollinearity, adding polynomial features, and applying ridge regression for improved performance.

## Dataset
The dataset used in this project is `BangaloreHousing.csv`. It includes various features related to house properties in Bangalore, such as the area, number of bedrooms, and the presence of amenities like a gymnasium, swimming pool, etc.

## Project Structure
- **📦 Import Libraries**: Import necessary libraries for `data manipulation`, `visualization`, and `machine learning`.
- **📊 Load Data**: Load the dataset and visualize the distribution of house prices.
- **❌ Remove Outliers**: Identify and remove extreme outliers from the `Price` column.
- **📐 Feature Selection and Standardization**: Select relevant features and standardize them.
- **📈 Train-Test Split and Linear Regression**: Train and evaluate a basic `linear regression` model.
- **🔍 Check for Multicollinearity**: Calculate `Variance Inflation Factor (VIF)` to identify `multicollinearity`.
- **✂️ Remove High VIF Features**: Remove features with `high VIF` values.
- **🔄 Recursive Feature Elimination (RFE)**: Select top features using `RFE`.
- **📉 Polynomial Features and Linear Regression**: Generate polynomial features and train a linear regression model.
- **🔗 Ridge Regression**: Train and evaluate a `ridge regression` model, with `cross-validation` for performance stability.

## Requirements
- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- statsmodels

To install the required libraries, you can use pip:
```sh
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels
```

## Running the Notebook

1. Make sure you have the required libraries installed.
2. Load the BangaloreHousing.csv dataset into the same directory as the Jupyter Notebook.
3. Run the notebook cells sequentially to reproduce the results.

```css
This `README.md` provides a comprehensive overview of your project, detailing the steps taken and the rationale behind them without including the code itself, as per your request.
```

## Methodology

### 1. 📚 Importing Libraries

### 2. 📂 Loading Data
Loading the dataset from a CSV file and display the structure of the dataset, highlighting at least the first few rows.

### 3. 📊 Visualizing the Distribution of House Prices
Histogram for the distribution of house prices. This will help to see if there are outliers.

### 4. ❌ Removing Outliers
Removing the significant outliers for the Price column to fine-tune the model and recheck the distribution.

### 5. 📐 Feature Selection and Standardization
Subsetting relevant features for the model and standardizing each feature with a mean of 0 and a standard deviation of 1.

### 6. 📈 Train-Test Splitting and Linear Regression
Splitting the data into training and test datasets, train the model using linear regression, and evaluate the model's performance using the Mean Squared Error and R-squared (R²) score.

### 7. 📊 Visualization for Linear Regression
Visualizing the Actual vs. Predicted Prices
Plotting the actual values against the predicted values for the prices with the residuals to understand how well the model works visually. Printing the coefficients and an intercept of the model.

### 8. 🔍 Checking for Multicollinearity
Calculating the Variance Inflation Factor (VIF) to determine multicollinearity among features.

### 9. ✂️ Removing High VIF Features
Variables that exhibit very high VIF values are dropped to reduce the multicollinearity and to make the model more stable.

### 10. 🔄 Recursive Feature Elimination (RFE)
Applying RFE to pick the best features contributing most to the model's prediction.

### 11. 📉 Polynomial Features and Linear Regression
Polynomial features are generated to account for the non-linearity in the relationships, and then the linear model is retrained using these features. The model is then validated on how improved it is.

### 12. 🧹 Removing Outliers from Features
Removing the values of selected features with outliers to improve the model further.

### 13. 🔗 Ridge Regression
Applying ridge regression to address/overcome overfitting - in which a regularization term is applied to linear regression . Cross-validation of model performance ensures that such performance is replicable.

Combining the Ridge regression with the linear model did a great job in its performance. The R^2 score came up to be about 0.773, which means the present model explains about 77.3% of the variation in the target variable. The cross-validated R^2 scores are not very varied, with the average being about 0.744. This means that the model generalizes well.