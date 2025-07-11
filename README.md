代码：

数据放在data文件夹下（需要下载coco数据集的图片并指定路径），训练结果放在output文件夹下，配置文件放在config文件夹下
启动训练：
python -m torch.distributed.run --nproc_per_node=8 --master-port 25110 retrieval.py --config ./configs/vitl14_336/coco/soft_label.yaml