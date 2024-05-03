import pandas as pd

PATHWAY_2B_ADDED = 'OVC'

# Load the CSV file to see its structure
csv_file_path = 'cosb.csv'
current_courses_df = pd.read_csv(csv_file_path)
print(current_courses_df.head())

course_numbers = [
    "ACCT-1302", "ACCT-1341", "ANTH-3465", "ANTH-3488", "ART-2470", "ART-2471", 
    "ART-3314", "ART-3471", "ART-3480", "ARTH-3425", "ARTH-3442", "ARTH-3493", 
    "BAT-3394", "BIOL-3426", "BIOL-3457", "BUSN-3311", "BUSN-3314", "BUSN-3461", 
    "CHEM-4346", "CHEM-4347", "CHEM-4360", "CHIN-3412", "CHIN-3414", "CLAC-3346", 
    "CLAS-1319", "CLAS-2359", "CLAS-2406", "CLAS-3338", "COMM-1301", "COMM-3342", 
    "COMM-3442", "CSCI-3321", "EAST-2421", "ECON-3346", "ECON-3439", "EDUC-1431", 
    "EDUC-2204", "EDUC-2205", "EDUC-3410", "ENGL-3347", "ENGL-3473", "ENGR-2309", 
    "ENGR-4381", "ENTR-1442", "ENVI-3410", "GEOS-1403", "GEOS-1407", "GEOS-3422", 
    "GEOS-4420", "GERM-3402", "GNED-3321", "GRST-3315", "GRST-3435", "HCOM-1433", 
    "HCOM-3362", "HCOM-3434", "HIST-3461", "HIST-3467", "HIST-3468", "HRM-4382", 
    "HRM-4390", "INTB-3346", "MATH-3310", "MATH-4394", "MGMT-4382", "MUSC-1343", 
    "MUSC-1345", "MUSC-1347", "MUSC-4321", "NEUR-3457", "NEUR-4360", "PHYS-3194", 
    "PLSI-2150", "PLSI-3434", "PLSI-3435", "PSYC-3368", "RELI-2355", "RELI-2359", 
    "RELI-2371", "RELI-3338", "RELI-3445", "RELI-3446", "RELI-3457", "RELI-4494", 
    "RUSS-3302", "SOCI-3465", "SPAN-3346", "SPAN-3421", "SPAN-3422", "SPAN-3441", 
    "SPAN-3442", "SPMT-2301", "SPMT-3316", "THTR-1442", "THTR-2310", "THTR-2312", 
    "THTR-2313", "THTR-3412", "THTR-3413", "THTR-3436", "THTR-3480", "URBS-3465"
]

new_rows = []
for course in course_numbers:
    course_number = course
    if course_number in current_courses_df['number'].values:
        idx = current_courses_df[current_courses_df['number'] == course_number].index[0]
        existing_pathway = current_courses_df.at[idx, 'pathway']
        if pd.isna(existing_pathway):
            current_courses_df.at[idx, 'pathway'] = PATHWAY_2B_ADDED
        else:
            current_courses_df.at[idx, 'pathway'] = str(existing_pathway) + '-' + PATHWAY_2B_ADDED
    else:
        new_row = {
            'number': course_number,
            'coursename': course.replace('-', ' '),
            'description': '',
            'prereq': '',
            'pathway': PATHWAY_2B_ADDED
        }
        new_rows.append(new_row)


if new_rows:
    new_courses_df = pd.DataFrame(new_rows)
    current_courses_df = pd.concat([current_courses_df, new_courses_df], ignore_index=True)


final_updated_csv_path = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.csv'
current_courses_df.to_csv(final_updated_csv_path, index=False)
print(final_updated_csv_path)
