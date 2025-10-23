"""Website blocking service using hosts file manipulation"""
import os
import platform
import re
from datetime import datetime

class WebsiteBlocker:
    """Manages website blocking through hosts file"""
    
    REDIRECT_IP = "127.0.0.1"
    
    PRESETS = {
        'social_media': [
            'facebook.com', 'www.facebook.com',
            'twitter.com', 'www.twitter.com', 'x.com', 'www.x.com',
            'instagram.com', 'www.instagram.com',
            'tiktok.com', 'www.tiktok.com',
            'reddit.com', 'www.reddit.com',
            'linkedin.com', 'www.linkedin.com'
        ],
        'news': [
            'cnn.com', 'www.cnn.com',
            'bbc.com', 'www.bbc.com',
            'nytimes.com', 'www.nytimes.com',
            'reddit.com', 'www.reddit.com'
        ],
        'entertainment': [
            'youtube.com', 'www.youtube.com',
            'netflix.com', 'www.netflix.com',
            'twitch.tv', 'www.twitch.tv'
        ]
    }
    
    def __init__(self):
        self.hosts_path = self._get_hosts_path()
        self.is_blocking = False
    
    def _get_hosts_path(self):
        """Get hosts file path based on OS"""
        system = platform.system()
        if system == 'Windows':
            return r'C:\Windows\System32\drivers\etc\hosts'
        elif system in ['Linux', 'Darwin']:
            return '/etc/hosts'
        else:
            raise OSError(f"Unsupported OS: {system}")
    
    def validate_url(self, url):
        """Validate and clean URL"""
        url = re.sub(r'^https?://', '', url)
        url = url.rstrip('/').split('/')[0]
        pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return url if re.match(pattern, url) else None
    
    def enable_blocking(self, sites):
        """Enable blocking for given sites"""
        try:
            with open(self.hosts_path, 'r') as f:
                content = f.read()
            
            # Remove existing FocusGuard section
            if '# FocusGuard START' in content:
                start = content.find('# FocusGuard START')
                end = content.find('# FocusGuard END')
                if end > start:
                    content = content[:start] + content[end + len('# FocusGuard END\n'):]
            
            # Add new blocking section
            if sites:
                block_section = '\n# FocusGuard START\n'
                block_section += f'# Updated: {datetime.now().isoformat()}\n'
                for site in sites:
                    block_section += f"{self.REDIRECT_IP} {site}\n"
                block_section += '# FocusGuard END\n'
                content += block_section
            
            with open(self.hosts_path, 'w') as f:
                f.write(content)
            
            self.is_blocking = True
            return True
        except PermissionError:
            raise PermissionError("Run with admin/sudo privileges")
        except Exception as e:
            raise Exception(f"Error updating hosts: {e}")
    
    def disable_blocking(self):
        """Disable all blocking"""
        try:
            with open(self.hosts_path, 'r') as f:
                content = f.read()
            
            if '# FocusGuard START' in content:
                start = content.find('# FocusGuard START')
                end = content.find('# FocusGuard END')
                if end > start:
                    content = content[:start] + content[end + len('# FocusGuard END\n'):]
            
            with open(self.hosts_path, 'w') as f:
                f.write(content)
            
            self.is_blocking = False
            return True
        except Exception as e:
            raise Exception(f"Error disabling blocking: {e}")
    
    def get_preset_sites(self, category):
        """Get preset sites for a category"""
        return self.PRESETS.get(category, [])
