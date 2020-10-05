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

3. Since I was looking at portions of total ID's available I chose to use the Pearson's correlation coefficientfor a sample vs population as defined here: ![Sample PCC](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#For_a_sample). The Pearson correlation distance is 1 - this value. 
    a. 1 - the first formula (Eq. 3 on the Wikipedia Page under 'For a Sample') is implemented in method `_calculate_r_value(self, set_a, set_b) -> float:` of the ` class Pearson_Correlation_Distance():` using sets to reduce runtime.

4. Once implemented I created basic tests and a naive for-loop (SLOW method) to check calculations against the (FAST method) described in #3 above. These tests can be ![found in this file](https://github.com/tmatrixhy/gphk-take-home/blob/main/notebooks/colab_/2020.10.1-Graphika-Initial_Exploration.ipynb) at the bottom. The Markdown in the file explains what is being performed.

#### Results for smaller dataset (CF_docl_matrix.json):
```
Average SLOW method time (ms):  329.4571097691854
Average FAST method time (ms):  0.19491275151570636

Total   SLOW method time (ms):  98837.13293075562
Total   FAST method time (ms):  58.473825454711914

Average Error                :  6.93012314201269e-14
```
Using the optimized method, the average speed of calculations has been around 1-1.5 minutes on most machines for the smaller dataset.

There was a noted speedup of 1690x on the colab machine between the naive for-loop and the optimized calculation using sets.

Note the error between the two methods is described as the absolute value of their differences. abs ( r_dist_slow - r_dist_fast ). I could not reduce this figure anymore.

#### Results for larger dataset (AB_docl_matrix.json):
![The processing time using the optimized method can be found here](https://github.com/tmatrixhy/gphk-take-home/blob/main/notebooks/jupyter/2020.10.3-Graphika_Large_File_Output_Generator.ipynb).
It came to roughly 1.5 hours (5581196.881 ms) on my home machine.

[Download link for adjacency matrix.](https://drive.google.com/file/d/1HiTQjGAL-RRLSB7lhu_bzGoMk_kLYk8a/view?usp=sharing)
[Download link for adjacency list.](https://drive.google.com/file/d/1YTaVTKhtSlr8BBdB404_uu-B_5UN9UXn/view?usp=sharing)

Please note these files might require permissions as they're hosted on my University's Google Drive account. If this does not work please let me know where I can upload the files so you may view them.

#Quesiton 2
The best method I could come up with for storing the data within the program was a dictionary of sets instead of lists. Using sets optimizes for quick comparisons between two sets since there is a O(1) lookup factor.

The program I have written boils down to a single method that compares two sets of sparse vectors represented by indices where the value is either '0' or '1' and outputs a single number representing similarity between those two.

To me the execution of this mini program can be built directly into the database system. As far as I can understand the dataflow this problem currently requires is as follows:

1. API that collects data from sources such as Twitter, Reddit, x. 
2. There is a stored feature list where this inputdata is compared against. If the data from the source is flagged as having this feature, the index number is added to the user_id. This process yields a sparse feature vector.
3. For static analysis at a given time it makes sense to collect all user_id's under question in a file such as the json which was provided and exporting to csv's where its easy to import the file once again. Some things that can be done to reduce file size:
    a. Data compression for output using zip files rather than direct csv output. The code can be factored to open a zip file directly.
    b. Store based on importance of user: Linked Lists could be used to represent users, with trees formed based on similarity distance calculated. Only save trees which are determined to be significant. 
4. Streaming analysis is also possible on a batch basis (Ex: 30 minute batch) through the following manner:
    a. Implement the optimized distance calculation directly on the database (this is possible in PostgreSQL and many other commercial database systems through various programming languages).
    b. On every batch the database takes all users with updated feature vectors and re-calculates their similarity.
    c. For Relational Databases: save these distances in a table with the time as the 'primary key'.
    d. Use time series analysis to see similarity in "real-time".

# Question 3

I attempted to optimize the speed prior to submission but was running against time for this take home exercise. The method which I started, ![and can be found here](https://github.com/tmatrixhy/gphk-take-home/blob/main/notebooks/jupyter/2020.10.3-Graphika_Ray_Experiments.ipynb), was to use the ![ray](https://github.com/ray-project/ray) library. This feature rich library allows for the parallelization and distribution of tasks. 

1. For the first method of optimization In our senario, I would have liked the `_calculate_r_value(self, set_a, set_b) -> float:` method to be distributed evenly amongst all cpus available and later if any other nodes in a cluster were avaialble. Unfortunately, I believe the current hangup in code lies in the way that I am pre-processing the data. I believe the fix to making this run efficiently with the current code requires segementation the data prior to executing the ray methods.

2. I would like to explore the cosine similarity on this problem versus pearson coorelation distance. Since I have not used pearson coorelation distance before it is something that I do not have an intuitive feel for. As for cosine similarity, I had previously encountered this in university when we were discussing the netflix movie recommender system which won an award.

3. After discussing both pearson correlation distance and cosine similarity on this problem with the team and gaining a deeper understanding of what we're actually measuring; I would begin doing further literature review for better clustering methods using sparse feature vectors.

For a littler clarification on number 3 above, I would personally like to see the users and their features for two comparable clusters generated with each #1 and #2. 