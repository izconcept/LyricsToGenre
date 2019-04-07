import pyspark
import os
import json
import string
import re
import time
from pathlib import Path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from pyspark.sql import SparkSession, SQLContext, Row
from pyspark.sql.functions import udf, explode
from pyspark.sql.types import *
from pyspark import SparkContext
from pyspark.ml.feature import HashingTF, IDF, Tokenizer


ROOT_DIR = Path(__file__).parents[1]
filename = os.path.join(ROOT_DIR, 'data/songsWithLyrics.json')


def tokenize(text):
    # Remove Genius meta data before tokenizing
    text = re.sub(r'\[(.*?)\]', ' ', text)
    # Split into words
    tokens = word_tokenize(text)
    # Convert to lower case
    tokens = [w.lower() for w in tokens]
    # Remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # Remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # Filter out stop words
    words = [w for w in words if not w in english_stopwords]
    # (optional) Converts words to its stem
    # words = [porter.stem(word) for word in words]
    return words


sc = SparkContext(appName="Bag of words processor")
sqlContext = SQLContext(sc)

# Broadcast these words so nodes can find them
english_stopwords = stopwords.words("english")
sc.broadcast(english_stopwords)

data = []
count = 0
# Create DF
with open(filename) as f:
    temp_data = json.load(f)
    for song in temp_data:
        if len(song) == 4:
            data.append(song)
        else:
            count += 1

df = sqlContext.createDataFrame(Row(**x) for x in data)

# Tokenize lyrics and add column
tokenize_udf = udf(tokenize, ArrayType(StringType()))
df = df.withColumn('tokens', tokenize_udf(df.lyrics))

# Unique number of words. Needed for TF
NUMBER_OF_UNIQUE_WORDS = df.select(explode(df.tokens)).distinct().count()

# Adds new column called 'tf' for term frequency
hashingTF = HashingTF(inputCol="tokens", outputCol="tf",
                      numFeatures=NUMBER_OF_UNIQUE_WORDS)
df = hashingTF.transform(df)

# Adds TF-IDF
idf = IDF(inputCol="tf", outputCol="tf-idf")
idfModel = idf.fit(df)
df = idfModel.transform(df)

# Stores as pandas dataframe to be used by classifier
df.toPandas().to_pickle("data/dataset.pkl")
