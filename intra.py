import asyncio
from typing import Iterator
from pyppeteer import launch
import time
from bs4 import BeautifulSoup
import os
import re

with open('test.txt', 'a') as file:
    file.write('Test content')
with open('output_lessonplan.txt', 'w') as f:
    f.write('')

with open('credentials.txt', 'r') as c:
    user = [line.rstrip('\n') for line in c]
    print(user)
    print(user[0], user[1])

htmlthing = ''
Iterator = 0


async def main():   
    html = htmlthing
    browser = await launch(headless=True)  # Launch a headless browser
    page = await browser.newPage()
    

    await page.goto('https://intranet.tam.ch/krm/timetable/classbook')
    
    await page.type('#loginuser', str(user[0]))
    await page.type('#loginpassword', str(user[1]))
    await page.click('.login--school-login--login-button')
    time.sleep(5)
    #html = await page.content()
    elements = await page.querySelectorAll('.k-scheduler-layout.k-scheduler-workWeekview')
    
    for element in elements:
        html += await page.evaluate('(element) => element.innerHTML', element)
        
    #print(html)  
    with open('output.txt', 'w', errors='ignore') as f:
            f.write(html)
    print("HTML content saved to output.txt")
    
    await browser.close()


    




asyncio.get_event_loop().run_until_complete(main())
print("i got here!")
with open('output.txt', 'r') as s:
    htmlsauce = s.read()


soup = BeautifulSoup(htmlsauce, 'html.parser')

lessons = []

for lesson in soup.find_all('div', class_=['in-event-type-cancel', 'in-event-type-lesson']):
    print("working!")
    is_canceled = 'CANCELED - ' if 'in-event-type-cancel' in lesson.get('class') else ''
    lesson_name = lesson.find('span', class_='in-title').get_text(strip=True)
    lesson_time = lesson.find('span', class_='in-time').get_text(strip=True)
    teacher = lesson.find('span', class_='in-teacher').get_text(strip=True)
    class_name = lesson.find('span', class_='in-class').get_text(strip=True)
    room = lesson.find('span', class_='in-room').get_text(strip=True)

    if is_canceled != '':
        lesson_info = f"[{is_canceled}] {lesson_name} -- {lesson_time} -- {teacher}, {class_name}, {room}"
    elif is_canceled == '':
        lesson_info = f"{lesson_name} -- {lesson_time} -- {teacher}, {class_name}, {room}"
    lessons.append(lesson_info)
with open('output_lessonplan.txt', 'a') as temp: temp.write('DAYBREAK' + '\n')
for lesson in lessons:
    with open('output_lessonplan.txt', 'a') as final:
        final.write(lesson + '\n')
        with open('daybreak.txt', 'r') as day:
            search = day.read()
            if lesson in search: final.write('DAYBREAK' + '\n')
    print(lesson)
print(lessons)



time.sleep(1)



from bs4 import BeautifulSoup

# Read lesson plan data from the file
with open('output_lessonplan.txt', 'r') as file:
    lesson_plan_data = file.read()

# Split the lesson plan data by DAYBREAK
days = lesson_plan_data.split('DAYBREAK') 

# HTML template
html_template = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.getElementsByTagName("html")[0].className += " js";</script>
  <link rel="stylesheet" href="assets/css/style.css">
  <title>Schedule Template | CodyHouse</title>
</head>
<body>
  <header class="cd-main-header text-center flex flex-column flex-center">
    <h1 class="text-xl">This Week's timetable:</h1>
  </header>

  <div class="cd-schedule cd-schedule--loading margin-top-lg margin-bottom-lg js-cd-schedule">
    <div class="cd-schedule__timeline">
      <ul>
        <li><span>06:00</span></li>
        <li><span>06:30</span></li>
        <li><span>07:00</span></li>
        <li><span>08:30</span></li>
        <li><span>09:00</span></li>
        <li><span>09:30</span></li>
        <li><span>10:00</span></li>
        <li><span>10:30</span></li>
        <li><span>11:00</span></li>
        <li><span>11:30</span></li>
        <li><span>12:00</span></li>
        <li><span>12:30</span></li>
        <li><span>13:00</span></li>
        <li><span>13:30</span></li>
        <li><span>14:00</span></li>
        <li><span>14:30</span></li>
        <li><span>15:00</span></li>
        <li><span>15:30</span></li>
        <li><span>16:00</span></li>
        <li><span>16:30</span></li>
        <li><span>17:00</span></li>
        <li><span>17:30</span></li>
        <li><span>18:00</span></li>
      </ul>
    </div> <!-- .cd-schedule__timeline -->

    <div class="cd-schedule__events">
      <ul>
        <!-- Events will be dynamically generated here -->
      </ul>
    </div>

    <div class="cd-schedule-modal">
      <header class="cd-schedule-modal__header">
        <div class="cd-schedule-modal__content">
          <span class="cd-schedule-modal__date"></span>
          <h3 class="cd-schedule-modal__name"></h3>
        </div>

        <div class="cd-schedule-modal__header-bg"></div>
      </header>

      <div class="cd-schedule-modal__body">
        <div class="cd-schedule-modal__event-info"></div>
        <div class="cd-schedule-modal__body-bg"></div>
      </div>

      <a href="#0" class="cd-schedule-modal__close text-replace">Close</a>
    </div>

    <div class="cd-schedule__cover-layer"></div>
  </div> <!-- .cd-schedule -->

  <script src="assets/js/util.js"></script> <!-- util functions included in the CodyHouse framework -->
  <script src="assets/js/main.js"></script>
