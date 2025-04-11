import boto3
from datetime import datetime

def find_stopped_instances(region="ap-south-1"):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
    )
    
    stopped_instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            stopped_instances.append(instance['InstanceId'])
    
    return stopped_instances

def find_unattached_volumes(region="ap-south-1"):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_volumes(
        Filters=[{"Name": "status", "Values": ["available"]}]
    )

    volumes = []
    for volume in response['Volumes']:
        volumes.append(volume['VolumeId'])
    return volumes

def get_total_aws_cost():
    ce = boto3.client('ce')
    start = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    end = datetime.today().strftime('%Y-%m-%d')

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )

    amount = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    currency = response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit']
    return float(amount), currency

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

    print("\n🔍 Checking for unattached EBS volumes...")
    unattached = find_unattached_volumes(region)
    with open(log_file, "a") as f:
        if unattached:
            print(f"💾 Found {len(unattached)} unattached EBS volume(s):")
            f.write("\nUnattached EBS Volumes:\n")
            for vol in unattached:
                print(f"  → {vol}")
                f.write(f"{vol}\n")
        else:
            print("✅ No unattached EBS volumes found.")
            f.write("\nNo unattached EBS volumes found.\n")

    print("\n💰 Fetching total AWS bill for the current month...")
    try:
        total_cost, currency = get_total_aws_cost()
        print(f"📊 Total AWS Cost (till today): {total_cost:.2f} {currency}")
        with open(log_file, "a") as f:
            f.write(f"\nTotal AWS Cost (till today): {total_cost:.2f} {currency}\n")
    except Exception as e:
        print(f"❌ Failed to fetch billing data: {e}")
        with open(log_file, "a") as f:
            f.write(f"\nFailed to fetch AWS billing data: {e}\n")
