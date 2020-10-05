# Graphika Take Home

Results of the take home project.


#Installation & Run

Project utilizes Python=3.8.6.

Extract .zip to directory.
```
    pip install -r requirements.txt
```

#Usage

From command line:
```
    python3 .\src\generate_data.py .\data\[input_file]
```

Input: 
```
    -- [input_file]   - adjacency list in json file with { index_value : [list] ...} format.
                        ex: CF_docl_matrix.json
```

Output:
```
    -- output_files - adjacency_matrix.csv + adjacency_list.csv
        'matrix' = MxM upper triangular matrix.
                    row 0 identify's user_id
                    [user_id 1][user_id 2] = PCD
          'list' = Adjacency list with each row in 
                    [user_id 1, user_id 2, PCD] format.
                      
            PCD == Pearson correlation distance
```

#Directory & Files

```
Directory structure:

┌───data
│       CF_docl_matrix.json
│           └───|# Data file given for analysis
|
├───notebooks
│   ├───colab_
│   │       2020.10.1-Graphika-Initial_Exploration.ipynb
|   |           └───|# Experiments utilizing Google Colab - Initial Exploration & PCD Tests
|   |
│   │       2020.10.3-Graphika-Parallel_Execution.ipynb
|   |           └───|# Experiments utilizing Google Colab - Initial Parallellization Attempt
│   │
│   └───jupyter
│           2020.10.3-Graphika_Large_File_Output_Generator.ipynb
|               └───|# Used to generate results of larger dataset (AB_docl_matrix.json) 
|
│           2020.10.3-Graphika_Ray_Experiments.ipynb
│               └───|#- Local experiments with Ray - Works but not optimized at all.
|
├───results_csv
│       adjacency_list.csv
|           └───|# PCD of CF_docl_matrix.json in Adjacency List format.
|
│       adjacency_matrix.csv
|           └───|# PCD of CF_docl_matrix.json in Adjacency Matrix format.
│
├───src
│       generate_data.py
|           └───|# Python script to generate PCD.
|
└─  README.md
```

#Question 1

1. I approached this problem by first researching Pearson correlation distance. It was not a metric I had used before therefore I tried to gain a sense of what we were trying to accomplish by generating this data using this specific metric.

2. Examined the dataset to determine how 'big' of a sparse matrix I would have to work with. For the smaller json file (CF_docl_matrix.json) the max index value was 459316, for the larger file (AB_docl_matrix.json) the max index value was 45453.

3. Since I was looking at portions of total ID's available I chose to use the Pearson's correlation coefficientfor a sample as defined here: ![Sample PCC](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#For_a_sample)