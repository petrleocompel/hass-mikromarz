import requests


class MikromarzApi:
    ip: str

    def __init__(self, ip: str):
        self.ip = ip

    # 23;01;08;10;39;29;0083951977;SE1-PM2;000;082;000;034;000;101;000;000;169;237;004;000;228;063;005;000;054;012;007;000;000;000;000;000;000;000;000;000;000;000;000;000;000;000;
    def get_data(self) -> str:
        res = requests.get(f"http://{self.ip}/dataout.htm")

        if res.status_code != 200:
            raise ValueError("Not working")
        return res.text
