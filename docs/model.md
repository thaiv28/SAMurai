# SAMurai Model Implementation

SAMurai uses a Naive Bayes model for document classification. The problem with traditional implementations of Naive Bayes (e.g. from Scikit-Learn) is that all features must come from the same distribution: categorical, multinomial, or Gaussian, etc. 

In the case of SAMurai, our model needs to compute the categorical distribution for many features (NAICS code, Department Posted, Location), and the multinomial distribution for the text. 

Therefore, we implemented a custom Naive Bayes model in [samurai/model/nb.py](../samurai/model/nb.py). This model decomposes our features into two types: categorical and multinomial. We use the Scikit-Learn Naive Bayes categrorical and multinomial models respectively to calculate the independent probabilities of positive/negative classification, which are then multiplied against each other.

### An Example

For example, example X's features are split based on whether they are multinomial (description, attachments) or categorical (everything else). 

The multinomial features of example X give a 0.8 probability of positive classification and a 0.2 probability of negative classification. The categorical features give a 0.4 probability of positive classification and a 0.6 probability of negative classification.

Therefore, the "score" we give example X for positive classification is $0.8 * 0.4 = 0.32$. 

The score for negative classification is $0.2 * 0.6 = 0.12$. 

These scores are then softmaxed to give probabilities of $0.55$ and $0.45$ for positive and negative classifications respectively!

In reality, we compute these probabilities using their log forms, which we add together. 

## Categorical Features

The features that are follow a categorical distribution are as follows:
```
Department/Ind.Agency', 'CGAC', 'Sub-Tier', 'FPDS Code', 'Office', 'AAC Code', 'Type', 'SetASideCode', 'NaicsCode', 'ClassificationCode', 'OrganizationType', 'State', 'City', 'ZipCode', 'CountryCode'
```

We use ordinal encoding as opposed to one-hot encoding in our implementation. Although ordinal encoding isn't typically recommended when categorical values don't have an innate ordering, Naive Bayes models aren't capable of finding relationships between the ordering of values.

For example, Naive Bayes will treat the ordinally-encoded values `1` and `2` the same as `1` and `85`. Therefore, ordinal encoding is used because of its convenience and more dense-representation as compared to one-hot.

## Multinomial Features

Only two features are multinomially encoded: the description, and the content of the attachments. The text of both of these features are scraped from the contract page.

This text is encoded using TFIDF-vectorization, which is a modification on Bag-of-Words representation that penalizes words that are frequently used in every document. We chose TFIDF-vectorization to dilute the power of words that appear frequently that were not caught by our stopwords list.

