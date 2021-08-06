# ./tmiv-v3.1/install.gcc/bin/Encoder -c TMIV_config.json -p SourceDirectory input_dataset/apartment2 -p OutputDirectory output

# ./tmiv-v3.1/install.gcc/bin/Decoder -c TMIV_config.json -p SourceDirectory input_dataset/apartment2 -p OutputDirectory output -p OutputCameraName v1

./HM/bin/TAppEncoderStatic -c config/HM_config.cfg -i output/ATL_R0_Td_c00_1024x1024_yuv420p10le.yuv -b output/bitstream -o output/rec.yuv