"""Test module for verifying all project dependencies are working correctly."""

import numpy as np
import numpy.typing as npt
import torch
import cv2  # type: ignore
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import yaml
import tqdm
import seaborn as sns
from PIL import Image
import pytest
from norfair.tracker import Detection, Tracker  # type: ignore


class TestBasicDependencies:
    """Test class for basic dependency functionality."""
    
    def test_numpy(self) -> None:
        """Test NumPy functionality."""
        arr = np.array([1, 2, 3], dtype=np.int64)
        assert arr.mean() == 2.0, "NumPy array mean calculation failed"
        assert arr.dtype == np.int64, "NumPy array dtype is incorrect"
        assert len(arr) == 3, "NumPy array length is incorrect"

    def test_pytorch(self) -> None:
        """Test PyTorch functionality."""
        tensor = torch.tensor([1., 2., 3.])
        assert tensor.mean().item() == 2.0, "PyTorch tensor mean calculation failed"
        assert tensor.dtype == torch.float32, "PyTorch tensor dtype is incorrect"
        assert tensor.shape == torch.Size([3]), "PyTorch tensor shape is incorrect"

    def test_opencv(self) -> None:
        """Test OpenCV functionality."""
        blank_image = np.zeros((100, 100, 3), np.uint8)
        cv2.rectangle(blank_image, (30, 30), (70, 70), (255, 255, 255), -1)  # type: ignore
        assert blank_image.shape == (100, 100, 3), "OpenCV image shape is incorrect"
        assert blank_image.dtype == np.uint8, "OpenCV image dtype is incorrect"
        # Check that rectangle was drawn (white pixel should exist)
        assert np.any(blank_image[50, 50] == [255, 255, 255]), "OpenCV rectangle drawing failed"

    def test_matplotlib(self) -> None:
        """Test matplotlib functionality."""
        blank_image = np.zeros((100, 100, 3), np.uint8)
        fig = plt.figure(figsize=(2, 2))  # type: ignore
        assert fig is not None, "Matplotlib figure creation failed"
        plt.imshow(blank_image)  # type: ignore
        plt.title("Test Plot")  # type: ignore
        plt.close()

    def test_pandas(self) -> None:
        """Test pandas functionality."""
        df = pd.DataFrame({'test': [1, 2, 3]})
        assert len(df) == 3, "Pandas DataFrame length is incorrect"
        assert df['test'].mean() == 2.0, "Pandas DataFrame mean calculation failed"
        assert list(df.columns) == ['test'], "Pandas DataFrame columns are incorrect"
        assert df['test'].sum() == 6, "Pandas DataFrame sum calculation failed"

    def test_yaml(self) -> None:
        """Test YAML functionality."""
        test_data: dict[str, str | list[int]] = {'name': 'test', 'values': [1, 2, 3]}
        yaml_string = yaml.dump(test_data)
        assert isinstance(yaml_string, str), "YAML dump failed to return string"
        
        loaded_data = yaml.safe_load(yaml_string)
        assert loaded_data is not None, "YAML load returned None"
        assert loaded_data['name'] == 'test', "YAML load failed to preserve string value"
        assert loaded_data['values'] == [1, 2, 3], "YAML load failed to preserve list value"

    def test_tqdm(self) -> None:
        """Test tqdm functionality."""
        test_list = list(range(10))
        processed: list[int] = []
        
        # Test tqdm with disabled output for testing
        progress_bar = tqdm.tqdm(test_list, desc="Testing tqdm", disable=True)
        for item in progress_bar:
            processed.append(item * 2)
        
        assert len(processed) == 10, "Tqdm processing failed - incorrect length"
        assert processed[0] == 0, "Tqdm processing failed - incorrect first value"
        assert processed[-1] == 18, "Tqdm processing failed - incorrect last value"
        assert all(processed[i] == i * 2 for i in range(10)), "Tqdm processing failed - incorrect transformation"

    def test_seaborn(self) -> None:
        """Test seaborn functionality."""
        # Reset seaborn settings first
        sns.reset_orig()
        sns.set_theme()
        
        test_df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        assert len(test_df) == 3, "Test DataFrame creation failed"
        
        fig = plt.figure(figsize=(2.0, 2.0))  # type: ignore
        assert fig is not None, "Matplotlib figure creation failed"
        
        ax = sns.scatterplot(data=test_df, x='x', y='y')
        assert ax is not None, "Seaborn scatterplot creation failed"
        
        plt.close()

    def test_pil(self) -> None:
        """Test PIL (Pillow) functionality."""
        blank_image = np.zeros((100, 100, 3), np.uint8)
        
        # Test array to PIL conversion
        pil_image = Image.fromarray(blank_image.astype('uint8'), 'RGB')
        assert pil_image.size == (100, 100), "PIL image creation failed - incorrect size"
        assert pil_image.mode == 'RGB', "PIL image creation failed - incorrect mode"
        
        # Test image resizing
        resized_image = pil_image.resize((50, 50))
        assert resized_image.size == (50, 50), "PIL image resizing failed"
        assert resized_image.mode == 'RGB', "PIL image resizing changed mode"

    def test_norfair(self) -> None:
        """Test norfair functionality."""
        # Test Detection creation
        points: npt.NDArray[np.int_] = np.array([[50, 50]])
        scores: npt.NDArray[np.float64] = np.array([0.9])
        detections = [Detection(points=points, scores=scores)]
        
        assert len(detections) == 1, "Norfair Detection creation failed"
        assert np.array_equal(detections[0].points, points), "Norfair Detection points incorrect"  # type: ignore
        assert np.array_equal(detections[0].scores, scores), "Norfair Detection scores incorrect"  # type: ignore
        
        # Test Tracker creation and update
        tracker = Tracker(distance_function="mean_euclidean", distance_threshold=30)
        assert tracker is not None, "Norfair Tracker creation failed"
        
        tracked_objects = tracker.update(detections=detections)
        assert isinstance(tracked_objects, list), "Norfair tracker update failed to return list"
        # First update might return 0 objects as tracks need time to initialize


