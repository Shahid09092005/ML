# -*- coding: utf-8 -*-
"""29_Pipeline.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KB-fEi_F8uTvh3J8iVmOQhvfymiTV8rZ
"""

!pip install -q kaggle 

from google.colab import files
files.upload()

#making a directory
!mkdir ~/.kaggle

#Copy the kaggle.json to created folder
!/content/kaggle.json ~/.kaggle/

#permisson for the json to act
! chmod 600 /content/kaggle.json ~/.kaggle/

!kaggle datasets download -d brendan45774/test-file

! unzip /content/test-file.zip

import pandas as pd
df=pd.read_csv('/content/tested.csv')

df.head(5)

"""**Data Cleaning**"""

df.drop(columns=['PassengerId','Name','Cabin','Ticket'],inplace=True)

# selecing the 2nd row
np.array(df.iloc[1])

df.sample(5)

df.shape

df.isnull().sum()

"""**train_test_split is found in model_selection**"""

from sklearn.model_selection import train_test_split

x_train , x_test , y_train , y_test = train_test_split(df.drop(columns=['Survived']) , df['Survived'] , test_size=0.3 , random_state=0)

# we do fit when we need any preprocessing like StandardScale, MinMaxScale etc

x_train.head(5)  #contains independent columns

y_train.head(5) #contains dependent/target column

"""**Preprocessing**"""

x_train.isnull().sum()

x_train.sample(5)

x_train.shape

x_train.nunique()

"""here we can analysis that
Sex , Embarked are the Nomical Categorical Dataset.
if Pclass is in categorical dataset then it will Ordinal cat. dataset
"""

from sklearn.preprocessing import OrdinalEncoder , OneHotEncoder , MinMaxScaler , Sca
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

"""**Column Transformer**"""

# Imputer Transformer to handle the missing value with the help of SimpleImputer
trf1 = ColumnTransformer( [
    ('impute_age',SimpleImputer(strategy='mean'),[2,5]) ] ,  #we use SimpleImputer because we filling the values
      remainder='passthrough')        #[2,5] , It is best pratice to use the index of the column_name instead of the column names

# OneHotEncoder      sprase , handle_unknown are the parameters of OneHotEncoder
trf2 = ColumnTransformer( [            #here we want to make prediction that's why we do not drop the first column
        ('ohe_sex_embarked', OneHotEncoder( sparse_output = False , handle_unknown='ignore') , [1,6]) ] ,
    remainder='passthrough'
)
#   sparse is bool type ,  default is true means it will return a sparse matrix and false means dense array
#   handle_unknown is str type , default is 'error' means if unknown categories are encountered during transformation.
#      and if handle_unknown is 'ignore' means This ignores unknown categories and returns a result with zeros in their place.

# Scaling                  This slice object can then be used to extract a portion of a sequence, such as a list, tuple, or string.
trf3=ColumnTransformer( [   # ex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]---> my=slice(0,3)----> lst=[my]-->print(lst)-->[0,1,2]
        ('scale' , MinMaxScaler() , slice(0,8)) ]
)  #here we not use the StandardScaler because we use the DecisionTreeRegression which show no effect on StandardScaler

from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectKBest ,chi2

# feature selection

trf4 = SelectKBest( score_func = chi2 , k=8); # k means only top 8 colums out of 10 are uses.
# Note : before OneHotEncoder ther are 7 columns in x_train . During OneHotEncoder , colums no. 1(sex) is Replace with 2 column
#     and column no. 6(Embarked) is replace with  3 columns , so total column is (7-2+2+3=10) 10. We do drop first column bcz we're using DTC

# The Chi-Square test evaluates the independence of a feature with respect to the target variable.
# It measures how much the observed distribution of the feature differs from the expected distribution
# if the feature and target were independent.

#  Train the Model
trf5=DecisionTreeClassifier()

from sklearn.pipeline import Pipeline , make_pipeline

"""**Create  Pipeline**"""

pipe = Pipeline( [
    ( 'trf1' , trf1 ) ,                 # Pipeline take a list in which it takes the value in tuple and
    ( 'trf2' , trf2 ) ,                  # each tuple contains 2 values 1st is transformer_name and 2nd is his object
    ( 'trf3' , trf3 ) ,
    ( 'trf4' , trf4 ) ,
    ( 'trf5' , trf5 )
] )

# alternate way
# pipe=make_pipeline( trf1 , trf2 , trf3 , trf4 , trf5)

"""'Pipeline' requires the naming of steps and 'make_pipeline' does not

same goes too ColumnTransformer and make_column_transformer
"""

pipe.fit(x_train,y_train)  # training the model

# through pipe.fit(x_train , y_traint ) it trained the model
pipe.named_steps['trf1'].transformers_[0][1].statistics_  # it tell the fill mean value in place of missing numberical data

# predict
y_pred=pipe.predict(x_test)

from sklearn.metrics import accuracy_score
accuracy_score( y_test , y_pred )

"""**CrossVAlidation Using Pipeline**"""

from sklearn.model_selection import cross_val_score
cross_val_score( pipe , x_train , y_train , cv = 5 , scoring='accuracy').mean()

"""**GridSearch using Pipeline** learn in future

**Exporting the Pipeline**
"""

# export
import pickle
pickle.dump( pipe , open( 'pipe.pkl','wb') )



"""**Procuction Code**"""

import pickle
import numpy as np

pipe=pickle.load(open('/content/pipe.pkl','rb'))

# assume user input as
input=np.array([3, 'female', 47.0, 1, 0, 7.0, 'S'], dtype=object).reshape(1,7)

pipe.predict(input)
