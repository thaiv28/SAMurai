
# SAMurai
<p align="center">

  <img src="/docs/images/samurai.jpeg" alt="Samurai looking through contracts" width="300"/>
</p>

SAMurai is a machine learning model that is used to classify government contracts
from [SAM.gov](https://sam.gov/content/home) based on their suitability for a specific company.

Users can provide suitable government contracts in a text file, and automatically
create a dataset for the model to use.

The model is a Naive Bayes model that takes into account the categorical features
of the dataset and the multinomial features. Take a look at [docs/model.md](/docs/model.md) for more details on the implementation.

### Create the dataset
Follow the instructions in [docs/dataset.md](/docs/dataset.md) to create a dataset
that can be used to train the model.

### Run the model
After creating the dataset, run the following command to train and run testing
on your model:
```bash
python3 sam_classifier/pipeline/main.py
```

### Automate the pipeline
Instructions for automating the pipeline of sending SAM.gov API results through
the model can be found at [docs/automation.md](/docs/automation.md)

## Future Work
- Build a neural network for classification
