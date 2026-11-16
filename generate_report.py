#!/usr/bin/env python3
"""
Official Form-3 Weekly Progress Report Generator for SKIT Jaipur.
Matches the official Department of Computer Science & Engineering guideline and sample format.
Supports all 8 academic project weeks and consolidated final semester evaluations.
"""
import subprocess
from collections import defaultdict
import datetime
import io
import os
import sys
import html

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# -------------------------------------------------------------
# CONFIGURATION: Institution, Department & Student Directory
# -------------------------------------------------------------
COLLEGE_NAME = "Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur"
DEPARTMENT_NAME = "Department of Computer Science & Engineering (Artificial Intelligence)"
PROJECT_ID = "SKIT/AI/2023-2027/023"
SUPERVISOR_NAME = "Dr. Mehul Mahrishi"

AUTHOR_MAP = {
    "YashAjmera1": "Yash Ajmera (23ESKCA125)",
    "Yash Ajmera": "Yash Ajmera (23ESKCA125)",
    "Kunal Rana": "Kunal Rana (23ESKCA300)",
    "Kunal-Rana-07": "Kunal Rana (23ESKCA300)",
    "rajnish-moon": "Rajnish Kumar Patel (23ESKCA087)",
    "Rajnish Kumar Patel": "Rajnish Kumar Patel (23ESKCA087)",
    "gourvishal036-lang": "Vishal Gour (23ESKCA121)",
    "Vishal Gour": "Vishal Gour (23ESKCA121)",
}

WEEK_SCHEDULE = {
    1: ("2026-08-10", "2026-08-25", "Week 1: Literature Survey, Wireframes & Transfer Learning Backbone"),
    2: ("2026-08-26", "2026-08-31", "Week 2: Database Schema Design & NBAGR Raw Dataset Hierarchy"),
    3: ("2026-09-01", "2026-09-18", "Week 3: Image Preprocessing Pipeline & React 19 Frontend Setup"),
    4: ("2026-09-19", "2026-09-30", "Week 4: FastAPI REST Routing & Dataset Statistical Distribution"),
    5: ("2026-10-01", "2026-10-12", "Week 5: Project Infrastructure Scaffolding & CI Workflows"),
    6: ("2026-10-13", "2026-10-25", "Week 6: Transfer Learning Training Loop, UI Upload & Deduplication"),
    7: ("2026-10-26", "2026-11-07", "Week 7: Evaluation Benchmarks, Validation Shields & 70/15/15 Splits"),
    8: ("2026-11-08", "2026-11-16", "Week 8: Multi-Tier OOD Gatekeeper, Breed Catalog & Academic Forms"),
}


def get_repo_info():
    """Extracts the exact repository name and branch reliably in GitHub Codespaces or local git."""
    repo_name = "SKIT-AI-2023-2027-023-cattle-buffalo-breed-recognition"
    branch_name = "main"
    try:
        root_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], encoding='utf-8').strip()
        repo_name = os.path.basename(root_path)
    except Exception:
        try:
            remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8').strip()
            repo_name = remote_url.rstrip('/').split('/')[-1].replace('.git', '')
        except Exception:
            repo_name = os.path.basename(os.getcwd())
    try:
        branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], encoding='utf-8').strip()
    except Exception:
        pass
    return repo_name, branch_name


def normalize_author(raw_author):
    """Maps git username or email alias to official SKIT student roll name."""
    clean = raw_author.strip()
    if clean in AUTHOR_MAP:
        return AUTHOR_MAP[clean]
    for key, val in AUTHOR_MAP.items():
        if key.lower() in clean.lower():
            return val
    return clean


