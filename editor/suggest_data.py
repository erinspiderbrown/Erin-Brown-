"""List every number / stat mention in a transcript so each one can get a data graphic.
usage: python3 suggest_data.py work/words.json"""
import json, re, sys
NUMW = r'(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|half|percent|first|second|third)'
UNITS = r'(seconds?|sec|mph|miles|meters?|m|yards?|percent|%|points?|pr|pb|times?|years?|days?|weeks?|months?|followers|views|dollars?|k|place|rank)'
words = json.load(open(sys.argv[1]))
for i, w in enumerate(words):
    t = w['w'].lower().strip('.,!?')
    if re.search(r'\d', t) or re.fullmatch(NUMW, t):
        ctx = ' '.join(x['w'] for x in words[max(0, i - 6): i + 7])
        unit = next((x['w'] for x in words[i + 1: i + 4] if re.fullmatch(UNITS, x['w'].lower().strip('.,!?'))), '')
        print(f"{w['s']:7.2f}s  {w['w']:>10} {unit:<10} | {ctx}")
