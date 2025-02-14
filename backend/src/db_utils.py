import boto3

# Initialize the DynamoDB client
dynamodb = boto3.resource("dynamodb", region_name="eu-west-1",
                          aws_access_key_id="YOUR_ACCESS_KEY", aws_secret_access_key="YOUR_SECRET_KEY")

# Set the table name
TABLE_NAME = "IoT_Events"

# Reference the table
table = dynamodb.Table(TABLE_NAME)


def write_item(item_data):
    """Write a single item to the DynamoDB table."""
    try:
        response = table.put_item(Item=item_data)
        print(f"Item inserted: {item_data}")
        return response
    except Exception as e:
        print(f"Error inserting item: {e}")


def read_item(key):
    """Read a single item from the table by primary key."""
    try:
        response = table.get_item(Key=key)
        if "Item" in response:
            return response["Item"]
        else:
            print("Item not found")
            return None
    except Exception as e:
        print(f"Error reading item: {e}")


def scan_table():
    """Scan the whole table and retrieve all items."""
    try:
        response = table.scan()
        items = response.get("Items", [])
        
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response.get("Items", []))
        
        return items
    except Exception as e:
        print(f"Error scanning table: {e}")
        return []