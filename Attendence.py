
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False

# Dummy data to simulate student names
students_data = {
    1: 'John Doe',
    2: "Jane Smith",
    3: "Ansari Jamal Ahmad Taj Mohmmad",
    4: "Baid Prerna Rajkamal",
    5: "Bhandari Jimil Jitesh",
    6: "Bhanushali Keval Jivanbhai",
    7: "Bind Prabhudev Vinod",
    8: "Bind Shivani Vinod",
    9: "Chaudhary Juned Ahmed Mukhtar Ali",
    10: "Chauhan Abhishek Ishwar",
    11: "Chauhan Priti Shambhu",
    12: "Chheda Chintan Mahendra",
    13: "Dabhi Raghav Ghanshyambhal",
    14: "Dadiani Ravi Prakash",
    15: "Desai Jeet Rajiv",
    16: "Desai Neel Chetan",
    17: "Gajjar Harsh Nayanchandra",
    18: "Gohil Priya Jagdish",
    19: "Goswami Darshana Vileshgiri",
    20: "Goswarni Nidhi Hemantbharthi",
    21: "Hevin Dinesh",
    22: "Jaiswal Ashutosh Ashok",
    23: "Jha Diya Randhir",
    24: "Joshi Siddhi Amit",
    25: "Kahar Devin Plyush",
    26: "Khan Amirsuhail Naseemahmed",
    27: "Kamli Sneh Prakash",
    28: "Koladiya Surohi Vipul",
    29: "Makani Simon Azadbhai",
    30: "Malik Sneha Praful",
    31: "Mandal Kaushal Santosh",
    32: "Maurya Ranjana Bakelal",
    33: "Mazi Pinki Sadanial",
    34: "Mishra Aditya Ravi",
    35: "Mishra Chanchal Sanjay",
    36: "Mistry Krisha Vipulkumar",
    37: "Munshi Shakib Shakilahmed",
    38: "Nair Dhrutt Unnikrishna",
    39: "Pal Aarju Pramod",
    40: "Panchal Ishita Anil",
    41: "Panchal Yash Hitesh",
    42: "Pandey Anurag Nagendra",
    43: "Pandya Harsh Bharatbhal",
    44: "Pandya Yash Nilay",
    45: "Parmar Krisha Kaushik",
    46: "Patel Anjali Virendra",
    47: "Patel Meet Hemant",
    48: "Patel Neel Sureshbhai",
    49: "Patel Pal Ashwin",
    50: "Patel Shrutika Suresh",
    51: "Patel Trushika Jitendra",
    52: "Pathak Ashutosh R",
    53: "Pathak Kiran Dinesh",
    54: "Pawar Anjali Prakash",
    55: "Pillai Vinish Vijay",
    56: "Prasad Preeti Motichand",
    57: "Rai Aman Gaurishnakar",
    58: "Panchal Yash Hitesh",
    59: "Pandey Anurag Nagendra",
    60: "Pandya Harsh Bharatbhal",
    61: "Pandya Yash Nilay",
    62: "Parmar Krisha Kaushik",
    63: "Patel Anjali Virendra",
    64: "Patel Meet Hemant",
    65: "Patel Neel Sureshbhai",
    66: "Patel Pal Ashwin",
    67: "Patel Shrutika Suresh",
    68: "Patel Trushika Jitendra",
    69: "Pathak Ashutosh R",
    70: "Pathak Kiran Dinesh",
    71: "Pawar Anjali Prakash",
    72: "Pillai Vinish Vijay",
    73: "Prasad Preeti Motichand",
    74: "Rai Aman Gaurishnakar",
    75: "Patel Neel Sureshbhai",
    76: "Patel Pal Ashwin",
    77: "Patel Shrutika Suresh",
    78: "Patel Trushika Jitendra",
    79: "Pathak Ashutosh R",
    80: "Pathak Kiran Dinesh",
    81: "Pawar Anjali Prakash",
    82: "Pillai Vinish Vijay",
    83: "Prasad Preeti Motichand",
    84: "Rai Aman Gaurishnakar",
    85: "Badtya Indra Prabhat",
    86: "Bebale Vidya Anand",
    87: "Bhandari Abhi Chetan",
    88: "Bhandari Mantra Mukesh",
    89: "Bhandari Shruti Kaushik",
    90: "Bharti Satyam Shrikant",
    91: "Bindra Akhilesh Narendrabhai",
    92: "Birari Harshda Satish",
    93: "Chauhan Devendra Sanjaykumar",
    94: "Chauhan Hitesh Omprakash",
    95: "Chauhan Vanshika Dilip",
    96: "Choudhary Ravi Rajaram",
    97: "Gautam Abhishek Jilajeet",
    98: "Gautam Satyam Narendra",
    99: "Godhasara Darshak Pravinbhai",
    100: "Gupta Sandeep Upendra",
    101: "Jha Bharat Digambar",
    102: "Jha Ritesh Sitakant",
    103: "Kami Janki Tejbhadur",
    104: "Kamli Utsav Umesh",
    105: "Kanabar Mohit Jayeshbhai",
    106: "Karde Harshal Sarang",
    107: "Karlekar Kashish Santosh",
    108: "Kazi Imran Abdulkalam",
    109: "Khan Ishaque Md Akbar",
    110: "Khimani Arpi Kanaiyalal",
    111: "Kushwaha Amarjitkumar Sureshsinh",
    112: "Kuzhichamadathil Amal Santosh",
    113: "Mansuri Muzzamil FazalHussain",
    114: "Mehra Nikita Sachin",
    115: "Mistry Deep Himmatbhai",
    116: "Morwal Aditya Arun",
    117: "Nishad Nirajkumar Kishor",
    118: "Odedra Rajveer Anandbhai",
    119: "Pal Ankit Ramshankar",
    120: "Pandey Amitesh Sanjeev",
    121: "Pandit Sandeep Meghan",
    122: "Patel Chirag Ranjt",
    123: "Patel Khushl litendrabhai",
    124: "Patel Mayank Manish",
    125: "Patel Pramit Mahesh",
    126: "Patel Shrey Uttambhal",
    127: "Pathan Mo Kaif Samim",
    128: "Patil Tushar Sharadbhai",
    129: "Prajapati Babita Raghunath",
    130: "Prajapati Kunj Shaileshbhai",
    131: "Prajapati Raj Pankaj",
    132: "Prasad Vikas talan",
    133: "Rai Khushi Rajiv",
    134: "Ramawat Komal Sanjay",
    135: "Rathod Mayank Bhupendrabhai",
    136: "Rayni Arman Sarfarajbhai",
    137: "Rohit Prembhai Shaileshbhai",
    138: "Saini Pooja Bhanaram",
    139: "Sainy Abhishek Pappu",
    140: "Salvi Vighnesh Parshuram",
    141: "Sankhala Dishant Ramswardop",
    142: "Sawai Jagdish Rathod",
    143: "Sayyed Nargis Yasmeen Ashadur rehman",
    144: "Shah Hetvi Pragnesh",
    145: "Shah Mitava Pareshkumar",
    146: "Sharma Dhruv Rajesh",
    147: "Sharma Kumari Anjali Phoolwas",
    148: "Siddiqui Jazi Danish",
    149: "Singh Harsh Rajkumar",
    150: "Singh Kaushal Satish",
    151: "Singh Nihal Surendra",
    152: "Singh Sakshi Hareram",
    153: "Singh Siksha Santosh",
    154: "Singh Vinect Ashok",
    155: "Singh Vishal Hareram",
    156: "Teli Ghanshyam Narendra",
    157: "Thakur Khushi Mohansingh",
    158: "Tiwari Devans Arvind",
    159: "Vidhale Isha Liladharrao",
    160: "Yadav Riya Ramlakhan",
    161: "Yadav Tejas Dnyaneshwar",
    162: "Yash Jagjit Singh"
}



