==========================================================================================================================================
Read Me
==========================================================================================================================================

Rohit Kapoor			kapoor.83@osu.edu
Nandkumar Khobare		khobare.1@osu.edu

The Ohio State University, Columbus
CSE-5243 Introduction to Data Mining - Assignment 5
==========================================================================================================================================

Requirements:
1. Assignment5 requires below for execution.
	Python 2.7
2. Make sure user has read and write access in the execution directory, output directory
   and dataset directory which contains all the data.

==========================================================================================================================================

Instructions for running program:
1. Copy all the submitted directories and makefile in a directory.

2. Open stdlinux terminal in the directory above and run below command.

make
-- This will run the python program and will output all the experiment data on the console including time taken and Mean Square error between
-- true Jaccard Similarity and k MeanHash sketch.
-- User is asked for the input for choosing value of k.

Note:
Alternatively, you can use below command directly.
cd Processor; python reader.py

IMPORTANT:
The program will run on reduced dataset. We've provided code such that grader will be able to run program fast and without any code change.
You'll be asked to choose the value for k for MinHash sketch generation.
Possible and good values are 16, 32, 64, 128 and 256. But you can choose different if desired.
No validations are being performed on the user input. Wrong choice may cause program to fail.

==========================================================================================================================================

The following files have been submitted as part of this project:
1. bs4
   This is the Beautiful Soup 4 folder. DO NOT MODIFY ANY FILES INSIDE IT.
   This is there just to remove external dependency of Beautiful Soup from our project.

2. Processor\reader.py
   This is the main program which contains the source code for obtaining desired result.
   This file has all the logic from reading dataset files above, parsing them
   for document tags such as topics, body and dateline.
   First, we calcualted Jaccard similarity between each document and stored them in memory.
   Then, we calcualted k MinHash sketch similarities for various values of k.
   K value is chosen to be 16, 32, 64, 128 and 256.
   In the end, these similarities will then be used for comparing with k MinHash sketch similarities and will be used to get
   Mean Squared Error.
   The code also contains time checkpoints to measure the performance for the experiments.

==========================================================================================================================================
User Output:
There will be no output file.
   
Console output:
Experiment data will be displayed on console.
Information such as Files parsed, No. of Shingles, No. of Documents, Jaccard Similarity generation times etc will be printed on console.
Finally, no. of similarities comparisons which will be (n-1)(n-2)/2 where n - no. of documents.

User Input:
User is allowed to choose value for k in MinHash sketch generation.

==========================================================================================================================================