def get_git_metrics(interval="weekly", since=None, until=None):
    """
    Parses Git commit logs accurately across all 4 team members.
    Filters by author date in Python to avoid committer-date exclusion anomalies after rebases.
    """
    today = datetime.date.today()
    git_args = ['git', 'log', '--no-merges', '--pretty=format:COMMIT|||%h|||%an|||%ad|||%s', '--date=short', '--numstat']

    if since and until:
        scope_title = f"{since} to {until}"
    elif interval == "weekly":
        since_date = (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        scope_title = f"Last 7 Days (Since {since_date})"
    elif interval == "monthly":
        since_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        scope_title = f"Last 30 Days (Since {since_date})"
    else:
        scope_title = "Complete 8-Week Project Lifecycle (2026-08-10 to 2026-11-16)"

    try:
        raw_output = subprocess.check_output(git_args, encoding='utf-8', errors='replace')
    except subprocess.CalledProcessError:
        print("[ERROR] Git command failed. Please ensure you are inside a Git repository.")
        return None, None, None, scope_title

    students = defaultdict(lambda: {"commits": 0, "added": 0, "deleted": 0, "active_days": set()})
    timeline_activity = defaultdict(lambda: defaultdict(int))
    student_logs = defaultdict(list)
    current_author = None
    current_date_str = None

    for line in raw_output.strip().split('\n'):
        line = line.strip()
        if not line:
            continue

        if line.startswith('COMMIT|||'):
            parts = line.split('|||')
            if len(parts) >= 5:
                sha = parts[1].strip()
                raw_auth = parts[2].strip()
                date_str = parts[3].strip()
                msg = parts[4].strip()
            else:
                continue

            # --- IGNORE AUTOMATED BOTS ---
            if "bot" in raw_auth.lower() or "github-actions" in raw_auth.lower():
                current_author = None
                continue
            # -----------------------------

            # Date Range Filter (based on commit author date)
            if since and until:
                if not (since <= date_str <= until):
                    current_author = None
                    continue
            elif interval == "weekly" and not (since and until):
                since_date = (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
                if date_str < since_date:
                    current_author = None
                    continue
            elif interval == "monthly" and not (since and until):
                since_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
                if date_str < since_date:
                    current_author = None
                    continue

            current_author = normalize_author(raw_auth)
            current_date_str = date_str

            students[current_author]["commits"] += 1
            students[current_author]["active_days"].add(current_date_str)
            student_logs[current_author].append((date_str, sha, msg))

            try:
                dt = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date()
                if interval == "weekly":
                    period_key = dt.strftime("%b %d")
                elif interval == "monthly":
                    period_key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
                else:
                    period_key = dt.strftime("%b %Y")
                timeline_activity[period_key][current_author] += 1
            except Exception:
                pass
        elif current_author and not line.startswith('COMMIT|||'):
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                students[current_author]["added"] += int(parts[0])
                students[current_author]["deleted"] += int(parts[1])

    return students, timeline_activity, student_logs, scope_title


def create_charts(students, timeline_activity, interval):
    """Generates visual workload and trend charts."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
    authors = list(students.keys())
    short_authors = [a.split(" (")[0] for a in authors]
    periods = sorted(timeline_activity.keys())

    # 1. Timeline Line Chart
    if periods and authors:
        for i, author in enumerate(authors):
            counts = [timeline_activity[p].get(author, 0) for p in periods]
            ax1.plot(periods, counts, marker='o', linewidth=2, label=short_authors[i])
        ax1.set_title(f"Commit Timeline ({interval.capitalize()})", fontsize=10, fontweight='bold')
        ax1.set_ylabel("Commits")
        ax1.tick_params(axis='x', rotation=30)
        ax1.grid(True, linestyle='--', alpha=0.5)
        ax1.legend(fontsize=8)
    else:
        ax1.text(0.5, 0.5, "No commits found in this interval", ha='center', va='center')

    # 2. Net LOC Bar Chart
    if authors:
        net_loc = [students[a]["added"] - students[a]["deleted"] for a in authors]
        colors_list = ['#1E3A8A', '#0D9488', '#B45309', '#7C3AED', '#4338CA']
        ax2.bar(short_authors, net_loc, color=colors_list[:len(authors)], width=0.45)
        ax2.set_title("Net Lines of Code Written", fontsize=10, fontweight='bold')
        ax2.set_ylabel("LOC (Added - Deleted)")
        ax2.tick_params(axis='x', rotation=15)
        ax2.grid(axis='y', linestyle='--', alpha=0.5)
    else:
        ax2.text(0.5, 0.5, "No LOC changes recorded", ha='center', va='center')

    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=200)
    plt.close()
    img_buffer.seek(0)
    return Image(img_buffer, width=500, height=170)


def generate_pdf(interval="weekly", since=None, until=None, custom_filename=None, week_num=None):
    repo_name, branch_name = get_repo_info()
    students, timeline_activity, student_logs, scope_title = get_git_metrics(interval, since, until)
    if students is None:
        return

    date_stamp = datetime.date.today().strftime("%Y-%m-%d")

    if week_num:
        report_title = f"Weekly Progress Report (Form-3) - Week {week_num}"
        doc_name = f"Form-3_Week-{week_num}_{since}_to_{until}.pdf"
    elif since and until:
        report_title = "Weekly Progress Report (Form-3)"
        doc_name = f"{repo_name}_Weekly_Progress_Report_Form-3_{since}_to_{until}.pdf"
    elif interval == "weekly":
        report_title = "Weekly Progress Report (Form-3)"
        doc_name = f"{repo_name}_Weekly_Progress_Report_Form-3_{date_stamp}.pdf"
    elif interval == "monthly":
        report_title = "Monthly Progress Report (Form-3)"
        doc_name = f"{repo_name}_Monthly_Progress_Report_Form-3_{date_stamp}.pdf"
    else:
        report_title = "Final Project Evaluation Report (Form-3 Consolidated)"
        doc_name = f"{repo_name}_Final_Report_{date_stamp}.pdf"

    if custom_filename:
        doc_name = custom_filename

    doc = SimpleDocTemplate(
        doc_name,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    college_style = ParagraphStyle(
        'CollegeStyle', parent=styles['Heading1'],
        fontSize=13, leading=16, textColor=colors.HexColor("#0F172A"), alignment=1, spaceAfter=2
    )
    dept_style = ParagraphStyle(
        'DeptStyle', parent=styles['Normal'],
        fontSize=9.5, leading=13, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=5
    )
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading2'],
        fontSize=12.5, leading=16, textColor=colors.HexColor("#1A365D"), alignment=1, spaceAfter=4
    )
    repo_style = ParagraphStyle(
        'RepoStyle', parent=styles['Normal'],
        fontSize=9, leading=13, textColor=colors.HexColor("#0F172A"), spaceAfter=2
    )
    meta_style = ParagraphStyle(
        'MetaStyle', parent=styles['Normal'],
        fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=6
    )
    section_style = ParagraphStyle(
        'SectionStyle', parent=styles['Heading2'],
        fontSize=10, leading=13, textColor=colors.HexColor("#0F172A"), spaceBefore=6, spaceAfter=3
    )
    sub_section_style = ParagraphStyle(
        'SubSectionStyle', parent=styles['Heading3'],
        fontSize=8.5, leading=11, textColor=colors.HexColor("#1E40AF"), spaceBefore=4, spaceAfter=2
    )
    msg_style = ParagraphStyle(
        'MsgStyle', parent=styles['Normal'],
        fontSize=7.5, leading=9.5, textColor=colors.HexColor("#1E293B")
    )
    meta_cell_style = ParagraphStyle(
        'MetaCellStyle', parent=styles['Normal'],
        fontSize=7.5, leading=9.5, textColor=colors.HexColor("#475569"), alignment=1
    )
    marks_style = ParagraphStyle(
        'MarksStyle', parent=styles['Normal'],
        fontSize=8.5, leading=11, textColor=colors.HexColor("#0F172A"), alignment=1
    )
    sig_block_style = ParagraphStyle(
        'SigBlockStyle', parent=styles['Normal'],
        fontSize=8.5, leading=14, textColor=colors.HexColor("#0F172A"), alignment=0
    )

    story = []

    # 1. Header with College & Department Name and Form-3 Title
    story.append(Paragraph(f"<b>{html.escape(COLLEGE_NAME)}</b>", college_style))
    story.append(Paragraph(f"<b>{html.escape(DEPARTMENT_NAME)}</b>", dept_style))
    story.append(Paragraph(f"<u><b>{report_title}</b></u>", title_style))
    story.append(Spacer(1, 2))

    # 2. Metadata (Project ID, Repo, Branch, Scope, Supervisor)
    story.append(Paragraph(f"<b>Project ID:</b> <code>{PROJECT_ID}</code> &nbsp;|&nbsp; <b>Supervisor:</b> {SUPERVISOR_NAME} &nbsp;|&nbsp; <b>Branch:</b> <code>{html.escape(branch_name)}</code>", repo_style))
    story.append(Paragraph(f"<b>Evaluation Window:</b> {scope_title} &nbsp;|&nbsp; <b>Generated On:</b> {datetime.date.today().strftime('%B %d, %Y')}", meta_style))

    # 3. Individual Summary Table
    story.append(Paragraph("1. Individual Contribution Breakdown", section_style))
    total_commits = sum(data["commits"] for data in students.values())
    table_data = [["Student Name (Roll No)", "Commits (%)", "Lines Added", "Lines Deleted", "Net LOC", "Active Days"]]

    if students:
        for name in sorted(students.keys()):
            data = students[name]
            pct = (data["commits"] / total_commits * 100) if total_commits > 0 else 0
            net = data["added"] - data["deleted"]
            table_data.append([
                html.escape(name),
                f"{data['commits']} ({pct:.1f}%)",
                f"+{data['added']:,}",
                f"-{data['deleted']:,}",
                f"{net:,}",
                f"{len(data['active_days'])} days"
            ])
    else:
        table_data.append(["No commits found in this period. Run with 'final' to see all commits.", "-", "-", "-", "-", "-"])

    table = Table(table_data, colWidths=[160, 75, 75, 75, 75, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(table)
    story.append(Spacer(1, 5))

    # 4. Visual Charts
    story.append(Paragraph("2. Visual Trends & Volume", section_style))
    chart_image = create_charts(students, timeline_activity, interval)
    story.append(chart_image)
    story.append(Spacer(1, 5))

    # 5. Detailed Commit Logs per Student WITH Vertically Merged Mentor Marks
    story.append(Paragraph(f"3. Detailed Commit Logs & Mentor Evaluation ({interval.capitalize()})", section_style))
    if not student_logs:
        story.append(Paragraph("<i>No commit logs found for this timeframe.</i>", styles['Normal']))
    else:
        for student_name in sorted(student_logs.keys()):
            logs = student_logs[student_name]
            student_section = []
            student_section.append(Paragraph(f"<b>Student:</b> {html.escape(student_name)} &mdash; <i>{len(logs)} commit(s)</i>", sub_section_style))

            log_table_data = [["Date", "Hash", "Commit Message", "Mentor Marks (/10)"]]

            # Place the clean marking line in the first row
            first_date, first_sha, first_msg = logs[0]
            safe_msg = html.escape(first_msg) if first_msg else "(No commit message)"
            log_table_data.append([
                Paragraph(first_date, meta_cell_style),
                Paragraph(f"<code>{first_sha}</code>", meta_cell_style),
                Paragraph(safe_msg, msg_style),
                Paragraph("<b>_____ / 10</b>", marks_style)
            ])

            # Subsequent commit rows have blank placeholder for merged cell
            for date_val, sha_val, msg_val in logs[1:]:
                safe_msg = html.escape(msg_val) if msg_val else "(No commit message)"
                log_table_data.append([
                    Paragraph(date_val, meta_cell_style),
                    Paragraph(f"<code>{sha_val}</code>", meta_cell_style),
                    Paragraph(safe_msg, msg_style),
                    ""
                ])

            num_rows = len(log_table_data)
            log_table = Table(log_table_data, colWidths=[65, 50, 335, 90])

            t_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#475569")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
                ('TOPPADDING', (0, 0), (-1, -1), 2.5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ('ROWBACKGROUNDS', (0, 1), (2, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ('SPAN', (3, 1), (3, num_rows - 1)),               # Vertically merge mentor marks column
                ('VALIGN', (3, 1), (3, num_rows - 1), 'MIDDLE'),     # Vertically center the marks line
                ('BACKGROUND', (3, 1), (3, num_rows - 1), colors.HexColor("#FEF3C7")), # Accent for marks area
            ]

            log_table.setStyle(TableStyle(t_style))
            student_section.append(log_table)
            student_section.append(Spacer(1, 4))
            story.append(KeepTogether(student_section))

    # 6. Symmetrical Signatures
    story.append(Spacer(1, 14))

    mentor_cell = [
        Paragraph("<b>Name:</b> ___________________________", sig_block_style),
        Paragraph("<b>Designation:</b> Project Mentor", sig_block_style),
        Spacer(1, 4),
        Paragraph("<b>Signature:</b> ________________________", sig_block_style),
    ]

    coordinator_cell = [
        Paragraph("<b>Name:</b> ___________________________", sig_block_style),
        Paragraph("<b>Designation:</b> Lab Coordinator", sig_block_style),
        Spacer(1, 4),
        Paragraph("<b>Signature:</b> ________________________", sig_block_style),
    ]

    sig_table = Table([[mentor_cell, coordinator_cell]], colWidths=[270, 270])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('LEFTPADDING', (1, 0), (1, -1), 40),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))

    story.append(KeepTogether(sig_table))

    doc.build(story)
    print(f"\n[SUCCESS] Generated: {doc_name}")
    print(f" -> Found {len(students)} student(s) and {total_commits} total commits.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Form-3 Weekly Progress Report Generator for SKIT Jaipur")
    parser.add_argument("interval_pos", nargs="?", default=None, help="weekly, monthly, or final")
    parser.add_argument("--interval", choices=["weekly", "monthly", "final"], default=None)
    parser.add_argument("--all-weeks", action="store_true", help="Generate reports for all 8 academic weeks")
    parser.add_argument("--week", type=int, choices=range(1, 9), help="Generate report for specific week")
    parser.add_argument("--output-dir", default="weekly_reports", help="Directory to save weekly reports")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    if args.all_weeks:
        print("Generating Form-3 reports for all 8 academic weeks matching official college template...")
        for w, (since_d, until_d, desc) in WEEK_SCHEDULE.items():
            target_file = os.path.join(args.output_dir, f"Form-3_Week-{w}_{since_d}_to_{until_d}.pdf")
            generate_pdf(interval="weekly", since=since_d, until=until_d, custom_filename=target_file, week_num=w)
        # Also generate final consolidated 8-week report
        final_file = os.path.join(args.output_dir, f"Form-3_final_{datetime.date.today().strftime('%Y-%m-%d')}.pdf")
        generate_pdf(interval="final", custom_filename=final_file)
        final_consolidated_file = os.path.join(args.output_dir, "Form-3_final_8-Weeks_Consolidated.pdf")
        generate_pdf(interval="final", custom_filename=final_consolidated_file)
        print("Completed all 8 weekly reports and final consolidated report!")
    elif args.week:
        since_d, until_d, desc = WEEK_SCHEDULE[args.week]
        target_file = os.path.join(args.output_dir, f"Form-3_Week-{args.week}_{since_d}_to_{until_d}.pdf")
        generate_pdf(interval="weekly", since=since_d, until=until_d, custom_filename=target_file, week_num=args.week)
    else:
        chosen_interval = args.interval or args.interval_pos or "weekly"
        generate_pdf(chosen_interval)
