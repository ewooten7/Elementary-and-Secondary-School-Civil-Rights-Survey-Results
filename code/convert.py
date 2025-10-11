import csv
from pathlib import Path

# --- Schema Definitions ---
# These schemas define the fields we want to extract from the start of each block.

SYSTEM_SCHEMA = [
    ("OE School System Code",4,"numeric"),
    ("SKIP_0", 4, "skip"),
    ("System Name", 32, "literal"),
    ("System Street Address", 32, "literal"),
    ("System City", 16, "literal"),
    ("System County", 16, "literal"),
    ("System State", 16, "literal"),
    ("System Zip Code", 8, "literal"),
    ("Chief Administrative Officer", 20, "literal"),
    ("Number of School Campus Forms", 4, "numeric"),
    ("System Pupils: American Indian", 4, "numeric"),
    ("System Pupils: Black", 4, "numeric"),
    ("System Pupils: Asian American", 4, "numeric"),
    ("System Pupils: Spanish Surname", 4, "numeric"),
    ("System Pupils: Other", 4, "numeric"),
    ("System Pupils: Total", 4, "numeric"),
    #("SKIP_1", 24, "skip"),
    ("Nonresident Pupils",4,"numeric"),
    ("Resident Pupils",4,"numeric"),
    ("Expelled: American Indian",4,"numeric"),
    ("Expelled: Black",4,"numeric"),
    ("Expelled: Asian",4,"numeric"),
    ("Expelled: Spanish Surname",4,"numeric"),
    ("Expelled: Other",4,"numeric"),
    ("Expelled: Total",4,"numeric"),
    ("Resident Pupils in another System",4,"numeric"),
    ("Resident Pupils in nonpublic schools",4,"numeric"),
    ("Resident School Age not in School",4,"numeric"),
    ("System Teachers: American Indian",4,"numeric"),
    ("System Teachers: Black",4,"numeric"),
    ("System Teachers: Asian",4,"numeric"),
    ("System Teachers: Spanish Surname",4,"numeric"),
    ("System Teachers: Other",4,"numeric"),
    ("System Teachers: Total",4,"numeric"),
    ("Professional Staff: American Indian",4,"numeric"),
    ("Professional Staff: Black",4,"numeric"),
    ("Professional Staff: Asian",4,"numeric"),
    ("Professional Staff: Spanish Surname",4,"numeric"),
    ("Professional Staff: Other",4,"numeric"),
    ("Professional Staff: Total",4,"numeric"),
    ("Professionals in more than one school: American Indian",4,"numeric"),
    ("Professionals in more than one school: Black",4,"numeric"),
    ("Professionals in more than one school: Asian",4,"numeric"),
    ("Professionals in more than one school: Spanish Surname",4,"numeric"),
    ("Professionals in more than one school: Other",4,"numeric"),
    ("Professionals in more than one school: Total",4,"numeric"),
    #("SKIP_2", 32, "skip"),
    ("Bilingual Instruction",4,"numeric"),
    ("Bilingual Teachers",4,"numeric"),
    ("Bilingual Pupils",4,"numeric"),
    ("Bilingual Material",4,"numeric"),
    ("New School Property",4,"numeric"),
    ("New School Construction",4,"numeric"),
    ("New School Capacity",4,"numeric"),
    ("New School (Greater Minority) Composition",4,"numeric"),
    ("Year",4,"numeric"),
    ("State Code",4,"numeric"),
    ("SRG Code",16,"skip"),
    ("Assurance",4,"numeric"),
    ("Litigation Code",4,"numeric"),
    #("SKIP_3", 4, "skip"),
    ("Selection Code",4,"numeric"),
    ("Sampling Weight ",4,"numeric"),
    ("Pupils in Another System: American Indian", 4, "numeric"),
    ("Pupils in Another System: Black", 4, "numeric"),
    ("Pupils in Another System: Asian American", 4, "numeric"),
    ("Pupils in Another System: Spanish Surname", 4, "numeric"),
    ("Pupils in Another System: Other", 4, "numeric"),
    #("SKIP_4", 20, "skip"),
    ("Pupils in Non-Public Schools: American Indian", 4, "numeric"),
    ("Pupils in Non-Public Schools: Black", 4, "numeric"),
    ("Pupils in Non-Public Schools: Asian American", 4, "numeric"),
    ("Pupils in Non-Public Schools: Spanish Surname", 4, "numeric"),
    ("Pupils in Non-Public Schools: Other", 4, "numeric"),
    ("School Age not in School: American Indian", 4, "numeric"),
    ("School Age not in School: Black", 4, "numeric"),
    ("School Age not in School: Asian American", 4, "numeric"),
    ("School Age not in School: Spanish Surname", 4, "numeric"),
    ("School Age not in School: Other", 4, "numeric"),
    ("Non-Resident Pupils: American Indian", 4, "numeric"),
    ("Non-Resident Pupils: Black", 4, "numeric"),
    ("Non-Resident Pupils: Asian American", 4, "numeric"),
    ("Non-Resident Pupils: Spanish Surname", 4, "numeric"),
    ("Non-Resident Pupils: Other", 4, "numeric"),
    ("Resident Pupils: American Indian", 4, "numeric"),
    ("Resident Pupils: Black", 4, "numeric"),
    ("Resident Pupils: Asian American", 4, "numeric"),
    ("Resident Pupils: Spanish Surname", 4, "numeric"),
    ("Resident Pupils: Other", 4, "numeric"),
    ("1970 OE code", 4, "numeric"),
]

