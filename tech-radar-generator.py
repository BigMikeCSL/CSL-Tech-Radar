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
  <script src="http://zalando.github.io/tech-radar/release/radar-0.8.js"></script>
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

<table>
  <tr>
  <td>
  
  <h3>What is the Tech Radar?</h3>
  
  <p>
  The Zalando Tech Radar is a list of technologies, complemented by an assessment result, called <em>ring assignment</em>. We use four rings with the following semantics:
  </p>
  
  <ul>
  <li><strong>ADOPT</strong> &mdash; Technologies we have high confidence in to serve our purpose, also in large scale. Technologies with a usage culture in our Zalando production environment, low risk and recommended to be widely used.</li>
  <li><strong>TRIAL</strong> &mdash; Technologies that we have seen work with success in project work to solve a real problem; first serious usage experience that confirm benefits and can uncover limitations. TRIAL technologies are slightly more risky; some engineers in our organization walked this path and will share knowledge and experiences.</li>
  <li><strong>ASSESS</strong> &mdash; Technologies that are promising and have clear potential value-add for us; technologies worth to invest some research and prototyping efforts in to see if it has impact. ASSESS technologies have higher risks; they are often brand new and highly unproven in our organisation. You will find some engineers that have knowledge in the technology and promote it, you may even find teams that have started a prototyping effort.</li>
  <li><strong>HOLD</strong> &mdash; Technologies not recommended to be used for new projects. Technologies that we think are not (yet) worth to (further) invest in. HOLD technologies should not be used for new projects, but usually can be continued for existing projects.</li>
  </ul>
  
  </td><td>
  
  <h3>What is the purpose?</h3>
  
  <p>
  The Tech Radar is a tool to inspire and support Engineering teams at Zalando to pick the best technologies for new projects; it provides a platform to share knowledge and experience in technologies, to reflect on technology decisions and continuously evolve our technology landscape. Based on the <a href="https://www.thoughtworks.com/radar">pioneering work of ThoughtWorks</a>, our Tech Radar sets out the changes in technologies that are interesting in software development &mdash; changes that we think our engineering teams should pay attention to and use in their projects.
  </p>
  
  <h3>How do we maintain it?</h3>
  
  <p>
  The Tech Radar is maintained by our <em>Principal Engineers</em> &mdash; who facilitate and drive the technology selection discussions at Zalando across the Engineering Community. Assignment of technologies to rings is the outcome of ring change proposals, which are discussed and voted on. The Tech Radar is open for contribution for all Engineering teams at Zalando and depends on their active participation to share lessons learned, pitfalls, and contribute to good practices on using the technologies.<br/>
  </p>
  
  <p>
  Check out our <a href="https://engineering.zalando.com/tags/tech-radar.html">Engineering Blog</a> for more information on how we approach Technology Selection and use the Tech Radar at Zalando.
  </p>
  
  <p>
  <em>BTW, if you would like to create your own Tech Radar &mdash; we have <a href="https://github.com/zalando/tech-radar">open sourced the code</a> to generate this visualization.</em>
  </p>
  
  </td></tr>
  </table>

</body>
</html>
"""

# Save the generated HTML content to a file
output_file_path = 'tech_radar.html'
with open(output_file_path, mode='w', encoding='utf-8') as file:
    file.write(html_content)

print(f"Tech Radar HTML has been generated and saved to {output_file_path}")
