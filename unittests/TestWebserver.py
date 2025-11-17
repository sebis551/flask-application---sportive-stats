import requests
import json
import unittest

from datetime import datetime, timedelta
from time import sleep
import os

from deepdiff import DeepDiff

total_score = 0

ONLY_LAST = False

class TestWebserver(unittest.TestCase):
    def setUp(self):
        os.system("rm -rf results/*")
        output_dir = f"output"
        input_dir = f"input"
        input_files = os.listdir(input_dir)


        for input_file in input_files:
            # Get the index from in-idx.json
            # The idx is between a dash (-) and a dot (.)
            idx = input_file.split('-')[1]
            idx = int(idx.split('.')[0])

            with open(f"{input_dir}/{input_file}", "r") as fin:
                # Data to be sent in the POST request
                req_data = json.load(fin)
                # Sending a POST request to the Flask endpoint
                res = requests.post(f"http://127.0.0.1:5000/api/state_mean", json=req_data)
        requests.get("http://127.0.0.1:5000/api/graceful_shutdown")


    def check_res_timeout(self, res_callable, ref_result, timeout_sec, id = 0,  poll_interval = 0.2):
        initial_timestamp = datetime.now()
        response = res_callable()
            # print(response)
        
            # Asserting that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
            # Asserting the response data
        response_data = response.json()
        self.assertEqual(response_data, ref_result)

            

    
    def test_jobs(self):
        self.helper_test_endpoint("jobs")
    
    def test_num_jobs(self):
        self.helper_test_endpoint("jobs_num")

    def helper_test_endpoint(self, endpoint):
        global total_score

        output_dir = f"{endpoint}/output"
        input_dir = f"{endpoint}/input"
        input_files = os.listdir(input_dir)

        test_suite_score = 50
        test_score = 50
        local_score = 0

        with open(f"{output_dir}/out.json", "r") as fout:
            ref_result = json.load(fout)
        self.check_res_timeout(
                    res_callable = lambda: requests.get(f"http://127.0.0.1:5000/api/{endpoint}"),
                    ref_result = ref_result,
                    timeout_sec = 1)
        local_score += test_score
        total_score += min(round(local_score), test_suite_score)

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        print(f"Total score {total_score}")
