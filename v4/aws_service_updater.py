import json
import requests
from bs4 import BeautifulSoup
import time
import os
import re
from datetime import datetime

class AwsServiceUpdater:
    def __init__(self, services_file='aws_services.json'):
        self.services_file = services_file
        self.current_services = self.load_current_services()
        self.update_log = []
        
    def load_current_services(self):
        """Load current AWS services from file"""
        try:
            with open(self.services_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def save_services(self, services):
        """Save updated services to file"""
        with open(self.services_file, 'w') as file:
            json.dump(services, file, indent=4)
        
        # Also save a backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"aws_services_backup_{timestamp}.json"
        with open(backup_file, 'w') as file:
            json.dump(services, file, indent=4)
            
        return backup_file
    
    def fetch_aws_services_from_docs(self):
        """Fetch AWS services from the AWS documentation"""
        print("Fetching AWS services from AWS documentation...")
        
        # AWS service categories page
        url = "https://docs.aws.amazon.com/index.html"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            services = {}
            
            # Find service categories
            categories = soup.select('div.category')
            
            for category in categories:
                category_name = category.select_one('h2').text.strip()
                
                # Find all services in this category
                service_links = category.select('ul li a')
                
                for link in service_links:
                    service_name = link.text.strip()
                    service_url = link.get('href')
                    
                    # Skip non-service links
                    if not service_url or not service_name:
                        continue
                        
                    # Normalize service name to match our format
                    normalized_name = self.normalize_service_name(service_name)
                    
                    # Skip if we couldn't normalize the name
                    if not normalized_name:
                        continue
                    
                    # Check if we already have this service
                    if normalized_name in self.current_services:
                        # Update category if needed
                        if self.current_services[normalized_name]["category"] != category_name:
                            self.current_services[normalized_name]["category"] = category_name
                            self.update_log.append(f"Updated category for {normalized_name} to {category_name}")
                    else:
                        # Add new service with default values
                        self.current_services[normalized_name] = {
                            "description": f"{service_name} - AWS service (description pending)",
                            "category": category_name,
                            "difficulty": "Medium",  # Default difficulty
                            "certification_notes": f"This is a newer AWS service. Research its key features and use cases for certification exams."
                        }
                        self.update_log.append(f"Added new service: {normalized_name} in category {category_name}")
                        
                    # Try to fetch more details about this service
                    if service_url and service_url.startswith('http'):
                        try:
                            time.sleep(1)  # Be nice to AWS servers
                            service_response = requests.get(service_url)
                            if service_response.status_code == 200:
                                service_soup = BeautifulSoup(service_response.text, 'html.parser')
                                
                                # Try to find a description
                                description_elem = service_soup.select_one('div.description')
                                if description_elem:
                                    description = description_elem.text.strip()
                                    if description:
                                        self.current_services[normalized_name]["description"] = description
                                        self.update_log.append(f"Updated description for {normalized_name}")
                        except Exception as e:
                            print(f"Error fetching details for {service_name}: {e}")
            
            return self.current_services
            
        except Exception as e:
            print(f"Error fetching AWS services: {e}")
            return None
    
    def fetch_certification_updates(self):
        """Fetch AWS certification exam updates"""
        print("Fetching AWS certification exam updates...")
        
        # AWS certification page
        url = "https://aws.amazon.com/certification/certification-prep/"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find exam guides which often contain updates
            exam_guides = soup.select('a[href*="exam-guide"]')
            
            for guide in exam_guides:
                guide_url = guide.get('href')
                if guide_url and guide_url.startswith('http'):
                    try:
                        time.sleep(1)  # Be nice to AWS servers
                        guide_response = requests.get(guide_url)
                        if guide_response.status_code == 200:
                            guide_soup = BeautifulSoup(guide_response.text, 'html.parser')
                            
                            # Look for content about exam domains
                            domains = guide_soup.select('div.content h3, div.content h4')
                            
                            for domain in domains:
                                domain_text = domain.text.strip()
                                if any(keyword in domain_text.lower() for keyword in ['domain', 'section', 'area']):
                                    # Found a domain section, look for services mentioned
                                    content = domain.find_next('ul')
                                    if content:
                                        for item in content.select('li'):
                                            item_text = item.text.strip()
                                            
                                            # Look for service names in the content
                                            for service_name in self.current_services.keys():
                                                if service_name.lower() in item_text.lower():
                                                    # Update certification notes
                                                    domain_info = f"Exam domain: {domain_text} - {item_text}"
                                                    if "certification_notes" in self.current_services[service_name]:
                                                        if domain_info not in self.current_services[service_name]["certification_notes"]:
                                                            self.current_services[service_name]["certification_notes"] += f"\n\n{domain_info}"
                                                            self.update_log.append(f"Updated certification notes for {service_name} with exam domain info")
                                                    else:
                                                        self.current_services[service_name]["certification_notes"] = domain_info
                                                        self.update_log.append(f"Added certification notes for {service_name}")
                    except Exception as e:
                        print(f"Error fetching exam guide {guide_url}: {e}")
            
            return self.current_services
            
        except Exception as e:
            print(f"Error fetching certification updates: {e}")
            return None
    
    def normalize_service_name(self, name):
        """Normalize service name to our format (uppercase, no spaces)"""
        # Extract the main service name (before any "Amazon" or "AWS" prefixes)
        name = name.replace("Amazon", "").replace("AWS", "").strip()
        
        # Handle special cases
        if "S3" in name:
            return "S3"
        if "EC2" in name:
            return "EC2"
        if "RDS" in name:
            return "RDS"
        if "Lambda" in name:
            return "LAMBDA"
        
        # Remove common words and punctuation
        name = re.sub(r'[^\w\s]', '', name)
        name = re.sub(r'\s+', '', name)
        
        # Convert to uppercase
        return name.upper() if name else None
    
    def update_from_aws_blogs(self):
        """Update service information from AWS blogs"""
        print("Fetching updates from AWS blogs...")
        
        # AWS What's New blog
        url = "https://aws.amazon.com/new/"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find recent announcements
            announcements = soup.select('div.blog-post')
            
            for announcement in announcements[:20]:  # Limit to recent announcements
                title_elem = announcement.select_one('h2')
                if not title_elem:
                    continue
                    
                title = title_elem.text.strip()
                
                # Check if this announcement mentions any of our services
                for service_name in self.current_services.keys():
                    if service_name.lower() in title.lower():
                        # Get the announcement date
                        date_elem = announcement.select_one('time')
                        date_str = date_elem.text.strip() if date_elem else "Recent update"
                        
                        # Get the announcement content
                        content_elem = announcement.select_one('p')
                        content = content_elem.text.strip() if content_elem else ""
                        
                        # Update certification notes with this new information
                        update_info = f"Recent update ({date_str}): {title} - {content}"
                        if "certification_notes" in self.current_services[service_name]:
                            if update_info not in self.current_services[service_name]["certification_notes"]:
                                self.current_services[service_name]["certification_notes"] += f"\n\n{update_info}"
                                self.update_log.append(f"Added recent update for {service_name}")
                        else:
                            self.current_services[service_name]["certification_notes"] = update_info
                            self.update_log.append(f"Added certification notes for {service_name} with recent update")
            
            return self.current_services
            
        except Exception as e:
            print(f"Error fetching AWS blog updates: {e}")
            return None
    
    def run_update(self):
        """Run the complete update process"""
        print("Starting AWS services update process...")
        
        # Fetch services from AWS docs
        self.fetch_aws_services_from_docs()
        
        # Fetch certification updates
        self.fetch_certification_updates()
        
        # Update from AWS blogs
        self.update_from_aws_blogs()
        
        # Save the updated services
        backup_file = self.save_services(self.current_services)
        
        print(f"Update completed. Services saved to {self.services_file}")
        print(f"Backup saved to {backup_file}")
        print(f"Total updates: {len(self.update_log)}")
        
        for update in self.update_log:
            print(f"- {update}")
        
        return len(self.update_log)

# Add command line argument handling
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Update AWS services database for Hangman game')
    parser.add_argument('--docs-only', action='store_true', help='Only update from AWS documentation')
    parser.add_argument('--cert-only', action='store_true', help='Only update from certification exam guides')
    parser.add_argument('--blogs-only', action='store_true', help='Only update from AWS blogs')
    
    args = parser.parse_args()
    
    updater = AwsServiceUpdater()
    
    if args.docs_only:
        print("Updating from AWS documentation only...")
        updater.fetch_aws_services_from_docs()
        updater.save_services(updater.current_services)
    elif args.cert_only:
        print("Updating from certification exam guides only...")
        updater.fetch_certification_updates()
        updater.save_services(updater.current_services)
    elif args.blogs_only:
        print("Updating from AWS blogs only...")
        updater.update_from_aws_blogs()
        updater.save_services(updater.current_services)
    else:
        updater.run_update()

