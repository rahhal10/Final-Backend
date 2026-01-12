#!/usr/bin/env python3
"""AI Chatbot Visualizations - Creates charts and graphs for AB report evaluation"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from analyze_logs import ChatLogAnalyzer

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

class ChatVisualizer:
    def __init__(self, analyzer=None):
        self.analyzer = analyzer or ChatLogAnalyzer()
        self.output_dir = Path("analysis_results/charts")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_query_type_distribution(self):
        """Create bar chart showing query type distribution"""
        if self.analyzer.df is None:
            print("ERROR: No data loaded")
            return None
        
        query_counts = self.analyzer.df['query_type'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(query_counts.index, query_counts.values, 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        
        ax.set_title('Distribution of User Query Types', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Query Type', fontsize=12)
        ax.set_ylabel('Number of Queries', fontsize=12)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        output_path = self.output_dir / "query_type_distribution.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Query type distribution chart saved to {output_path}")
        return output_path
    
    def create_agent_action_analytics(self):
        """Create pie chart and bar chart for agent actions"""
        if self.analyzer.df is None:
            print("ERROR: No data loaded")
            return None
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        action_counts = self.analyzer.df['has_agent_action'].value_counts()
        ax1.pie(action_counts.values, labels=['No Agent Action', 'Has Agent Action'], 
               colors=['#FF6B6B', '#4ECDC4'], autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 12})
        ax1.set_title('Agent Action Trigger Rate', fontsize=14, fontweight='bold')
        
        action_success = self.analyzer.df[self.analyzer.df['has_agent_action']]['status'].value_counts()
        bars = ax2.bar(['Success', 'Error'], 
                      [action_success.get('success', 0), action_success.get('error', 0)],
                      color=['#4ECDC4', '#FF6B6B'])
        
        ax2.set_title('Agent Action Success Rate', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Number of Actions', fontsize=12)
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        ax2.grid(axis='y', alpha=0.3)
        plt.suptitle('Agent Action Analytics', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        output_path = self.output_dir / "agent_action_analytics.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Agent action analytics chart saved to {output_path}")
        return output_path
    
    def create_user_activity_timeline(self):
        """Create timeline chart showing user activity patterns"""
        if self.analyzer.df is None:
            print("ERROR: No data loaded")
            return None
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        hourly_activity = self.analyzer.df.groupby('hour').size()
        hours = list(range(24))
        activity_counts = [hourly_activity.get(hour, 0) for hour in hours]
        
        ax1.bar(hours, activity_counts, color='#45B7D1', alpha=0.7)
        ax1.set_title('User Activity by Hour of Day', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Hour of Day', fontsize=12)
        ax1.set_ylabel('Number of Conversations', fontsize=12)
        ax1.set_xticks(range(0, 24, 2))
        ax1.grid(axis='y', alpha=0.3)
        
        max_activity = max(activity_counts)
        peak_hours = [i for i, count in enumerate(activity_counts) if count == max_activity]
        for hour in peak_hours:
            ax1.axvline(x=hour, color='red', linestyle='--', alpha=0.5, label=f'Peak: {hour}:00')
        ax1.legend()
        
        daily_activity = self.analyzer.df.groupby('date').size()
        ax2.plot(daily_activity.index, daily_activity.values, 
                marker='o', linewidth=2, markersize=6, color='#4ECDC4')
        ax2.set_title('Daily Conversation Trend', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Number of Conversations', fontsize=12)
        ax2.grid(True, alpha=0.3)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.suptitle('User Activity Timeline Analysis', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        output_path = self.output_dir / "user_activity_timeline.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"User activity timeline chart saved to {output_path}")
        return output_path
    
    def create_response_analysis(self):
        """Create analysis of response lengths and patterns"""
        if self.analyzer.df is None:
            print("ERROR: No data loaded")
            return None
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        ax1.hist(self.analyzer.df['response_length'], bins=20, color='#96CEB4', 
                alpha=0.7, edgecolor='black')
        ax1.set_title('Response Length Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Response Length (characters)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.grid(axis='y', alpha=0.3)
        
        mean_length = self.analyzer.df['response_length'].mean()
        ax1.axvline(mean_length, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {mean_length:.1f}')
        ax1.legend()
        
        ax2.scatter(self.analyzer.df['prompt_length'], self.analyzer.df['response_length'], 
                   alpha=0.6, color='#FF6B6B')
        ax2.set_title('Prompt vs Response Length', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Prompt Length (characters)', fontsize=12)
        ax2.set_ylabel('Response Length (characters)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        z = np.polyfit(self.analyzer.df['prompt_length'], self.analyzer.df['response_length'], 1)
        p = np.poly1d(z)
        ax2.plot(self.analyzer.df['prompt_length'], p(self.analyzer.df['prompt_length']), 
                "r--", alpha=0.8, linewidth=2, label='Trend Line')
        ax2.legend()
        
        plt.suptitle('Response Analysis', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        output_path = self.output_dir / "response_analysis.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Response analysis chart saved to {output_path}")
        return output_path
    
    def create_evaluation_summary_table(self):
        """Create a summary table for evaluation metrics"""
        if self.analyzer.df is None:
            print("ERROR: No data loaded")
            return None
        
        stats = self.analyzer.generate_basic_stats()
        query_analysis = self.analyzer.analyze_query_types()
        action_stats, action_types = self.analyzer.analyze_agent_actions()
        
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('tight')
        ax.axis('off')
        
        table_data = [
            ['Metric', 'Value', 'Description'],
            ['Total Conversations', str(stats.get('Total Conversations', 'N/A')), 'Total number of chat interactions'],
            ['Unique Users', str(stats.get('Unique Users', 'N/A')), 'Number of distinct users'],
            ['Success Rate', stats.get('Success Rate', 'N/A'), 'Percentage of successful responses'],
            ['Agent Actions Triggered', str(stats.get('Agent Actions Triggered', 'N/A')), 'Number of times agent actions were executed'],
            ['Avg Prompt Length', stats.get('Avg Prompt Length', 'N/A'), 'Average user input length'],
            ['Avg Response Length', stats.get('Avg Response Length', 'N/A'), 'Average AI response length'],
            ['Most Common Query Type', query_analysis.index[0] if query_analysis is not None else 'N/A', 'Most frequent type of user query'],
            ['Peak Activity Hour', str(self.analyzer.df.groupby('hour').size().idxmax()) + ':00', 'Hour with most user activity'],
        ]
        
        table = ax.table(cellText=table_data, loc='center', cellLoc='left',
                        colWidths=[0.3, 0.2, 0.5])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2)
        
        for i in range(3):
            table[(0, i)].set_facecolor('#4ECDC4')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        for i in range(1, len(table_data)):
            for j in range(3):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f0f0f0')
        
        plt.title('Chatbot Evaluation Summary', fontsize=16, fontweight='bold', pad=20)
        
        output_path = self.output_dir / "evaluation_summary_table.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Evaluation summary table saved to {output_path}")
        return output_path
    
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("Generating all visualizations...")
        
        if self.analyzer.df is None:
            if not self.analyzer.load_logs():
                return False
        
        charts = [
            self.create_query_type_distribution(),
            self.create_agent_action_analytics(),
            self.create_user_activity_timeline(),
            self.create_response_analysis(),
            self.create_evaluation_summary_table()
        ]
        
        successful_charts = [chart for chart in charts if chart is not None]
        print(f"Generated {len(successful_charts)} visualizations in {self.output_dir}")
        return successful_charts

def main():
    """Main function to generate all visualizations"""
    print("Starting Visualization Generation...")
    
    visualizer = ChatVisualizer()
    charts = visualizer.generate_all_visualizations()
    
    if charts:
        print(f"\nAll visualizations generated successfully!")
        print(f"Check {visualizer.output_dir} for all charts")
    else:
        print("\nFailed to generate visualizations")

if __name__ == "__main__":
    import numpy as np
    main()
