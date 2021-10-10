import os
import requests
import jwt
import uuid
from bs4 import BeautifulSoup
import time
from urllib.parse import urlencode
import hashlib
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText

def sendmsg(sendtext):
    s = smtplib.SMTP('smtp.gmail.com', 587)# 세션 생성
    s.starttls() # TLS 보안 시작
    s.login('gmail.com', 'zfgc')# 로그인 인증
    msg = MIMEText(str(sendtext))# 보낼 메시지 설정
    msg['Subject'] = '햄스터매매법 작동현황'
    s.sendmail("gmail.com", "naver.com", msg.as_string())# 메일 보내
    s.quit()# 세션 종료
def sendmsgB(sendtext):
    # 세션 생성
    s = smtplib.SMTP('smtp.gmail.com', 587)# 세션 생성
    s.starttls()# TLS 보안 시작
    s.login('gmail.com', 'zfg')# 로그인 인증
    msg = MIMEText(str(sendtext))# 보낼 메시지 설정
    msg['Subject'] = '매수완료'
    s.sendmail("gmail.com", "naver.com", msg.as_string())# 메일 보내
    s.quit()# 세션 종료
def sendmsgS(sendtext):
    # 세션 생성
    s = smtplib.SMTP('smtp.gmail.com', 587)# 세션 생성
    s.starttls()# TLS 보안 시작
    s.login('gmail.com', 'zfg')# 로그인 인증
    msg = MIMEText(str(sendtext))# 보낼 메시지 설정
    msg['Subject'] = '[거래완료]'
    s.sendmail("gmail.com", "naver.com", msg.as_string())# 메일 보내
    s.quit()# 세션 종료

access_key = ''
secret_key = ''

server_url = 'https://api.upbit.com'
upbit_url = 'https://api.upbit.com/v1/market/all'
price_url = 'https://api.upbit.com/v1/trades/ticks'

# 지갑
purchaseMoney = 10000
currentMoney  = purchaseMoney
presentMoney  = purchaseMoney
buyCoinPrice  = 0  # 구매시 가격

coinName = []
# 시간
nowTime = time.time()
preTime = nowTime

purchase = 0
benefit = 0
choseCoin = ''
presentCoin = ''

def get_price(name):
    querystring = {"market": "KRW-" + name, "count": "1"}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", price_url, headers=headers, params=querystring)
    response = response.text
    response = response.split('"')
    time.sleep(0.05)
    return float(response[16].replace(":", "").replace(",", ""))


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

