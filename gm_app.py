import argparse
import os
import random
import time

import requests


class GenyMotionEmulatorUtil:
    def __init__(self) -> None:
        self.bearer_token: str = None
        self.api_uri = 'https://api.geny.io/cloud'
        self.instance_uuid = '95016679-8f8d-4890-b026-e4ad889aadf1'
        self.user_email = os.getenv('GM_USERNAME')
        self.user_pwd = os.getenv('GM_PASSWORD')
        self.cur_id: str = None
        self.timeout = 60

    def login(self):
        response = requests.post(f'{self.api_uri}/v1/users/login', json={
            'email': self.user_email,
            'password': self.user_pwd
        })

        assert response.ok, f'Genymotion login failed!, Reason: {response.text}'
        assert 'token' in response.json(), 'No "token" found genymotion login'
        token = response.json()['token']
        self.bearer_token = f'Bearer {token}'

        return token

    def list_instances(self) -> list[dict]:
        response = requests.get(f'{self.api_uri}/v2/instances?state=BOOTING&state=ONLINE&ordering=created_at', headers={
            'Authorization': self.bearer_token
        })
        results = response.json()['results']
        return results

    def get_instance_id(self) -> list[dict]:
        results = self.list_instances()
        return results[0]['uuid']

    def start_instance(self):
        print(f'Creating an emulator instance!')
        random_id = ''.join(random.choices('0123456789', k=6))
        response = requests.post(
            f'{self.api_uri}/v1/recipes/{self.instance_uuid}/start-disposable',
            json={
                'instance_name': f'Instance-{random_id}'
            },
            headers={
                'Authorization': self.bearer_token
            },
        )
        
        assert response.status_code != 200, f'Unable to start Emulator Instance. Reason: {response.text}'
        self.cur_id = response.json()['uuid']
        print(f'Instance started with ID: {random_id}')

        self.wait_until_running()
        print(f'Instance in STARTED state with: {self.cur_id}')        

    def wait_until_running(self):
        end_time = time.time() + self.timeout

        while True:
            if time.time() > end_time:
                raise TimeoutError(
                    f"Emulator didn't come in started state after {self.timeout} seconds."
                )

            time.sleep(5)

            response = requests.get(f'{self.api_uri}/v1/instances/{self.cur_id}', headers={
                'Authorization': self.bearer_token
            })

            if not response.ok or response.json().get('state', '') != 'ONLINE':
                continue
            else:
                break


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '--start-instance',
        help='Starts a new Emulator instance',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--get-instance-id',
        help='Fetches newly started instance if',
        default=False,
        action='store_true',
    )
    args, _ = parser.parse_known_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    genymotion_manager = GenyMotionEmulatorUtil()
    genymotion_manager.login()

    if args.start_instance:
        genymotion_manager.start_instance()
    
    if args.get_instance_id:
        print(genymotion_manager.get_instance_id())
