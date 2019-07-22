import json
import boto3
import os

s3 = boto3.resource('s3')
comprehend = boto3.client('comprehend')
translate = boto3.client('translate')
firehose = boto3.client('firehose')

def lambda_handler(event, context):
    print(event)
    
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        
        obj = s3.Object(s3_bucket, s3_key)
        tweets_as_string = obj.get()['Body'].read().decode('utf-8') 
        
        tweets = tweets_as_string.split('\n')
        for tweet_string in tweets:
            
            if len(tweet_string) < 1:
                continue
            
            tweet = json.loads(tweet_string)
            
            if tweet['lang'] != 'en':
                response = translate.translate_text(
                    Text=tweet['text'],
                    SourceLanguageCode=tweet['lang'],
                    TargetLanguageCode='en')
                comprehend_text = response['TranslatedText']
            else:
                comprehend_text = tweet['text']
            
            sentiment_response = comprehend.detect_sentiment(
                    Text=comprehend_text,
                    LanguageCode='en'
                )
            print(sentiment_response)
            
            entities_response = comprehend.detect_entities(
                    Text=comprehend_text,
                    LanguageCode='en'
                )
                
            print(entities_response)
            
            sentiment_record = {
                'tweetid': tweet['id'],
                'text': comprehend_text,
                'originaltext': tweet['text'],
                'sentiment': sentiment_response['Sentiment'],
                'sentimentposscore': sentiment_response['SentimentScore']['Positive'],
                'sentimentnegscore': sentiment_response['SentimentScore']['Negative'],
                'sentimentneuscore': sentiment_response['SentimentScore']['Neutral'],
                'sentimentmixedscore': sentiment_response['SentimentScore']['Mixed']
            }
            
            response = firehose.put_record(
                DeliveryStreamName=os.environ['SENTIMENT_STREAM'],
                Record={
                    'Data': json.dumps(sentiment_record) + '\n'
                }
            )
            
            seen_entities = []
            for entity in entities_response['Entities']:
                id = entity['Text'] + '-' + entity['Type']
                if (id in seen_entities) == False:
                    entity_record = {
                        'tweetid': tweet['id'],
                        'entity': entity['Text'],
                        'type': entity['Type'],
                        'score': entity['Score']
                    }
                    
                    response = firehose.put_record(
                        DeliveryStreamName=os.environ['ENTITY_STREAM'],
                        Record={
                            'Data': json.dumps(entity_record) + '\n'
                        }
                    )
                    seen_entities.append(id)
            
    return 'true'