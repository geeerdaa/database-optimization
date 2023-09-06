from datetime import datetime, timedelta
from typing import List, Dict
import math

def convert_to_dynamodb_documents(user_id: int, day: datetime.date, activity_scores: List[int]) -> List[Dict]:
    documents = []
    start_time = datetime(day.year, day.month, day.day, 0, 0, 0)
    interval = timedelta(seconds=30)
    timestamp = math.floor(start_time.timestamp())
    
    for score in activity_scores:
        document = {
            "u": user_id,
            "t": timestamp,
            "v": [score]
        }
        documents.append(document)
        timestamp += 30
    
    return documents

# Calculate the cost
num_users = 1000000
num_scores_per_day = 2880
num_days = 30

num_writes = num_users * num_scores_per_day * num_days
num_reads = num_users * 2 * num_days

write_cost = math.ceil(num_writes / 1000000) * 1.25
read_cost = math.ceil(num_reads / 1000000) * 0.25

total_cost = write_cost + read_cost

print("Estimated cost for the month: $", total_cost)
