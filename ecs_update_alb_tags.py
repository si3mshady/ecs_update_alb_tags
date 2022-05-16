import boto3 

REGION = 'us-west-2'
CLUSTERS = ['cluster0', 'cluster1']

#MUST SUPPLY CLUSTER NAME AND SERVICE for script to functio
CLUSTER_SERVICE_MAPPING_EAST = {CLUSTERS[0]:"serviceName", CLUSTERS[1]:"serviceName"}

CLUSTER_SERVICE_MAPPING_WEST = {CLUSTERS[0]:"serviceNameWest0",\
CLUSTERS[1]:"serviceNameWest1"}

svc_tg_list = []
svc_alb_list = []


def match_service_with_target_group(cluster: str,service: str, region=REGION) -> list:
    ecs = boto3.client('ecs', region_name=region)
    kwargs = {"cluster":cluster, "services": [service]}
    result = ecs.describe_services(**kwargs)
    #target group arn looks like this, use split to break string by '/' then access the index of string starting from end
    # arn:aws:elasticloadbalancing:us-east-1:888:targetgroup/app-Targe-dsss/kjdkjska
    tg = result['services'][0]['loadBalancers'][0]['targetGroupArn'].split('/')[-2]
    svc_tg_list.append({service:tg})
    cluster 
    return svc_tg_list
    

def match_tg_with_alb(region=REGION):
    for element in svc_tg_list:
        for service_name ,target_group in element.items(): #use items to iterate a dictionary 
            elb = boto3.client('elbv2', region_name=region)
            response = elb.describe_target_groups(Names=[target_group])
            alb = response.get('TargetGroups')[0]['LoadBalancerArns'][0]
            svc_alb = {service_name: alb}
            kwargs = {"arn":alb,"tg":target_group,"service_name":service_name}
            add_tag(**kwargs)
            svc_alb_list.append(svc_alb)

def add_tag(arn,tg,service_name):
    service_name_mini = service_name.split('--')[3] #change if naming conventin changes 
    elb = boto3.client('elbv2', region_name=REGION)
    elb.add_tags(
    ResourceArns=[arn],Tags=[{
            'Key': 'Application',
            'Value': f'{service_name_mini}-{tg}-{REGION}'
        },
    ]
)

def init() -> None:
    if REGION == 'us-east-1':
        for k,v in CLUSTER_SERVICE_MAPPING_EAST.items():
            try:
                match_service_with_target_group(k,v)
            except Exception as e:
                print(e)
    if REGION == 'us-west-2':
        for k,v in CLUSTER_SERVICE_MAPPING_WEST.items():
            try:
                    match_service_with_target_group(k,v)
            except Exception as e:
                print(e)
                   
            
    match_tg_with_alb()
    print(svc_alb_list)


if __name__ == "__main__":
    init()

#Elliott Arnold 7-11  5-16-22  update tagging on application load balancer and generate mappings for later use

