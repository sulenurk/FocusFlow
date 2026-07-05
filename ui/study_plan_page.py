import uuid
import customtkinter as ctk

from ui.theme import COLORS
from ui.components import (
    AppCard,
    PageTitle,
    PageSubtitle,
    PrimaryButton,
    SecondaryButton,
    PillButton,
    PriorityBadge,
    SubjectIcon,
    AppEntry,
)


SUBJECT_META = {
    "math": {"icon": "∑"},
    "physics": {"icon": "⚗"},
    "chemistry": {"icon": "🧪"},
    "turkish": {"icon": "📘"},
    "biology": {"icon": "☘"},
    "history": {"icon": "⌛"},
    "geography": {"icon": "🌍"},
    "other": {"icon": "•"},
}


class StudyPlanPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLORS["bg"])
        self.app = app

        self.active_filter = "all_tasks"

        self.subject_options = [
            "math",
            "physics",
            "chemistry",
            "turkish",
            "biology",
            "history",
            "geography",
            "other",
        ]

        self.priority_options = ["low", "medium", "high"]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_filter_bar()
        self.create_task_list()
        self.create_add_task_card()

        self.render_tasks()

    def create_header(self):
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, padx=36, pady=(30, 10), sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = PageTitle(self.header, self.app.t("study_plan_title"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = PageSubtitle(self.header, self.app.t("study_plan_subtitle"))
        self.subtitle_label.grid(row=1, column=0, pady=(4, 0), sticky="w")

        self.add_top_button = PrimaryButton(
            self.header,
            text=f"+ {self.app.t('add_task')}",
            command=self.focus_task_name_entry,
            width=130
        )
        self.add_top_button.grid(row=0, column=1, rowspan=2, sticky="e")

    def create_filter_bar(self):
        self.filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.filter_frame.grid(row=1, column=0, padx=36, pady=(16, 12), sticky="w")

        self.filter_buttons = {}

        filters = ["all_tasks", "today", "this_week", "completed"]

        for index, filter_key in enumerate(filters):
            button = PillButton(
                self.filter_frame,
                text=self.app.t(filter_key),
                active=(filter_key == self.active_filter),
                command=lambda key=filter_key: self.change_filter(key),
                width=110
            )
            button.grid(row=0, column=index, padx=(0, 10))
            self.filter_buttons[filter_key] = button

    def create_task_list(self):
        self.task_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["card_soft"],
            scrollbar_button_hover_color=COLORS["primary"]
        )
        self.task_scroll.grid(row=2, column=0, padx=36, pady=(0, 12), sticky="nsew")
        self.task_scroll.grid_columnconfigure(0, weight=1)

    def create_add_task_card(self):
        self.add_card = AppCard(self)
        self.add_card.grid(row=3, column=0, padx=36, pady=(8, 30), sticky="ew")
        self.add_card.grid_columnconfigure(1, weight=1)

        self.add_title = ctk.CTkLabel(
            self.add_card,
            text=self.app.t("add_new_task"),
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.add_title.grid(row=0, column=0, columnspan=7, padx=20, pady=(18, 8), sticky="w")

        self.subject_menu = ctk.CTkOptionMenu(
            self.add_card,
            values=[self.app.t(item) for item in self.subject_options],
            width=135,
            height=42,
            fg_color=COLORS["input"],
            button_color="#DDD6FE",
            button_hover_color="#C4B5FD",
            text_color=COLORS["input_text"],
            dropdown_fg_color=COLORS["surface"],
            dropdown_text_color=COLORS["text"],
            command=None
        )
        self.subject_menu.set(self.app.t("math"))
        self.subject_menu.grid(row=1, column=0, padx=(20, 8), pady=(8, 20), sticky="ew")

        self.task_name_entry = AppEntry(
            self.add_card,
            placeholder_text=self.app.t("task_name")
        )
        self.task_name_entry.grid(row=1, column=1, padx=8, pady=(8, 20), sticky="ew")

        self.focus_entry = AppEntry(
            self.add_card,
            placeholder_text=self.app.t("focus_minutes"),
            width=100
        )
        self.focus_entry.insert(0, "25")
        self.focus_entry.grid(row=1, column=2, padx=8, pady=(8, 20))

        self.break_entry = AppEntry(
            self.add_card,
            placeholder_text=self.app.t("break_minutes"),
            width=100
        )
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=1, column=3, padx=8, pady=(8, 20))

        self.priority_menu = ctk.CTkOptionMenu(
            self.add_card,
            values=[self.app.t(item) for item in self.priority_options],
            width=110,
            height=42,
            fg_color=COLORS["input"],
            button_color="#DDD6FE",
            button_hover_color="#C4B5FD",
            text_color=COLORS["input_text"],
            dropdown_fg_color=COLORS["surface"],
            dropdown_text_color=COLORS["text"]
        )
        self.priority_menu.set(self.app.t("medium"))
        self.priority_menu.grid(row=1, column=4, padx=8, pady=(8, 20))

        self.add_button = PrimaryButton(
            self.add_card,
            text=self.app.t("add_task"),
            command=self.add_task,
            width=110
        )
        self.add_button.grid(row=1, column=5, padx=(8, 20), pady=(8, 20))

    def focus_task_name_entry(self):
        self.task_name_entry.focus_set()

    def get_key_from_translated_value(self, translated_value, options):
        for key in options:
            if self.app.t(key) == translated_value:
                return key
        return options[0]

    def change_filter(self, filter_key):
        self.active_filter = filter_key

        for key, button in self.filter_buttons.items():
            is_active = key == filter_key
            button.configure(
                fg_color=COLORS["primary_soft"] if is_active else COLORS["surface_light"],
                text_color=COLORS["text"] if is_active else COLORS["muted"]
            )

        self.render_tasks()

    def add_task(self):
        title = self.task_name_entry.get().strip()
        focus_value = self.focus_entry.get().strip()
        break_value = self.break_entry.get().strip()

        if not title:
            return

        try:
            focus_minutes = int(focus_value)
            break_minutes = int(break_value)
        except ValueError:
            return

        if focus_minutes <= 0 or break_minutes < 0:
            return

        selected_subject = self.get_key_from_translated_value(
            self.subject_menu.get(),
            self.subject_options
        )

        selected_priority = self.get_key_from_translated_value(
            self.priority_menu.get(),
            self.priority_options
        )

        new_task = {
            "id": f"task_{uuid.uuid4().hex[:8]}",
            "subject": selected_subject,
            "title": title,
            "focus_minutes": focus_minutes,
            "break_minutes": break_minutes,
            "priority": selected_priority,
            "status": "pending"
        }

        self.app.app_data.setdefault("tasks", []).append(new_task)
        self.app.save_app_data()

        self.task_name_entry.delete(0, "end")
        self.focus_entry.delete(0, "end")
        self.focus_entry.insert(0, "25")
        self.break_entry.delete(0, "end")
        self.break_entry.insert(0, "5")

        self.render_tasks()

    def render_tasks(self):
        for widget in self.task_scroll.winfo_children():
            widget.destroy()

        tasks = self.app.app_data.get("tasks", [])

        if self.active_filter == "completed":
            tasks = [task for task in tasks if task.get("status") == "completed"]

        if not tasks:
            empty_label = ctk.CTkLabel(
                self.task_scroll,
                text="No tasks yet.",
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=15)
            )
            empty_label.grid(row=0, column=0, padx=20, pady=40)
            return

        for row_index, task in enumerate(tasks):
            card = TaskCard(
    self.task_scroll,
    self.app,
    task,
    on_start=self.start_task,
    on_delete=self.delete_task,
    on_complete=self.complete_task
)
            card.grid(row=row_index, column=0, pady=7, sticky="ew")

    def delete_task(self, task_id):
        self.app.app_data["tasks"] = [
            task for task in self.app.app_data.get("tasks", [])
            if task.get("id") != task_id
        ]
        self.app.save_app_data()
        self.render_tasks()

    def complete_task(self, task_id):
        for task in self.app.app_data.get("tasks", []):
            if task.get("id") == task_id:
                task["status"] = "completed"

        self.app.save_app_data()
        self.render_tasks()

    def refresh_texts(self):
        self.title_label.configure(text=self.app.t("study_plan_title"))
        self.subtitle_label.configure(text=self.app.t("study_plan_subtitle"))
        self.add_top_button.configure(text=f"+ {self.app.t('add_task')}")
        self.add_title.configure(text=self.app.t("add_new_task"))
        self.task_name_entry.configure(placeholder_text=self.app.t("task_name"))
        self.focus_entry.configure(placeholder_text=self.app.t("focus_minutes"))
        self.break_entry.configure(placeholder_text=self.app.t("break_minutes"))
        self.add_button.configure(text=self.app.t("add_task"))

        for key, button in self.filter_buttons.items():
            button.configure(text=self.app.t(key))

        self.subject_menu.configure(values=[self.app.t(item) for item in self.subject_options])
        self.priority_menu.configure(values=[self.app.t(item) for item in self.priority_options])

        self.render_tasks()

    def start_task(self, task_id):
        self.app.set_active_task(task_id)


