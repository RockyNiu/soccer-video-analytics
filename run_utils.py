import json
from typing import List, Optional, Tuple

import numpy as np
from norfair.tracker import Detection  # type: ignore
from norfair.camera_motion import MotionEstimator, CoordinatesTransformation  # type: ignore

from inference import Converter, YoloV5
from soccer import Ball, Match, Team


def load_teams_from_config(config_path: str, fps: float) -> Tuple[List[Team], Match]:
    """
    Load teams and match configuration from a JSON config file.

    Parameters
    ----------
    config_path : str
        Path to the JSON configuration file
    fps : float
        Frames per second for the match

    Returns
    -------
    Tuple[List[Team], Match]
        List of Team objects and Match object configured from the config file

    Raises
    ------
    FileNotFoundError
        If config file doesn't exist
    ValueError
        If config format is invalid
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    if 'teams' not in config:
        raise ValueError("Configuration file must contain 'teams' key")
    
    # Create Team objects from config
    teams = []
    team_map = {}
    
    for team_config in config['teams']:
        # Skip referee team for match purposes
        if team_config.get('name', '').lower() == 'referee':
            continue
            
        if 'name' not in team_config or 'abbreviation' not in team_config:
            raise ValueError(f"Team config must have 'name' and 'abbreviation' keys: {team_config}")
        
        # Convert color arrays to tuples
        color = tuple(team_config.get('color', [0, 0, 0]))
        board_color = team_config.get('board_color')
        if board_color is not None:
            board_color = tuple(board_color)
        text_color = tuple(team_config.get('text_color', [0, 0, 0]))
        
        team = Team(
            name=team_config['name'],
            abbreviation=team_config['abbreviation'],
            color=color,
            board_color=board_color,
            text_color=text_color
        )
        
        teams.append(team)
        team_map[team.name] = team
    
    # Create Match object
    match_config = config.get('match', {})
    home_team_name = match_config.get('home_team')
    away_team_name = match_config.get('away_team')
    initial_possession_name = match_config.get('initial_possession')
    
    # Find home and away teams
    home_team = None
    away_team = None
    
    if home_team_name and home_team_name in team_map:
        home_team = team_map[home_team_name]
    elif teams:
        home_team = teams[0]
    
    if away_team_name and away_team_name in team_map:
        away_team = team_map[away_team_name]
    elif len(teams) > 1:
        away_team = teams[1]
    
    if not home_team or not away_team:
        raise ValueError("Unable to determine home and away teams from configuration")
      # Create match
    match = Match(home=home_team, away=away_team, fps=int(fps))
    
    # Set initial possession
    if initial_possession_name and initial_possession_name in team_map:
        match.team_possession = team_map[initial_possession_name]
    else:
        match.team_possession = away_team  # Default to away team as in original code
    
    return teams, match


def get_ball_detections(
    ball_detector: YoloV5, frame: np.ndarray
) -> List[Detection]:
    """
    Uses custom Yolov5 detector in order
    to get the predictions of the ball and converts it to
    Norfair.Detection list.

    Parameters
    ----------
    ball_detector : YoloV5
        YoloV5 detector for balls
    frame : np.ndarray
        Frame to get the ball detections from

    Returns
    -------
    List[norfair.Detection]
        List of ball detections
    """
    ball_df = ball_detector.predict([frame])
    ball_df = ball_df[ball_df["confidence"] > 0.3]
    return Converter.DataFrame_to_Detections(ball_df)


def get_player_detections(
    person_detector: YoloV5, frame: np.ndarray
) -> List[Detection]:
    """
    Uses YoloV5 Detector in order to detect the players
    in a match and filter out the detections that are not players
    and have confidence lower than 0.35.

    Parameters
    ----------
    person_detector : YoloV5
        YoloV5 detector
    frame : np.ndarray
        Frame to get the player detections from

    Returns
    -------
    List[norfair.Detection]
        List of player detections
    """

    person_df = person_detector.predict([frame])
    person_df = person_df[person_df["name"] == "person"]
    person_df = person_df[person_df["confidence"] > 0.35]
    person_detections = Converter.DataFrame_to_Detections(person_df)
    return person_detections


def create_mask(frame: np.ndarray, detections: List[Detection]) -> np.ndarray:
    """
    Creates mask in order to hide detections and goal counter for motion estimation

    Parameters
    ----------
    frame : np.ndarray
        Frame to create mask for.
    detections : List[norfair.Detection]
        Detections to hide.

    Returns
    -------
    np.ndarray
        Mask.
    """

    if not detections:
        mask = np.ones(frame.shape[:2], dtype=frame.dtype)
    else:
        detections_df = Converter.Detections_to_DataFrame(detections)
        mask = YoloV5.generate_predictions_mask(detections_df, frame, margin=40)

    # remove goal counter
    mask[69:200, 160:510] = 0

    return mask


def update_motion_estimator(
    motion_estimator: MotionEstimator,
    detections: List[Detection],
    frame: np.ndarray,
) -> Optional[CoordinatesTransformation]:
    """
    Update coordinate transformations every frame

    Parameters
    ----------
    motion_estimator : MotionEstimator
        Norfair motion estimator class
    detections : List[Detection]
        List of detections to hide in the mask
    frame : np.ndarray
        Current frame

    Returns
    -------
    Optional[CoordinatesTransformation]
        Coordinate transformation for the current frame, or None if motion estimation fails
    """
    
    mask = create_mask(frame=frame, detections=detections)
    
    try:
        coord_transformations = motion_estimator.update(frame, mask=mask)
        return coord_transformations
    except Exception as e:
        error_msg = str(e)
        if ("findHomography" in error_msg or 
            "at least 4 corresponding point sets" in error_msg or
            "'NoneType' object is not subscriptable" in error_msg or
            "sparse flow" in error_msg.lower()):
            # Motion estimation failed due to insufficient features or optical flow issues
            print(f"Warning: Motion estimation failed ({type(e).__name__}: {error_msg}). Trying fallback strategies...")
            
            # Fallback 1: Try with a less restrictive mask (smaller margin)
            try:
                if detections:
                    detections_df = Converter.Detections_to_DataFrame(detections)
                    fallback_mask = YoloV5.generate_predictions_mask(detections_df, frame, margin=20)
                    # Still remove goal counter but with smaller area
                    fallback_mask[69:200, 160:510] = 0
                else:
                    fallback_mask = np.ones(frame.shape[:2], dtype=frame.dtype)
                    fallback_mask[69:200, 160:510] = 0
                
                coord_transformations = motion_estimator.update(frame, mask=fallback_mask)
                print("Success with reduced margin mask.")
                return coord_transformations
            except Exception:
                pass
            
            # Fallback 2: Try with no mask (allow detection areas)
            try:
                no_mask = np.ones(frame.shape[:2], dtype=frame.dtype)
                # Only remove goal counter
                no_mask[69:200, 160:510] = 0
                
                coord_transformations = motion_estimator.update(frame, mask=no_mask)
                print("Success with minimal mask (goal counter only).")
                return coord_transformations
            except Exception:
                pass
            
            # Fallback 3: Try with completely open frame (no masking)
            try:
                full_mask = np.ones(frame.shape[:2], dtype=frame.dtype)
                coord_transformations = motion_estimator.update(frame, mask=full_mask)
                print("Success with no mask.")
                return coord_transformations
            except Exception:
                pass
            
            # All fallbacks failed, return None
            print("All motion estimation strategies failed. Using identity transformation.")
            return None
        else:
            # Re-raise other exceptions
            raise e


def get_main_ball(detections: List[Detection], match: Optional[Match] = None) -> Ball:
    """
    Gets the main ball from a list of balls detection

    The match is used in order to set the color of the ball to
    the color of the team in possession of the ball.

    Parameters
    ----------
    detections : List[Detection]
        List of detections
    match : Match, optional
        Match object, by default None

    Returns
    -------
    Ball
        Main ball
    """
    # Create Ball with the first detection if available, otherwise with a default box
    if detections:
        ball = Ball(detection=detections[0])
    else:
        # Create a ball with a default box when no detections are available
        from inference.box import Box
        ball = Ball(box=Box(x=0, y=0, width=10, height=10))

    if match:
        ball.set_color(match)

    return ball