</body>
</html>
'''

# Create BeautifulSoup object from the HTML template
soup = BeautifulSoup(html_template, 'html.parser')

# Find the <ul> tag inside <div class="cd-schedule__events">
events_ul = soup.find('div', class_='cd-schedule__events').find('ul')
a=0
iterr=0
# Iterate over each day's data
for day_data in days:
    # Split the day's data into individual events
    events = day_data.strip().split('\n')

    # Extract the day name
    day_name = ["","Monday", "Tuesday", "Wednesday", "Thursday", "Friday",""]

    # Create a new <li> tag for the day
    day_li = soup.new_tag('li', class_='cd-schedule__group')
    day_div = soup.new_tag('div', class_='cd-schedule__top-info')
    day_span = soup.new_tag('span')
    day_span.string = day_name[a]
    day_div.append(day_span)
    day_li.append(day_div)

    # Create a new <ul> tag for the day's events
    events_ul_day = soup.new_tag('ul')

    # Iterate over each event in the day's data
    for event in events:#[1:]:
        # Split the event data into its components
        event_parts = [part.strip() for part in event.split('--')]
        if len(event_parts) >= 3:
        # Extract the event details
            event_name = event_parts[0].strip()
            event_time = event_parts[1].strip()
            event_location = event_parts[2].strip()


        # Determine the event's cancellation status
            is_canceled = event_name.startswith('[CANCELED - ]')
            data_event = 'event-1' if is_canceled else 'event-2'

            # Create a new <li> tag for the event
            event_li = soup.new_tag('li', class_='cd-schedule__event')
            event_a = soup.new_tag('a', href='#0', class_='cd-schedule__name')
            event_a['data-start'] = event_time.split('-')[0].strip()
            event_a['data-end'] = event_time.split('-')[1].strip()
            event_a['data-content'] = event_parts[0].replace('[CANCELED - ]', '').strip()
            event_a['data-event'] = data_event
            event_em = soup.new_tag('em', class_='cd-schedule__name')
            event_em.string = event_name.replace('[CANCELED - ]', '').strip()

            event_a.append(event_em)
            event_li.append(event_a)
            events_ul_day.append(event_li)
        else:
            print(f"Ignoring event with insufficient data: {event}", len(event_parts))
        print("iterated!")

    # Append the <ul> tag of events to the day's <li> tag
    day_li.append(events_ul_day)

    # Append the day's <li> tag to the main <ul> tag of events
    events_ul.append(day_li)
    a=a+1
    iterr+=1
    print("oneloop")
    #if iterr == 6: break

# Print the modified HTML
with open("index.html", 'w') as f:
    f.write(soup.prettify().replace('class_', 'class'))
#print(soup.prettify())


















































"""

# Read the HTML file
# Read the HTML file
# Read the HTML template
import re
from bs4 import BeautifulSoup

# Read lesson plan data from a file
with open('output_lessonplan.txt', 'r') as file:
    lesson_plan_data = file.read()

# Split the lesson plan data by DAYBREAK to get individual days
days = lesson_plan_data.split('DAYBREAK\n')

# HTML template
html_template = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.getElementsByTagName("html")[0].className += " js";</script>
  <link rel="stylesheet" href="assets/css/style.css">
  <title>Schedule Template | CodyHouse</title>
</head>
<body>
  <header class="cd-main-header text-center flex flex-column flex-center">
    <h1 class="text-xl">This Week's timetable:</h1>
  </header>

  <div class="cd-schedule cd-schedule--loading margin-top-lg margin-bottom-lg js-cd-schedule">
    <div class="cd-schedule__timeline">
      <ul>
        <li><span>09:00</span></li>
        <li><span>09:30</span></li>
        <li><span>10:00</span></li>
        <li><span>10:30</span></li>
        <li><span>11:00</span></li>
        <li><span>11:30</span></li>
        <li><span>12:00</span></li>
        <li><span>12:30</span></li>
        <li><span>13:00</span></li>
        <li><span>13:30</span></li>
        <li><span>14:00</span></li>
        <li><span>14:30</span></li>
        <li><span>15:00</span></li>
        <li><span>15:30</span></li>
        <li><span>16:00</span></li>
        <li><span>16:30</span></li>
        <li><span>17:00</span></li>
        <li><span>17:30</span></li>
        <li><span>18:00</span></li>
      </ul>
    </div>
  
    <div class="cd-schedule__events">
      <ul>
        {content}
      </ul>
    </div>
  
    <div class="cd-schedule__cover-layer"></div>
  </div>
  
  <script src="assets/js/util.js"></script>
  <script src="assets/js/main.js"></script>
</body>
</html>
'''

