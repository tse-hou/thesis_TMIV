import os
import pandas as pd
from sys import argv
from cal_quality_metric import cal_quality_1024x1024


def produce_testcases():
    testcases = []
    for i in range(1, 8):
        num_view_per_pass = [i]
        testcases.append({"num_Passes": len(num_view_per_pass),
                         "num_view_per_pass": num_view_per_pass})

    for i in range(1, 8):
        for j in range(i+1, 8):
            num_view_per_pass = [i, j]
            testcases.append(
                {"num_Passes": len(num_view_per_pass), "num_view_per_pass": num_view_per_pass})

    for i in range(1, 8):
        for j in range(i+1, 8):
            for k in range(j+1, 8):
                num_view_per_pass = [i, j, k]
                testcases.append(
                    {"num_Passes": len(num_view_per_pass), "num_view_per_pass": num_view_per_pass})
    return testcases


def parse_quality_metric(rec_video, ori_video):
    cal_quality_1024x1024(rec_video, ori_video)
    df = pd.read_csv("vmaflog.csv")
    return df.iloc[0]["psnr"]


def parse_theo_time(log_path):
    log_data = []
    theo_time = 0
    with open(log_path, 'r') as f:
        log_data = f.readlines()
    for line in log_data:
        if("Total" in line):
            line_data = line.split(' ')
            theo_time = line_data[2]
            break
    return theo_time


def main():
    dataset_name = argv[1]
    testcases = produce_testcases()
    results = {"Dataset": [], "Frame": [], "Synthesized.View": [],
               "X.passes": [], "WS.PSNR": [], "CEL": [], "theo_time": [], "p1": [], "p2": [], "p3": []}
    for target_view_idx in range(200):
        theo_time_list = []
        for num_view in range(1, 8):
            num_view_per_pass_str = '_'.join(
                str(x) for x in [num_view])
            log_path = f"output/{dataset_name}/decode_log/{target_view_idx}/{num_view_per_pass_str}.log"
            theo_time = parse_theo_time(log_path)
            theo_time_list.append(theo_time)
        for testcase in testcases:
            # parse testcase info
            results['Dataset'].append(dataset_name)
            results['Frame'].append(0)
            results['Synthesized.View'].append(target_view_idx)
            results['X.passes'].append(testcase['num_Passes'])
            for i in range(3):
                if(i < testcase['num_Passes']):
                    results[f'p{i+1}'].append(testcase['num_view_per_pass'][i])
                else:
                    results[f'p{i+1}'].append(0)
            # parse theo_time
            results['theo_time'].append(
                theo_time_list[testcase['num_view_per_pass'][testcase['num_Passes']-1]])
            # parse quality metic
            rec_video = f"output/{dataset_name}/target_view/{target_view_idx}/{num_view_per_pass_str}_1024x1024_yuv420p10le.yuv"
            ori_video = f"GT/{dataset_name}/frames{target_view_idx}.yuv"
            ws_psnr = parse_quality_metric(rec_video, ori_video)
            results["WS.PSNR"].append(ws_psnr)
            # CEL
            results["CEL"].append((ws_psnr-20)/theo_time)

    df = pd.DataFrame(data=results)
    df.to_csv(f"results/{dataset_name}_raw.csv")
