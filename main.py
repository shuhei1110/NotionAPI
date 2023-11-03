"""NotionAPI's main file


    ToDo:
        - notion_clientというライブラリをインストール
        - NotionAPIのアクセストークンをNOTION_TOKENという変数名で環境変数に設定

"""
import os
import datetime
from notion_client import Client

token = os.environ.get("NOTION_TOKEN")
client = Client(auth=token)

#データベースIDを設定
database_id = "hogehoge"

property_name_1 = "\u30b9\u30c6\u30fc\u30bf\u30b9" #ステータス

tag_name_1 = "\u5b8c\u4e86" #完了
tag_name_2 = "\u672a\u7740\u624b" #未着手
tag_name_3 = "\u975e\u8868\u793a" #非表示

def print_datetime(f):
    def wrapper(*args, **kwargs):
        print(f'Start: {datetime.datetime.now()}')
        f(*args, **kwargs)
        print(f'End: {datetime.datetime.now()}')
    return wrapper

def read_pages_from_db(db_id:str, property_name:str, tag_name:str) -> list:
    """Read all pages id from database

        Args:
            db_id(str):
            property_name(str):
            tag_name(str):

        Responses
            page_ids(list):

        Notes:

    """
    response = client.databases.query(
        **{
            "database_id": db_id,
            "filter": {
                "property": property_name,
                "select": {
                    "equals": tag_name
                }
            }
        }
    )

    results = response["results"]
    page_ids = [result["id"] for result in results]

    return page_ids

def get_page_title(page_id:str) -> str:
    """
        Args:
            page_id(str):

        Responses:
            page_ids(list):
        
        Notes:

    """
    response = client.pages.retrieve(
        **{
            "page_id": page_id,
            "properties": [
                "Title"
            ]
        }
    )

    result = response["properties"]["Name"]["title"][0]["plain_text"]

    return result

def update_db(page_id:str, property_name:str, tag_name:str) -> dict:
    """Update databese contents

        Args:
            db_id(str):Database's ID
            property_name(str):
            tag_name(str)

        Responses:
            response(dict):

        Notes:

    """

    response = client.pages.update(
            **{
                "page_id": page_id,
                "properties": {
                    property_name: {
                        "select": {
                            "name": tag_name,
                            }
                        }
                }
            }
        )

    return response

@print_datetime
def main():
    """Main function

        Args:
            None

        Returns:
            None

        Notes:

    """
    db_id = database_id
    page_ids = read_pages_from_db(db_id, property_name_1, tag_name_1)    
    
    for page_id in page_ids:
        page_title = get_page_title(page_id)

        _ = update_db(page_id, property_name_1, tag_name_3)
        print(page_title)


if __name__ == "__main__":
    main()
