from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np
import pandas as pd


class BaseDetector(ABC):
    @abstractmethod
    def predict(self, input_image: List[np.ndarray]) -> pd.DataFrame:

        """
        Predicts the bounding boxes of the objects in the image

        Parameters
        ----------

        input_image: List[np.ndarray]
            List of input images

        Returns
        -------
        result: pd.DataFrame
            DataFrame containing the bounding boxes and the class of the objects


        The DataFrame must contain the following columns:
        - xmin: int
        - ymin: int
        - xmax: int
        - ymax: int
        - confidence: float
        - class: str
        """

        pass

    @staticmethod
    def generate_predictions_mask(
        predictions: pd.DataFrame, img: np.ndarray, margin: int = 0
    ) -> np.ndarray:
        """
        Generates a mask of the predictions bounding boxes

        Parameters
        ----------
        predictions : pd.DataFrame
            DataFrame containing the bounding boxes and the class of the objects
        img : np.ndarray
            Image where the predictions were made
        margin : int, optional
            Margin to add to the bounding box, by default 0

        Returns
        -------
        np.ndarray
            Mask of the predictions bounding boxes

        Raises
        ------
        TypeError
            If predictions type is not pd.DataFrame
        """

        if type(predictions) != pd.DataFrame:
            raise TypeError("predictions must be a pandas dataframe")

        mask = np.ones(img.shape[:2], dtype=img.dtype)

        for index, row in predictions.iterrows():

            xmin = round(row["xmin"])
            ymin = round(row["ymin"])
            xmax = round(row["xmax"])
            ymax = round(row["ymax"])

            mask[ymin - margin : ymax + margin, xmin - margin : xmax + margin] = 0

        return mask
