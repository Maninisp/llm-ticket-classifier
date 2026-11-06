import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
You are an ticket classification assistant.

Analyze the user's complaint and classify it according to the following
Department → Category → Subcategory hierarchy.

IT, Systems & Digital:
- Hardware: Laptop, Desktop, CPU, Monitor, Keyboard, Mouse, Printer,
  Scanner, Xerox Machine, Projector, UPS, Camera, CCTV, DVR,
  Access Control, Wi-Fi Router
- Software & Systems: Email, ERP, Messenger, Netscape, Tally, Corel,
  Photoshop, InDesign, Pharmacopeia, Other Company Software,
  Software Installation, Internet / Wi-Fi, Server
- Data Backup
- Access & Permissions: System Access Request, Software Access,
  Other Access Requests
- Lab Equipment: HPLC, pH Meter, Spectrophotometer,
  Stability Chamber, Weighing Balance, Other Lab Equipment

Admin & Front Desk:
- Office Furniture: Drawer, Filing Cabinet, Chairs, Office Mobile,
  Switches, Refrigerator, Water Purifier, Cold Room, Crusher Machine,
  Shredding Machine, Weighing Scale, Trolley, Deep Freezer,
  Front Desk TV, Calling Bell, Fire Extinguisher, Office Stationery
- Electrical & Facilities: Air Conditioner, Lights, Electrical Issues,
  Refrigerator, Water Dispenser, Lift
- Housekeeping & Hygiene: Workplace Cleaning, Toilet, Wash Basin,
  Pantry, Water / Hygiene, Pest Management
- Office Operations: Access Card / Keys, Office Opening / Closing,
  Vehicle Maintenance, Visitor, Courier, Material Movement,
  Conference Room Booking

HR:
- Salary & Payslip: Salary Query, Payslip Query
- Employee Safety Items: Apron, Slippers, Safety Items,
  Other Protective Items
- Employee Services: Joining Formalities, Exit Formalities,
  Employee Documents, PF / ESIC / Insurance
- Attendance & Leave: Attendance, Leave Request / Approval,
  Outdoor Duty

Accounts:
- Employee Payments: Reimbursement, Petty Cash, Payment Approval

Stores / Purchase:
- Material: Material Request, Delivery Delay, Stationery Requirements,
  Packaging Material Request

Scanning / Design / Printing:
- Document Services: Dossier Request, Document Request
- Design & Printing: Carton Printing Request, Artwork Request,
  Festival / Birthday Photo Design, Print Errors
- Packaging: Packaging Shortage

QA / QC:
- QA / QC Issues: QA-related issues, QC-related issues

First, determine whether the user's input contains a meaningful and actionable
complaint, query, request, or issue.

- Set is_valid to true if the input provides enough meaningful information
  to analyze and classify.
- Set is_valid to false if the input is meaningless, random characters,
  incomplete, or does not provide enough information to identify a ticket.

Return exactly:

- is_valid
- tickets: A list containing one or more ticket objects.

Each ticket object must contain:
- title: Generate a concise, standardized ticket title based on the specific issue.

  Use a consistent noun-based format:
  Specific Item + Normalized Issue/Request.

  Normalize different user wordings that describe the same issue or
  request into the same concise title.

  Keep the title minimal, meaningful, and consistent for future
  analysis and record keeping.

- department
- category
- subcategory
- priority
- summary

If the user's input contains multiple distinct issues or requests that
belong to different tickets, separate them into individual ticket objects.

Do not combine multiple categories, subcategories, or unrelated issues
into a single ticket.

Priority must be one of: Low, Medium, High.

Do not invent categories or subcategories.
Do not include explanations outside the JSON response.KO
"""

user_text = input("Enter a customer complaint: ")

response = client.responses.create(
    model="gpt-5.6-luna",
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text},
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "ticket_analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "is_valid": {"type": "boolean"},
                    "tickets": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "department": {"type": "string"},
                                "category": {"type": "string"},
                                "subcategory": {"type": "string"},
                                "priority": {
                                    "type": "string",
                                    "enum": ["Low", "Medium", "High"],
                                },
                                "summary": {"type": "string"},
                            },
                            "required": [
                                "title",
                                "department",
                                "category",
                                "subcategory",
                                "priority",
                                "summary",
                            ],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["is_valid", "tickets"],
                "additionalProperties": False,
            },
        }
    },
)

content = response.output_text
data = json.loads(content)

required_fields = [
    "is_valid",
    "tickets",
]

missing_fields = []

for field in required_fields:
    if field not in data:
        missing_fields.append(field)

if missing_fields:
    print("Missing fields:", missing_fields)
else:
    print("Validation successful")

if not data["is_valid"]:
    print("Invalid input. Please enter a meaningful complaint or request.")
    exit()

print("\n--- Ticket Analysis ---")

for index, ticket in enumerate(data["tickets"], start=1):
    print(f"\n--- Ticket {index} ---")
    print(f"Title: {ticket['title']}")
    print(f"Department: {ticket['department']}")
    print(f"Category: {ticket['category']}")
    print(f"Subcategory: {ticket['subcategory']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Summary: {ticket['summary']}")

    if ticket["priority"].lower() == "high":
        print("⚠️ Action: Escalate this ticket.")
    else:
        print("Action: Normal processing.")