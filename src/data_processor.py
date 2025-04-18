import json
import pandas as pd
import csv
import matplotlib.pyplot as plt
from statistics import mean

def load_json_file(file_path):
    # Load JSON data from a file
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

def process_time_series(raw_data):
    """
    Process time series data from raw JSON data.
    """
    if "scores" not in raw_data:
        print("Error: 'scores' key not found in the data.")
        return []
    
    scores = raw_data["scores"]
    cleaned_data = []

    for i, rec in enumerate(scores):
        if "skill" not in rec:
            print(f"Skipping record {i+1}: missing 'skill' key.")
            continue
        if "score" not in rec:
            print(f"Skipping record {i+1}: missing 'score' key.")
            continue
        try:
            score_val = float(rec["score"])
        except Exception:
            print(f"Skipping record {i+1}: invalid score '{rec.get('score')}'")
            continue
        rec["score"] = score_val
        rec["record_number"] = i + 1
        cleaned_data.append(rec)
    
    cleaned_data.sort(key=lambda x: x["record_number"])
    return cleaned_data

def write_time_series_csv(data, output_filename):
    """
    Write processed time series data to a CSV file.
    """
    if not data:
        print("No valid time series data to write.")
        return

    fieldnames = ["record_number", "skill", "score"]
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in data:
            row = {field: record.get(field) for field in fieldnames}
            writer.writerow(row)
    print(f"Time series CSV written to: {output_filename}")

def process_proficiency_by_skill(raw_data, valid_skills, allowed_proficiencies):
    """
    Process proficiency data by skill from raw JSON data.
    """
    if "scores" not in raw_data:
        print("No 'scores' key found in raw data.")
        return []
    scores = raw_data["scores"]
    skill_data = {}

    for i, rec in enumerate(scores):
        if "skill" not in rec or "score" not in rec:
            continue
        skill = rec["skill"]
        try:
            score_val = float(rec["score"])
        except Exception:
            continue

        if score_val not in allowed_proficiencies:
            continue

        if skill not in valid_skills:
            continue
        
        if skill not in skill_data:
            skill_data[skill] = {"count": 0, "scores": []}
        
        skill_data[skill]["count"] += 1
        skill_data[skill]["scores"].append(score_val)
    
    aggregated = []
    for skill, stats in skill_data.items():
        avg_score = mean(stats["scores"]) if stats["scores"] else 0
        aggregated.append({
            "skill": skill,
            "count": stats["count"],
            "average_score": round(avg_score, 2)
        })
    return aggregated

def write_proficiency_csv(aggregated, output_filename):
    """
    Write proficiency data to a CSV file.
    """
    if not aggregated:
        print("No valid proficiency data to write.")
        return
    fieldnames = ["skill", "count", "average_score"]
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rec in aggregated:
            writer.writerow(rec)
    print(f"Proficiency CSV written to: {output_filename}")

def visualize_proficiency(aggregated, output_image):
    """
    Visualize proficiency data using a scatter plot.
    """
    if not aggregated:
        print("No data to visualize.")
        return
    skills = [rec["skill"] for rec in aggregated]
    avg_scores = [rec["average_score"] for rec in aggregated]
    counts = [rec["count"] for rec in aggregated]

    plt.figure(figsize=(10, 6))
    plt.scatter(skills, avg_scores, s=[c * 50 for c in counts], alpha=0.6)
    plt.xlabel("Skill")
    plt.ylabel("Average Score")
    plt.title("Proficiency by Skill (Bubble Size = Number of Records)")
    plt.grid(True)

    for i, count in enumerate(counts):
        plt.annotate(f"{count}", (skills[i], avg_scores[i]),
                     textcoords="offset points", xytext=(0,10), ha='center')
    plt.savefig(output_image)
    plt.show()
    print(f"Visualization saved as {output_image}")