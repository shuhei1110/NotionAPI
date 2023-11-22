"""NotionAPI's main file


    ToDo:
        Attempt that controll DB in test environment

"""

import os
from notion_client import Client

token = os.environ.get("NOTION_TOKEN")
client = Client(auth=token)

test_db_id = "0fe6066d5323405ea7f5e3ea86a192b4" 

test_page_id = "be16fc7419eb4467b7817e99f4941c9c"

#database_id = "0e95767d933e4266baa7c550390d8894"
database_id = "c58eb74b3e8744c4ad35021dac4cf845"

tag_name_1 = "\u5b8c\u4e86" #完了
tag_name_2 = "\u672a\u5b8c\u4e86" #未完了
tag_name_3 = "\u975e\u8868\u793a" #非表示
tag_name_4 = "\u30b9\u30c6\u30fc\u30bf\u30b9" #ステータス

def read_db(db_id):
    """Get databese contents

        Args:
            db_id(String):Databese's ID

        Responses:


        Notes:

    """
    response = client.databases.query(
            **{
                "database_id": db_id,
                "filter": {
                    "property": "\u30b9\u30c6\u30fc\u30bf\u30b9",
                    "status": {
                        "equals": "Done"
                        }
                    }
            }
        )

    return response

def read_pages_from_db(db_id):
    """Read all pages id from database

        Args:
            db_id(String):

        Responses

        Notes:

    """
    response = client.databases.query(
        **{
            "database_id": db_id,
            "filter": {
                "property": "\u30b9\u30c6\u30fc\u30bf\u30b9",
                "select": {
                    "equals": tag_name_1
                }
            }
        }
    )

    results = response["results"]
    page_ids = [result["id"] for result in results]

    return page_ids

def get_page_title(page_id):
    """
    """
    response = client.pages.retrieve(
        **{
            "page_id": page_id,
            "properties": [
                "Title"
            ]
        }
    )

    #return response["properties"]["名前"]["title"][0]["plain_text"]
    return response["properties"]["Name"]["title"][0]["plain_text"]

def update_db(page_id, ):
    """Update databese contents

        Args:
            db_id(String):Database's ID

        Responses:

        Notes:

    """

    response = client.pages.update(
            **{
                "page_id": page_id,
                "properties": {
                    "\u30b9\u30c6\u30fc\u30bf\u30b9": {
                        "select": {
                            "name": "Done",
                        }
                    },
                    "\u30b9\u30c6\u30fc\u30bf\u30b9": {
                        "select": {
                            "name": "Not started",
                            }
                        }
                }
            }
        )

    print("notion database update response")

    return response


def main():
    """Main function

        Args:
            None

        Returns:
            None

        Notes:

    """
    db_id = database_id
    page_ids = read_pages_from_db(db_id)
    
    #print(page_ids)
    for page_id in page_ids:
        page_title = get_page_title(page_id)

        #_ = update_db(page_id)
        print(page_title)


if __name__ == "__main__":
    main()
