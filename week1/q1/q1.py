import json
import numpy as np
import matplotlib.pyplot as plt

def inv_transform(distribution: str, num_samples: int, **kwargs) -> list:
    """ Populate the 'samples' list from the desired distribution """
    
    samples = []
    uniform_samples = np.random.uniform(0, 1, num_samples)

    if distribution == "exponential":
        # Exponential distribution with rate parameter lambda
        lam = kwargs.get("lambda", 1.0)
        samples = -np.log(1 - uniform_samples) / lam
    elif distribution == "cauchy":
        # Standard Cauchy distribution
        samples = np.tan(np.pi * (uniform_samples - 0.5))

    return samples.tolist()  # Convert to list before returning

if __name__ == "__main__":
    np.random.seed(42)

    for distribution in ["cauchy", "exponential"]:
        file_name = "q1_" + distribution + ".json"
        args = json.load(open(file_name, "r"))
        samples = inv_transform(**args)
        
        with open("q1_output_" + distribution + ".json", "w") as file:
            json.dump(samples, file)

        # Plot and save the histogram
        plt.hist(samples, bins=50, density=True)
        plt.title(f"{distribution.capitalize()} Distribution")
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.savefig(f"q1_{distribution}.png")
        plt.clf()
