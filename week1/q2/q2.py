import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def PCA(init_array: pd.DataFrame, dimensions: int = 2):
    """ Perform PCA on the init_array and reduce it to the specified number of dimensions """
    
    # Standardize the data (zero mean)
    standardized_data = (init_array - init_array.mean()) / init_array.std()

    # Compute the covariance matrix
    covariance_matrix = np.cov(standardized_data, rowvar=False)

    # Compute the eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Sort the eigenvalues and eigenvectors in descending order
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    # Select the top 'dimensions' eigenvectors
    selected_eigenvectors = sorted_eigenvectors[:, :dimensions]

    # Transform the data
    final_data = np.dot(standardized_data, selected_eigenvectors)

    return sorted_eigenvalues, final_data

if __name__ == '__main__':
    init_array = pd.read_csv("pca_data.csv", header=None)
    sorted_eigenvalues, final_data = PCA(init_array)

    # Save the transformed data
    np.savetxt("transform.csv", final_data, delimiter=',')

    # Print the sorted eigenvalues
    for eig in sorted_eigenvalues:
        print(eig)

    # Plot and save a scatter plot of the final_data
    plt.scatter(final_data[:, 0], final_data[:, 1])
    plt.title("PCA Scatter Plot")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.savefig("out.png")
    plt.show()
