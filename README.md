Public datasets ( MS COCO, Flickr30K, ECCV Caption.) must be downloaded manually due to licensing and size constraints.
Training code：
python -m torch.distributed.run --nproc_per_node=8 --master-port 25110 retrieval.py --config ./configs/vitl14_336/coco/soft_label.yaml
