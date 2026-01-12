#!/usr/bin/env python3
"""AI Chatbot Log Analysis - Processes chat_logs.jsonl for AB report evaluation"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import Counter

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ChatLogAnalyzer:
    def __init__(self, log_file_path="conversation_logs/chat_logs.jsonl"):
        self.log_file_path = Path(log_file_path)
        self.df = None
        self.analysis_results = {}
        
    def load_logs(self):
        """Load and parse JSONL log file into DataFrame"""
        logs = []
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        logs.append(json.loads(line.strip()))
                    except json.JSONDecodeError as e:
                        print(f"Warning: Invalid JSON on line {line_num}: {e}")
            
            if not logs:
                print("No logs found or all logs were invalid")
                return False
                
            self.df = pd.DataFrame(logs)
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            self._extract_features()
            
            print(f"Loaded {len(self.df)} conversation logs")
            return True
            
        except FileNotFoundError:
            print(f"ERROR: Log file not found: {self.log_file_path}")
            return False
        except Exception as e:
            print(f"ERROR: Error loading logs: {e}")
            return False
    
    def _extract_features(self):
        """Extract additional features for analysis"""
        def categorize_query(prompt):
            prompt_lower = prompt.lower()
            if any(kw in prompt_lower for kw in ['add to cart', 'cart', 'buy', 'purchase', 'enroll']):
                return 'Cart Action'
            elif any(kw in prompt_lower for kw in ['course', 'learn', 'recommend', 'show me', 'what courses']):
                return 'Course Search'
            elif any(kw in prompt_lower for kw in ['what', 'how', 'why', 'help', 'explain']):
                return 'General Question'
            elif any(kw in prompt_lower for kw in ['hello', 'hi', 'hey', 'good']):
                return 'Greeting'
            else:
                return 'Other'
        
        self.df['query_type'] = self.df['user_prompt'].apply(categorize_query)
        self.df['hour'] = self.df['timestamp'].dt.hour
        self.df['date'] = self.df['timestamp'].dt.date
        self.df['has_agent_action'] = self.df['agent_actions'].apply(len) > 0
        self.df['action_count'] = self.df['agent_actions'].apply(len)
        self.df['prompt_length'] = self.df['user_prompt'].str.len()
        self.df['response_length'] = self.df['model_response'].str.len()
    
    def generate_basic_stats(self):
        """Generate basic statistics table"""
        if self.df is None:
            print("ERROR: No data loaded. Call load_logs() first.")
            return None
        
        stats = {
            'Total Conversations': len(self.df),
            'Unique Users': self.df['user_email'].nunique(),
            'Success Rate': f"{(self.df['status'] == 'success').mean():.1%}",
            'Agent Actions Triggered': self.df['has_agent_action'].sum(),
            'Avg Prompt Length': f"{self.df['prompt_length'].mean():.1f} chars",
            'Avg Response Length': f"{self.df['response_length'].mean():.1f} chars",
            'Date Range': f"{self.df['timestamp'].min().date()} to {self.df['timestamp'].max().date()}"
        }
        
        return stats
    
    def analyze_query_types(self):
        """Analyze distribution of query types"""
        if self.df is None:
            return None
        
        query_counts = self.df['query_type'].value_counts()
        query_percentages = (query_counts / len(self.df) * 100).round(1)
        
        return pd.DataFrame({
            'Count': query_counts,
            'Percentage': query_percentages
        })
    
    def analyze_agent_actions(self):
        """Analyze agent action effectiveness"""
        if self.df is None:
            return None
        
        action_stats = {
            'Total Conversations': len(self.df),
            'Conversations with Actions': self.df['has_agent_action'].sum(),
            'Action Success Rate': f"{(self.df[self.df['has_agent_action']]['status'] == 'success').mean():.1%}",
            'Total Actions': self.df['action_count'].sum()
        }
        
        action_types = [action.get('type', 'Unknown') 
                       for actions in self.df['agent_actions'] 
                       for action in actions]
        
        return action_stats, dict(Counter(action_types))
    
    def analyze_user_activity(self):
        """Analyze user activity patterns"""
        if self.df is None:
            return None
        
        return {
            'hourly_activity': self.df.groupby('hour').size(),
            'daily_activity': self.df.groupby('date').size(),
            'top_users': self.df['user_email'].value_counts().head(10)
        }
    
    def save_analysis_results(self, output_dir="analysis_results"):
        """Save all analysis results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        stats = self.generate_basic_stats()
        if stats:
            with open(output_path / "basic_stats.txt", 'w') as f:
                f.write("=== Chatbot Analysis Statistics ===\n\n")
                for key, value in stats.items():
                    f.write(f"{key}: {value}\n")
        
        query_analysis = self.analyze_query_types()
        if query_analysis is not None:
            query_analysis.to_csv(output_path / "query_types.csv")
        
        action_stats, action_types = self.analyze_agent_actions()
        if action_stats:
            with open(output_path / "agent_actions.txt", 'w') as f:
                f.write("=== Agent Action Statistics ===\n\n")
                for key, value in action_stats.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n=== Action Types ===\n")
                for action_type, count in action_types.items():
                    f.write(f"{action_type}: {count}\n")
        
        user_activity = self.analyze_user_activity()
        if user_activity:
            user_activity['hourly_activity'].to_csv(output_path / "hourly_activity.csv")
            user_activity['daily_activity'].to_csv(output_path / "daily_activity.csv")
            user_activity['top_users'].to_csv(output_path / "top_users.csv")
        
        print(f"Analysis results saved to {output_path}")
        return output_path

def main():
    """Main function to run the analysis"""
    print("Starting Chat Log Analysis...")
    
    analyzer = ChatLogAnalyzer()
    if not analyzer.load_logs():
        return
    
    print("\nBasic Statistics:")
    stats = analyzer.generate_basic_stats()
    if stats:
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    print("\nQuery Type Analysis:")
    query_analysis = analyzer.analyze_query_types()
    if query_analysis is not None:
        print(query_analysis)
    
    print("\nAgent Action Analysis:")
    action_stats, action_types = analyzer.analyze_agent_actions()
    if action_stats:
        for key, value in action_stats.items():
            print(f"  {key}: {value}")
    
    analyzer.save_analysis_results()
    print("\nAnalysis complete! Check analysis_results/ folder for detailed outputs.")

if __name__ == "__main__":
    main()
