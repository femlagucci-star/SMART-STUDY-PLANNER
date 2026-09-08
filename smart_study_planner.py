"""
Smart Study Planner
--------------------
A console-based program that helps a student log, review and analyse
their study sessions across different subjects over a semester.

Name: Kulumba Ronald
Registration Number: VU-BBC-2603-0511-DAY

Data is stored in a plain text file (study_log.txt) so that sessions
persist across multiple runs of the program.
"""

# Name of the file used to persist session data between runs.
DATA_FILE = "study_log.txt"

# The delimiter used to separate fields when a session is written to
# (or read from) the data file. A pipe is used because it is unlikely
# to appear naturally inside a subject name, topic or date.
DELIMITER = "|"


def pad(text, width):
    """
    Convert text to a string and pad it with spaces up to at least
    'width' characters. If the text is already longer than 'width'
    (e.g. a long subject name), always add two extra spaces afterwards
    so it never runs straight into the next column in a printed table.
    """
    text = str(text)
    if len(text) >= width:
        return text + "  "
    return text.ljust(width)


# ---------------------------------------------------------------------
# (c) classify_session(duration)
# ---------------------------------------------------------------------
def classify_session(duration):
    """
    Classify a study session based on its duration in minutes.

    Short  : under 30 minutes
    Medium : 30 to 90 minutes (inclusive)
    Long   : over 90 minutes
    """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


# ---------------------------------------------------------------------
# (g) save_sessions() / load_sessions()
# ---------------------------------------------------------------------
def save_sessions(sessions):
    """
    Save every logged session to DATA_FILE, one session per line.
    Each line has the format: subject|topic|date|duration
    """
    with open(DATA_FILE, "w") as file:
        for session in sessions:
            line = DELIMITER.join([
                session["subject"],
                session["topic"],
                session["date"],
                str(session["duration"]),
            ])
            file.write(line + "\n")
    print(f"Saved {len(sessions)} session(s) to '{DATA_FILE}'.")


def load_sessions():
    """
    Load sessions from DATA_FILE, if it exists, and return them as a
    list of dictionaries. If the file does not exist yet (e.g. the very
    first run of the program), return an empty list instead of crashing.
    """
    sessions = []
    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    # Skip any blank lines in the file.
                    continue
                parts = line.split(DELIMITER)
                if len(parts) != 4:
                    # Skip any malformed/corrupted line rather than crash.
                    continue
                subject, topic, date, duration_text = parts
                try:
                    duration = float(duration_text)
                except ValueError:
                    # Skip lines where duration isn't a valid number.
                    continue
                sessions.append({
                    "subject": subject,
                    "topic": topic,
                    "date": date,
                    "duration": duration,
                })
    except FileNotFoundError:
        # No saved data yet - this is normal on the first ever run.
        print(f"No existing '{DATA_FILE}' found. Starting with an empty log.")
    return sessions


