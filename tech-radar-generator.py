import csv
import datetime

# Read the CSV file
file_path = 'radar.csv'
entries = []

with open(file_path, mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    headers = csv_reader.fieldnames
    print(f"Headers: {headers}")
    for row in csv_reader:
        # Determine the ring based on the CSV value
        ring = {
            'Adopt': 0,
            'Trial': 1,
            'Assess': 2,
            'Hold': 3
        }[row['Ring']]

        quadrant = {
            'Infrastructure': 0,
            'Data Stores': 1,
            'Libraries & Frameworks': 2,
            'Tools': 3,
        }[row['Quadrant']]

        print("Ring is ", ring)
        print("Quadrant is ", quadrant)
        print("Technology name is", row['Technology Name'])
        
        entry = {
            'label': row['Technology Name'],
            'quadrant': quadrant, 
            'ring': ring,
            'moved': 0,
            'link': row['Page URL']
        }
        entries.append(entry)

# Generate the HTML content
date_str = datetime.datetime.now().strftime("%Y.%m")

html_content = f"""
<!DOCTYPE html>
<html lang="en">

<head>
  <meta http-equiv="Content-type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>CSL BE Tech Radar</title>

  <script src="https://d3js.org/d3.v4.min.js"></script>
  <script src="https://zalando.github.io/tech-radar/release/radar-0.8.js"></script>
</head>

<body>


<svg id="radar"></svg>

<script type="text/javascript">
  const infrastructureQuadrant = 0;
  const dataStoresQuadrant = 1;
  const frameworksAndLibrariesQuadrant = 2;
  const toolsQuadrant = 3;

  const adoptRing = 0;
  const trialRing = 1;
  const assessRing = 2;
  const holdRing = 3;

  const movedOut = -1;
  const notMoved = 0;
  const movedIn = 1;

  radar_visualization({{
  svg_id: "radar",
  width: 1450,
  height: 1000,
  scale: 1.0,
  colors: {{
    background: "#fff",
    grid: "#bbb",
    inactive: "#ddd"
  }},
  title: "CSL BE Tech Radar",
  date: "{date_str}",
  quadrants: [
    {{ name: "Infrastructure" }},
    {{ name: "Data Stores" }},
    {{ name: "Libraries & Frameworks" }},
    {{ name: "Tools" }}
  ],
  rings: [
    {{ name: "ADOPT",  color: "#5ba300" }},
    {{ name: "TRIAL", color: "#009eb0" }},
    {{ name: "ASSESS",  color: "#c7ba00" }},
    {{ name: "HOLD",  color: "#e09b96" }}
  ],
  print_layout: true,
  links_in_new_tabs: true,
  entries: [
"""

# Add entries to the HTML content
for entry in entries:
    html_content += f"""
    {{
        label: "{entry['label']}",
        quadrant: {entry['quadrant']},
        ring: {entry['ring']},
        moved: {entry['moved']},
        link: "{entry['link']}"
    }},
    """

html_content += """
  ]
});
</script>
</body>
</html>
"""

# Save the generated HTML content to a file
output_file_path = 'index.html'
with open(output_file_path, mode='w', encoding='utf-8') as file:
    file.write(html_content)

print(f"Tech Radar HTML has been generated and saved to {output_file_path}")
