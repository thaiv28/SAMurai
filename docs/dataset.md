# Create a dataset

To train an accurate model, we first need to create a dataset that accurately
represents how contracts should be classified.

SAMurai offeres different utilities to help out in creating this dataset. They are
found in the [samurai/data/](../samurai/data/) directory.

## Manually list positive classifications
First, we must find and select the SAM contracts that are good fits for the company.
These positive classifications will be used to train the model. If you already have a list of positive contracts, skip to [Attach positive labels](#attach-positive-labels). 

Otherwise, a list of all government contracts can be found on [SAM.gov](https://www.SAM.gov/). Narrow the results to a closed time frame (ex: past week) and apply any suitable filters. The contracts here will encompass your entire dataset, both positive and negative results. Therefore, it is important that you analyze every contract within this range. Every contract not saved as a positive classification will be fed into the model as a negative one.

Save the solicitation number for every positive contract.

## Generate dataset from SAM archive
Next, we use the SAM archives as a convenient way to generate a CSV file that contains all the features for the dataset. Head to the [SAM Archives](https://sam.gov/data-services/Contract%20Opportunities/Archived%20Data?privacy=Public) and download the file that corresponds to the year that you searched.

### Eliminate contracts
Next, we must eliminate any contracts that you did not manually analyze. 

Assuming you analyzed every contract within a certain date range (as recommended above), we can simply eliminate all the contracts not within that range. In [samurai/files/dates.txt](../samurai/files/dates.txt), list all the dates within the range you analyzed.

Additionally, you may have applied some filters on the search results, as described above. In [samurai/files/filters.txt](../samurai/files/filters.txt) list the filters as follows:
```
categoryName
categoryValue
```
The category names should directly match up with the column names in the archive csv. For example, to filter out the NAICS code to only 541330, list this in the `filters.txt`.
```
naicsCode
541330
```

Finally, run the script [samurai/data/mining/archives.py](../samurai/data/mining/label.py) to generate the final dataset. Change the variable `ARCHIVE_LOCATION` to the directoy where the previously downloaded archive is stored. Run the script.

```
python archives.py
```

This will finish the data mining process for the dataset. It will filter out the unused contracts, split them into csv files by date, and then scrape the attachments on the contracts. The content of these attachments will be attached to the descriptions of the contracts to be used for multinomial (BoW) classification.

### Attach positive labels

Lastly, we must attach the positive labels to the positive contracts. List out the Solicitation #'s for the positive contracts in [samurai/files/labels.txt.txt](../samurai/files/filters.txt), each on a different line. Navigate to `samurai/data/mining` and run the script:

```
python3 label.py
```

The dataset is now created! It will be stored in `samurai/files/archives`!