# Get data from ExploreCourses API
Python parse_EC_API.py 20162017 > ../ec_data/output_20162017.txt
Python parse_EC_API.py 20152016 > ../ec_data/output_20152016.txt
Python parse_EC_API.py 20142015 > ../ec_data/output_20142015.txt
Python parse_EC_API.py 20132014 > ../ec_data/output_20132014.txt
Python parse_EC_API.py 20122013 > ../ec_data/output_20122013.txt
Python parse_EC_API.py 20112012 > ../ec_data/output_20112012.txt
cat ../ec_data/output_20112012.txt > ../ec_data/output_allcourses.txt
tail -n +2 ../ec_data/output_20122013.txt >> ../ec_data/output_allcourses.txt
tail -n +2 ../ec_data/output_20132014.txt >> ../ec_data/output_allcourses.txt
tail -n +2 ../ec_data/output_20142015.txt >> ../ec_data/output_allcourses.txt
tail -n +2 ../ec_data/output_20152016.txt >> ../ec_data/output_allcourses.txt
tail -n +2 ../ec_data/output_20162017.txt >> ../ec_data/output_allcourses.txt

# Delete entries for which schedule is None (NA)
awk -F "\t" '{if ($16 != "None" && $17 != "None" && $18 != "None") print}' ../ec_data/output_allcourses.txt > ../ec_data/output_courses_w_times.txt

# Make course ID dictionary:
cat ../ec_data/output_allcourses.txt | Python make_course_dicts.py

# To recreate prereqs.json:
cd /Users/kennethqin/Documents/Stanford\ Coterm\ Year/ICME\ Research/pathways_project/edusalsa/stanfordreq-master
python stanfordreq.py ../explorecourses_20152016.json ../../dict/prereqs_20152016.json

# Make NESTED prereq dictionary that takes into account ‘and’/‘or’ structure:
cd /Users/kennethqin/Documents/Stanford\ Coterm\ Year/ICME\ Research/pathways_project/python_scripts
cat ../dict/prereqs_20152016.json | Python make_req_dict_nested.py
# Output has been hard-coded to be ‘req_dict_nested.json’
# Each key corresponds to a course
# The 1st value is the list of the course prereqs; 
# the 2nd value is the list of the course coreqs

# To reformat a manually-typed .txt file of degree requirements (such as 
# reqs_geophysics0.txt) into a JSON for easy manipulation, use format_reqs_json.py:
python format_reqs_json.py ../degree_reqs/geophysics/reqs_geophysics0.txt ../degree_reqs/geophysics/reqs_geophysics.json

# To get all relevant courses for a degree program (including prerequisites),
# run a manually-typed .txt file of degree requirements (such as
# reqs_geophysics0.txt) through relevant_courses.py:
python relevant_courses.py ../degree_reqs/geophysics/reqs_geophysics0.txt ../ec_data/relevant_courses/rc_geophysics.txt

# To parse the JSON file representing degree requirements into a Constraint-
# class object
#Python parse_reqs_to_constraint.py '../degree_reqs/json/reqs_geophysics_name.json'
# Made OBSOLETE due to integration of constraint module in print_pathways.py (see below)

# Test use of new ‘constraint’ module in print_pathways.py:

python print_pathways.py ../degree_reqs/geophysics/reqs_geophysics0_sub.txt 2012 6 6 'MATH 51, MATH 20, MATH 21, MATH 41, MATH 42, MATH 52, MATH 19, PHYSICS 41' 

python print_pathways.py ../degree_reqs/geophysics/reqs_geophysics0_sub.txt 2012 6 6 ’MATH 51, MATH 20, MATH 21, MATH 41, MATH 42, MATH 52, MATH 19, PHYSICS 41' | awk -F '\t' '$5 == "True" {print $4}'

python print_pathways.py ../degree_reqs/ecoevo/reqs_ecoevo_sub.txt 2012 6 6 'MATH 19, MATH 20, MATH 21, MATH 41, MATH 42, PHYSICS 41, CHEM 31X, CHEM 33' | python post_print_pathways.py > ../out_pathways/pathways_ecoevo_sub.txt

python print_pathways.py ../degree_reqs/ecoevo/reqs_ecoevo.txt 2012 3 3 'MATH 19, MATH 20, MATH 21, MATH 41, MATH 42, PHYSICS 41, CHEM 31X, CHEM 33, BIO 41, BIO 42, BIO 43' | python post_print_pathways.py > ../out_pathways/pathways_ecoevo.txt


# Here are some good prereqs to assume in course history:
'MATH 19, MATH 20, MATH 21, MATH 41, MATH 42, PHYSICS 41, CHEM 31A, CHEM 31B, CHEM 33’

# Get the length of a prereq chain
# Enter anything as 2nd arg for verbose
Python len_prereq_chain.py 'BIO 41' d
Python len_prereq_chain.py 'ECON 52' d
Python len_prereq_chain.py 'MATH 104' d

# Get minimum prereq chain length of a degree program (or any other JSON representing constraints)
python len_prereq_chain_fromjson.py '../degree_reqs/ecoevo/reqs_ecoevo_sub.json'

# Used R script to create course term_id lookup table
# Hard-coded as “ec_data/Course_terms.txt”
Rscript ../create_course_term_lookup.R

# Convert the course term_id lookup table into JSON file
cat ../ec_data/Course_terms.txt | python course_terms_txt2json.py ../ec_data/Course_terms.json
