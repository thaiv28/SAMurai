# Automating the data pipeline for inference

This model is best used in combination with a pipeline that can automatically retrieve and classify contracts as they are released.

SAM.gov provides a handy API for retrieving contracts, the documentation of which can be found [here](https://open.gsa.gov/api/get-opportunities-public-api/).

We can use this API to retrieve contracts as they are posted by government departments and automatically run them through model inference. The functions in [samurai/inference/api.py](../samurai/inference/api.py) can be modified to restrict the contracts that an API returns.

Then, either hosted or locally, run a script that calls `python3 samurai/inference/main.py`. This will call the API, run the results through the model, and print out any positive contract results. This can easily be modified to run automatically and alert you when a positive contract is found.

