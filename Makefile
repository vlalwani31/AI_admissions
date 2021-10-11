install-python:
	\
	brew update;\
	brew install pyenv;\
	pyenv install 3.6.5;\

install-dependencies:
	\
	brew update;\
	brew install tesseract;\
	brew install poppler;\
	brew install opencv;\
	brew tap mongodb/brew\
	brew install mongodb-community@4.2\
	pip install --upgrade pip;\
	pip install -r requirements.txt;\
	python3 -m spacy download en_core_web_sm;\
	npm install --save-dev electron;\
	npm install;\

train:
	\
	source ./env/bin/activate;\
	brew services start mongodb-community@4.2;\
	python3 -m ai_admissions\
			--TranscriptDir ./train_transcripts\
			--train ./training_data.csv\
			--preprocess;\
	brew services stop mongodb-community@4.2;\

test:
	\
	source ./env/bin/activate;\
	brew services start mongodb-community@4.2;\
	python3 -m ai_admissions\
			--TranscriptDir ./test_transcripts\
			--preprocess;\

open-db:
	brew services start mongodb-community@4.2;\

close-db:
	brew services stop mongodb-community@4.2;\

app:
	npm start;\