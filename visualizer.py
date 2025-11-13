"""
Visualization Module
Handles all chart generation and data visualization for the study tracker.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Dict, List
import tkinter as tk


class Visualizer:
    """Creates various charts and visualizations for study data"""
    
    @staticmethod
    def create_pie_chart(subject_time: Dict[str, int], parent_window: tk.Toplevel):
        """
        Create a pie chart showing time distribution by subject.
        
        Args:
            subject_time: Dictionary mapping subjects to minutes
            parent_window: Tkinter window to display chart in
        """
        if not subject_time:
            return
        
        # Create figure
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        subjects = list(subject_time.keys())
        times = list(subject_time.values())
        
        colors = plt.cm.Set3(range(len(subjects)))
        
        wedges, texts, autotexts = ax.pie(
            times,
            labels=subjects,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )
        
        # Make percentage text more readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title("Study Time Distribution by Subject", fontsize=14, fontweight='bold')
        
        # Add canvas to window
        canvas = FigureCanvasTkAgg(fig, parent_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    @staticmethod
    def create_bar_chart(subject_time: Dict[str, int], parent_window: tk.Toplevel):
        """
        Create a bar chart showing total time spent on each subject.
        
        Args:
            subject_time: Dictionary mapping subjects to minutes
            parent_window: Tkinter window to display chart in
        """
        if not subject_time:
            return
        
        # Sort by time
        sorted_subjects = sorted(subject_time.items(), key=lambda x: x[1], reverse=True)
        subjects = [s[0] for s in sorted_subjects]
        times = [s[1] for s in sorted_subjects]
        
        # Create figure
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        bars = ax.bar(subjects, times, color='#4a90e2', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{int(height)} min',
                ha='center',
                va='bottom',
                fontweight='bold'
            )
        
        ax.set_xlabel("Subject", fontsize=12, fontweight='bold')
        ax.set_ylabel("Time (minutes)", fontsize=12, fontweight='bold')
        ax.set_title("Total Study Time by Subject", fontsize=14, fontweight='bold')
        
        # Rotate x-axis labels if needed
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        # Add canvas to window
        canvas = FigureCanvasTkAgg(fig, parent_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    @staticmethod
    def create_productivity_chart(sessions: List[Dict], parent_window: tk.Toplevel):
        """
        Create a line chart showing productivity over time.
        
        Args:
            sessions: List of study sessions
            parent_window: Tkinter window to display chart in
        """
        if not sessions:
            return
        
        # Extract productivity data
        productivity_scores = [s['productivity'] for s in sessions]
        session_numbers = list(range(1, len(sessions) + 1))
        
        # Create figure
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        ax.plot(session_numbers, productivity_scores, marker='o', linewidth=2, 
                markersize=8, color='#e74c3c', alpha=0.7)
        
        # Add average line
        avg_productivity = sum(productivity_scores) / len(productivity_scores)
        ax.axhline(y=avg_productivity, color='#27ae60', linestyle='--', 
                   linewidth=2, label=f'Average: {avg_productivity:.2f}')
        
        ax.set_xlabel("Session Number", fontsize=12, fontweight='bold')
        ax.set_ylabel("Productivity Level", fontsize=12, fontweight='bold')
        ax.set_title("Productivity Trend Over Time", fontsize=14, fontweight='bold')
        ax.set_ylim(0, 6)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        fig.tight_layout()
        
        # Add canvas to window
        canvas = FigureCanvasTkAgg(fig, parent_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    @staticmethod
    def create_daily_study_chart(sessions: List[Dict], parent_window: tk.Toplevel):
        """
        Create a bar chart showing study time per day.
        
        Args:
            sessions: List of study sessions
            parent_window: Tkinter window to display chart in
        """
        if not sessions:
            return
        
        from datetime import datetime
        
        # Group sessions by date
        daily_time = {}
        for session in sessions:
            try:
                date = datetime.strptime(session['timestamp'], "%Y-%m-%d %H:%M:%S").date()
                date_str = date.strftime("%m/%d")
                daily_time[date_str] = daily_time.get(date_str, 0) + session['duration']
            except ValueError:
                continue
        
        # Sort by date
        dates = sorted(daily_time.keys())
        times = [daily_time[d] for d in dates]
        
        # Create figure
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        bars = ax.bar(dates, times, color='#9b59b6', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=9
            )
        
        ax.set_xlabel("Date", fontsize=12, fontweight='bold')
        ax.set_ylabel("Time (minutes)", fontsize=12, fontweight='bold')
        ax.set_title("Daily Study Time", fontsize=14, fontweight='bold')
        
        # Rotate x-axis labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        # Add canvas to window
        canvas = FigureCanvasTkAgg(fig, parent_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
