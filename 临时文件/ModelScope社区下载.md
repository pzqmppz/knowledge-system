ModelScope 下载模型时如何指定下载地址
https://modelscope.cn/docs/models/download

无论是使用命令行还是ModelScope SDK，模型会下载到~/.cache/modelscope/hub默认路径下。如果需要修改 cache 目录，可以手动设置环境变量：MODELSCOPE_CACHE，完成设置后，模型将下载到该环境变量指定的目录中。

下载整个模型repo到指定目录（path/to/dir）
    modelscope download --model 'Qwen/Qwen2-7b' --local_dir 'path/to/dir'
 --local_dir "E:\ai-deploy\models\Qwen3-TTS"
 --local_dir "E:\ai-deploy\models\Qwen3-TTS-Base"
