# Background

This repository is a modernized fork of [Soccer Video Analytics](https://github.com/tryolabs/soccer-video-analytics) by Tryolabs, enhanced with several improvements for better maintainability, type safety, and configurability.

## Key Improvements

- **Python 3.10+ Support**: Updated to work with the latest Python version
- **Poetry 2.0+ Package Management**: Modern dependency management and virtual environment handling
- **Type Annotations**: Added comprehensive typing throughout the codebase for better IDE support and code reliability
- **Unit Testing**: Implemented pytest-based test suite for core functionality validation
- **Dynamic Team Configuration**: Enhanced `team_config.json` for comprehensive team management including colors, visual styling, match setup, and team identification
- **Enhanced Code Quality**: Improved code structure and documentation

These updates make the project more robust, easier to maintain, and more flexible for different soccer match scenarios.

# Soccer Video Analytics

This repository contains the companion code of the blog post [Automatically measuring soccer ball possession with AI and video analytics](https://tryolabs.com/blog/2022/10/17/measuring-soccer-ball-possession-ai-video-analytics) by [Tryolabs](https://tryolabs.com).

<a href="https://www.youtube.com/watch?v=CWnlGBVaRpQ" target="_blank">
<img src="https://user-images.githubusercontent.com/33181424/193869946-ad7e3973-a28e-4640-8494-bf899d5df3a7.png" width="60%" height="50%">
</a>

For further information on the implementation, please check out the post.

## How to install

To install the necessary dependencies we use [Poetry](https://python-poetry.org/docs). After you have it installed, follow these instructions:

1. Clone this repository:

   ```bash
   git clone git@github.com:tryolabs/soccer-video-analytics.git
   ```

2. Install the dependencies:

   ```bash
   poetry install
   ```

3. Optionally, download the ball.pt file [from the GitHub release](https://github.com/tryolabs/soccer-video-analytics/releases/tag/v0). Please note that this is just a toy model that overfits to a few videos, not a robust ball detection model.

4. Configure team colors by setting up the `team_config.json` file (see Team Configuration section below).

## Team Configuration

This project uses a `team_config.json` file to dynamically control team information, colors, visual styling, and match setup. You need to create this file in the root directory to define the teams and their corresponding properties.

### Setting up team_config.json

Create a `team_config.json` file in the project root with the following structure:

```json
{
  "teams": [
    {
      "name": "Chelsea",
      "abbreviation": "CHE",
      "colors": ["blue", "green"],
      "color": [255, 0, 0],
      "board_color": [244, 86, 64],
      "text_color": [255, 255, 255]
    },
    {
      "name": "Man City",
      "abbreviation": "MNC",
      "colors": ["sky_blue"],
      "color": [240, 230, 188],
      "board_color": null,
      "text_color": [0, 0, 0]
    },
    {
      "name": "Referee",
      "abbreviation": "REF",
      "colors": ["black"],
      "color": [0, 0, 0],
      "board_color": null,
      "text_color": [255, 255, 255]
    }
  ],
  "match": {
    "home_team": "Chelsea",
    "away_team": "Man City",
    "initial_possession": "Man City"
  }
}
```

### Configuration Properties

#### Team Properties
- **`name`**: Full team name (e.g., "Chelsea")
- **`abbreviation`**: 3-letter uppercase team code (e.g., "CHE")
- **`colors`**: Array of jersey colors for player classification (see available colors below)
- **`color`**: RGB values [R, G, B] for team's primary display color
- **`board_color`**: RGB values for scoreboard/UI elements (null to use primary color)
- **`text_color`**: RGB values for text displayed over team colors

#### Match Configuration
- **`home_team`**: Name of the home team
- **`away_team`**: Name of the away team  
- **`initial_possession`**: Which team starts with ball possession

### Example Configurations

#### Basic Configuration (Legacy Format)
```json
{
  "teams": [
    {
      "name": "Team A",
      "abbreviation": "TMA",
      "colors": ["blue", "white"],
      "color": [0, 0, 255],
      "board_color": null,
      "text_color": [255, 255, 255]
    },
    {
      "name": "Team B",
      "abbreviation": "TMB", 
      "colors": ["red", "black"],
      "color": [255, 0, 0],
      "board_color": null,
      "text_color": [255, 255, 255]
    }
  ],
  "match": {
    "home_team": "Team A",
    "away_team": "Team B",
    "initial_possession": "Team A"
  }
}
```

#### Advanced Configuration (Chelsea vs Man City)
```json
{
  "teams": [
    {
      "name": "Chelsea",
      "abbreviation": "CHE",
      "colors": ["blue", "white"],
      "color": [0, 86, 179],
      "board_color": [244, 86, 64],
      "text_color": [255, 255, 255]
    },
    {
      "name": "Man City",
      "abbreviation": "MNC",
      "colors": ["sky_blue"],
      "color": [108, 171, 221],
      "board_color": [25, 25, 112],
      "text_color": [255, 255, 255]
    }
  ],
  "match": {
    "home_team": "Chelsea",
    "away_team": "Man City",
    "initial_possession": "Man City"
  }
}
```

**Note**: Make sure to customize the team names, abbreviations, colors, and match setup to match the teams in your video for accurate player classification and proper team identification throughout the analysis.

## How to run

First, make sure to initialize your environment using `poetry env activate`.

To run one of the applications (possession computation and passes counter) you need to use flags in the console.

These flags are defined in the following table:

| Argument | Description | Default value |
| ----------- | ----------- | ----------- |
| `--possession` or `--passes` | Use `--possession` to run the possession counter or `--passes` to run the passes counter | None, but one is mandatory |
| `--model` | Path to the soccer ball model weights (`pt` format) | `models/ball.pt` |
| `--video` | Path to the input video | `videos/soccer_possession.mp4` |
| `--config` | Path to the team configuration JSON file | `team_config.json` |

The following command shows you how to run this project:

```
python run.py [--possession | --passes] [--model <path-to-model>] [--video <path-to-video>] [--config <path-to-config>]
```

>__Warning__: You have to run this command on the root of the project folder.

Here is an example on how to run the command:
    
```bash
python run.py --possession --model models/ball.pt --video videos/soccer_possession.mp4 --config team_config.json
```

An mp4 video will be generated after the execution. The name is the same as the input video with the suffix `_out` added.
