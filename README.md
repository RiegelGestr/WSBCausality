# The causal role of the Reddit collective action on the GameStop short squeeze  Repository

![alt text](https://github.com/RiegelGestr/WSBCausality/blob/main/pic.png)

This repository contains the code and data necessary to reproduce the analysis presented in the paper titled "[The dynamics of the Reddit collective action leading to the GameStop short squeeze]". 
The repository is organized into two main folders: `main` and `supp`.

📝[Papert]([https://arxiv.org/abs/2401.14999](https://doi.org/10.1038/s44260-025-00029-z))


## Main Folder

The `main` folder contains the code for reproducing the analysis of the main text of the paper:
- **`fig/`**: This folder contains the figures reproduced by the scripts starting with "fig_".
- **`data/`**: This folder contains the data used in the analysis. Some data may not be included in this repository (screenshot) but can be found by contacting us via email [you can find it in the paper].
- The Python scripts starting with "fig_" reproduce the figures used in the main text, while the remaining scripts perform the core analysis
## Supp Folder

The `supp` folder contains multiple sub-folders, each dedicated to the analysis of a specific section in the supplementary material of the paper. In each folder there is a figure folder **`fig/`**, containing the figure, and a data folder **`data/`**, containing the data used for the analysis
## Requirements

- **`requirements_python.txt`**: Python dependencies required for the main analysis.
  - Install with `pip install -r requirements_python.txt`.
- **`requirements_julia.txt`**: Julia dependencies required for specific Julia scripts.
  - Install with `julia -e 'using Pkg; Pkg.activate("."); Pkg.instantiate()'` or the equivalent Julia package manager command.

## Data Availability

The raw screenshot data are no present in this repository. We will release the data on Zenodo soon.
For any questions or issues, please create an issue in the GitHub repository or contact us by email.
