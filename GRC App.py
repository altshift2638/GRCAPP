# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 21:17:13 2024

@author: muska
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json


class ISO27001ComplianceLogger:
    def __init__(self):
        self.business_name = "Your Business Name"
        self.controls = {  # ISO 27001:2022 controls (expand as needed)
            "A.5.1": "Policies for information security",
            "A.5.2": "Review of policies for information security",
            "A.6.1": "Organization of information security roles",
            "A.6.2": "Segregation of duties",
            "A.7.1": "Screening and recruitment",
            "A.7.2": "Termination and change of employment",
        }
        self.compliance_log = {control: {"status": "Not Assessed", "notes": ""} for control in self.controls}

    def set_business_name(self, name):
        self.business_name = name

    def log_compliance(self, control, status, notes=""):
        if control not in self.compliance_log:
            return f"Control '{control}' does not exist."
        self.compliance_log[control] = {"status": status, "notes": notes}
        return f"Compliance logged for '{control}' as '{status}'."

    def view_incomplete_controls(self):
        return {
            control: data
            for control, data in self.compliance_log.items()
            if data["status"] != "Compliant"
        }

    def compliance_progress(self):
        total = len(self.controls)
        compliant = sum(1 for data in self.compliance_log.values() if data["status"] == "Compliant")
        return (compliant / total) * 100

    def export_incomplete(self, filepath):
        try:
            export_data = {
                "business_name": self.business_name,
                "timestamp": datetime.now().isoformat(),
                "incomplete_controls": self.view_incomplete_controls(),
            }
            with open(filepath, "w") as file:
                json.dump(export_data, file, indent=4)
            return "Incomplete controls exported successfully."
        except Exception as e:
            return f"Error exporting incomplete controls: {str(e)}"


class ISO27001ComplianceApp:
    def __init__(self, root):
        self.logger = ISO27001ComplianceLogger()
        self.root = root
        self.root.title("Tanuki Compliance - ISO 27001:2022 Checklist")

        # Business Name Input
        tk.Label(root, text="Business Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.business_name_entry = tk.Entry(root, width=40)
        self.business_name_entry.insert(0, self.logger.business_name)
        self.business_name_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Save Name", command=self.save_business_name).grid(row=0, column=2, padx=10, pady=5)

        # Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

        # Tabs
        self.checklist_tab = ttk.Frame(self.notebook)
        self.audit_tab = ttk.Frame(self.notebook)
        self.guide_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.checklist_tab, text="Checklist")
        self.notebook.add(self.audit_tab, text="Audit View")
        self.notebook.add(self.guide_tab, text="Guide")

        # Checklist Tab
        self.setup_checklist_tab()

        # Audit View Tab
        self.setup_audit_tab()

        # Guide Tab
        self.setup_guide_tab()

    def save_business_name(self):
        name = self.business_name_entry.get()
        if name.strip():
            self.logger.set_business_name(name)
            messagebox.showinfo("Success", f"Business name set to '{name}'.")
        else:
            messagebox.showerror("Error", "Business name cannot be empty.")

    def setup_checklist_tab(self):
        tk.Label(self.checklist_tab, text="Compliance Checklist").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.control_tree = ttk.Treeview(self.checklist_tab, columns=("status", "notes"), show="headings", height=15)
        self.control_tree.heading("status", text="Status")
        self.control_tree.heading("notes", text="Notes")
        self.control_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        self.update_control_tree()

        tk.Label(self.checklist_tab, text="Select Control:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.control_combobox = ttk.Combobox(self.checklist_tab, values=list(self.logger.controls.keys()), width=30)
        self.control_combobox.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.checklist_tab, text="Status:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.status_combobox = ttk.Combobox(self.checklist_tab, values=["Compliant", "Non-Compliant", "Partially Compliant"], width=30)
        self.status_combobox.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.checklist_tab, text="Notes:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.notes_entry = tk.Entry(self.checklist_tab, width=40)
        self.notes_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self.checklist_tab, text="Log Compliance", command=self.log_compliance).grid(row=5, column=1, sticky=tk.E, padx=10, pady=5)

    def setup_audit_tab(self):
        tk.Label(self.audit_tab, text="Audit View - Incomplete Controls").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.incomplete_tree = ttk.Treeview(self.audit_tab, columns=("status", "notes"), show="headings", height=15)
        self.incomplete_tree.heading("status", text="Status")
        self.incomplete_tree.heading("notes", text="Notes")
        self.incomplete_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Define the progress label here before updating the tree
        tk.Label(self.audit_tab, text="Compliance Progress:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.progress_label = tk.Label(self.audit_tab, text="0%")
        self.progress_label.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        tk.Button(self.audit_tab, text="Export Incomplete", command=self.export_incomplete).grid(row=3, column=2, sticky=tk.E, padx=10, pady=5)

        self.update_incomplete_tree()

    def setup_guide_tab(self):
        guide_text = """
        ISO 27001:2022 Compliance Guide

        A.5.1 - Policies for information security
        Ensure your organization has policies in place for managing information security. 
        The policies should define the scope and objectives of information security.

        A.5.2 - Review of policies for information security
        Regular reviews should be conducted to ensure the policies are still applicable and effective.

        A.6.1 - Organization of information security roles
        Designate roles and responsibilities for information security within your organization.

        A.6.2 - Segregation of duties
        Make sure duties are divided in such a way that no individual has control over all aspects of any critical task.

        A.7.1 - Screening and recruitment
        Screen and verify employees, contractors, and third-party users before they access sensitive information.

        A.7.2 - Termination and change of employment
        Implement processes to ensure proper management of employees leaving or transitioning within the organization.
        """

        guide_label = tk.Label(self.guide_tab, text=guide_text, justify=tk.LEFT, anchor="w", font=("Arial", 10), padx=10, pady=10)
        guide_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def update_control_tree(self):
        for row in self.control_tree.get_children():
            self.control_tree.delete(row)
        for control, data in self.logger.compliance_log.items():
            self.control_tree.insert("", tk.END, values=(control, data["status"], data["notes"]))

    def update_incomplete_tree(self):
        for row in self.incomplete_tree.get_children():
            self.incomplete_tree.delete(row)
        for control, data in self.logger.view_incomplete_controls().items():
            self.incomplete_tree.insert("", tk.END, values=(control, data["status"], data["notes"]))
        self.progress_label.config(text=f"{self.logger.compliance_progress():.2f}%")

    def log_compliance(self):
        control = self.control_combobox.get()
        status = self.status_combobox.get()
        notes = self.notes_entry.get()

        if not control or not status:
            messagebox.showerror("Error", "Control and Status are required.")
            return

        message = self.logger.log_compliance(control, status, notes)
        messagebox.showinfo("Success", message)
        self.update_control_tree()
        self.update_incomplete_tree()

    def export_incomplete(self):
        filepath = "incomplete_controls.json"
        message = self.logger.export_incomplete(filepath)
        messagebox.showinfo("Export Log", message)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ISO27001ComplianceApp(root)
    root.mainloop()
