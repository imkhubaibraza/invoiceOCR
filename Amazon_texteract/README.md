
# Analyzing Invoices and receipts with Amazon texteract
To analyze invoice and receipt documents, you use the AnalyzeExpense API, and pass a document file as input.


### Requirments
---

* create an virtual environment, activate and install requiremnts.txt

```
virtualenv env
source env/bin/activate
pip install -r requirments.txt

```
* You must have an [AWS (Amazon Web Services)](http://aws.amazon.com/) account.


*  Reaplce `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` with your keys

```
export AWS_ACCESS_KEY_ID=#Replace_yours
export export AWS_SECRET_ACCESS_KEY=#Replace_yours

```

* [Create S3 bucket ](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)


## Quick Strat
* In `start.py` you have to pass `bucket`, `imagename` and `region`
* Run `python start.py`



