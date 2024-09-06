<div align="center">
<h3> Integrating emerging technologies deployed at scale within prospective life-cycle assessments</h3>
<div align="center">
<img src="https://github.com/MargotCha/Integrated-LCA-master/blob/main/graphical%20abstract.png" width="600" />
</div>


<div align="left">

---

### 📖  Description

The repository contains data files and tailored notebooks and codes to create the LCI database and reproduce the results presented in the article.
DOI: https://doi.org/10.1016/j.spc.2024.08.016
<div align="center">

*Charalambous et al.*, 2024. <span style="color:orange">Integrating emerging technologies deployed at scale within prospective life-cycle assessments.</span>

</div>

---


## 📂 Repository Structure

```sh
└── Integrated-LCA-master/
    ├── .gitignore
    ├── LICENSE
    ├── Notebooks/
    │   └── Setting up/ 
    │      └── 01-Setup non-integrated LCA.ipynb
    │      └── 02-Setup integrated LCA.ipynb
    │   └── Calculations/
    │      └── 01-Non-integrated LCA calculation.ipynb
    │      └── 02-Integrated LCA calculations.ipynb
    │   └── Fetching info/
    │      └── 01-Diesel market regional share.py
    │      └── 02-Diesel market share.py
    │      └── 03-Synthetic diesel market share.py
    │   └── Plotting/ 
    │      └── 01-Main-manuscript.ipynb
    │      └── 02-Supplementary.ipynb
    │   └── Examples/
    │      └── example_notebook.ipynb
    ├── Data/
    │   └── LCIA/     
    ├── IntLCA/
    │   ├── __init__.py
    │   ├── IntLCA.py
    │   └── utils/
    ├── README.md
    ├── environment.yml
    ├── graphical_abstract.png

```


---

## ⚙️ Documentation

📍 The [Data](https://github.com/MargotCha/Integrated-LCA-master/tree/main/Data) folder includes:

- The [LCIA](https://github.com/MargotCha/Integrated-LCA-master/tree/main/Data/LCIA) folder→ Three excel files that are used for creating or updating the LCIA method.

📍 The [Notebooks](https://github.com/MargotCha/Integrated-LCA-master/tree/main/Notebooks) folder includes:
- [Setting up](https://github.com/MargotCha/Integrated-LCA-master/tree/main/Notebooks/Setting%20up) folder → Notebooks to create the databases
- [Calculations](https://github.com/MargotCha/Integrated-LCA-master/tree/main/Notebooks/Calculations) folder → Notebooks to calculate LCA impacts
- [Examples](https://github.com/MargotCha/Integrated-LCA-master/tree/main/Notebooks/Examples) folder → Notebook that shows how to perform integrated LCA with matrices
- [Plotting](https://github.com/MargotCha/Integrated-LCA-master/tree/main/Notebooks/Plotting) folder → Notebooks to plot the LCA impacts
- [Fetcing info](https://github.com/MargotCha/Integrated-LCA-master/tree/main/Notebooks/Fetching%20info) folder → Notebooks to fetch information from the environmental databases

📍 The [IntLCA](https://github.com/MargotCha/Integrated-LCA-master/tree/main/Notebooks) folder  → Includes a  package created to perform integrated LCA. The file includes utils folder with all the modules required.


---
## 🔧 Installation

To install the IntLCA package use pypi:

```sh
pip install IntLCA-dev
```

---
## 🚀 Usage

To ensure the replication of the results presented in the article, it is highly recommended starting a new environment. 

### 1. Set Up the Environment

Using Anaconda, build the environment using `environment.yml`:

```bash
conda env create -f environment.yml
```
Details on how to use  the package are provided in the corresponding notebooks.
Reach out if you encounter issues!


