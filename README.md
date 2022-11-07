# Arbiter
**Hackathon judging system, built for HackPHS 2022.** Based on both standard round-robin percentage system and minimum arc feedback set exponential-time algorithm.
## Usage
`python3 main.py`
## Dependencies
Requires `flask`.
## Issues
- [ ] Store all votes in case of server outage
- [ ] Possible frontend dashboard glitch where not all entries are shown
- [ ] Ensure all projects are seen a roughly equal number of times
- [x] Distribution system project duplication
- [x] Slowness of exact mFAS calculation
