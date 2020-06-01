#!/usr/bin/env python

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json

AccessKey = "LTAI4GGx8PrdY2aAsbsMd3Eh"
AccessKeySecret = "WwPei7XZpyoyzfUu7iwqK24e2WQvhy"

client = AcsClient(AccessKey, AccessKeySecret)

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('http')
request.set_version('2017-05-25')
request.set_action_name('SendSms')


def send_msg(phone_number, code):
    request.add_query_param('SignName', "清风博客")
    request.add_query_param('PhoneNumbers', phone_number)
    request.add_query_param('TemplateCode', "SMS_188565540")
    code = {'code': code}
    request.add_query_param('TemplateParam', json.dumps(code))
    response = client.do_action_with_exception(request)
    return response


def check_state_code(message):
    if type(message) == bytes:
        message = message.decode()
    return message['Code'] == 'ok'


