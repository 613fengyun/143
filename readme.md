# README for Visualization Script

## File Structure

This project has a main Python script (`./final_code/main.py`) that generates visualizations for review data from an e-commerce platform. The script is dependent on a data file, which is found as `truncated_filtered_reviews.csv`.

The directory structure is as follows:
```
ECE_143_Project/
│
├── final-code/ # The Code to be used in the jupyter notebook portion and reviewed.
│   ├── data_parser.py # Code to parse the amazon review data (not needed to run since we're using a smaller pre-processed data that could be uploaded to the GitHub repo)
│   └── main.py # Main Code that contains the processing and visualization code.
├── final-plots/ # Contains all of the final visualization files that ended up in use for the presentation
├── scratch-code/ # Contains code from individual testing
├── plots/ # Contains all of the old plots that were made during testing and processing
├── truncated_filtered_reviews.csv # The filtered dataset that the code parses
└── ECE 143 Group 12 Slides.pdf # Presentation Slides PDF
└── presentation_graphs_notebook.ipynb # The jupyter notebook that runs and gets all of the graphs used in the presentation
```
note: Due to the large file size of the original filtered reviews csv file, there is a trucated_filtered_reviews.csv which is shortened to be within GitHub's file limits. Due to this, you may not have similar results to the results stored on the respository. 

## How to Run the Code

To run the script, please ensure that you have Python installed on your system along with the required third-party modules.

1. Install the necessary Python modules using `pip` if you haven't already:
   ```
   pip install pandas matplotlib seaborn nltk wordcloud numpy
   ```
   
2. Ensure that you have changed directory into the GitHub repo's base directory

3. locate `~/final_code/main.py` and go to the bottom and uncomment the 3 functions that are `{name}_main()`

4. Run `main.py` from the repository base directory as the working directory. 

## Third-Party Modules Used

The script uses the following third-party Python modules:

- `pandas`: A fast, powerful, flexible and easy-to-use open-source data analysis and manipulation tool.
- `matplotlib`: A comprehensive library for creating static, animated, and interactive visualizations in Python.
- `seaborn`: A Python data visualization library based on matplotlib, providing a high-level interface for drawing attractive and informative statistical graphics.
- `nltk`: Python module that includes a library of stopwords which are used to filter stop words out of reviews when doing word frequency counts.
- `wordcloud`: Visualization module that allows for creation of wordclouds while utilizing matplotlib.
- `numpy`: used for the isnan function

Please ensure these modules are installed before executing the script. If the modules are not installed, the script will not run successfully.
