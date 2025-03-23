import csv
import os
from config.const import BEST_SCORES_FILE


def load_best_scores():
    if not os.path.exists(BEST_SCORES_FILE):
        return {}

    best_scores = {}
    with open(BEST_SCORES_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if len(row) == 2:
                name, score = row
                best_scores[name] = int(score)
    return best_scores


def save_best_scores(best_scores):
    with open(BEST_SCORES_FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        for name, score in best_scores.items():
            writer.writerow([name, score])


def update_best_score(username, score):
    best_scores = load_best_scores()
    if username not in best_scores or score > best_scores[username]:
        best_scores[username] = score
        save_best_scores(best_scores)
