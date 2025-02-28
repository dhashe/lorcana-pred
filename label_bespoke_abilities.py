#!/usr/bin/env python3

import csv
import re

keywords = [
    "Bodyguard (This character may enter play exerted. An opposing character who challenges one of your characters must choose one with Bodyguard if able.)",
    "Evasive (Only characters with Evasive can challenge this character.)",
    "Resist +1 (Damage dealt to this character is reduced by 1.)",
    "Resist +2 (Damage dealt to this character is reduced by 2.)",
    "Resist +3 (Damage dealt to this character is reduced by 3.)",
    "Shift 1 (You may pay 1{i} to play this on top of one of your characters named",
    "Shift 2 (You may pay 2{i} to play this on top of one of your characters named",
    "Shift 3 (You may pay 3{i} to play this on top of one of your characters named",
    "Shift 4 (You may pay 4{i} to play this on top of one of your characters named",
    "Shift 5 (You may pay 5{i} to play this on top of one of your characters named",
    "Shift 6 (You may pay 6{i} to play this on top of one of your characters named",
    "Shift 7 (You may pay 7{i} to play this on top of one of your characters named",
    "Shift 8 (You may pay 8{i} to play this on top of one of your characters named",
    "Shift 9 (You may pay 9{i} to play this on top of one of your characters named",
    "Support (Whenever this character quests, you may add their {s} to another chosen character's {s} this turn.)",
    "Challenger +1 (While challenging, this character gets +1 {s}.)",
    "Challenger +2 (While challenging, this character gets +2 {s}.)",
    "Challenger +3 (While challenging, this character gets +3 {s}.)",
    "Challenger +4 (While challenging, this character gets +4 {s}.)",
    "Challenger +5 (While challenging, this character gets +5 {s}.)",
    "Challenger +6 (While challenging, this character gets +6 {s}.)",
    "Challenger +7 (While challenging, this character gets +7 {s}.)",
    "Reckless (This character can't quest and must challenge each turn if able.)",
    "Rush (This character can challenge the turn they're played.)",
    "Singer 6 (This-character counts as cost6 {i} to sing songs.)",
    "Singer 3 (This-character counts as cost 3 to sing songs.)",
    "Singer 4 (This-character counts as cost 4 to sing songs.)",
    "Singer 5 (This-character counts as cost 5 to sing songs.)",
    "Singer 6 (This-character counts as cost 6 to sing songs.)",
    "Singer 7 (This-character counts as cost 7 to sing songs.)",
    "Singer 8 (This-character counts as cost 8 to sing songs.)",
    "Singer 9 (This-character counts as cost 9 to sing songs.)",
    "Ward (Opponents can't choose this character except to challenge.)",
]

for i in range(len(keywords)):
    keywords[i] = re.sub(r'[^a-zA-Z]', '', keywords[i])

def has_non_keyword_abilities(body_text):
    body_text = re.sub(r'[^a-zA-Z]', '', body_text)
    for keyword in keywords:
        body_text = body_text.replace(keyword, "")
    body_text = re.sub(r"Shift.*toplaythisontopofoneofyourcharactersname", "", body_text)

    return len(body_text) > 15


with open("input_to_bespoke_abilities.csv") as csvfile, open("bespoke_abilities.csv", "w+") as outfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    writer = csv.writer(outfile, delimiter=',', quotechar='"')
    first = True
    for row in reader:
        if first:
            first = False
            writer.writerow(list(row) + ["Has_Bespoke"])
            continue
        body_text = row[1]
        if body_text in ["", "NA"]:
            writer.writerow(list(row) + [0])
        else:

            x = int(has_non_keyword_abilities(body_text))
            writer.writerow(list(row) + [x])
