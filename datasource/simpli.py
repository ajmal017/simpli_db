from core.dependencies import request_url

def get_simpli_info(ctx={}, **kwargs):
    info_url = 'http://api.simpli.kr/info/?token=blendedrequesttoken'
    res = request_url(info_url)
    print(res.json())


if __name__ == '__main__':
    get_simpli_info()