SCHOOL_SCHEMA = [

  (
    "School District OE Code Number",
    4,
    "numeric"
  ),
  (
    "School Campus Form Number",
    4,
    "numeric"
  ),
  (
    "School Name",
    32,
    "literal"
  ),
  (
    "Grade Offered: Pre-Kindergarten",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Kindergarten",
    4,
    "numeric"
  ),
  (
    "Grade Offered: First",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Second",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Third",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Fourth",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Fifth",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Sixth",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Seventh",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Eighth",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Ninth",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Tenth",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Eleventh",
    4,
    "numeric"
  ),
 (
    "Grade Offered: Twelfth",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Ungraded",
    4,
    "numeric"
  ),
  (
    "Grade Offered: Special Education",
    4,
    "numeric"
  ),
  (
    "Pupils: American Indian",
    4,
    "numeric"
  ),
  (
    "Pupils: Black",4,"numeric"),
      (
    "Pupils: Asian American",
    4,
    "numeric"
  ),
  (
    "Pupils: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Pupils: Other",
    4,
    "numeric"
  ),
  (
    "Pupils: Total",
    4,
    "numeric"
  ),
  (
    "Retained: American Indian",
    4,
    "numeric"
  ),
  (
    "Retained: Black",
    4,
    "numeric"
  ),
  (
    "Retained: Asian American",
    4,
    "numeric"
  ),
  (
    "Retained: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Retained: Other",
    4,
    "numeric"
  ),
  (
    "Retained: Total",
    4,
    "numeric"
  ),
  (
    "Grade 12: American Indian",
    4,
    "numeric"
  ),
  (
    "Grade 12: Black",
    4,
    "numeric"
  ),
  (
    "Grade 12: Asian American",
    4,
    "numeric"
  ),
  (
    "Grade 12: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Grade 12: Other",
    4,
    "numeric"
  ),
  (
    "Grade 12: Total",
    4,
    "numeric"
  ),
  (
    "Special Education: American Indian",
    4,
    "numeric"
  ),
  (
    "Special Education: Black",
    4,
    "numeric"
  ),
  (
    "Special Education: Asian American",
    4,
    "numeric"
  ),
  (
    "Special Education: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Special Education: Other",
    4,
    "numeric"
  ),
  (
    "Special Education: Total",
    4,
    "numeric"
  ),
    (
    "School Teachers: American Indian",
    4,
    "numeric"
  ),
  (
    "School Teachers: Black",
    4,
    "numeric"
  ),
  (
    "School Teachers: Asian American",
    4,
    "numeric"
  ),
  (
    "School Teachers: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "School Teachers: Other",
    4,
    "numeric"
  ),
  (
    "School Teachers: Total",
    4,
    "numeric"
  ),
  (
    "Principals: American Indian",
    4,
    "numeric"
  ),
  (
    "Principals: Black",
    4,
    "numeric"
  ),
  (
    "Principals: Asian American",
    4,
    "numeric"
  ),
  (
    "Principals: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Principals: Other",
    4,
    "numeric"
  ),
  (
    "Principals: Total",
    4,
    "numeric"
  ),
  (
    "Assistant Principals: American Indian",
    4,
    "numeric"
  ),
  (
    "Assistant Principals: Black",
    4,
    "numeric"
  ),
  (
    "Assistant Principals: Asian American",
    4,
    "numeric"
  ),
  (
    "Assistant Principals: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Assistant Principals: Other",
    4,
    "numeric"
  ),
  (
    "Assistant Principals: Total",
    4,
    "numeric"
  ),
  (
    "Other Staff: American Indian",
    4,
    "numeric"
  ),
  (
    "Other Staff: Black",
    4,
    "numeric"
  ),
  (
    "Other Staff: Asian American",
    4,
    "numeric"
  ),
  (
    "Other Staff: Spanish Surname",
    4,
    "numeric"
  ),
    (
    "Other Staff: Other",
    4,
    "numeric"
  ),
  (
    "Other Staff: Total",
    4,
    "numeric"
  ),
  (
    "Filler",
    32,
    "skip"
  ),
  (
    "Pupils Bused",
    4,
    "numeric"
  ),
  (
    "Departmentalized English (Yes = 1)",
    4,
    "numeric"
  ),
  (
    "School Street",
    32,
    "literal"
  ),
  (
    "School City",
    16,
    "literal"
  ),
  (
    "School County",
    32,
    "literal"
  ),
  (
    "School Zip Code",
    4,
    "literal"
  ),
  (
    "Grade 3: American Indian",
    4,
    "numeric"
  ),
  (
    "Grade 3: Black",
    4,
    "numeric"
  ),
  (
    "Grade 3: Asian American",
    4,
    "numeric"
  ),
  (
    "Grade 3: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Grade 3: Other",
    4,
    "numeric"
  ),
  (
    "Grade 3: Total",
    4,
    "numeric"
  ),
  (
    "Grade 6: American Indian",
    4,
    "numeric"
  ),
  (
    "Grade 6: Black",
    4,
    "numeric"
  ),
  (
    "Grade 6: Asian American",
    4,
    "numeric"
  ),
  (
    "Grade 6: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Grade 6: Other",
    4,
    "numeric"
  ),
  (
    "Grade 6: Total",
    4,
    "numeric"
  ),
  (
    "Grade 9: American Indian",
    4,
    "numeric"
  ),
    (
    "Grade 9: Black",
    4,
    "numeric"
  ),
  (
    "Grade 9: Asian American",
    4,
    "numeric"
  ),
  (
    "Grade 9: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Grade 9: Other",
    4,
    "numeric"
  ),
  (
    "Grade 9: Total",
    4,
    "numeric"
  ),
  (
    "Lowest Grade Offered",
    4,
    "numeric"
  ),
  (
    "American Indian in Lowest Grade",
    4,
    "numeric"
  ),
  (
    "Black in Lowest Grade",
    4,
    "numeric"
  ),
  (
    "Asian American in Lowest Grade",
    4,
    "numeric"
  ),
  (
    "Spanish Surname in Lowest Grade",
    4,
    "numeric"
  ),
  (
    "Other in Lowest Grade",
    4,
    "numeric"
  ),
  (
    "Total in Lowest Grade",
    4,
    "numeric"
  ),
  (
    "New Staff: American Indian",
    4,
    "numeric"
  ),
  (
    "New Staff: Black",
    4,
    "numeric"
  ),
  (
    "New Staff: Asian American",
    4,
    "numeric"
  ),
  (
    "New Staff: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "New Staff: Other",
    4,
    "numeric"
  ),
  (
    "New Staff: Total",
    4,
    "numeric"
  ),
  (
    "Lunch Program Offered (Yes = 1)",
    4,
    "numeric"
  ),
  (
    "Participants in Lunch Program: American Indian",
    4,
    "numeric"
  ),
  (
    "Participants in Lunch Program: Black",
    4,
    "numeric"
  ),
  (
    "Participants in Lunch Program: Asian American",
    4,
    "numeric"
  ),
    (
    "Participants in Lunch Program: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Participants in Lunch Program: Other",
    4,
    "numeric"
  ),
  (
    "Participants in Lunch Program: Total",
    4,
    "numeric"
  ),
  (
    "Eligible for Lunch Program: Am. Indian",
    4,
    "numeric"
  ),
  (
    "Eligible for Lunch Program: Black",
    4,
    "numeric"
  ),
  (
    "Eligible for Lunch Program: Asian American",
    4,
    "numeric"
  ),
  (
    "Eligible for Lunch Program: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Eligible for Lunch Program: Other",
    4,
    "numeric"
  ),
  (
    "Eligible for Lunch Program: Total",
    4,
    "numeric"
  ),
  (
    "Receiving Lunch Program: American Indian",
    4,
    "numeric"
  ),
  (
    "Receiving Lunch Program: Black",
    4,
    "numeric"
  ),
  (
    "Receiving Lunch Program: Asian American",
    4,
    "numeric"
  ),
  (
    "Receiving Lunch Program: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Receiving Lunch Program: Other",
    4,
    "numeric"
  ),
  (
    "Receiving Lunch Program: Total",
    4,
    "numeric"
  ),
  (
    "Elementary Teachers: American Indian",
    4,
    "numeric"
  ),
  (
    "Elementary Teachers: Black",
    4,
    "numeric"
  ),
  (
    "Elementary Teachers: Asian American",
    4,
    "numeric"
  ),
  (
    "Elementary Teachers: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Elementary Teachers: Other",
    4,
    "numeric"
  ),
  (
    "Elementary Teachers: Total",
    4,
    "numeric"
  ),
  (
    "Secondary Teachers: American Indian",
    4,
    "numeric"
  ),
    (
    "Secondary Teachers: Black",
    4,
    "numeric"
  ),
  (
    "Secondary Teachers: Asian American",
    4,
    "numeric"
  ),
  (
    "Secondary Teachers: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Secondary Teachers: Other",
    4,
    "numeric"
  ),
  (
    "Secondary Teachers: Total",
    4,
    "numeric"
  ),
  (
    "Other Teachers: American Indian",
    4,
    "numeric"
  ),
  (
    "Other Teachers: Black",
    4,
    "numeric"
  ),
  (
    "Other Teachers: Asian American",
    4,
    "numeric"
  ),
  (
    "Other Teachers: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Other Teachers: Other",
    4,
    "numeric"
  ),
  (
    "Other Teachers: Total",
    4,
    "numeric"
  ),
  (
    "# Sections in Lowest Grade: 0-19%",
    4,
    "numeric"
  ),
  (
    "# Sections in Lowest Grade: 20-49%",
    4,
    "numeric"
  ),
  (
    "# Sections in Lowest Grade: 50-79%",
    4,
    "numeric"
  ),
  (
    "# Sections in Lowest Grade: 80-100%",
    4,
    "numeric"
  ),
  (
    "1970 OE Code",
    4,
    "numeric"
  )
]

