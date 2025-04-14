import data_processor as dp

def extract_valid_skills(skills_data):
    """
    Extract a set of valid skill strings from skills_data.
    Expected format: { "skills": [ { "skill": "A" }, { "skill": "B" }, ... ] }
    """
    if not skills_data or "skills" not in skills_data:
        print("No valid skills data found.")
        return set()
    return {item.get("skill") for item in skills_data["skills"] if "skill" in item}

def extract_allowed_proficiencies(prof_data):
    """
    Extract allowed proficiencies from proficiency data.
    Expected format: { "proficiency": [0,1,2,...] }
    Returns a set of allowed numeric values.
    """
    if not prof_data or "proficiency" not in prof_data:
        print("No proficiency constraints found.")
        return set()
    return {float(val) for val in prof_data["proficiency"]}

def main():

    data_file = "data.json"
    skills_file = "skills.json"
    proficiency_file = "proficiency.json"
    time_series_csv = "time_series.csv"
    proficiency_csv = "proficiency_report.csv"
    visualization_image = "proficiency_visualization.png"

    # Load raw data from data.json
    raw_data = dp.load_json_file(data_file)
    if raw_data is None:
        print("Error loading data.")
        return

    # Load and extract valid skills
    skills_json = dp.load_json_file(skills_file)
    valid_skills = extract_valid_skills(skills_json)
    if not valid_skills:
        print("Proceeding without filtering by skills.")

    # Load and extract allowed proficiencies
    prof_json = dp.load_json_file(proficiency_file)
    allowed_proficiencies = extract_allowed_proficiencies(prof_json)
    if not allowed_proficiencies:
        print("Proceeding without proficiency filtering.")

    # Process the time series
    time_series_data = dp.process_time_series(raw_data)
    dp.write_time_series_csv(time_series_data, time_series_csv)

    # Process the proficiency-by-skill report
    proficiency_aggregated = dp.process_proficiency_by_skill(raw_data, valid_skills, allowed_proficiencies)
    dp.write_proficiency_csv(proficiency_aggregated, proficiency_csv)

    # Generate the visualization
    dp.visualize_proficiency(proficiency_aggregated, visualization_image)

if __name__ == "__main__":
    main()
