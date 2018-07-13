# Kids' Activities
### A Website to Keep Track of Educational Events for Children

## Overview
This repository is meant to create and maintain a website that gathers information from various locations that regularly host events and gather their schedules into one place so that parents don't have to go searching around the internet to find events for their children. The idea is meant to be expandable to any number of cities, but for the moment, we only have events for Washington, DC.

In terms of the actual files in this repository, most of the heavy lifting is done by the Python scripts (and by [HTML5 UP](html5up.net) for creating the lovely template that we used to make this website). The Python scripts gather information about upcoming events from various institutions around Washington, DC and insert them into the HTML files for the website with the necessary formatting. This then creates an interactive map that displays where the events are with a marker with a radius proportional to the number of events at that location.

The website is updated automatically using the following bash script:
```bash
cd ~/Kids-Activities
python3 collect-data.py
python3 make-table.py
git add map.html geojson.js
git commit -m "daily event update"
git push
```
We are currently working on getting it to run every day at midnight. It works except for the part where I need to enter my login information when I push.

## Next Steps
At the moment, we load in all events from each location irrespective of their appropriateness for children. In time, we hope to be able not only to separate the children's events from the adults' events but also to separate the children's events by age range.

We also hope somehow to make the python scripts run automatically every night around midnight so that we can ensure that the website will be regularly updated without our having to update it manually.

Finally, we should at some point add the capability for users/parents to add in their own events and import them into our map.

Note: Minor changes might include removing redundancy in `collect-data.py`, especially considering the different ways to parse the character '-'. Also, I should see if it could be faster.