# --- NEW: Classroom Schema Definition ---
CLASSROOM_SCHEMA = [
  (
    "OE School System Code",
    4,
    "numeric"
  ),
  (
    "School Code",
    4,
    "numeric"
  ),
  (
    "Grade Level",
    4,
    "numeric"
  ),
  (
    "Classroom Code",
    4,
    "numeric"
  ),
  (
    "Section Pupils: American Indian",
    4,
    "numeric"
  ),
  (
    "Section Pupils: Black",
    4,
    "numeric"
  ),
  (
    "Section Pupils: Asian American",
    4,
    "numeric"
  ),
  (
    "Section Pupils: Spanish Surname",
    4,
    "numeric"
  ),
  (
    "Section Pupils: Other",
    4,
    "numeric"
  )
]


SYSTEM_BLOCK_SIZE = 468
SCHOOL_BLOCK_SIZE = 712
CLASSROOM_BLOCK_SIZE = 36


def parse_record(byte_block, schema):
    record = {}
    pos = 0
    for field_name, size, field_type in schema:
        if pos + size > len(byte_block):
            print(f"⚠️ Warning: Incomplete data block. Stopping parse for this record.")
            break
        chunk = byte_block[pos : pos + size]
        if field_type == "literal":
            record[field_name] = chunk.decode("cp037", errors="replace").strip()
        elif field_type == "numeric":
            record[field_name] = int.from_bytes(chunk, "big")
        pos += size
    return record


