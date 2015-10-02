==========================================================================================================================================
Read Me
==========================================================================================================================================

Rohit Kapoor			kapoor.83@osu.edu
Nandkumar Khobare		khobare.1@osu.edu

The Ohio State University, Columbus
CSE-5243 Introduction to Data Mining - Assignment 2
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
-- This will run the python program and generate two output tab files namely FeatureVector.tab and FeatureVector_reduced.tab.
-- Then program will perform 4 sets of experiments on data (each classifier on each type of feature vector)	

Note:
Alternatively, you can use below command directly.
cd Classifier; python reader.py

3. Run below command in the same directory for cleaning output directory.

make clean
-- Cleans the output directory with all the files.

Note:
If you run program in a row, output from earler execution gets overwrittern.
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
By default, code carries out Naive Bayes classifier experiment.
You will need to comment line 198 and uncomment line 197 and then run program to carry out experiment using k Nearest Neighbours classifier.
==========================================================================================================================================

The following files have been submitted as part of this project:
1. bs4
   This is the Beautiful Soup 4 folder. DO NOT MODIFY ANY FILES INSIDE IT.
   This is there just to remove external dependency of Beautiful Soup from our project.

2. Classifier\reader.py
   This is the main program which contains the source code for obtaining desired result.
   This file has all the logic from reading dataset files above, parsing them
   for document tags, generating feature vectors and then writing them to a file.
   As part of this assignment we have converted original feature vector in a required format for the
   Orange as input.
   Then we have created pared down version of this vector as well.
   Both these feature vectors are tab delimited files.
   In the end 4 experiments has been performed (each classifier on each type of the feature vector).
   We have chosen Naive Bayes and k Nearest Neighbours classifier for the experiment.

3. Classifier\newcollections.py
   Python 2.6 don't have collections module implemented. We need Counter class from it.
   This counter class provides functionality to give frequency for input words in descending manner.
   It is very optimized than normal implementation using dictionary and then sorting out the terms.
   So to make use of it, we have copied the collections module as newcollections module which is then gets
   imported in the main program above.
   Altough, this file is not necessary if you can import Counter from collections module itself.

==========================================================================================================================================
Output:
There will be two output files.
1. FeatureVector.tab
   This output file contains the binary representation of the frequency of words in all the documents.
   We have selected 2048 words for our full-size feature vector.
   Unlike original feature vector this file is specifically modified to serve as input to the Orange Data Mining tool.
   First row is header contains all the feature names whereas second row specifies their type (d for discrete).
   Third row is optional flags. Here we have indicated that topics is class.
   Rest of the rows in the file represent the topics. Each row starts with the topic.
   Columns are the features (or words in our case but those not appearing in the topics) found in all the documents.
   We've considered only 2048 words which has maximum frequency.
   If a particular document does not contain a word it's corresponding value against topic will be 0 else 1.
   
2. FeatureVector_reduced.tab
   This output file is just the reduced version of above FeatureVector. Instead of 2048 features we created this reduced version
   is made up of 512 features. This is for experimental purpose to see how reduced features affect the accuracy for classifiers.

Console output:
Experiment data will be displayed on console.
This data includes 4 experiments performed i.e each classifier on each type of feature vector.
Full feature vector contains 2048 features
Reduced feature vector contains 512 features
Classifier 1 is Naive Bayes
Classifier 2 is k Nearest Neighbours
Below details will be displayed for each of the combination above
1. Accuracy
2. Performance data for execution such as Training and testing time
==========================================================================================================================================