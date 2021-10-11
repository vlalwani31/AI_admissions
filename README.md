![Image](./app_data/ai_admission_logo.png?raw=true)
# Notes for Team AI-Admission (Future)
## Get Started
- Read the `README_SOFTWARE.` It explains all the modules and familiarize yourself with the file structure. 
- Primarily focus on the following files:      
  - `__main__.py` in the `ai_admissions` module
  -  `tesseract_ocr.py` and `transcript.py` in the `ocr` sub-module.
  -  `get_features.py` and `gray_listing.py` in the `data_extraction` sub-module.
- Read the system design pipelines and figures in the final report and watch our final demo video to get a quick explanation at https://drive.google.com/drive/folders/1eFhkSaPz2n672O1XF8JqLDzTVkUkYkmB
  
## Current State
- Our system uses the tesseract OCR to extract text from the transcripts. Based on our experimentation, the OCR provides a 98.4% character-wise accuracy.
- Our program is able to train a model given a a directory of transcripts along with a CSV file containing the labels for the given data.
- Our program is able to compute recommendation scores given a directory of transcripts. All scores would be displayed on a table after the calculation is completed along with another table that displays all transcripts that failed to be processed along with the corresponding error codes.
- The system uses an Support Vector Regression model trained on the UCLA admissions data-set available on Kaggle to calculate the prediction scores. The model has a mean square error loss of less than 2%.
- Our system interacts with a MongoDb locally to save the trained model, extracted features and model predictions.
- All the above mentioned functionality of the system is packaged into a desktop app for MacOS, and can be accessed via a GUI.
- Each transcript is processed in under 40 seconds including times for pre-processing, text extraction, feature extraction, saving to the data-base and calculating the recommendation score.
  
## Possible Future Work
- The extracted cumulative GPA needs to be normalized to a standard grading criteria
- Need to collect a lot of transcripts because there is currently a lack to transcripts to test on
- Try using BERT to encode the text of transcript into a uniform embedding space to use as input for Deep Learning Prediction models once more data is obtained.
- Explore Snorkel to extract course similarity/relevance score from the transcripts as another feature.
- Try threading the program's execution
- Find a quite extensive list of college rankings from worldwide to generate better University rating feature.
- The user should be allowed to load previously trained models from the database.
