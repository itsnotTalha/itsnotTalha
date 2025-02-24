import requests

USERNAME = "itsTalha"
API_URL = f"https://codestats.net/api/users/{USERNAME}"
README_PATH = "README.md"

# Assumption: ~300 XP ≈ 1 minute of coding (adjust as needed)
XP_PER_MINUTE = 300

def fetch_coding_time():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        total_xp = data["total_xp"]

        # Convert XP to estimated time
        total_minutes = total_xp / XP_PER_MINUTE
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)

        languages = data["languages"]
        
        # Filter out languages without 'xp' and sort
        sorted_langs = sorted(
            ((lang, info) for lang, info in languages.items() if "xp" in info),  # Corrected here
            key=lambda x: x[1]["xp"],
            reverse=True
        )

        lang_times = []
        for lang, info in sorted_langs[:5]:  # Top 5 languages
            lang_xp = info["xp"]
            lang_minutes = lang_xp / XP_PER_MINUTE
            lang_hours = int(lang_minutes // 60)
            lang_min = int(lang_minutes % 60)
            lang_times.append(f"- {lang}: {lang_hours}h {lang_min}m")

        return hours, minutes, "\n".join(lang_times)
    return None, None, None

def update_readme():
    hours, minutes, lang_times = fetch_coding_time()
    if hours is None:
        print("Failed to fetch coding time data.")
        return

    with open(README_PATH, "r") as file:
        readme = file.readlines()

    start_marker = "<!-- CODESTATS:START -->"
    end_marker = "<!-- CODESTATS:END -->"

    new_content = []
    inside_block = False
    for line in readme:
        if line.strip() == start_marker:
            inside_block = True
            new_content.append(line)
            new_content.append(f"**Total Coding Time:** {hours}h {minutes}m\n\n")
            new_content.append("### Time Spent Per Language:\n")
            new_content.append(lang_times + "\n\n")
            continue
        if line.strip() == end_marker:
            inside_block = False
        if not inside_block:
            new_content.append(line)

    with open(README_PATH, "w") as file:
        file.writelines(new_content)

if __name__ == "__main__":
    update_readme()