class TaskCard(AppCard):
    def __init__(self, parent, app, task, on_start, on_delete, on_complete):
        super().__init__(parent)
        self.app = app
        self.task = task
        self.on_start = on_start
        self.on_delete = on_delete
        self.on_complete = on_complete

        self.grid_columnconfigure(1, weight=1)

        subject = task.get("subject", "other")
        subject_meta = SUBJECT_META.get(subject, SUBJECT_META["other"])

        self.icon = SubjectIcon(
            self,
            subject_key=subject,
            icon_text=subject_meta["icon"]
        )
        self.icon.grid(row=0, column=0, rowspan=2, padx=(18, 14), pady=16)

        title_text = f"{self.app.t(subject)} - {task.get('title', '')}"

        self.title = ctk.CTkLabel(
            self,
            text=title_text,
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        self.title.grid(row=0, column=1, padx=0, pady=(16, 2), sticky="ew")

        detail_text = (
            f"◷ {task.get('focus_minutes', 0)} {self.app.t('focus_minutes')}   "
            f"○ {task.get('break_minutes', 0)} {self.app.t('break_minutes')}"
        )

        self.details = ctk.CTkLabel(
            self,
            text=detail_text,
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.details.grid(row=1, column=1, padx=0, pady=(0, 16), sticky="ew")

        self.priority = PriorityBadge(self, task.get("priority", "medium"))
        self.priority.grid(row=0, column=2, rowspan=2, padx=12, pady=20)

        self.start_button = SecondaryButton(
            self,
            text=f"▶ {self.app.t('start_task')}",
            command=lambda: self.on_start(task.get("id")),
            width=92
        )
        self.start_button.grid(row=0, column=3, rowspan=2, padx=(0, 8), pady=20)

        self.complete_button = SecondaryButton(
            self,
            text="✓",
            command=lambda: self.on_complete(task.get("id")),
            width=44
        )
        self.complete_button.grid(row=0, column=4, rowspan=2, padx=(0, 8), pady=20)

        self.delete_button = SecondaryButton(
            self,
            text="×",
            command=lambda: self.on_delete(task.get("id")),
            width=44
        )
        self.delete_button.grid(row=0, column=5, rowspan=2, padx=(0, 18), pady=20)