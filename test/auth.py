import requests
import json

AUTH_ACCOUNT = '_dep375_bm_api_search'
AUTH_KEY = '564d904dbff248e4a3288b95d535f2c1'

#BASE_URL = 'http://test-auth.nie.netease.com'  # 测试环境地址
BASE_URL = 'http://int-auth.nie.netease.com' # 内网正式环境地址
# BASE_URL = 'http://auth.nie.netease.com' # 外网正式环境地址

# 请求 v2 接口同时生成 v2 token
def get_token(ttl=24*60*60):
    token_url = '%s/api/v2/%s' % (BASE_URL, 'tokens')
    data = {
        'user': AUTH_ACCOUNT,
        'key': AUTH_KEY,
        'ttl': ttl,  # token 的有效期，不填的话，默认有效时间是 24 小时，可以根据自行需要调整, 最大不超过 24 小时
    }
    res = requests.post(token_url, json=data, timeout=10)
    if not str(res.status_code).startswith('20'):
        raise Exception('failed to get token from auth: %s' % res.text)

    key_obj = res.json()

    return key_obj.get('token')

def main():
    print(get_token())

if __name__ == '__main__':
    main()