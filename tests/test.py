# write a script to test the api with set of parameters and track the time and file size of the output
import requests
import time
import json
# param type: {[testing_title]:[...test_params]}
params = {
    "vertices_with_constant_cardinality": [
        {
            "card": 100,
            "xsize": 500,
            "ysize": 500,
            "vertices_bound": [3, 10],
            "irregularity_clip": 0.8,
            "spikiness_clip": 0.8
        },
        {
            "card": 100,
            "xsize": 500,
            "ysize": 500,
            "vertices_bound": [3, 100],
            "irregularity_clip": 0.8,
            "spikiness_clip": 0.8
        },
        # {
        #     "card": 100,
        #     "xsize": 500,
        #     "ysize": 500,
        #     "vertices_bound": [3, 1000],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 100,
        #     "xsize": 500,
        #     "ysize": 500,
        #     "vertices_bound": [3, 10000],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 1000,
        #     "xsize": 1000,
        #     "ysize": 1000,
        #     "vertices_bound": [3, 10],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 1000,
        #     "xsize": 1000,
        #     "ysize": 1000,
        #     "vertices_bound": [3, 100],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 1000,
        #     "xsize": 1000,
        #     "ysize": 1000,
        #     "vertices_bound": [3, 1000],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 1000,
        #     "xsize": 1000,
        #     "ysize": 1000,
        #     "vertices_bound": [3, 10000],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 10000,
        #     "xsize": 10000,
        #     "ysize": 10000,
        #     "vertices_bound": [3, 10],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 10000,
        #     "xsize": 10000,
        #     "ysize": 10000,
        #     "vertices_bound": [3, 100],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 10000,
        #     "xsize": 10000,
        #     "ysize": 10000,
        #     "vertices_bound": [3, 1000],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 10000,
        #     "xsize": 10000,
        #     "ysize": 10000,
        #     "vertices_bound": [3, 10000],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 100000,
        #     "xsize": 100000,
        #     "ysize": 100000,
        #     "vertices_bound": [3, 10],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 100000,
        #     "xsize": 100000,
        #     "ysize": 100000,
        #     "vertices_bound": [3, 100],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        # {
        #     "card": 100000,
        #     "xsize": 100000,
        #     "ysize": 100000,
        #     "vertices_bound": [3, 1000],
        #     "irregularity_clip": 0.8,
        #     "spikiness_clip": 0.8
        # },
        {
            "card": 100000,
            "xsize": 100000,
            "ysize": 100000,
            "vertices_bound": [3, 10000],
            "irregularity_clip": 0.8,
            "spikiness_clip": 0.8
        }
    ],
    "cardinality_with_constant_vertices": [

        {
            "card": 1000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 10000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 20000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 30000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 40000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        }, {
            "card": 50000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },

        {
            "card": 60000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },

        {
            "card": 70000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 80000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },

        {
            "card": 90000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },

        {
            "card": 100000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 200000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 300000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 400000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 500000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },
        {
            "card": 600000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        },

        {
            "card": 700000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip": 0.6,
            "spikiness_clip": 0.6
        }
    ]



}

# output: [dataset_id, time_taken,..params]*3
# output into csv file


# 33
# Define the API endpoint and parameters
api_url = "http://127.0.0.1:5000"


# Define a function to make API requests and measure time


def make_api_request(url, params):
    cleanup_needed = True
    resp = None
    elapsed_time = 0
    try:

        start_time = time.time()
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(params), headers=headers)
        end_time = time.time()
        elapsed_time = end_time - start_time
        resp = response
        cleanup_needed = False
    except Exception as e:
        print(e)
        cleanup_needed = True
    return resp, elapsed_time, cleanup_needed


# Make the API request and measure time

# test_cases_vertices = params["vertices_with_constant_cardinality"]
# test_cases_cardinality = params["cardinality_with_constant_vertices"]

# For Vertices with constant cardinality
for test_title in params.keys():
    result = []
    print(
        f"Starting tests for {test_title} with {len(params[test_title])} test cases")

    with open(f"{test_title}.csv", "w") as f:
        f.write("dataset_id, Tries ,time_taken,card,xsize,ysize,vertices_bound_min,vertices_bound_max,irregularity_clip,spikiness_clip\n")
        f.close()

    for test_case in params[test_title]:
        # run it 3 times
        for i in range(3):

            response, elapsed_time, cleanup = make_api_request(
                api_url, test_case)

            # Check if the request was successful
            if response != None and response.status_code == 200:
                # print("API request successful.")
                resp_data = response.json()
                dataset_id = resp_data["dataset_id"]
                result.append([dataset_id, i + 1, f"{elapsed_time:.2f}", test_case["card"], test_case["xsize"], test_case["ysize"],
                              test_case["vertices_bound"][0], test_case["vertices_bound"][1], test_case["irregularity_clip"], test_case["spikiness_clip"]])
                with open(f"{test_title}.csv", "a") as f:
                    f.write(",".join(list(map(lambda x: str(x), result[-1]))))
                    f.write("\n")
                    f.close()

            elif response != None:
                print(
                    f"API request failed with status code {response.status_code}")
            else:
                print("API request failed")
                # break

        print("Done with test case: ", test_case)
