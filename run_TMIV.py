import os
import json
import pandas as pd
from pathlib import Path
from sys import argv
TMIV_ENCODER_PATH = "./tmiv-v3.1/install.gcc/bin/Encoder"
TMIV_DECODER_PATH = "./tmiv-v3.1/install.gcc/bin/Decoder"
TMIV_CONFIG_PATH = "config/TMIV_config.json"
HM_ENCODER_PATH = "./HM/bin/TAppEncoderStatic"
HM_CONFIG_PATH = "config/HM_config.cfg"



def modify_target_view_pose(dataset_name, target_view_idx):
    user_pose_df = pd.read_csv(f"user_pose/{dataset_name}p01.csv")
    userpose = user_pose_df.iloc[target_view_idx]
    pd.DataFrame(userpose).T.to_csv(f"input_dataset/{dataset_name}/{dataset_name}_tmp.csv", index=False)


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


def modify_config_before_encode(dataset_name,tmiv_config_path_for_this_dataset):
    json_data = {}
    with open(tmiv_config_path_for_this_dataset) as f:
        json_data = json.load(f)
    json_data["SourceCameraParameters"] = f"{dataset_name}.json"
    json_data["SourceDirectory"] = f"input_dataset/{dataset_name}"
    json_data["OutputDirectory"] = f"output/{dataset_name}"
    json_data["PoseTracePath"] = f"{dataset_name}_tmp.csv"
    with open(tmiv_config_path_for_this_dataset, 'w') as f:
        json.dump(json_data, f)

def modify_config_before_decode(dataset_name, num_Passes, num_view_per_pass, tmiv_config_path_for_this_dataset):
    json_data = {}
    with open(tmiv_config_path_for_this_dataset) as f:
        json_data = json.load(f)
    json_data["Decoder"]["MultipassRenderer"]["NumberOfViewsPerPass"] = num_view_per_pass
    json_data["Decoder"]["MultipassRenderer"]["NumberOfPasses"] = num_Passes
    json_data["OutputDirectory"] = f"output/{dataset_name}/rec"
    with open(tmiv_config_path_for_this_dataset, 'w') as f:
        json.dump(json_data, f)


def TMIV_encode(tmiv_config_path_for_this_dataset):
    os.system(f"{TMIV_ENCODER_PATH} -c {tmiv_config_path_for_this_dataset}")


def TMIV_decode(log_path,tmiv_config_path_for_this_dataset):
    os.system(f"{TMIV_DECODER_PATH} -c {tmiv_config_path_for_this_dataset} > {log_path}")

def HM_encode_decode(dataset_name):
    MIV_output_folder = f"output/{dataset_name}"
    os.system(f"mkdir {MIV_output_folder}/rec")
    p = Path(f"{MIV_output_folder}")
    videos_list = list(p.glob("*.yuv"))
    for video in videos_list:
        os.system(f"{HM_ENCODER_PATH} -c {HM_CONFIG_PATH} -i {video} -b output/bitstream -o {MIV_output_folder}/rec/{video.name}")
    os.system(f"cp {MIV_output_folder}/ATL_R0_Tm_c00.bit {MIV_output_folder}/rec")


def main():
    dataset_name = argv[1]
    tmiv_config_path_for_this_dataset = f"config/TMIV_config_{dataset_name}.json"
    os.system(f"cp {TMIV_CONFIG_PATH} {tmiv_config_path_for_this_dataset}")
    os.system(f"mkdir output/{dataset_name}")
    os.system(f"mkdir output/{dataset_name}/decode_log")
    os.system(f"mkdir output/{dataset_name}/target_view")
    modify_config_before_encode(dataset_name,tmiv_config_path_for_this_dataset)
    TMIV_encode(tmiv_config_path_for_this_dataset)
    HM_encode_decode(dataset_name)
    for target_view_idx in range(200):
        print(f"target_view: {target_view_idx}")
        os.system(f"mkdir output/{dataset_name}/target_view/{target_view_idx}")
        os.system(f"mkdir output/{dataset_name}/decode_log/{target_view_idx}")
        modify_target_view_pose(dataset_name, target_view_idx)
        testcases = produce_testcases()
        for testcase in testcases:
            modify_config_before_decode(dataset_name, testcase["num_Passes"], testcase["num_view_per_pass"],tmiv_config_path_for_this_dataset)
            num_view_per_pass_str = '_'.join(str(x) for x in testcase['num_view_per_pass'])
            TMIV_decode(f"output/{dataset_name}/decode_log/{target_view_idx}/{num_view_per_pass_str}.log",tmiv_config_path_for_this_dataset)
            os.system(f"mv output/{dataset_name}/rec/output_1024x1024_yuv420p10le.yuv output/{dataset_name}/target_view/{target_view_idx}/{num_view_per_pass_str}_1024x1024_yuv420p10le.yuv")

if __name__ == "__main__":
    main()