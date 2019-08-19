# Style Transfer for HD Video
## Introduction
Since it is not practical to apply optimization-based video style transfer 
on 6000X4000 resolution video, we first use style transfer on low resolution 1500X1000 video, 
and then utilize super resolution (SRGAN). Note that we apply and modify 2 projects in github(See Ref).
For the following arguments, just specify the corresponging file directory.


## Usage
1. put "Sky" directory (required data) in the main directory. 

2. use ffmpeg to save every video frame. Note that folders should be first created in case error occurs.
    ``` 
    ffmpeg -i "Sky/content/sky1/Video1_LR.avi" "video_input_LR/Video1_LR/frame_%04d.ppm"
    ```

3. compute optical flow
    ```
    cd "neural-style-tf-master/optical_flow/"
    bash make-opt-flow.sh "../../video_input_LR/Video1_LR/frame_%04d.ppm" "../../video_input_LR/Video1_LR/"
    ```

4. download the pretrained VGG-19 model weights (http://www.vlfeat.org/matconvnet/pretrained/), 
and put "imagenet-vgg-verydeep-19.mat" in "neural-style-tf-master".

5. in "neural-style-tf-master" directory, run style transfer with specified input, output, style
    ```
    python3 neural_style.py --video \
                            --video_input_dir "../video_input_LR/Video1_LR" \
                            --video_output_dir "../video_output_LR/Video1_LR_style1" \
                            --style_imgs_dir "../Sky/style (option 2.2)" \
                            --style_imgs "1.jpg" \
                            --end_frame "72" \
                            --max_size "1500" \
                            --verbose
    ```

6. Then, download the pretrained SRGAN model weights (https://github.com/tensorlayer/srgan/releases/download/1.2.0/g_srgan.npz), 
and put "g_srgan.npz" in "srgan-1.2.0/checkpoint".

7. Now, we use SRGAN to enhance the resolution. Since using GPU may cause 
memory error (resolution too high), we use CPU to evaluate.
    ```
    cd "../srgan-1.2.0/"
    CUDA_VISIBLE_DEVICES="" python3 main.py --mode evaluate --input_dir "../video_output_LR/Video1_LR_style1/" --output_dir "../video_output_HR/Video1_HR_style1/"
    ```

8. use mask to filter uninterested regions.
    ```
    cd "../"
    python3 apply_mask.py --input_dir "video_output_HR/Video1_HR_style1/" \
                          --output_dir "video_output_HR_masked/Video1_HR_style1/" \
                          --mask_path "Sky/mask/mask_HR1.png"
    ```

9. Finally, use ffmpeg to convert frames to video
    ```
    ffmpeg -framerate 24 -i "video_output_HR_masked/Video1_HR_style1/frame_%04d.png" -c:v libx264 -pix_fmt yuv420p "Video1_HR_style1_stylized_masked.mp4"
    ```


## REFERENCE: 
1. https://github.com/cysmith/neural-style-tf
2. https://github.com/tensorlayer/srgan?fbclid=IwAR0NpqMU7IBLij-V_DQ0Z7gDMziMV3bVJ2ocgNDdnUcAQZqAicyl0yKXMO0
