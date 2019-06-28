import json
from PIL import Image
import torch


BOX = 'box'
CAT = 'category'
PATH = 'path'
CLASS = 'class'
SUB_ID = 'subject_id'



class LabelBabelDataset(torch.utils.data.Dataset):
    def __init__(self, df, transforms):
        df[BOX] = df[BOX].apply(json.loads)
        self.df = df
        self.transforms = transforms

    def __getitem__(self, idx):
        subject = self.df.iloc[idx]

        image = Image.open(subject[PATH]).convert('RGB')

        klass = int(subject[CLASS])
        labels = torch.full((1,), klass, dtype=torch.int64)

        boxes = [subject[BOX]]
        boxes = torch.as_tensor(boxes, dtype=torch.float32)

        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])

        target = {
            'boxes': boxes,
            'labels': labels,
            'image_id': torch.tensor([subject[SUB_ID]]),
            'area': area,
            'iscrowd': torch.zeros((1,), dtype=torch.int64),
        }

        if self.transforms is not None:
            image, target = self.transforms(image, target)

        return image, target

    def __len__(self):
        return self.df.shape[0]
