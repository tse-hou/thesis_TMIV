import os
import pandas as pd
from sys import argv


def cal_quality_1920x1080(reconstructed_video, ref_video):
    os.system(
        f'~/bin/ffmpeg -s:v 1920x1080 -pix_fmt yuv420p10le -r 30 -i {reconstructed_video} -s:v 1920x1080 -pix_fmt yuv420p10le -r 30 -i {ref_video} -filter_complex "[0:v]scale=1920x1080:flags=bicubic,format=pix_fmts=yuv420p10le,fps=fps=30/1[main]; [1:v]scale=1920x1080:flags=bicubic,format=pix_fmts=yuv420p10le,fps=fps=30/1[ref]; [main][ref]libvmaf=psnr=true:ssim=true:model_path=/usr/local/share/model/vmaf_v0.6.1.json:log_path=vmaflog.csv:log_fmt=csv" -f null -')


def cal_quality_480x270(reconstructed_video, ref_video):
    os.system(
        f'~/bin/ffmpeg -s:v 480x270 -pix_fmt yuv420p10le -r 30 -i {reconstructed_video} -s:v 480x270 -pix_fmt yuv420p10le -r 30 -i {ref_video} -filter_complex "[0:v]scale=480x270:flags=bicubic,format=pix_fmts=yuv420p10le,fps=fps=30/1[main]; [1:v]scale=480x270:flags=bicubic,format=pix_fmts=yuv420p10le,fps=fps=30/1[ref]; [main][ref]libvmaf=psnr=true:ssim=true:model_path=/usr/local/share/model/vmaf_v0.6.1.json:log_path=vmaflog.csv:log_fmt=csv" -f null -')


def cal_quality_1024x1024(reconstructed_video, ref_video):
    os.system(
        f'~/bin/ffmpeg -s:v 1024x1024 -pix_fmt yuv420p10le -r 30 -i {reconstructed_video} -s:v 1024x1024 -pix_fmt yuv420p10le -r 30 -i {ref_video} -filter_complex "[0:v]scale=1024x1024:flags=bicubic,format=pix_fmts=yuv420p10le,fps=fps=30/1[main]; [1:v]scale=1024x1024:flags=bicubic,format=pix_fmts=yuv420p10le,fps=fps=30/1[ref]; [main][ref]libvmaf=psnr=true:ssim=true:model_path=/usr/local/share/model/vmaf_v0.6.1.json:log_path=vmaflog.csv:log_fmt=csv" -f null -')


def summarize_quality_metric(quality_output_file):
    df = pd.read_csv(quality_output_file)
    print(f"psnr: mean: {df['psnr'].mean()}, std: {df['psnr'].std()}")
    print(f"ssim: mean: {df['ssim'].mean()}, std: {df['ssim'].std()}")
    print(f"vmaf: mean: {df['vmaf'].mean()}, std: {df['vmaf'].std()}")


# cal_quality_1024x1024("/home/tsehou/tmiv-v3.1/output/apartment1/target_view/0/2_5_7_1024x1024_yuv420p10le.yuv",
#                       "/home/tsehou/tmiv-v3.1/GT/apartment1/frames0.yuv")
# summarize_quality_metric("vmaflog.csv")
