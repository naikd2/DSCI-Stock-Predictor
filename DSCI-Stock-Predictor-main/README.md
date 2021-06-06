# DSCI-Stock-Predictor


Capstone 1 includes the Data Acquistion, Pre-Processing, and EDA of our project.  The project is in regards to predicting the movement in stock price based on the language of social media posts.  As seen we break down our folders into Code, Data, Reports, and the Presentation.  With the Reports and Presentation being self explanatory, we will explain what is in the Code and Data Folders.

Code Folder:

	-   Additional Code = These are pieces of code that were used for eventually compiled into the Project Code

	-   4 Months Reddit Posts_Comments Combined = The first analysis included Reddit Posts and Stock data from January-April of 2020.  This code includes 		    Preprocessing and EDA.

	-   8 Mos and Post and Comments Separated = This folder includes analysis from October 2020-May 2021.  In addition, the Posts and Comments in this analysis 		have been separated into their own objects in all Preprocessing and EDA.

Data Folder:

	-   Yahoo Finance = This folder the Finance Data from our 4 companies we did analysis on over the 8 month time span
	
	-   8_mos_DataFrame.csv = This file is our Compiled Data Frame with all of our features over 8 months, with Posts and Comments Separated.  ***It is 		    important to note, I think in Capstone 2, we should consider filtering out a fewer amount of comments (something we did). This will give us a plentiful 		amount of posts and comments if we want more.
	    
	-   Posts and Comments = This folder contains Data Objects that were written to Json Objects for easy retrieval, they include the Posts, Comments, the Word 		Count Structures.  These objects are separated into sub-folders, based on weather they were an analysis done when the Posts and Comments were all 	   	       combined together, or weather it was an analysis done just on the posts or the comments.