print('┌─────────────────────────────────────────────────────────┐')
print('│               햄스터 손안에 내인생 매수법               │')
print('└─────────────────────────────────────────────────────────┘')
print(datetime.now())
print('\n\n')
sendmsg("거래시작 \n 거래금액 : "+str(purchaseMoney))
mode = 0
playTime = 0
while 1:
    nowDate = datetime.now()
    A = int(nowDate.hour)
    if A > 6 and A < 18:  # 활동시간
        randomMin = 60 * 60 * 1
        randomMax = 60 * 60 * 3
    else:
        randomMin = 5
        randomMax = 60 * 60 * 1

    nowTime = time.time()
    if mode == 0:  # 코인 교체 유무
        if playTime > 0:
            b = random.randint(0, 10)
            if b < 7: # 70%
                print('[교체 O ]')
                querystring = {"isDetails": "false"}
                headers = {"Accept": "application/json"}
                response = requests.request("GET", upbit_url, headers=headers, params=querystring)
                soup = BeautifulSoup(response.content, 'html.parser')
                soup = soup.prettify()
                soup = soup.split('"')
                coinName = []
                for i in range(len(soup)):
                    if soup[i].startswith('KRW'):
                        coinName.append(str(soup[i]).replace("KRW-", ""))
                choseNum = random.randint(0, len(coinName))
                choseCoin = coinName[int(choseNum)]
                print("선택!:", choseCoin)
            else:
                print('[교체 X ]')
                if choseCoin == '':  # 첫 시작
                    querystring = {"isDetails": "false"}
                    headers = {"Accept": "application/json"}
                    response = requests.request("GET", upbit_url, headers=headers, params=querystring)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    soup = soup.prettify()
                    soup = soup.split('"')
                    coinName = []
                    for i in range(len(soup)):
                        if soup[i].startswith('KRW'):
                            coinName.append(str(soup[i]).replace("KRW-", ""))
                    choseNum = random.randint(0, len(coinName))
                    choseCoin = coinName[int(choseNum)]
                    print("랜덤:", choseCoin)
            randomWaitTime = random.randint(randomMin, randomMax)
            print('>>현재 매도 시간:', datetime.now())
            print('>>예상 매수 시간:', datetime.now() + timedelta(seconds=randomWaitTime))
            print(">>현재까지  이윤:", benefit)
            sendmsgS("이윤 : " + str(round((current_money - present_money), 3)) + '\n누적이윤 : ' + str(
                benefit) + '\n거래한 코인 : ' + str(presentCoin) + '\n다음거래할 코인 : ' + str(choseCoin) + '\n다음 매수시간 : '+ str(datetime.now() + timedelta(seconds=randomWaitTime)) )
            while 1:
                nowTime = time.time()
                time.sleep(1)
                if nowTime - preTime > randomWaitTime:
                    mode = 0
                    break
        else:
            b = random.randint(0, 10)
            if b == 1 or b == 4 or b == 7 or b == 8:
                print('[교체 O ]')
                querystring = {"isDetails": "false"}
                headers = {"Accept": "application/json"}
                response = requests.request("GET", upbit_url, headers=headers, params=querystring)
                soup = BeautifulSoup(response.content, 'html.parser')
                soup = soup.prettify()
                soup = soup.split('"')
                coinName = []
                for i in range(len(soup)):
                    if soup[i].startswith('KRW'):
                        coinName.append(str(soup[i]).replace("KRW-", ""))
                choseNum = random.randint(0, len(coinName))
                choseCoin = coinName[int(choseNum)]
                print("선택!:", choseCoin)
            else:
                print('[교체 X ]')
                if choseCoin == '':  # 첫 시작
                    querystring = {"isDetails": "false"}
                    headers = {"Accept": "application/json"}
                    response = requests.request("GET", upbit_url, headers=headers, params=querystring)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    soup = soup.prettify()
                    soup = soup.split('"')
                    coinName = []
                    for i in range(len(soup)):
                        if soup[i].startswith('KRW'):
                            coinName.append(str(soup[i]).replace("KRW-", ""))
                    choseNum = random.randint(0, len(coinName))
                    choseCoin = coinName[int(choseNum)]
                    print("랜덤:", choseCoin)
        mode = 1
    elif mode == 1:  # 매수준비
        print("매수 준비")
        buyCoinPrice = get_price(choseCoin)
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
        res = requests.get(server_url + "/v1/accounts", headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        soup = soup.prettify()
        soup = soup.split('"')
        current_money = round(float(soup[7]), 2)
        present_money = current_money
        print("현재 자금:", current_money, "원")
        if current_money < purchaseMoney:
            print("자금 부족")
            break
        else:
            purchase_amount = float(purchaseMoney / buyCoinPrice)
            print("매수개수:", str(purchase_amount))
            print("주문가격:", str(buyCoinPrice))

        query = {
            'market': 'KRW-' + str(choseCoin),
            'side': 'bid',  # bid 매수 ask 매도
            'volume': str(purchase_amount),  # 주문량
            'price': str(buyCoinPrice),  # 주문가격
            'ord_type': 'limit',  # 주문타입 limit지정가 price 시장가(매수) market 시장가(매도)
        }
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
        res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        soup = soup.prettify()
        soup = soup.split('"')
        purchase_uuid = soup[3]
        print("//////////////////////////////////////////////////////////////////////////////////////")
        print(res.text)
        print("//////////////////////////////////////////////////////////////////////////////////////")
        print(str(datetime.now()))
        print("주문신청 완료")
        print("채결 대기중")
        preTime = time.time()
        mode = 2

    elif mode == 2:  # 매수확인
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
        res = requests.get(server_url + "/v1/accounts", headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        soup = soup.prettify()
        soup = soup.split('"')
        current_coin = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        count = 0
        for i in range(len(soup)):
            if soup[i] == 'currency':
                current_coin[count] = soup[i + 2]
                count = count + 1
        a = 0
        for i in range(len(current_coin)):
            if current_coin[i] == choseCoin:
                a = 1
        if a == 1:
            mode = 3
            print()
            print("채결 완료")
            preTime = time.time()
        else:
            A = get_price(choseCoin)
            if nowTime - preTime > 30 and A != buyCoinPrice:
                print("채결실패 - 취소")
                query = {
                    'uuid': str(purchase_uuid),
                }
                query_string = urlencode(query).encode()
                m = hashlib.sha512()
                m.update(query_string)
                query_hash = m.hexdigest()
                payload = {
                    'access_key': access_key,
                    'nonce': str(uuid.uuid4()),
                    'query_hash': query_hash,
                    'query_hash_alg': 'SHA512',
                }
                jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
                authorize_token = 'Bearer {}'.format(jwt_token)
                headers = {"Authorization": authorize_token}
                res = requests.delete(server_url + "/v1/order", params=query, headers=headers)
                mode = 1

    elif mode == 3:  # 기다림
        randomWaitTime = random.randint(randomMin, randomMax)
        print('>>현재 매수 시간:', str(datetime.now()))
        print('>>예상 매도 시간:', datetime.now() + timedelta(seconds=randomWaitTime))
        print(">>현재까지  이윤:", benefit)
        sendmsgB('매수완료 : '+str(choseCoin)+'\n현재 매수 시간 : '+str(datetime.now())+'\n다음 매도 시간 : '+str(datetime.now() + timedelta(seconds=randomWaitTime)))
        while 1:
            nowTime = time.time()
            time.sleep(1)
            if nowTime - preTime > randomWaitTime:
                mode = 4
                break

    elif mode == 4:  # 매도
        print("매도 준비")
        sellCoinPrice = get_price(choseCoin)
        # purchase_amount = float(purchaseMoney / sellCoinPrice)
        print("매도개수:", str(purchase_amount))
        print("주문가격:", str(sellCoinPrice))
        query = {
            'market': 'KRW-' + str(choseCoin),
            'side': 'ask',  # bid 매수 ask 매도
            'volume': str(purchase_amount),  # 주문량
            'price': str(sellCoinPrice),  # 주문가격
            'ord_type': 'limit',  # 주문타입 limit지정가 price 시장가(매수) market 시장가(매도)
        }
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
        res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        soup = soup.prettify()
        soup = soup.split('"')
        purchase_uuid = soup[3]
        print("//////////////////////////////////////////////////////////////////////////////////////")
        print(res.text)
        print("//////////////////////////////////////////////////////////////////////////////////////")
        print("매도신청 완료")
        mode = 5
        print("채결 대기중")
        pre_time = time.time()

    elif mode == 5:  # 매도 확인
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
        res = requests.get(server_url + "/v1/accounts", headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        soup = soup.prettify()
        soup = soup.split('"')
        current_coin = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        count = 0
        for i in range(len(soup)):
            if soup[i] == 'currency':
                current_coin[count] = soup[i + 2]
                count = count + 1
        a = 0
        for i in range(len(current_coin)):
            if current_coin[i] == choseCoin:
                a = 1
        if a == 0:
            mode = 6
            print()
            print("채결 완료")
            # 채결 후 손익확인
            payload = {
                'access_key': access_key,
                'nonce': str(uuid.uuid4()),
            }
            jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
            authorize_token = 'Bearer {}'.format(jwt_token)
            headers = {"Authorization": authorize_token}
            res = requests.get(server_url + "/v1/accounts", headers=headers)
            preTime = time.time()
            soup = BeautifulSoup(res.content, 'html.parser')
            soup = soup.prettify()
            soup = soup.split('"')
            current_money = round(float(soup[7]), 2)
            benefit = round((benefit + current_money - present_money), 3)  # 손익계산
            purchaseMoney = round((purchaseMoney + current_money - present_money), 3)  # 손익피드백
        else:
            A = get_price(choseCoin)
            if nowTime - preTime > 30 and A != sellCoinPrice:
                print("채결실패 - 취소")
                query = {
                    'uuid': str(purchase_uuid),
                }
                query_string = urlencode(query).encode()
                m = hashlib.sha512()
                m.update(query_string)
                query_hash = m.hexdigest()
                payload = {
                    'access_key': access_key,
                    'nonce': str(uuid.uuid4()),
                    'query_hash': query_hash,
                    'query_hash_alg': 'SHA512',
                }
                jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
                authorize_token = 'Bearer {}'.format(jwt_token)
                headers = {"Authorization": authorize_token}
                res = requests.delete(server_url + "/v1/order", params=query, headers=headers)
                mode = 4
                preTime = time.time()
    elif mode == 6:  # 마치며
        playTime = playTime + 1
        presentCoin = choseCoin
        mode = 0
