"""
GUI Components Module
Contains all GUI-related components and windows for the study tracker.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Callable, Optional
from utils import Constants, MessageGenerator, TimeFormatter, Validator


class StudyInputForm:
    """Input form for logging study sessions"""
    
    def __init__(self, parent: tk.Frame, on_save: Callable, on_clear: Callable):
        """
        Initialize the study input form.
        
        Args:
            parent: Parent tkinter frame
            on_save: Callback function for save button
            on_clear: Callback function for clear button
        """
        self.parent = parent
        self.on_save = on_save
        self.on_clear = on_clear
        
        self.subject_entry = None
        self.duration_entry = None
        self.productivity_var = None
        self.productivity_label = None
        self.notes_text = None
        
        self._create_form()
    
    def _create_form(self):
        """Create the form widgets"""
        
        # Form title
        form_title = tk.Label(
            self.parent,
            text="Log Study Session",
            font=Constants.HEADING_FONT,
            bg=Constants.WHITE,
            fg=Constants.TEXT_COLOR
        )
        form_title.pack(pady=15)
        
        # Subject
        subject_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        subject_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(subject_frame, text="Subject:", font=Constants.NORMAL_FONT, 
                bg=Constants.WHITE).pack(anchor=tk.W)
        self.subject_entry = ttk.Entry(subject_frame, font=Constants.NORMAL_FONT)
        self.subject_entry.pack(fill=tk.X, pady=5)
        
        # Duration
        duration_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        duration_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(duration_frame, text="Duration (minutes):", font=Constants.NORMAL_FONT, 
                bg=Constants.WHITE).pack(anchor=tk.W)
        self.duration_entry = ttk.Entry(duration_frame, font=Constants.NORMAL_FONT)
        self.duration_entry.pack(fill=tk.X, pady=5)
        
        # Productivity Score
        productivity_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        productivity_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(productivity_frame, text="Productivity Level (1-5):", 
                font=Constants.NORMAL_FONT, bg=Constants.WHITE).pack(anchor=tk.W)
        self.productivity_var = tk.IntVar(value=3)
        
        productivity_scale = ttk.Scale(
            productivity_frame,
            from_=1,
            to=5,
            orient=tk.HORIZONTAL,
            variable=self.productivity_var,
            command=self._update_productivity_label
        )
        productivity_scale.pack(fill=tk.X, pady=5)
        
        self.productivity_label = tk.Label(
            productivity_frame,
            text="3 - Good",
            font=Constants.SMALL_FONT,
            bg=Constants.WHITE,
            fg=Constants.PRIMARY_COLOR
        )
        self.productivity_label.pack()
        
        # Notes
        notes_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        notes_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(notes_frame, text="Notes (optional):", font=Constants.NORMAL_FONT, 
                bg=Constants.WHITE).pack(anchor=tk.W)
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=5, 
                                                     font=Constants.SMALL_FONT)
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        button_frame.pack(pady=20, padx=20, fill=tk.X)
        
        save_button = tk.Button(
            button_frame,
            text="Save Study Session",
            command=self.on_save,
            bg=Constants.PRIMARY_COLOR,
            fg=Constants.WHITE,
            font=Constants.BUTTON_FONT,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        save_button.pack(fill=tk.X, pady=5)
        
        clear_button = tk.Button(
            button_frame,
            text="Clear Form",
            command=self.on_clear,
            bg=Constants.DANGER_COLOR,
            fg=Constants.WHITE,
            font=Constants.SMALL_FONT,
            cursor="hand2"
        )
        clear_button.pack(fill=tk.X, pady=5)
    
    def _update_productivity_label(self, value):
        """Update the productivity level label"""
        value = int(float(value))
        self.productivity_label.config(text=MessageGenerator.get_productivity_label(value))
    
    def get_values(self) -> dict:
        """Get form values"""
        return {
            'subject': self.subject_entry.get().strip(),
            'duration': self.duration_entry.get().strip(),
            'productivity': self.productivity_var.get(),
            'notes': self.notes_text.get("1.0", tk.END).strip()
        }
    
    def clear(self):
        """Clear all form fields"""
        self.subject_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.productivity_var.set(3)
        self.notes_text.delete("1.0", tk.END)
        self._update_productivity_label(3)

