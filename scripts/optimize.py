import boto3

def list_stopped_instances():
    ec2 = boto3.client('ec2')

    print("🔍 Checking for stopped EC2 instances...")
    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
    )

    stopped_instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            stopped_instances.append(instance['InstanceId'])

    if stopped_instances:
        print(f"⚠️ Found {len(stopped_instances)} stopped instance(s):")
        for instance_id in stopped_instances:
            print(f"  → {instance_id}")
    else:
        print("✅ No stopped instances found. You're good!")

if __name__ == "__main__":
    list_stopped_instances()
