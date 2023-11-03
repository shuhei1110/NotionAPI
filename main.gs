function main() {
  const NOTION_API_KEY = PropertiesService.getScriptProperties().getProperty('NOTION_API_KEY');
  const database_id = 'c58eb74b3e8744c4ad35021dac4cf845';  

  let page_ids = queryPage(NOTION_API_KEY, database_id);

  console.log(page_ids);

  if (page_ids.length >0){
    for (let i=0; i<page_ids.length; i++){
      updatePage(NOTION_API_KEY, page_ids[i])
      console.log("convert " + page_ids[i])
    }
  }else{
    console.log("There were no completed tasks.")
  }
}

function queryPage(NOTION_API_KEY, database_id){
  let url = 'https://api.notion.com/v1/databases/' + database_id + '/query';

  let payload = {
    'filter': {
      'property': 'ステータス',
      'select': {
        'equals': '完了'
      }
    }
  };

  let opts = {
    'method': 'POST',
    'headers': {
      'Notion-Version': '2022-06-28',
      'Authorization': 'Bearer ' + NOTION_API_KEY,
      'Content-Type': 'application/json'
    },
    'payload': JSON.stringify(payload),
  }

  var page_ids = [];

  let result = JSON.parse(UrlFetchApp.fetch(url, opts));
    for (let i=0; i<result.results.length; i++){
    page_ids.push(result.results[i]['id']);
  }

  return page_ids;
}

function updatePage(NOTION_API_KEY, page_id){
  let url = 'https://api.notion.com/v1/pages/' + page_id;

  let payload = {
    'properties': {
      'ステータス': {
        'select': {
          'name': '非表示'
        }
      }
    }
  }

  let opts = {
    'method': 'PATCH',
    'headers': {
      'Notion-Version': '2022-06-28',
      'Authorization': 'Bearer ' + NOTION_API_KEY,
      'Content-Type': 'application/json'
    },
    'payload': JSON.stringify(payload),
  }

  UrlFetchApp.fetch(url, opts);
}
