import numpy as np
import pandas as pd
import lightgbm as lgb
import pickle
import pdb
import warnings
import os

from pathlib import Path
from train.train_hyperopt import LGBOptimizer
from utils.preprocess_data import build_train


PATH = Path('data/')
TRAIN_PATH = PATH/'train'
DATAPROCESSORS_PATH = PATH/'dataprocessors'
MODELS_PATH = PATH/'models'
MESSAGES_PATH = PATH/'messages'


def create_folders():
	print("creating directory structure...")
	(PATH).mkdir(exist_ok=True)
	(TRAIN_PATH).mkdir(exist_ok=True)
	(MODELS_PATH).mkdir(exist_ok=True)
	(DATAPROCESSORS_PATH).mkdir(exist_ok=True)
	(MESSAGES_PATH).mkdir(exist_ok=True)


def download_data():
	train_path = PATH/'adult.data'
	test_path = PATH/'adult.test'

	COLUMNS = ["age", "workclass", "fnlwgt", "education", "education_num",
	           "marital_status", "occupation", "relationship", "race", "gender",
	           "capital_gain", "capital_loss", "hours_per_week", "native_country",
	           "income_bracket"]

	print("downloading training data...")
	df_train = pd.read_csv("http://mlr.cs.umass.edu/ml/machine-learning-databases/adult/adult.data",
	    names=COLUMNS, skipinitialspace=True, index_col=0)
	df_train.drop("education_num", axis=1, inplace=True)
	df_train.to_csv(train_path)
	df_train.to_csv(PATH/'train/train.csv')

	print("downloading testing data...")
	df_test = pd.read_csv("http://mlr.cs.umass.edu/ml/machine-learning-databases/adult/adult.test",
	    names=COLUMNS, skipinitialspace=True, skiprows=1, index_col=0)
	df_test.drop("education_num", axis=1, inplace=True)
	df_test.to_csv(test_path)



def create_data_processor():
	print("creating preprocessor...")
	dataprocessor = build_train(TRAIN_PATH/'train.csv', DATAPROCESSORS_PATH)



def create_model():
	print("creating model...")
	init_dataprocessor = 'dataprocessor_0_.p'
	dtrain = pickle.load(open(DATAPROCESSORS_PATH/init_dataprocessor, 'rb'))
	# LGBOpt = LGBOptimizer(dtrain, MODELS_PATH)
	# LGBOpt.optimize(maxevals=10)
	LGBOpt = LGBOptimizer(dtrain, str(MODELS_PATH))
	LGBOpt.optimize('f1_score', StratifiedKFold, n_splits=3, maxevals=10)

if __name__ == '__main__':
	create_folders()
	download_data()
	create_data_processor()
	create_model()