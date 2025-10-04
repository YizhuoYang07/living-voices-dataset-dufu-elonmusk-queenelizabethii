"""
API Configuration for Tang-Song Literature Chronological Map

This module contains configuration settings for accessing the 
Tang-Song Literature API to collect Du Fu's data.

Author: Living Voices Project
Date: 2024-10-04
"""

import json
from pathlib import Path
from typing import Dict, Optional


class APIConfig:
    """
    Configuration class for Tang-Song Literature API.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize API configuration.
        
        Args:
            config_file: Optional path to JSON config file with API settings
        """
        self.base_url = "https://souwenyuan.tsfz.net"
        
        self.endpoints = {
            "writing_overview": "/api/writing",
            "writing_by_dynasty": "/api/writing/{dynasty}",
            "writing_by_author": "/api/writing/{dynasty}/{authorName}/{authorId}",
            "writing_by_author_type": "/api/writing/{dynasty}/{authorName}/{authorId}/{writingType}",
            "writing_by_id": "/api/writing/{writingId}",
            "people_overview": "/api/people",
            "people_by_dynasty": "/api/people/{dynasty}",
            "people_by_id": "/api/people/{peopleId}",
        }
        
        self.du_fu_params = {
            "dynasty": "Tang",
            "authorName": "杜甫",
            "authorId": "17270"
        }
        
        self.request_config = {
            "timeout": 30,
            "retry_attempts": 3,
            "retry_delay": 2,
            "headers": {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        }
        
        if config_file and Path(config_file).exists():
            self._load_config(config_file)
    
    def _load_config(self, config_file: str):
        """
        Load configuration from JSON file.
        
        Args:
            config_file: Path to configuration file
        """
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        if "base_url" in config:
            self.base_url = config["base_url"]
        
        if "endpoints" in config:
            self.endpoints.update(config["endpoints"])
        
        if "request_config" in config:
            self.request_config.update(config["request_config"])
    
    def get_url(self, endpoint_key: str, **kwargs) -> str:
        """
        Construct full URL for an endpoint.
        
        Args:
            endpoint_key: Key from endpoints dictionary
            **kwargs: Parameters to format into the endpoint URL
            
        Returns:
            Full formatted URL
        """
        endpoint = self.endpoints.get(endpoint_key)
        if not endpoint:
            raise ValueError(f"Unknown endpoint: {endpoint_key}")
        
        formatted_endpoint = endpoint.format(**kwargs)
        return f"{self.base_url}{formatted_endpoint}"
    
    def get_du_fu_poems_url(self, writing_type: Optional[str] = None, page_no: int = 0) -> str:
        """
        Get URL for Du Fu's poems.
        
        Args:
            writing_type: Optional writing type filter (e.g., "詩")
            page_no: Page number (default 0)
            
        Returns:
            Full URL with query parameters
        """
        params = self.du_fu_params.copy()
        
        if writing_type:
            endpoint_key = "writing_by_author_type"
            params["writingType"] = writing_type
        else:
            endpoint_key = "writing_by_author"
        
        base_url = self.get_url(endpoint_key, **params)
        
        if page_no > 0:
            return f"{base_url}?pageNo={page_no}"
        
        return base_url
    
    def get_du_fu_biography_url(self) -> str:
        """
        Get URL for Du Fu's biographical information.
        
        Returns:
            Full URL for Du Fu's biography
        """
        return self.get_url(
            "people_by_id",
            peopleId=self.du_fu_params["authorId"]
        )
    
    def save_config(self, output_file: str):
        """
        Save current configuration to JSON file.
        
        Args:
            output_file: Path to save configuration
        """
        config = {
            "base_url": self.base_url,
            "endpoints": self.endpoints,
            "du_fu_params": self.du_fu_params,
            "request_config": self.request_config
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)


def main():
    """
    Test configuration setup.
    """
    config = APIConfig()
    
    print("API Configuration Test")
    print("=" * 70)
    print(f"Base URL: {config.base_url}")
    print(f"\nDu Fu Parameters:")
    for key, value in config.du_fu_params.items():
        print(f"  {key}: {value}")
    
    print(f"\nSample URLs:")
    print(f"  All poems: {config.get_du_fu_poems_url()}")
    print(f"  Page 2: {config.get_du_fu_poems_url(page_no=2)}")
    print(f"  Biography: {config.get_du_fu_biography_url()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
