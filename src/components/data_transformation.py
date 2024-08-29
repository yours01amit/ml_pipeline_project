import os, sys
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts/data_transformation", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def get_data_transformation_obj(self):
        try:

            logging.info("Data transformation started")

            numerical_features = ['age', 'workclass', 'education_num', 'marital_status', 'occupation',
       'relationship', 'race', 'sex', 'capital_gain', 'capital_loss',
       'hours_per_week', 'native_country']
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())             
                    
                ])
            
            preprocessor = ColumnTransformer([
                ("Num_pipeline", num_pipeline,numerical_features)
            ])

            return preprocessor
        

        except Exception as e:
            raise CustomException(e, sys)
        
    
    def remove_outliers_using_IQR(self, col, df):
        try:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)

            IQR = q3 - q1

            upper_limit = q3 + 1.5 * IQR
            lower_limit = q1 - 1.5 * IQR

            df.loc[(df[col] > upper_limit), col] = int(upper_limit)
            df.loc[(df[col] < lower_limit), col] = int(lower_limit)

            return df
        
        except Exception as e:
            logging.info("Outliers handling")
            raise CustomException(e, sys)
        
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            numerical_features = ['age', 'workclass', 'education_num', 'marital_status', 'occupation',
            'relationship', 'race', 'sex', 'capital_gain', 'capital_loss',
            'hours_per_week', 'native_country']
            

            for i in numerical_features:
                self.remove_outliers_using_IQR(col=i, df=train_data)

            logging.info("Outliers capped on our train data")

            for i in numerical_features:
                self.remove_outliers_using_IQR(col=i, df=test_data)

            logging.info("Outliers capped on our test data")

            preprocessor_obj = self.get_data_transformation_obj()

            target_column = "income"
            drop_column = [target_column]

            logging.info("Splitting traindata into dependent and independent features")
            input_feature_train_data = train_data.drop(drop_column, axis=1)
            target_feature_train_data = train_data[target_column]

            logging.info("Splitting test data into dependent and independent features")
            input_feature_test_data = test_data.drop(drop_column, axis=1)
            target_feature_test_data = test_data[target_column]

            # Applying transformation on our train and test data
            input_train_arr = preprocessor_obj.fit_transform(input_feature_train_data)
            input_test_arr = preprocessor_obj.transform(input_feature_test_data)

            # Applying preprocessor object on train data and test data
            train_array = np.c_[input_train_arr, np.array(target_feature_train_data)]
            test_array = np.c_[input_test_arr, np.array(target_feature_test_data)]

            save_obj(file_path=self.data_transformation_config.preprocessor_obj_file_path,
                     obj=preprocessor_obj)
            
            return(
                train_array,
                test_array,
                self.data_transformation_config.preprocessor_obj_file_path
            )






        except Exception as e:
            raise CustomException(e, sys)