@pytest.fixture
def sample_image() -> npt.NDArray[np.uint8]:
    """Fixture providing a sample image for testing."""
    return np.zeros((100, 100, 3), np.uint8)


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Fixture providing a sample DataFrame for testing."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10],
        'category': ['A', 'B', 'A', 'B', 'A']
    })


class TestIntegrationTests:
    """Test class for integration functionality between different libraries."""
    
    def test_integration_opencv_matplotlib(self, sample_image: npt.NDArray[np.uint8]) -> None:
        """Test integration between OpenCV and matplotlib."""
        # Draw on image with OpenCV
        cv2.rectangle(sample_image, (10, 10), (90, 90), (255, 0, 0), 2)  # type: ignore
        
        # Display with matplotlib
        fig = plt.figure(figsize=(3, 3))  # type: ignore
        plt.imshow(cv2.cvtColor(sample_image, cv2.COLOR_BGR2RGB))  # type: ignore
        plt.title("OpenCV + Matplotlib Integration")  # type: ignore
        plt.axis('off')  # type: ignore
        plt.close()
        
        assert fig is not None, "Integration test failed"

    def test_integration_pandas_seaborn(self, sample_dataframe: pd.DataFrame) -> None:
        """Test integration between pandas and seaborn."""
        # Create plot with seaborn using pandas DataFrame
        fig = plt.figure(figsize=(4, 3))  # type: ignore
        ax = sns.scatterplot(data=sample_dataframe, x='x', y='y', hue='category')
        
        assert ax is not None, "Pandas-Seaborn integration failed"
        assert len(sample_dataframe) == 5, "Sample DataFrame incorrect"
        
        plt.close()


class TestDependencyVersions:
    """Test class for checking dependency versions and compatibility."""
    
    def test_numpy_version(self) -> None:
        """Test NumPy version compatibility."""
        version: str = np.__version__
        assert version is not None, "NumPy version not available"
        # Check that we have at least NumPy 1.20
        major, minor = map(int, version.split('.')[:2])
        assert major >= 1 and minor >= 20, f"NumPy version too old: {version}"
    
    def test_torch_version(self) -> None:
        """Test PyTorch version compatibility."""
        version: str = torch.__version__
        assert version is not None, "PyTorch version not available"
        # Check that we have at least PyTorch 1.12
        major, minor = map(int, version.split('.')[:2])
        assert (major > 1) or (major == 1 and minor >= 12), f"PyTorch version too old: {version}"
    
    def test_opencv_version(self) -> None:
        """Test OpenCV version compatibility."""
        version: str = cv2.__version__  # type: ignore
        assert version is not None, "OpenCV version not available"
        assert isinstance(version, str), "OpenCV version is not a string"
        # Check that we have at least OpenCV 4.5
        major, minor = map(int, version.split('.')[:2])
        assert major >= 4 and minor >= 5, f"OpenCV version too old: {version}"


class TestParametrizedTests:
    """Test class for parametrized tests."""
    
    @pytest.mark.parametrize("data_type,expected", [
        (np.int32, np.int32),
        (np.float32, np.float32),
        (np.uint8, np.uint8),
    ])
    def test_numpy_dtypes(self, data_type: type[np.generic], expected: type[np.generic]) -> None:
        """Parametrized test for NumPy data types."""
        arr = np.array([1, 2, 3], dtype=data_type)
        assert arr.dtype == expected, f"NumPy dtype test failed for {data_type}"

    @pytest.mark.parametrize("size,expected_pixels", [
        ((50, 50), 2500),
        ((100, 100), 10000),
        ((200, 150), 30000),
    ])
    def test_pil_image_sizes(self, size: tuple[int, int], expected_pixels: int) -> None:
        """Parametrized test for PIL image sizes."""
        image = Image.new('RGB', size, color='red')
        assert image.size == size, f"PIL image size test failed for {size}"
        width, height = size
        assert width * height == expected_pixels, f"PIL pixel count test failed for {size}"