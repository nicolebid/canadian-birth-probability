# The Probability of Being Born in Canada

By Nicole Bidwell

## About

This analysis explores the likelihood of being born in Canada in a particular year and delves deeper to discover trends in birth probabilities over time. The summary, explanation, and interpretation of the analysis can be viewed in the report linked below. The report also describes the scripts used in the analysis. Further comments are included within each script for clarity.

The analysis is implemented in a data pipeline, with all the scripts in the `src` folder. Steps to reproduce the analysis by running the data pipeline locally are outlined below.

## 📄 Report 

The interactive HTML version of the report can be viewed [here](https://nicolebid.github.io/canadian-birth-probability/canadian_birth_probability.html).

## ⚙️ Reproducing the Analysis

This analysis can be run locally using a virtual environment. All required dependencies are listed in the [environment file](environment.yml). If you would like to set up the environment and run the pipeline to retrieve the data and obtain results in the `output` folder, follow the steps below.

### Set up

1. Clone the repository.

```
git clone https://github.com/nicolebid/canadian-birth-probability.git
```

2. Install the dependencies by running the following command from the root of the directory.

```
conda env create -f environment.yml
```

3. Activate the virtual environment. 

```
conda activate canadian-birth-probabilities
```
4. Run the scripts using the following commands (in order).

```
python -m src.retrieve_load
python -m src.calculate_probabilities
python -m src.graphs
```