
# Screenplay Evaluator

## Overview
The Screenplay Evaluator is a tool designed to qualitatively assess and compare human-written and AI-generated screenplays. It provides various analytical metrics to evaluate screenplay structure, syntax complexity, and overall coherence. This project aims to establish a robust framework for screenplay evaluation, leveraging machine learning and natural language processing techniques.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/screenplay-evaluator.git  
cd screenplay-evaluator  

# Create and activate a virtual environment (optional but recommended)
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  

# Install dependencies
pip install -r requirements.txt

#For spacy, install the necessary language model separately if needed
python -m spacy download en_core_web_sm

#For nltk, download required datasets if necessary:
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```
## Current Evaluator

| Evaluator    | File Extension | 
| -------- | ------- |
| Increasing Graph  | -increasingGraph.png   |
| Presence Graph    | -prescenceGraph.png  |
| Chord Graph   | -chord_plot.html   |
| Directed Graph | -DirectedGraph.png |
| Heaps Law | -HeapsLaw.png |
| Universal Part of Speech <br>Distribution and Gini Index| -pos_data.csv |  
| Detailed part-of-speech tag <br> Distribution and Gini Index | -tag_data.csv |
| Sentence Complexity | -yngves_and_frazier_mean.png |
| Sentence Word Count over time | -SentenceWordCountOverTime.png|
|Sentence Word Count Index| -SentenceWordCount.png |
|Scene by Sentence Length Over Time|-SceneBySentenceLengthOverTime.png|
|Scene by Sentence Length Index|-SceneBySentenceLengthIndex.png|
| SentimentAnalysis | -SentimentAnlysis.png |
| SVO | -SVO.json |
| TeriorCount |-terior_count.csv | 


    
## Usage & Examples
To run the Evaluator, simply execute the script named ScreenplayPrototype.py. This file contains several configurable variables that allow you to customize the input and output behavior.
When running the file, you can exclude evaluators by commenting out each section.
### Configurable Variables

| Variables    | Use | 
| -------- | ------- |
|directory_path | This variable sets the input where the file will read.|
| skipfile| Use to skip screenplays if running evaluator in batch.  |

