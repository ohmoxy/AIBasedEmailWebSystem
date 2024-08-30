import pymysql
import requests
import json
from datetime import datetime

# 定义全局变量

class aitext:
    mail_class1 = ''
    mail_status = ''
    mail_sum    = ''

def get_access_token():
    # 获取百度 AI 平台的访问令牌（access token）
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=#此处换为自己的令牌&client_secret=#同理"
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def main(mail):

    mail1 = f"规定9个分类：工作，通知，推销，订阅，账单，客服，邀请，教育，其他。你只需要回答邮件分类的名字，不要回答其他内容，不要增加标点符号。邮件内容：{mail}"
    mail2 = f"规定两个大类：正常，垃圾。你只需回答该信息的大类，不要回答其他内容，不要增加标点符号。邮件内容：{mail}"
    mail3 = f"总结邮件的概要，直接回答不要冗余或标点。邮件内容：{mail}"
    # 获取访问令牌
    access_token = get_access_token()
    
    # 获取信息的分类
    url_classify = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token
    
    payload_classify = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": mail1
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    # 发送获取分类信息的请求
    response_classify = requests.request("POST", url_classify, headers=headers, data=payload_classify)
    
    # 处理响应
    response_text_classify = response_classify.text
    response_json_classify = json.loads(response_text_classify)
    aitext.mail_class1 = response_json_classify['result']
    print("信息分类:", aitext.mail_class1)

    # 获取信息的状态
    url_status = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token
    
    payload_status = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": mail2
            }
        ]
    })

    # 发送获取状态信息的请求
    response_status = requests.request("POST", url_status, headers=headers, data=payload_status)
    
    # 处理响应
    response_text_status = response_status.text
    response_json_status = json.loads(response_text_status)
    aitext.mail_status = response_json_status['result']
    print("信息状态:", aitext.mail_status)
    
    # 获取信息的概要
    url_sum = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token
    
    payload_sum = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": mail3
            }
        ]
    })

    # 发送获取状态信息的请求
    response_sum = requests.request("POST", url_sum, headers=headers, data=payload_sum)
    
    # 处理响应
    response_text_sum = response_sum.text
    response_json_sum = json.loads(response_text_sum)
    aitext.mail_sum = response_json_sum['result']
    print("信息状态:", aitext.mail_sum)

    return aitext



def send_check(subject,content,need):
    if need:
        prompt = f'检查并对邮件提出修改意见，主题为{subject}，正文为{content}'
    else:
        prompt = f'检查并对邮件提出修改意见，主题为{subject}，正文为{content}，具体要求为{need}'
    # 获取访问令牌
    access_token = get_access_token()
    
    # 获取信息的分类
    url_classify = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token
    
    payload_classify = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    # 发送获取分类信息的请求
    response_classify = requests.request("POST", url_classify, headers=headers, data=payload_classify)
    
    # 处理响应
    response_text_classify = response_classify.text
    response_json_classify = json.loads(response_text_classify)
    send_ai = response_json_classify['result']
    print("信息分类:", send_ai)
    return send_ai

if __name__ == '__main__':
    mail,mail_class1, mail_status,mail_sum = main()