# ---------------------------------------------------------------------
# (b) add_session()
# ---------------------------------------------------------------------
def add_session(sessions):
    """
    Prompt the user for the details of a new study session and append
    it to the sessions list as a dictionary.
    """
    print("\n--- Add a Study Session ---")
    subject = input("Subject: ").strip()
    topic = input("Topic covered: ").strip()
    date = input("Date / day label (e.g. 2026-09-05 or 'Monday'): ").strip()

    # Keep re-prompting until a valid positive number is entered.
    duration = None
    while duration is None:
        duration_text = input("Duration in minutes: ").strip()
        try:
            value = float(duration_text)
            if value <= 0:
                print("Duration must be a positive number. Please try again.")
                continue
            duration = value
        except ValueError:
            print("That is not a valid number. Please try again.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    }
    sessions.append(session)
    print(f"Session added and classified as '{classify_session(duration)}'.")


# ---------------------------------------------------------------------
# (d) view_sessions()
# ---------------------------------------------------------------------
def view_sessions(sessions):
    """
    Display every logged session in a neatly formatted table, including
    its Short / Medium / Long classification from classify_session().
    """
    print("\n--- All Study Sessions ---")
    if not sessions:
        print("No sessions have been logged yet.")
        return

    header = pad("#", 4) + pad("Subject", 18) + pad("Topic", 20) + pad("Date", 15) + pad("Minutes", 10) + pad("Class", 8)
    print(header)
    print("-" * len(header))
    for index, session in enumerate(sessions, start=1):
        classification = classify_session(session["duration"])
        row = (
            pad(index, 4)
            + pad(session["subject"], 18)
            + pad(session["topic"], 20)
            + pad(session["date"], 15)
            + pad(f"{session['duration']:.0f}", 10)
            + pad(classification, 8)
        )
        print(row)


# ---------------------------------------------------------------------
# (e) search_by_subject(subject)
# ---------------------------------------------------------------------
def search_by_subject(sessions, subject):
    """
    Display only the sessions recorded for the given subject
    (case-insensitive match) along with the total time spent on it.
    If no sessions are found, display a clear message instead of an
    empty table.
    """
    matches = [s for s in sessions if s["subject"].lower() == subject.lower()]

    print(f"\n--- Sessions for '{subject}' ---")
    if not matches:
        print(f"No sessions found for subject '{subject}'.")
        return

    header = pad("#", 4) + pad("Topic", 20) + pad("Date", 15) + pad("Minutes", 10) + pad("Class", 8)
    print(header)
    print("-" * len(header))
    total_minutes = 0
    for index, session in enumerate(matches, start=1):
        classification = classify_session(session["duration"])
        row = (
            pad(index, 4)
            + pad(session["topic"], 20)
            + pad(session["date"], 15)
            + pad(f"{session['duration']:.0f}", 10)
            + pad(classification, 8)
        )
        print(row)
        total_minutes += session["duration"]

    print(f"\nTotal time spent on '{subject}': {total_minutes:.0f} minutes "
          f"({total_minutes / 60:.2f} hours).")


# ---------------------------------------------------------------------
# (f) study_statistics()
# ---------------------------------------------------------------------
def study_statistics(sessions):
    """
    Compute and display:
      - total hours studied overall
      - total hours studied per subject
      - the subject with the least total study time (weakest area)
      - the single longest session recorded
    """
    print("\n--- Study Statistics ---")
    if not sessions:
        print("No sessions have been logged yet.")
        return

    # Total hours overall.
    total_minutes = sum(session["duration"] for session in sessions)
    print(f"Total time studied overall: {total_minutes:.0f} minutes "
          f"({total_minutes / 60:.2f} hours).")

    # Total minutes per subject, built up manually with a dictionary.
    per_subject = {}
    for session in sessions:
        subject = session["subject"]
        per_subject[subject] = per_subject.get(subject, 0) + session["duration"]

    print("\nTime studied per subject:")
    header = pad("Subject", 22) + pad("Minutes", 10) + pad("Hours", 10)
    print(header)
    print("-" * len(header))
    for subject, minutes in per_subject.items():
        print(pad(subject, 22) + pad(f"{minutes:.0f}", 10) + pad(f"{minutes / 60:.2f}", 10))

    # Weakest subject: the one with the least total study time.
    weakest_subject = min(per_subject, key=per_subject.get)
    print(f"\nWeakest area (least total study time): {weakest_subject} "
          f"({per_subject[weakest_subject]:.0f} minutes).")

    # Single longest session recorded.
    longest = max(sessions, key=lambda s: s["duration"])
    print(f"\nLongest single session: {longest['subject']} - {longest['topic']} "
          f"({longest['duration']:.0f} minutes, "
          f"{classify_session(longest['duration'])}).")


# ---------------------------------------------------------------------
# (a) main() - menu-driven interface
# ---------------------------------------------------------------------
def main():
    """
    Display a menu offering: Add a study session, View all sessions,
    Search sessions by subject, View statistics, Save & exit.
    Keeps reappearing until the user chooses to exit and rejects
    invalid menu choices without crashing.
    """
    sessions = load_sessions()

    menu = """
========================================
       SMART STUDY PLANNER - MENU
========================================
1. Add a study session
2. View all sessions
3. Search sessions by subject
4. View statistics
5. Save & exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            subject = input("Enter subject to search for: ").strip()
            search_by_subject(sessions, subject)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Goodbye! Your sessions have been saved.")
            break
        else:
            # Reject invalid menu choices without crashing.
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()