# Function to create the database and table if they don't exist
import sqlite3

def create_table():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class TEXT,
                    division TEXT,
                    date TEXT,
                    subject TEXT,
                    roll_number INTEGER,
                    status TEXT,
                    student_name TEXT
                 )''')

    # Save dummy data into the database
    for roll_number, student_name in students_data.items():
        c.execute("INSERT INTO attendance (class, division, date, subject, roll_number, status, student_name) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  ('FYBCA', 'Div-1', '2023-07-28', 'Subject1', roll_number, 'absent', student_name))

    conn.commit()
    conn.close()

create_table()


# ... other parts of the code ...

@app.route('/api/save-attendance', methods=['POST'])
def save_attendance():
    data = request.get_json()
    print(data)
    # Extract data from the request
    class_name = data.get('class')
    division = data.get('division')
    date = data.get('date')
    subject = data.get('subject')
    attendance_data = data.get('attendance_data')

    # Check if 'attendance_data' is a list
    if not isinstance(attendance_data, list):
        return jsonify({'error': 'Invalid data format. "attendance_data" should be a list of objects.'}), 400

    # Save the attendance records to the database
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    try:
        for item in attendance_data:
            roll_number = item.get('roll_number')
            status = item.get('status')

            if not roll_number or not status:
                return jsonify({'error': 'Invalid data format. "roll_number" and "status" are required for each student.'}), 400

            # Check if the record exists in the database
            c.execute("SELECT * FROM attendance WHERE class=? AND division=? AND date=? AND subject=? AND roll_number=?",
                      (class_name, division, date, subject, roll_number))
            existing_record = c.fetchone()

            if existing_record:
                # Update the existing record
                c.execute("UPDATE attendance SET status=? WHERE id=?", (status, existing_record[0]))

        conn.commit()
    except sqlite3.OperationalError as e:
        return jsonify({'error': 'An operational error occurred while saving attendance data.'}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred while saving attendance data.'}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Attendance data saved successfully.'}), 200


#

# API endpoint to get student name by roll number
@app.route('/api/get-student', methods=['GET'])
def get_student():
    student_name = students_data
    if student_name:
        return jsonify( student_name)
    else:
        return jsonify({"error": "Student not found"}), 404


# API endpoint to get all attendance data
@app.route('/api/get-all-attendance', methods=['GET'])
def get_all_attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    print( c.execute("SELECT * FROM attendance"))
    rows = c.fetchall()
    conn.close()

    if not rows:  # Check if the rows list is empty
        return jsonify({"message": "No attendance records found."}), 404

    attendance_data = []
    for row in rows:
        attendance_data.append({
            'id': row[0],
            'division': row[1],
            'name': row[2],
            'roll_number': row[3],
            'subject': row[4],
            'status': row[5]
        })

    return jsonify(attendance_data), 200



if __name__ == '__main__':
    app.run(debug=True)
