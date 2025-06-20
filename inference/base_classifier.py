from abc import ABC, abstractmethod
from typing import List

import numpy as np
from norfair.tracker import Detection

from inference.box import Box


class BaseClassifier(ABC):
    @abstractmethod
    def predict(self, input_image: List[np.ndarray]) -> List[str]:
        """
        Predicts the class of the objects in the image

        Parameters
        ----------

        input_image: List[np.ndarray]
            List of input images

        Returns
        -------
        result: List[str]
            List of class names
        """
        pass

    def predict_from_detections(
        self, detections: List[Detection], img: np.ndarray
    ) -> List[Detection]:
        """
        Predicts the class of the objects in the image and adds the class in
        detection.data["classification"]

        Parameters
        ----------
        detections : List[norfair.Detection]
            List of detections
        img : np.ndarray
            Image

        Returns
        -------
        List[norfair.Detection]
            List of detections with the class of the objects
        """
        if not all(
            isinstance(detection, Detection) for detection in detections
        ):
            raise TypeError("detections must be a list of norfair.Detection")

        box_images = []

        for detection in detections:
            # Convert points to x, y, width, height format
            x1, y1 = detection.points[0]
            x2, y2 = detection.points[1]
            x = min(x1, x2)
            y = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            box = Box(x, y, width, height, img)
            box_images.append(box.img)

        class_name = self.predict(box_images)

        for detection, name in zip(detections, class_name):
            detection.data["classification"] = name

        return detections
