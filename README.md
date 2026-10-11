# Market Observer

This is a tool built to observe how various electricity markets globally address faults and outages. Of key interest is the behaviour of aggregated VPPs in these markets, and how they participate in the ancillary service market as well as the wholesale electricity market.

## Data sources used

- OpenElectricity for general unit level information
- NEMOSIS for dispatch information

API key = oe_RbS3WH4EftZSKkkUvDrfo5

From parent directory, run
`python3 ./src/nem-observer/nem.py`

Only 500 requests per day is allowed per API key