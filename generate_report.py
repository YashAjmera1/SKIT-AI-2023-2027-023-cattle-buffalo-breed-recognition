
import subprocess
import datetime
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

COLLEGE_NAME = (
    "Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur"
)
DEPARTMENT_NAME = "Department of Computer Science & Engineering"


def get_repo_info():
    repo = os.path.basename(os.getcwd())
    try:
        repo = os.path.basename(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                text=True
            ).strip()
        )
    except Exception:
        pass

    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], text=True
        ).strip() or "unknown"
    except Exception:
        branch = "unknown"

    return repo, branch


def generate_report(interval="weekly"):
    today = datetime.date.today()

    if interval == "weekly":
        since = today - datetime.timedelta(days=7)
        title = "Weekly Progress Report (Form-3)"
        scope = f"Last 7 days (since {since})"
    elif interval == "monthly":
        since = today - datetime.timedelta(days=30)
        title = "Monthly Progress Report (Form-3)"
        scope = f"Last 30 days (since {since})"
    else:
        since = None
        title = "Final Project Evaluation Report"
        scope = "Complete Project Lifecycle"

    command = [
        "git", "log", "--no-merges",
        "--pretty=format:COMMIT|||%h|||%an|||%ad|||%s",
        "--date=short", "--numstat"
    ]
    if since:
        command.append(f"--since={since.isoformat()}")

    try:
        output = subprocess.check_output(command, text=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        print("Could not read Git history:", exc.stderr)
        return

    students = defaultdict(
        lambda: {"commits": 0, "added": 0, "deleted": 0, "days": set(), "logs": []}
    )
    current_author = None
    current_date = None

    for line in output.splitlines():
        if line.startswith("COMMIT|||"):
            parts = line.split("|||", 4)
            if len(parts) != 5:
                current_author = None
                continue
            _, sha, author, date, message = parts
            current_author, current_date = author.strip(), date.strip()

            if "bot" in current_author.lower():
                current_author = None
                continue

            data = students[current_author]
            data["commits"] += 1
            data["days"].add(current_date)
            data["logs"].append((current_date, sha, message))
        elif current_author:
            parts = line.split()
            if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
                students[current_author]["added"] += int(parts[0])
                students[current_author]["deleted"] += int(parts[1])

    repo, branch = get_repo_info()
    date_stamp = today.isoformat()
    filename = f"{repo}_Form-3_{interval}_{date_stamp}.pdf"

    styles = getSampleStyleSheet()
    story = [
        Paragraph(COLLEGE_NAME, styles["Title"]),
        Paragraph(DEPARTMENT_NAME, styles["Heading2"]),
        Paragraph(title, styles["Heading2"]),
        Paragraph(f"Repository: {repo} | Branch: {branch}", styles["Normal"]),
        Paragraph(f"Period: {scope} | Generated: {date_stamp}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("1. Individual Contribution Breakdown", styles["Heading2"]),
    ]

    total = sum(d["commits"] for d in students.values())
    rows = [["Student", "Commits (%)", "Added", "Deleted", "Net LOC", "Active Days"]]

    for name, data in sorted(students.items()):
        percentage = data["commits"] / total * 100 if total else 0
        rows.append([
            name, f'{data["commits"]} ({percentage:.1f}%)',
            data["added"], data["deleted"],
            data["added"] - data["deleted"], len(data["days"])
        ])

    if not students:
        rows.append(["No commits found", "-", "-", "-", "-", "-"])

    table = Table(rows, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
    ]))
    story.extend([table, Spacer(1, 12)])

    story.append(Paragraph("2. Commit History", styles["Heading2"]))
    log_rows = [["Student", "Date", "Hash", "Commit Message"]]
    for name, data in sorted(students.items()):
        for date, sha, message in data["logs"]:
            log_rows.append([name, date, sha, message])

    log_table = Table(log_rows, colWidths=[100, 65, 55, 300], repeatRows=1)
    log_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#475569")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(log_table)

    doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
    doc.build(story)
    print(f"Report generated: {filename}")
    print(f"Students: {len(students)} | Commits: {total}")


if __name__ == "__main__":
    import sys
    chosen = sys.argv[1].lower() if len(sys.argv) > 1 else "weekly"
    if chosen not in ("weekly", "monthly", "final"):
        raise SystemExit("Choose weekly, monthly, or final")
    generate_report(chosen)
