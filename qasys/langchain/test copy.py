import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Generate sample data
np.random.seed(42)
n_samples, n_features = 100, 10
X = np.random.randn(n_samples, n_features)

# Only the first 3 features are important
true_coefficients = np.array([1.5, -2.0, 3.0] + [0] * (n_features - 3))

# Generate target variable with some noise
y = X.dot(true_coefficients) + np.random.normal(0, 0.5, size=n_samples)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and fit the LASSO model
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)

# Print the coefficients
print("LASSO coefficients:", lasso.coef_)
print("Intercept (bias term):", lasso.intercept_)

# Predict on the test set
y_pred = lasso.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Plot the true coefficients vs. estimated coefficients
plt.figure(figsize=(10,6))
plt.plot(true_coefficients, 'ro', label="True coefficients")
plt.plot(lasso.coef_, 'bx', label="LASSO estimated coefficients")
plt.axhline(0, color='gray', linestyle='--')
plt.legend()
plt.title("True vs LASSO Estimated Coefficients")
plt.show()