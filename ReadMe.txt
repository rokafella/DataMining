==========================================================================================================================================
Read Me
==========================================================================================================================================

Rohit Kapoor			kapoor.83@osu.edu
Nandkumar Khobare		khobare.1@osu.edu

The Ohio State University, Columbus
CSE-5243 Introduction to Data Mining - Assignment 4
==========================================================================================================================================

Requirements:
1. Assignment2 requires below for execution.
	Python 2.7
	NumPy 1.9.2
	SciPy 0.16.0 
	Orange 2.7.8
2. Make sure user has read and write access in the execution directory, output directory
   and dataset directory which contains all the data.

==========================================================================================================================================

Instructions for running program:
1. Copy all the submitted directories and makefile in a directory.

2. Open stdlinux terminal in the directory above and run below command.

make
-- This will run the python program and generate the feature vector output file FeatureVector.tab.
-- Then program will perform clustering experiments on data (each clustering on different distance metrics\similarity across features)	
-- User is asked for the inputs for clustering options

Note:
Alternatively, you can use below command directly.
cd Processor; python reader.py

3. Run below command in the same directory for cleaning output directory.

make clean
-- Cleans the output directory with all the files.

Note:
If you run program in a row, output FeatureVector from earler execution gets overwritten.
It is not necessary to run clean mechanism after each execution of the program but recommended.

IMPORTANT:
1.
In the beginning of program execution where import Orange takes place you might get below warning
/home/1/fuhry/local/lib/python2.6/site-packages/Orange/__init__.py:6: UserWarning: Module Orange was already imported from
/home/1/fuhry/local/lib/python2.6/site-packages/Orange/__init__.pyc, but /home/1/fuhry/local/lib/python2.6/site-packages is being added to sys.path
(At least I'm getting this warning. Not sure how to suppress it though.)
After this warning below statement takes few seconds to execute.
import pkg_resources
Do not EXIT\ABORT the program and let it do work.

2.
You'll be asked to choose clustering type first and then metrics of distance. Enter appropriate choice.
No validations are being performed on the user input. Wrong choice may cause program to fail.
If you choose clustering type as Hierarchical then you'll also get the choice for linkage viz. SINGLE, AVERAGE, COMPLETE

3.
No of centroids or clusters are taken as 77 which we found optimal during our testing. 
==========================================================================================================================================

The following files have been submitted as part of this project:
1. bs4
   This is the Beautiful Soup 4 folder. DO NOT MODIFY ANY FILES INSIDE IT.
   This is there just to remove external dependency of Beautiful Soup from our project.

2. Processor\reader.py
   This is the main program which contains the source code for obtaining desired result.
   This file has all the logic from reading dataset files above, parsing them
   for document tags, generating feature vectors and then writing them to a file.
   As part of this assignment we have converted original feature vector in a required format for the
   Orange as input.
   The feature vector created is a tab delimited file.
   In the end clustering experiments has been performed (each clustering algorithm on different metrics for distance).
   We have chosen k-means clustering and Hierarchical clustering for the experiment. For Hierarchical clustering, distance type
   for calculating similarity between features are also provided.

3. Processor\newcollections.py
   Python 2.6 don't have collections module implemented. We need Counter class from it.
   This counter class provides functionality to give frequency for input words in descending manner.
   It is very optimized than normal implementation using dictionary and then sorting out the terms.
   So to make use of it, we have copied the collections module as newcollections module which is then gets
   imported in the main program above.
   Although, this file is not necessary if you can import Counter from collections module itself.

==========================================================================================================================================
Output:
There will be a single output file.
1. FeatureVector.tab
   This output file contains the binary representation of the frequency of words in all the documents.
   We have selected 2048 words for our feature vector.
   Unlike original feature vector in Assignment1 this file is specifically modified to serve as input to the Orange Data Mining tool.
   First row is header contains all the feature names whereas second row specifies their type (d for discrete).
   Third row is optional flags. Here we have indicated that topics is class.
   Rest of the rows in the file represent the topics. Each row starts with the topic.
   Columns are the features (or words in our case but those not appearing in the topics) found in all the documents.
   We've considered only 2048 words as per the inverse document frequency ranking.
   If a particular document does not contain a word it's corresponding value against topic will be 0 else 1.
   
Console output:
Experiment data will be displayed on console.
This data includes experiments performed i.e each clustering algorithm on each metrics of distance or similarity across the feature vector.
Feature vector contains 2048 features

User Input:
User allowed options are as below
Clustering algorithm 1 is k-means clustering.
Clustering algorithm 2 is Hierarchical clustering.
Metrics of distance 1 is Euclidean
Metrics of distance 2 is Manhattan
Linkage 1 is SINGLE
Linkage 2 is AVERAGE
Linkage 3 is COMPLETE

==========================================================================================================================================