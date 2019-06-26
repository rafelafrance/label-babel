import random
import numpy as np
from PIL import Image
from torchvision.transforms import transforms as xforms
from torchvision.transforms import functional


class Compose:
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, image, target):
        for transform in self.transforms:
            image, target = transform(image, target)
        return image, target


class RandomHorizontalFlip:
    def __init__(self, prob):
        self.prob = prob

    def __call__(self, image, target):
        if random.random() < self.prob:
            height, width = image.shape[-2:]
            image = image.flip(-1)
            bbox = target['boxes']
            bbox[:, [0, 2]] = width - bbox[:, [2, 0]]
            target['boxes'] = bbox
        return image, target


class RandomVerticalFlip:
    def __init__(self, prob):
        self.prob = prob

    def __call__(self, image, target):
        if random.random() < self.prob:
            height, width = image.shape[-2:]
            image = image.flip(-2)
            bbox = target['boxes']
            bbox[:, [1, 3]] = height - bbox[:, [3, 1]]
            target['boxes'] = bbox
        return image, target


class RandomRotate:
    def __init__(self, prob90=0.25, prob180=0.25, prob270=0.25):
        self.prob90 = prob90
        self.prob180 = prob90 + prob180
        self.prob270 = self.prob180 + prob270

    def __call__(self, image, target):
        rnd = random.random()
        bbox = np.array(target['boxes'])
        height, width = image.shape[-2:]

        if rnd < self.prob90:
            bbox = bbox[:, [1, 2, 3, 0]]
            bbox[:, [1, 3]] = width - bbox[:, [1, 3]]
            image = image.rot90(1, [1, 2])
        elif rnd < self.prob180:
            bbox = bbox[:, [2, 3, 0, 1]]
            bbox[:, [0, 2]] = width - bbox[:, [0, 2]]
            bbox[:, [1, 3]] = height - bbox[:, [1, 3]]
            image = image.rot90(2, [1, 2])
        elif rnd < self.prob270:
            bbox = bbox[:, [3, 0, 1, 2]]
            bbox[:, [0, 2]] = height - bbox[:, [0, 2]]
            image = image.rot90(-1, [1, 2])

        target['boxes'] = bbox
        return image, target

    def rotate_boxes(self):
        pass


class ColorJitter:
    def __init__(self, brightness=0, contrast=0, saturation=0, hue=0):
        self.jitter = xforms.ColorJitter(
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
            hue=hue)

    def __call__(self, image, target):
        image = Image.fromarray(image.mul(255).permute(1, 2, 0).byte().numpy())
        image = self.jitter(image)
        image = functional.to_tensor(image)
        return image, target


class ToTensor:
    def __call__(self, image, target):
        image = functional.to_tensor(image)
        return image, target
