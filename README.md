# Laptop Price Prediction using K-Fold Cross Validation

This repository contains a machine learning project that predicts laptop prices based on data collected from [torob.com ↗️](https://torob.com/). The project utilizes the K-Fold Cross Validation technique to evaluate and improve the model's performance. The project utilizes data scraping techniques to collect laptop specifications and corresponding prices from the website. Using this data, a machine learning model is trained to accurately predict the price of a laptop given its specifications. This project also determines the best option among the dataset based on the desired features, using cosine similarity.

## Dataset

The dataset used for training and evaluation is obtained by scraping product listings from torob.com. The dataset includes the following features:

- Laptop brand
- Laptop model
- CPU specification
- RAM size
- Storage capacity
- Display size
- Graphics card
- Price

The dataset is preprocessed to handle missing values, categorical variables, and feature scaling as necessary. It is split into training and testing sets to evaluate the machine learning model's performance.

## Model Development

The machine learning model employed in this project is a regression model. Several regression algorithms are considered, including linear regression, decision tree regression, random forest regression, and gradient boosting regression. The models are trained and evaluated using appropriate performance metrics such as mean squared error (MSE) and R-squared.

To enhance the model's performance, feature engineering techniques, such as feature selection and dimensionality reduction, are applied. Additionally, hyperparameter tuning is performed to optimize the model's parameters.

## Results
The project aims to predict laptop prices accurately using K-Fold Cross Validation. The notebook provides detailed insights into the data analysis, preprocessing techniques, feature engineering, model selection, and evaluation metrics. The results include the model's performance measures such as mean absolute error (MAE), root mean squared error (RMSE), and R-squared score.


## Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- The developers would like to acknowledge [torob.com ↗️](https://torob.com/) for providing the data used in this project.
- The project structure and implementation are inspired by various machine learning tutorials and resources available online.
