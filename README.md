# Spam Detection - Text Classification

## Objective

The goal of this project is to classify text data from three different languages (English, French, and German) as either "Spam" or "Ham" (not spam). Using a machine learning model, we aim to accurately classify the dataset based on text features. The dataset is provided in a CSV file named `Task1.csv`.

## Dataset

The dataset consists of text messages labeled as "Spam" or "Ham" in three languages: English, French, and German.

##  Workflow

### 1. Data Loading & Preprocessing

- **Load the dataset:** Use Pandas to load the CSV file into a DataFrame.
- **Missing values:** Check for missing values and clean or remove them as necessary.
- **Balancing the dataset:** Ensure the dataset is balanced. If the dataset is imbalanced, apply techniques such as oversampling, undersampling, or using class weights in the model.

### 2. Feature Extraction

- **Vectorization:** Use `TfidfVectorizer` to convert the text data into numerical representations. The vectorizer should handle multiple languages.
- **Language-agnostic vectorization:** Ensure that the vectorization process works well across all languages (English, French, and German).

### 3. Model Training

- **Logistic Regression:** Train a Logistic Regression model using the preprocessed text data. Understand the principles of logistic regression to better implement and tune the model.
  
### 4. Model Evaluation

- **Accuracy:** Print the accuracy of the trained model.
- **Confusion Matrix:** Create a confusion matrix to visualize the model’s classification performance for "Spam" and "Ham" labels.