def process_file(filepath, out_systems_csv="systems.csv", out_schools_csv="schools.csv", out_classrooms_csv="classrooms.csv"):
    try:
        data = Path(filepath).read_bytes()
    except FileNotFoundError:
        print(f"❌ Error: File not found at '{filepath}'")
        return

    SYSTEM_MARKER = b'\x00\x00\x00\x01'
    SCHOOL_MARKER = b'\x00\x00\x00\x02'
    CLASSROOM_MARKER = b'\x00\x00\x00\x03'
    MARKER_SIZE = 4

    systems_data = []
    schools_data = []
    classrooms_data = []
    
    system_key_counter = 0
    current_system_key = None

    pos = 0
    while pos < len(data):
        pos_sys = data.find(SYSTEM_MARKER, pos)
        pos_sch = data.find(SCHOOL_MARKER, pos)
        pos_cls = data.find(CLASSROOM_MARKER, pos)

        positions = [p for p in [pos_sys, pos_sch, pos_cls] if p != -1]
        if not positions:
            break
        
        next_marker_pos = min(positions)
        marker = data[next_marker_pos : next_marker_pos + MARKER_SIZE]
        record_start = next_marker_pos + MARKER_SIZE

        if marker == SYSTEM_MARKER:
            print(f"Found System record at offset {next_marker_pos}")
            block_bytes = data[record_start : record_start + SYSTEM_BLOCK_SIZE]
            system_record = parse_record(block_bytes, SYSTEM_SCHEMA)
            
            system_key_counter += 1
            current_system_key = system_key_counter
            system_record['key'] = current_system_key
            systems_data.append(system_record)
            
            pos = record_start + SYSTEM_BLOCK_SIZE

        elif marker == SCHOOL_MARKER:
            print(f"Found School record at offset {next_marker_pos}")
            block_bytes = data[record_start : record_start + SCHOOL_BLOCK_SIZE]
            school_record = parse_record(block_bytes, SCHOOL_SCHEMA)
            
            if current_system_key is not None:
                school_record['key'] = current_system_key
                schools_data.append(school_record)
            else:
                print(f"⚠️ Warning: Found school record at {next_marker_pos} before any system record. Skipping.")

            pos = record_start + SCHOOL_BLOCK_SIZE
        
        elif marker == CLASSROOM_MARKER:
            print(f"Found Classroom record at offset {next_marker_pos}")
            block_bytes = data[record_start : record_start + CLASSROOM_BLOCK_SIZE]
            classroom_record = parse_record(block_bytes, CLASSROOM_SCHEMA)

            if current_system_key is not None:
                classroom_record['key'] = current_system_key
                classrooms_data.append(classroom_record)
            else:
                print(f"⚠️ Warning: Found classroom record at {next_marker_pos} before any system record. Skipping.")
            
            pos = record_start + CLASSROOM_BLOCK_SIZE

        else:
            pos = next_marker_pos + MARKER_SIZE

    if systems_data:
        system_fieldnames = ['key'] + [f[0] for f in SYSTEM_SCHEMA if f[2] != 'skip']
        with open(out_systems_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=system_fieldnames)
            writer.writeheader()
            writer.writerows(systems_data)
        print(f"\n✅ Saved {len(systems_data)} systems to {out_systems_csv}")

    if schools_data:
        school_fieldnames = ['key'] + [f[0] for f in SCHOOL_SCHEMA if f[2] != 'skip']
        with open(out_schools_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=school_fieldnames)
            writer.writeheader()
            writer.writerows(schools_data)
        print(f"✅ Saved {len(schools_data)} schools to {out_schools_csv}")

    if classrooms_data:
        classroom_fieldnames = ['key'] + [f[0] for f in CLASSROOM_SCHEMA if f[2] != 'skip']
        with open(out_classrooms_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=classroom_fieldnames)
            writer.writeheader()
            writer.writerows(classrooms_data)
        print(f"✅ Saved {len(classrooms_data)} classrooms to {out_classrooms_csv}")


#Run the parser
process_file("RG441.ESS.CVRGY72")