# Function to generate the HTML content for a day's schedule
def generate_day_schedule(day_data, event_counter):
    schedule_html = ''
    events = day_data.strip().split('\n')
    day_name = events[0]
    events = events[1:]  # Exclude the day name

    schedule_html += f'''
        <li class="cd-schedule__group">
          <div class="cd-schedule__top-info"><span>{day_name}</span></div>
    
          <ul>
    '''

    for event in events:
        canceled = False
        if '[CANCELED' in event:
            canceled = True
            event = re.sub(r'\[CANCELED - \]\s*', '', event)  # Remove the [CANCELED - ] prefix
        
        event_details = re.findall(r'(.+?) -- (.+?) -- (.+)', event)
        if event_details:
            event_time, event_name, event_location = event_details[0]
            time_match = re.findall(r'(\d{2}:\d{2})-(\d{2}:\d{2})', event_time)
            if time_match:
                start_time, end_time = time_match[0]
            else:
                start_time = end_time = ''
        else:
            event_name = ''
            start_time = end_time = ''

        if event_name:
            event_html = f'''
                <li class="cd-schedule__event">
                  <a data-start="{start_time}" data-end="{end_time}" data-content="{event_name}" data-event="event-{event_counter}" href="#0">
                    <em class="cd-schedule__name">{event_name}</em>
                  </a>
                </li>
            '''
            schedule_html += event_html

        if canceled:
            event_counter += 1

    schedule_html += '''
          </ul>
        </li>
    '''

    return schedule_html, event_counter

# Generate the HTML content for all days
event_counter = 1
schedule_content = ''
for day_data in days:
    day_schedule, event_counter = generate_day_schedule(day_data, event_counter)
    schedule_content += day_schedule

# Insert the generated content into the HTML template
final_html = html_template.format(content=schedule_content)

# Save the final HTML to a file
with open('index.html', 'w') as file:
    file.write(final_html)



"""









"""from bs4 import BeautifulSoup

# Read the data from the "output_lessonplan.txt" file
with open("output_lessonplan.txt", "r") as file:
    data = file.readlines()

# Load the HTML file
with open("index.html", "r") as file:
    html = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find the div with class "cd-schedule__events"
schedule_div = soup.find("div", class_="cd-schedule__events")

# Initialize variables to keep track of the current day and group
current_day = None
current_group = None

# Iterate over the data
for line in data:
    line = line.strip()
    if line == "DAYBREAK":
        # Reset the current day and group when encountering "DAYBREAK"
        current_day = None
        current_group = None
    elif line.startswith("[CANCELED - ]"):
        # Extract the event details from the canceled event line
        parts = line.split(" -- ")
        event_name = parts[1].strip().split(" ")[-1]
        event_time = parts[2].strip().split("-")
        event_start = event_time[0]
        event_end = event_time[1]
        event_group = parts[3].strip().split(", ")[0]

        # Create a new event element for the canceled event
        new_event = soup.new_tag("li", class_="cd-schedule__event")
        new_event.append(soup.new_tag("a", href="#0", data_start=event_start, data_end=event_end,
                                      data_content="event-" + event_group, data_event="event-2"))
        new_event.a.append(soup.new_tag("em", class_="cd-schedule__name"))
        new_event.a.em.string = event_name

        # Append the new event to the appropriate group
        if current_group is not None:
            current_group.ul.append(new_event)
    else:
        # Extract the event details from the line
        parts = line.split(" -- ")
        event_name = parts[0]
        event_time = parts[1].strip().split("-")
        event_start = event_time[0]
        event_end = event_time[1]
        event_group = parts[2].strip().split(", ")[0]

        # Create a new event element for the non-canceled event
        new_event = soup.new_tag("li", class_="cd-schedule__event")
        new_event.append(soup.new_tag("a", href="#0", data_start=event_start, data_end=event_end,
                                      data_content="event-" + event_group, data_event="event-1"))
        new_event.a.append(soup.new_tag("em", class_="cd-schedule__name"))
        new_event.a.em.string = event_name

        # Append the new event to the appropriate group
        if current_group is not None:
            current_group.ul.append(new_event)

    # Update the current day and group based on the existing structure in the HTML
    if current_day is None or current_day.span.string != event_group:
        current_day = schedule_div.find("div", string=event_group)
        current_group = current_day.find_next_sibling("ul")

# Save the modified HTML back to the file
with open("index.html", "w") as file:
    file.write(str(soup))


        <li><span>09:00</span></li>
        <li><span>09:30</span></li>
        <li><span>10:00</span></li>
        <li><span>10:30</span></li>
        <li><span>11:00</span></li>
        <li><span>11:30</span></li>
        <li><span>12:00</span></li>
        <li><span>12:30</span></li>
        <li><span>13:00</span></li>
        <li><span>13:30</span></li>
        <li><span>14:00</span></li>
        <li><span>14:30</span></li>
        <li><span>15:00</span></li>
        <li><span>15:30</span></li>
        <li><span>16:00</span></li>
        <li><span>16:30</span></li>
        <li><span>17:00</span></li>
        <li><span>17:30</span></li>
        <li><span>18:00</span></li>
        """