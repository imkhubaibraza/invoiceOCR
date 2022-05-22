import pandas as pd
import boto3
import io
from PIL import Image, ImageDraw

# export AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID
# export export AWS_SECRET_ACCESS_KEY=AWSSecretKey

def draw_bounding_box(key, val, width, height, draw):
    '''
        If a key is Geometry, draw the bounding box info in it
    '''
    if "Geometry" in key:
        # Draw bounding box information
        box = val["BoundingBox"]
        left = width * box['Left']
        top = height * box['Top']
        draw.rectangle([left, top, left + (width * box['Width']), top + (height * box['Height'])],
                       outline='black')
                       
                       
def smart_print(field):
    '''
        print all the labels and values
    '''
    
    if "LabelDetection" in field:
        print("Summary Label Detection - Confidence: {}".format(
            str(field.get("LabelDetection")["Confidence"])) + ", "
              + "Summary Values: {}".format(str(field.get("LabelDetection")["Text"])))
#         print(field.get("LabelDetection")["Geometry"])
    else:
        print("Label Detection - No labels.")
    if "ValueDetection" in field:
        print("Summary Value Detection - Confidence: {}".format(
            str(field.get("ValueDetection")["Confidence"])) + ", "
              + "Summary Values: {}".format(str(field.get("ValueDetection")["Text"])))
#         print(field.get("ValueDetection")["Geometry"])
    else:
        print("Value Detection - No values returned")

def process_text_detection(bucket, imagename , region = "us-west-2"):
    '''
        Get image from S3 and pass to expense analyzer
    '''
    
    # Get the IMAGES from S3
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket, imagename)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())

    # loading stream into image
    image = Image.open(stream)

    # Detect text in the image
    client = boto3.client('textract', region_name=region)

    # process using S3 object
    response = client.analyze_expense(
        Document={'S3Object': {'Bucket': bucket, 'Name': imagename}})

    # Set width and height to display image and draw bounding boxes
    # Create drawing object
    width, height = image.size
    draw = ImageDraw.Draw(image)

    for expense_doc in response["ExpenseDocuments"]:
        
        print("Expense Doc Summary:")
        for summary_field in expense_doc["SummaryFields"]:
            smart_print(summary_field)
            print()

        # TO draw bounding boxes
        for line_item_group in expense_doc["LineItemGroups"]:
            for line_items in line_item_group["LineItems"]:
                for expense_fields in line_items["LineItemExpenseFields"]:
                    for key, val in expense_fields["ValueDetection"].items():
                        if "Geometry" in key:
                            draw_bounding_box(key, val, width, height, draw)

        for label in expense_doc["SummaryFields"]:
            if "LabelDetection" in label:
                for key, val in label["LabelDetection"].items():
                    draw_bounding_box(key, val, width, height, draw)

    # saved image in current file
    image.save(imagename)
    return response

process_text_detection(bucket="khubaib-test" , imagename="pakaccountants-invoice-example.png" );