=================
目录
=================

- `介绍`_

- `使用说明`_

============
介绍
============

基于 `Beautiful Soup <https://www.crummy.com/software/BeautifulSoup/>`_ 与 `Flask <http://flask.pocoo.org/>`_ 开发的 `二娘 <https:///>`_ API

可以获取个人数据、种子信息及站点状况（后两者开发中）

============
使用说明
============
协议标准: HTTP POST

接口地址: `profile API <站内查看>`

请求样例：(python)

.. code:: python

  import requests
  import json
  
  data = {}
  data['uid'] = "44929"
  url = 'http://'
  page = requests.post(url, data = data).text
  data = json.loads(page)
  
样例返回:

.. code:: python

  {
    "id": "索尔",
    "error": "0",
    "join": "2017-04-29 18:45:45",
    "last": "2018-01-10 21:45:24",
    "transfer": {
        "share ratio": "6.104",
        "upload": [
            "25.164",
            "T"
        ],
        "download": [
            "4.123",
            "T"
        ],
        "raw": {
            "upload": [
                "14.377",
                "T"
            ],
            "download": [
                "20.345",
                "T"
            ]
        }
    },
    "bt": {
        "ratio": "62.775",
        "seeding": "59033",
        "leeching": "940"
    },
    "speed": {
        "download": "64kbps",
        "upload": "64kbps"
    },
    "gender": "伪娘",
    "class": "宅传教士",
    "title": "sor",
    "exp": "111",
    "uc": {
        "amount": 766509.43,
        "gold": "76",
        "silver": "65",
        "copper": "9"
    }
  }
  
错误码: (error)

.. code:: python

  -1: 用户不存在
  0: 正常
  1: Time out
  2: 隐私强
