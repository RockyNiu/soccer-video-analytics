from typing import List, TypedDict, Optional
import json
import os
from .box import Box
from .colors import HSVColor, black, blue, green, sky_blue


class TeamFilter(TypedDict):
    name: str
    colors: List[HSVColor]


class TeamFilters:
    """Manages team filters for soccer video analytics."""
    
    # Color mapping for configuration file
    _COLOR_MAP = {
        "black": black,
        "blue": blue,
        "green": green,
        "sky_blue": sky_blue,
    }
    
    def __init__(self):
        """Initialize with empty team filters."""
        self._filters: List[TeamFilter] = []
    
    def add_team_filter(self, name: str, colors: List[HSVColor]) -> None:
        """
        Add a new team filter.
        
        Parameters
        ----------
        name : str
            Team name
        colors : List[HSVColor]
            List of HSV colors for the team
        """
        team_filter: TeamFilter = {
            "name": name,
            "colors": colors,
        }
        self._filters.append(team_filter)
    
    def remove_team_filter(self, name: str) -> bool:
        """
        Remove a team filter by name.
        
        Parameters
        ----------
        name : str
            Name of the team filter to remove
            
        Returns
        -------
        bool
            True if filter was removed, False if not found
        """
        for i, filter_item in enumerate(self._filters):
            if filter_item["name"] == name:
                self._filters.pop(i)
                return True
        return False
    
    def get_team_filter(self, name: str) -> Optional[TeamFilter]:
        """
        Get a team filter by name.
        
        Parameters
        ----------
        name : str
            Name of the team filter
            
        Returns
        -------
        Optional[TeamFilter]
            Team filter if found, None otherwise
        """
        for filter_item in self._filters:
            if filter_item["name"] == name:
                return filter_item
        return None
    
    def get_all_filters(self) -> List[TeamFilter]:
        """
        Get all team filters.
        
        Returns
        -------
        List[TeamFilter]
            List of all team filters
        """
        return self._filters.copy()
    
    def get_team_names(self) -> List[str]:
        """
        Get all team names.
        
        Returns
        -------
        List[str]
            List of team names
        """
        return [filter_item["name"] for filter_item in self._filters]
    
    def update_team_colors(self, name: str, colors: List[HSVColor]) -> bool:
        """
        Update colors for an existing team filter.
        
        Parameters
        ----------
        name : str
            Name of the team
        colors : List[HSVColor]
            New list of colors
            
        Returns
        -------
        bool
            True if team was found and updated, False otherwise
        """
        for filter_item in self._filters:
            if filter_item["name"] == name:
                filter_item["colors"] = colors
                return True
        return False
    
    def clear_all_filters(self) -> None:
        """Remove all team filters."""
        self._filters.clear()
    
    def __len__(self) -> int:
        """Return number of team filters."""
        return len(self._filters)
    
    def __iter__(self):
        """Iterate over team filters."""
        return iter(self._filters)
    
    def to_hsv_classifier_format(self) -> List[dict]:
        """
        Convert team filters to format expected by HSVClassifier.
        
        Returns
        -------
        List[dict]
            List of dictionaries with 'name' and 'colors' keys
        """
        return [{"name": team_filter["name"], "colors": team_filter["colors"]} 
                for team_filter in self._filters]
    
    @classmethod
    def from_config_file(cls, config_path: str) -> 'TeamFilters':
        """
        Create TeamFilters instance from a configuration file.
        
        Parameters
        ----------
        config_path : str
            Path to the JSON configuration file
            
        Returns
        -------
        TeamFilters
            TeamFilters instance with teams loaded from config
            
        Raises
        ------
        FileNotFoundError
            If config file doesn't exist
        ValueError
            If config format is invalid or contains unknown colors
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if 'teams' not in config:
            raise ValueError("Configuration file must contain 'teams' key")
        
        team_filters = cls()
        
        for team_config in config['teams']:
            if 'name' not in team_config or 'colors' not in team_config:
                raise ValueError(f"Team config must have 'name' and 'colors' keys: {team_config}")
            
            # Convert color names to HSVColor objects
            colors = []
            for color_name in team_config['colors']:
                if color_name not in cls._COLOR_MAP:
                    raise ValueError(f"Unknown color '{color_name}'. Available colors: {list(cls._COLOR_MAP.keys())}")
                colors.append(cls._COLOR_MAP[color_name])
            
            team_filters.add_team_filter(
                name=team_config['name'],
                colors=colors
            )
        
        return team_filters
