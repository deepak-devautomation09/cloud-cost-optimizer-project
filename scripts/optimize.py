import boto3
from datetime import datetime

def find_stopped_instances(region="ap-south-1"):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(
        Filters=[
            {"Name": "instance-state-name", "Values": ["stopped"]}
        ]
    )
    
    stopped_instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            stopped_instances.append(instance['InstanceId'])
    
    return stopped_instances

def find_unattached_volumes(region="ap-south-1"):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_volumes(
        Filters=[
            {"Name": "status", "Values": ["available"]}
        ]
    )

    volumes = []
    for volume in response['Volumes']:
        volumes.append(volume['VolumeId'])
    return volumes

if __name__ == "__main__":
    region = "ap-south-1"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"logs/aws_cost_optimizer_log_{timestamp}.txt"

    print("🔍 Checking for stopped EC2 instances...")
    stopped = find_stopped_instances(region)
    with open(log_file, "w") as f:
        if stopped:
            print(f"⚠️ Found {len(stopped)} stopped instance(s):")
            f.write("Stopped EC2 Instances:\n")
            for instance_id in stopped:
                print(f"  → {instance_id}")
                f.write(f"{instance_id}\n")
        else:
            print("✅ No stopped instances found.")
            f.write("No stopped EC2 instances found.\n")

    # Check for Unattached EBS Volumes
    unattached = find_unattached_volumes(region)
    with open(log_file, "a") as f:
        if unattached:
            print(f"\n💾 Found {len(unattached)} unattached EBS volume(s):")
            f.write("\nUnattached EBS Volumes:\n")
            for vol in unattached:
                print(f"  → {vol}")
                f.write(f"{vol}\n")
        else:
            print("\n✅ No unattached EBS volumes found.")
            f.write("\nNo unattached EBS volumes found.\n")
