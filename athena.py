import boto3
import time
client = boto3.client('athena')


response = client.start_query_execution(
    QueryString='select team_id, name from lol.teams;',
    ResultConfiguration={
        'OutputLocation': 's3://power-rankings-hackathon/athena-results/',

    },
)
print(response)

q_id = response['QueryExecutionId']


while True:
    response = client.get_query_execution(
        QueryExecutionId=q_id
    ) 
    print(response)
    time.sleep(0.2)
    if response['QueryExecution']['Status']['State'] == 'SUCCEEDED':
        break
response = client.get_query_results(
    QueryExecutionId=q_id,

)
print(response)
