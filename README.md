#  Calculate Trueskill Data from Match History

## Running
1. Ensure you have Python installed.
2. Set up a virtual environment: `python -m venv env`
   - Activate the virtual environment:
      - On Unix or macOS:  `source env/bin/activate`
      - On Windows: `env\Scripts\activate`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Copy or rename `config.ini.example` to a new file named `config.ini` and fill out the required API information or alternatively provide the JSON filename if not using the API.
5. Run the program: `python main.py`
6. You can also pass arguments listed with `python main.py --help`
7. Developers can run the test harness with `python -m unittest test.py`
## Disclaimer
- The output table would be constantly changing so should simply be treated as an arbitrary snapshot in time.
- There is no consideration of individual performance in that match, only win/loss.
- There is no consideration of what positions were played, how good players are at that position, etc.
- If there is a large disparity of player skill it can often mean unbalanced matches.
- If there is a small time-period of recorded games and/or a small sample size of games the results can be less reliable.
- Pick order is not currently factored into the rating, and we don't know what advantage/disadvantage being under/over/accurately picked gives.
- I'm not a professional coder or statistician, so I may have messed up at some points, if you think that's the case feel free to create a pull request or issue.
- This was a quick and dirty project.

## Sample game (Required format)
- Pick order, captain is irrelevant to TrueSkill, completionTimestamp is unused, and it should be okay to set all of these to 0 in your JSON file/API if you don't have that data available
```json
{
	"timestamp": 1541469560890,
	"completionTimestamp": 1541473145720,
	"winningTeam": 2,
	"queue": {
		"id": 0,
		"name": "PUG"
	},
	"players": [
		{
			"user": {
				"id": 388126393680265225,
				"name": "George"
			},
			"team": 1,
			"captain": 1,
			"pickOrder": 0
		},
		{
			"user": {
				"id": 131017362785697793,
				"name": "Bob"
			},
			"team": 2,
			"captain": 1,
			"pickOrder": 0
		},
		{
			"user": {
				"id": 108959056705646592,
				"name": "Grant"
			},
			"team": 1,
			"captain": 0,
			"pickOrder": 1
		},
		{
			"user": {
				"id": 236345696108806144,
				"name": "Phillis"
			},
			"team": 2,
			"captain": 0,
			"pickOrder": 2
		},
		{
			"user": {
				"id": 332270273372094474,
				"name": "Adrian"
			},
			"team": 1,
			"captain": 0,
			"pickOrder": 3
		},
		{
			"user": {
				"id": 139883009720582146,
				"name": "Beckie"
			},
			"team": 2,
			"captain": 0,
			"pickOrder": 4
		},
		{
			"user": {
				"id": 438488085936865301,
				"name": "Sandy"
			},
			"team": 1,
			"captain": 0,
			"pickOrder": 5
		},
		{
			"user": {
				"id": 309441518538850304,
				"name": "Seth"
			},
			"team": 2,
			"captain": 0,
			"pickOrder": 6
		},
		{
			"user": {
				"id": 140668837707251713,
				"name": "Smith"
			},
			"team": 2,
			"captain": 0,
			"pickOrder": 7
		},
		{
			"user": {
				"id": 244257440294502401,
				"name": "Warren"
			},
			"team": 1,
			"captain": 0,
			"pickOrder": 8
		}
	]
}
