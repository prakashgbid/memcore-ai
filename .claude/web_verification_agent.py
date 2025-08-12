#!/usr/bin/env python3
"""
Web Action Verification Agent
Automatically verifies web actions and provides detailed reports
"""

import asyncio
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error
import yaml

class WebVerificationAgent:
    """Agent for automatic web action verification"""
    
    def __init__(self, config_path: str = "~/.claude/verification.yml"):
        """Initialize the verification agent"""
        self.config_path = Path(config_path).expanduser()
        self.config = self._load_config()
        self.results = []
        self.github_user = self.config.get('github_user', 'prakashgbid')
        
    def _load_config(self) -> Dict:
        """Load verification configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            'github_user': 'prakashgbid',
            'verification_rules': {
                'github_push': {
                    'retry_count': 3,
                    'retry_delay': 10
                },
                'pages_deploy': {
                    'retry_count': 6,
                    'retry_delay': 30
                }
            }
        }
    
    async def verify_github_repo(self, repo: str) -> Tuple[bool, str, str]:
        """Verify GitHub repository exists and is accessible"""
        url = f"https://github.com/{self.github_user}/{repo}"
        return await self._verify_url(url, "GitHub Repository", 
                                     retries=3, delay=10)
    
    async def verify_github_wiki(self, repo: str) -> Tuple[bool, str, str]:
        """Verify GitHub wiki exists and is accessible"""
        url = f"https://github.com/{self.github_user}/{repo}/wiki"
        return await self._verify_url(url, "GitHub Wiki",
                                     retries=3, delay=10)
    
    async def verify_github_pages(self, repo: str) -> Tuple[bool, str, str]:
        """Verify GitHub Pages site is live"""
        url = f"https://{self.github_user}.github.io/{repo}/"
        # Pages can take longer to deploy
        return await self._verify_url(url, "GitHub Pages",
                                     retries=6, delay=30)
    
    async def verify_pypi_package(self, package: str) -> Tuple[bool, str, str]:
        """Verify PyPI package exists"""
        api_url = f"https://pypi.org/pypi/{package}/json"
        url = f"https://pypi.org/project/{package}/"
        
        for attempt in range(3):
            try:
                with urllib.request.urlopen(api_url) as response:
                    if response.status == 200:
                        return (True, url, "✅ Package available on PyPI")
            except urllib.error.HTTPError as e:
                if e.code == 404 and attempt < 2:
                    await asyncio.sleep(20)
                    continue
                return (False, url, f"❌ Package not found (HTTP {e.code})")
            except Exception as e:
                return (False, url, f"❌ Error: {str(e)}")
        
        return (False, url, "❌ Package not available after 3 attempts")
    
    async def verify_npm_package(self, package: str) -> Tuple[bool, str, str]:
        """Verify npm package exists"""
        api_url = f"https://registry.npmjs.org/{package}"
        url = f"https://www.npmjs.com/package/{package}"
        
        for attempt in range(3):
            try:
                with urllib.request.urlopen(api_url) as response:
                    if response.status == 200:
                        return (True, url, "✅ Package available on npm")
            except urllib.error.HTTPError as e:
                if e.code == 404 and attempt < 2:
                    await asyncio.sleep(10)
                    continue
                return (False, url, f"❌ Package not found (HTTP {e.code})")
            except Exception as e:
                return (False, url, f"❌ Error: {str(e)}")
        
        return (False, url, "❌ Package not available after 3 attempts")
    
    async def _verify_url(self, url: str, description: str,
                         retries: int = 3, delay: int = 10) -> Tuple[bool, str, str]:
        """Generic URL verification with retries"""
        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    if response.status in [200, 301, 302]:
                        return (True, url, f"✅ {description} verified")
            except urllib.error.HTTPError as e:
                if e.code == 404 and attempt < retries - 1:
                    await asyncio.sleep(delay)
                    continue
                elif attempt == retries - 1:
                    if "github.io" in url:
                        return (False, url, f"⏳ {description} pending (may still be building)")
                    return (False, url, f"❌ {description} not found (HTTP {e.code})")
            except Exception as e:
                if attempt == retries - 1:
                    return (False, url, f"❌ Error: {str(e)}")
            
            await asyncio.sleep(delay)
        
        return (False, url, f"❌ {description} verification failed after {retries} attempts")
    
    async def batch_verify(self, action_type: str, items: List[str]) -> Dict:
        """Batch verify multiple items of the same type"""
        results = {
            'success': [],
            'failed': [],
            'pending': []
        }
        
        verify_funcs = {
            'github': self.verify_github_repo,
            'wiki': self.verify_github_wiki,
            'pages': self.verify_github_pages,
            'pypi': self.verify_pypi_package,
            'npm': self.verify_npm_package
        }
        
        if action_type not in verify_funcs:
            raise ValueError(f"Unknown action type: {action_type}")
        
        verify_func = verify_funcs[action_type]
        
        # Run verifications in parallel
        tasks = [verify_func(item) for item in items]
        results_list = await asyncio.gather(*tasks)
        
        for item, (success, url, message) in zip(items, results_list):
            result = {
                'item': item,
                'url': url,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
            if success:
                results['success'].append(result)
            elif "pending" in message.lower() or "building" in message.lower():
                results['pending'].append(result)
            else:
                results['failed'].append(result)
            
            self.results.append(result)
        
        return results
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate a verification report"""
        if not self.results:
            return "No verification results to report"
        
        report = ["# Web Action Verification Report\n"]
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"GitHub User: {self.github_user}\n")
        
        # Summary
        success_count = sum(1 for r in self.results if "✅" in r['message'])
        failed_count = sum(1 for r in self.results if "❌" in r['message'])
        pending_count = sum(1 for r in self.results if "⏳" in r['message'])
        
        report.append("\n## Summary\n")
        report.append(f"- Total Verifications: {len(self.results)}\n")
        report.append(f"- ✅ Successful: {success_count}\n")
        report.append(f"- ❌ Failed: {failed_count}\n")
        report.append(f"- ⏳ Pending: {pending_count}\n")
        
        # Details table
        report.append("\n## Verification Details\n")
        report.append("| Status | Item | URL | Message | Time |\n")
        report.append("|--------|------|-----|---------|------|\n")
        
        for result in self.results:
            status = "✅" if "✅" in result['message'] else "❌" if "❌" in result['message'] else "⏳"
            timestamp = result['timestamp'].split('T')[1].split('.')[0]
            report.append(f"| {status} | {result['item']} | [{result['url']}]({result['url']}) | {result['message']} | {timestamp} |\n")
        
        # Failed items detail
        if failed_count > 0:
            report.append("\n## Failed Verifications\n")
            for result in self.results:
                if "❌" in result['message']:
                    report.append(f"- **{result['item']}**: {result['message']}\n")
                    report.append(f"  - URL: {result['url']}\n")
                    report.append(f"  - Suggested Action: Check if the resource exists and URL is correct\n")
        
        # Pending items
        if pending_count > 0:
            report.append("\n## Pending Verifications\n")
            report.append("These items may still be processing:\n\n")
            for result in self.results:
                if "⏳" in result['message']:
                    report.append(f"- **{result['item']}**: {result['url']}\n")
                    report.append(f"  - Note: GitHub Pages can take 5-10 minutes to deploy\n")
        
        # Recommendations
        report.append("\n## Recommendations\n")
        if failed_count > 0:
            report.append("- Review failed items and ensure they were properly created/deployed\n")
            report.append("- Check repository settings for GitHub Pages if docs verification failed\n")
        if pending_count > 0:
            report.append("- Re-run verification for pending items in a few minutes\n")
        if success_count == len(self.results):
            report.append("- All verifications passed! ✅\n")
        
        report_text = "".join(report)
        
        # Save to file if specified
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(report_text)
            print(f"Report saved to: {output_path}")
        
        return report_text
    
    async def auto_verify_from_context(self, context: str) -> Dict:
        """Automatically detect and verify actions from context"""
        results = {
            'detected_actions': [],
            'verification_results': {}
        }
        
        # Detect GitHub repos
        if "pushed to github" in context.lower() or "github.com" in context:
            # Extract repo names (simplified pattern matching)
            import re
            repo_pattern = r'github\.com/[^/]+/([^/\s]+)'
            repos = re.findall(repo_pattern, context)
            if repos:
                results['detected_actions'].append(('github', repos))
                results['verification_results']['github'] = await self.batch_verify('github', repos)
        
        # Detect wiki updates
        if "wiki" in context.lower():
            # Could extract repo names from context
            pass
        
        # Detect Pages deployments
        if "github pages" in context.lower() or "github.io" in context:
            # Extract repo names from Pages URLs
            import re
            pages_pattern = r'\.github\.io/([^/\s]+)'
            repos = re.findall(pages_pattern, context)
            if repos:
                results['detected_actions'].append(('pages', repos))
                results['verification_results']['pages'] = await self.batch_verify('pages', repos)
        
        # Detect PyPI packages
        if "pypi" in context.lower() or "pip install" in context:
            import re
            pip_pattern = r'pip install ([a-z0-9-]+)'
            packages = re.findall(pip_pattern, context.lower())
            if packages:
                results['detected_actions'].append(('pypi', packages))
                results['verification_results']['pypi'] = await self.batch_verify('pypi', packages)
        
        return results


async def main():
    """Main function for testing"""
    agent = WebVerificationAgent()
    
    # Test with the projects we created
    projects = [
        'evolux-ai',
        'cognitron-engine',
        'codeforge-ai',
        'strategix-planner',
        'autonomix-engine',
        'flowmaster-orchestrator',
        'memcore-ai'
    ]
    
    print("🔍 Starting Web Action Verification\n")
    
    # Verify GitHub repositories
    print("Verifying GitHub Repositories...")
    github_results = await agent.batch_verify('github', projects)
    
    # Verify GitHub Wikis
    print("\nVerifying GitHub Wikis...")
    wiki_results = await agent.batch_verify('wiki', projects)
    
    # Verify GitHub Pages
    print("\nVerifying GitHub Pages...")
    pages_results = await agent.batch_verify('pages', projects)
    
    # Generate report
    print("\n" + "="*50)
    report = agent.generate_report("verification_report.md")
    print(report)
    
    return agent.results


if __name__ == "__main__":
    asyncio.run(main())