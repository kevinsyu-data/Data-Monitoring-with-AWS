import os
import json
import boto3
import urllib.request
from datetime import datetime, timezone

sns = boto3.client("sns")
s3 = boto3.client("s3")

GITHUB_EVENTS_URL = "https://api.github.com/events"

def fetch_events():
    req = urllib.request.Request(
        GITHUB_EVENTS_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-watchtower"
        }
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def lambda_handler(event, context):
    topic_arn = os.environ["SNS_ARN"]
    bucket = os.environ["S3_ARN"]

    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%dT%H%M%SZ")

    events = fetch_events()
    count = len(events)

    key = f"raw/github_events_{ts}.json"
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(events).encode("utf-8"),
        ContentType="application/json"
    )

    if count > 10:
        sns.publish(
            TopicArn=topic_arn,
            Subject="GitHub Watchtower ALERT",
            Message=f"High GitHub event volume detected.\n\n"
                    f"Time (UTC): {now.isoformat()}\n"
                    f"Event count: {count}\n"
                    f"Raw data: s3://{bucket}/{key}"
        )
        return {"status": "alert_sent", "count": count}

    return {"status": "ok", "count": count}
