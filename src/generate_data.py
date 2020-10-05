import numpy as np
import sys
import csv 
import json
import math
import time

class Pearson_Correlation_Distance():
  _id_list = [] # List of Anonymized Twitter ID's
  _data_set = {} # Set version of original data
  _max_feature = float('-inf') # maximum value in feature column
  _adjacency_matrix = None
  _adjacency_list = []
  
  def __init__(self, data):
    """
      Input: data : Dictionary in the following format: 
                    { index_value : [list of non-empty column names], ... }

        data pre-processing = O( n * max(m) )
        n = # of keys (index_value) in dictonary.
        m = len( [list of non-empty column names] ) in dictionary
    """
    for key in data: #O(n)
      # create list of ID's
      self._id_list.append(key) #O(1)

      # convert list to set
      self._data_set[key] = set(data[key]) #O(m)
      
      # keep track of the maximum value of feature (ID 'interests')
      self._max_feature = max(self._max_feature, max(self._data_set[key])) #O(m)
    
    # sort id list for cleaner, currently sorts by 'string' need to conv to 'int' ?
    self._id_list.sort()

    # Add 1 to max_feature to account for 0'th element
    self._max_feature += 1

    # Create empty adjacency matrix
    self._adjacency_matrix = np.zeros((len(self._id_list), len(self._id_list)))

  def _calculate_r_value(self, set_a, set_b) -> float:
    """
    Input:
      set_a : A vector of object type 'set' where elements represent indices 
              of a sparse vector.
      set_b : A vector of object type 'set' where elements represent indices 
                of a sparse vector.

      returns : An float representing the Pearson coorelation distance 
                  as defined in the supporting README.md

    """
    # length of set_a is the same as the sum of all 'x'
    sig_x = len(set_a)

    # mean of all set_a values = sum of all x / total feature count
    avg_x = sig_x / self._max_feature

    # do same calculations for 'y'
    sig_y = len(set_b)
    avg_y = sig_y / self._max_feature

    # Senario A: x = 1, y = 1  
    # -- Intersection Time Complexity (Avg): O(min(len(a), len(b)))
    sen_a = set_a.intersection(set_b) 
    numerator = len(sen_a) * ((1-avg_x) * (1-avg_y))
    denom_x = len(sen_a) * ((1-avg_x)**2)
    denom_y = len(sen_a) * ((1-avg_y)**2)

    # Senario B: x = 1, y = 0  
    # -- Difference Time Complexity (Avg): O(len(a))
    sen_b = set_a.difference(set_b)  
    numerator += len(sen_b) * ((1-avg_x) * (-avg_y))
    denom_x += len(sen_b) * ((1-avg_x)**2)
    denom_y += len(sen_b) * ((-avg_y)**2)

    # Senario C: x = 0, y = 1  
    # -- Difference Time Complexity (Avg): O(len(b))
    sen_c = set_b.difference(set_a)
    numerator += len(sen_c) * ((-avg_x) * (1-avg_y))
    denom_x += len(sen_c) * ((-avg_x)**2)
    denom_y += len(sen_c) * ((1-avg_y)**2)

    # Senario D: x = 0, y = 0  
    # -- Union Time Complexity (Avg): O(len(a) + len(b))
    sen_d = (self._max_feature - len(set_a.union(set_b)))
    numerator += sen_d * (avg_x * avg_y)
    denom_x += sen_d * (avg_x**2)
    denom_y += sen_d * (avg_y**2)

    denominator = math.sqrt(denom_x * denom_y)

    return 1 - (numerator / denominator)

  def create_matrix(self):
    """
      Create adjacency matrix and adjacency list of Pearson correlation 
          distance from stored data.

      Processing: O( 
                     ((len(id_values)^2) / 2 - len(id_values)) * 
                      max(len([list of non-empty column names])) * 2
                   )      
    """
    max(len([list of non-empty column names])) * 2
    start_time = time.time()

    for x in range(0,len(self._id_list)):
      for y in range(x+1, len(self._id_list)):
        self._adjacency_matrix[x][y] = self._calculate_r_value(self._data_set[self._id_list[x]], 
                                                         self._data_set[self._id_list[y]])
        self._adjacency_list.append([self._id_list[x], self._id_list[y], self._adjacency_matrix[x][y]])

    print("Time to Execute (ms): ", str((time.time() - start_time)*1000))

  def save(self):
    """
      Saves Class @pram _adjacency_matrix & _adjacency_list to CSV.
    """
    # Save Adjacency Matrix to CSV File
    try:
      with open('adjacency_matrix.csv', 'w', newline='') as fh:
        writer = csv.writer(fh, delimiter=',')
        writer.writerow(self._id_list)
      
        for x in self._adjacency_matrix:
          writer.writerow(x)
    
      csv_columns = ['id_1','id_2', 'PCD']
      
      with open('adjacency_list.csv', 'w', newline='') as fh:
        writer = csv.writer(fh, delimiter=',')
        writer.writerow(csv_columns)

        for x in self._adjacency_list:
          writer.writerow(x)
      
      print("Output files have been generated in base directory.")
    except:
      print("Could not save file.")

def main():
  """
  usage: python3 generate_data.py [input_file]
          -- input_file   - adjacency list in json file with { index_value : [list] ...} format 
          -- output_files - adjacency_matrix.csv + adjacency_list.csv
  
  output: 'matrix' = csv with MxM upper triangular matrix
                      row 0 identify's user_id
                      [user_id_1][user_id_2] = PCD
          'list'   = csv with adjacency list in 
                     { (user_id_1 , user_id_2): PCD }
                      
            PCD == Pearson correlation distance
  """
  if len(sys.argv) < 2:
    print("usage: python3 generate_data.py [input_file] [output_file]")
    print("       -- input_file  - adjacency list in json file with")
    print("                 { index_value : [list] ...} format")
    sys.exit()

  input_file = sys.argv[1]

  try:
    with open(input_file) as bg_file:
      data = json.load(bg_file)
  except:
    print("Error opening data file.")

  PCD = Pearson_Correlation_Distance(data)

  PCD.create_matrix()

  PCD.save()

  sys.exit()
if __name__ == '__main__':
  main()