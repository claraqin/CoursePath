
# I. Introduction #

## 1. Premise ##

*How many different paths can I possibly take to fulfill my degree requirements in time, and what would these paths look like?*

Every academic year, hundreds of first-year undergraduates at Stanford refer to the Bulletin, Stanford’s course catalog, to create their own ideal four-year plan. While this planning process may help students to gauge how much flexibility is allowed by their academic goals, many students come to realize that the plan itself is highly speculative. Because the times and availabilities of course offerings are subject to change year after year, it can be difficult to plan ahead - at least past the current academic year. In particular, there is a risk that a student who planned their courses meticulously may nonetheless fail to complete their degree requirements in time. Perhaps they were counting on a course being offered in a particular quarter, or perhaps the department’s requirements became unintentionally restrictive.

In hindsight, it is possible to assess the difficulty of completing a degree program given a set of constraints, based on publicly-available data from the Stanford Bulletin’s archives and associated websites (e.g. exploredegrees.stanford.edu and explorecourses.stanford.edu). With this information, we can identify all of the paths that were available to a student at any point in their undergraduate career, and note potential pitfalls and bottlenecks. Therefore, the goal of this project is not to predict the future; instead, the goal is to explore the full range of course paths that were allowed under a set of existing degree requirements, and in doing so, to inform broad-scale education initiatives at Stanford University.

## 2. Features ##

This project has two features that are in the process of being integrated:

1. An exhaustive search of all possible ways to successfully complete a given set of degree requirements - the output of which produces a summary chart.

2. A function that returns the length of a *prerequisite chain* - that is, the number of courses that must precede any given course, based on the pre/corequisites listed in the descriptions of the 2015-2016 ExploreCourses course descriptions.

## 3. Data Sources ##

All data used in this project is publicly available from the Stanford Bulletin and its archives:
* exploredegrees.stanford.edu
* exploredegrees.stanford.edu/archive/
* explorecourses.stanford.edu

## 4. Data Collection ##

### (a) ExploreCourses

See Appendix for details on data collection from ExploreCourses.

### (b) ExploreDegrees

Degree requirements must be manually entered based on the information provided on ExploreDegrees. For example, here is reqs_ecoevo_sub.txt, which includes a subset of the requirements for the Ecology and Evolution concentration of the Biology major.


```bash
%%bash
cat ../degree_reqs/ecoevo/reqs_ecoevo_sub.txt
```

    And[
    	BIO 41
    	BIO 42
    	Or[
    		BIO 43
    		BIOHOPK 43
    	]
    	Or[
    		BIO 101
    		BIOHOPK 172H
    	]
    	Or[
    		BIO 44X
    		BIO 44Y
    		BIOHOPK 44Y
    	]
    	Or[
    		And[
    			CHEM 31A
    			CHEM 31B
    		]
    		CHEM 31X
    	]
    	Or[
    		CHEM 33
    		CHEM 1
    	]
    	Or[
    		CHEM 35
    		CHEM 2
    	]
    ]


# II. CoursePath Analysis #

## 1. Dictionaries ##

Before the CoursePath analysis could begin, it was necessary to use the collected data to create two dictionaries; one to efficiently check course prerequisites, and another to encode courses by their unique course IDs.

### (a) Course prerequisites dictionary


```bash
%%bash

# Parse prereqs from 2015-2016 ExploreCourses API output
cd /Users/kennethqin/Documents/Stanford\ Coterm\ Year/ICME\ Research/pathways_project/edusalsa/stanfordreq-master
python stanfordreq.py ../explorecourses_20152016.json ../../dict/prereqs_20152016.json

# Make nested prerequisite dictionary that takes into account "and"/"or" structure
cd /Users/kennethqin/Documents/Stanford\ Coterm\ Year/ICME\ Research/pathways_project/python_scripts
cat ../dict/prereqs_20152016.json | Python make_req_dict_nested.py
```

### (b) Course name-ID dictionaries


```bash
%%bash

cat ../ec_data/output_allcourses.txt | Python make_course_dicts.py
```

## 2. Run Exhaustive Search ##

The exhaustive search behind CoursePath takes in a number of input parameters and returns a list of all possible course paths that may complete a given set of requirements.

Inputs:
    
1. manual_degree_reqs: file path to manually-entered text file of degree requirements (e.g. reqs_ecoevo_sub.txt)
    
2. start_year: year in the ExploreCourses catalogue from which to begin searching
    
3. T: number of quarters (excluding summers) over which to search
    
4. max_courses_per_qtr: max. no. of courses that a student may take in any quarter
    
5. start_path: string to indicate which courses have already been taken before the search begins (e.g. 'MATH 19, MATH 20, MATH 21, MATH 41, MATH 42, PHYSICS 41, CHEM 31X, CHEM 33')

Usage:

    python print_pathways.py [-h] [manual_degree_reqs] [start_year] [T] [max_courses_per_qtr] [start_path]


### Example on the subset of requirements for Ecology & Evolution:

Suppose that we start the 2012-2013 academic year having already taken the following courses:

* MATH 19
* MATH 20
* MATH 21
* MATH 41
* MATH 42
* PHYSICS 41
* CHEM 31X
* CHEM 33

And suppose we want to complete the degree requirements given as an example in section I.4.b, in 6 quarters or fewer, and not including summers. Also, assume that we take no more than 6 courses in any quarter.

The following command will exhaustively search through all course paths with those specifications. The output consists of 5 fields: 

* **t**, the current quarter for which the path has proposed a schedule
* **T**, the maximum number of quarters over which the path searches
* **branch_id**, a unique identifier for each path
* **pathway**, a string of course names, for which courses in the same quarter are separated by ',' and courses in adjacent quarters are separated by '|'
* **True/False**, indicating whether the completed path actually fulfills degree requirements; blank unless t = T.


```bash
%%bash

python print_pathways.py ../degree_reqs/ecoevo/reqs_ecoevo_sub.txt 2012 6 6 'MATH 19, MATH 20, MATH 21, MATH 41, MATH 42, PHYSICS 41, CHEM 31X, CHEM 33' | head
```

    t:0	T:6	branch_id:	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33	
    t:1	T:6	branch_id:.0	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33|	
    t:2	T:6	branch_id:.0.0	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33||	
    t:3	T:6	branch_id:.0.0.0	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33|||	
    t:4	T:6	branch_id:.0.0.0.0	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33||||	
    t:5	T:6	branch_id:.0.0.0.0.0	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33|||||	
    t:6	T:6	branch_id:.0.0.0.0.0.0	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33||||||	False
    t:6	T:6	branch_id:.0.0.0.0.0.1	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33||||||BIO 42	False
    t:5	T:6	branch_id:.0.0.0.0.1	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33|||||CHEM 35	
    t:6	T:6	branch_id:.0.0.0.0.1.0	pathway:MATH 19,MATH 20,MATH 21,MATH 41,MATH 42,PHYSICS 41,CHEM 31X,CHEM 33|||||CHEM 35|	False


    Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>
    BrokenPipeError: [Errno 32] Broken pipe


The raw output is not very informative, because it represents the set of *all* hypothetical course paths that may be realized, *regardless* of whether they actually satisfy degree requirements. We can pipe this through another script to return only those paths that satisfy degree requirements, and then aggregate those paths to generate a cumulative-distribution plot which describes, for each course and each quarter, the proportion of course-realizations that have occurred by then.

The quarter at which a course hits the 100%-mark is the point at which the course becomes a bottleneck to successful degree completion.

*Note: Graph generation only works on Macs with XQuartz installed.*


```bash
%%bash

python print_pathways.py ../degree_reqs/ecoevo/reqs_ecoevo_sub.txt 2012 6 6 'MATH 19, MATH 20, MATH 21, MATH 41, MATH 42, PHYSICS 41, CHEM 31X, CHEM 33' | python post_print_pathways.py > ../out_pathways/pathways_ecoevo_sub.txt

Rscript ../out_pathways/cumdist_pathways.R
```

# III. Length of Prerequisite Chain

A prerequisite chain is a chain of courses that must precede a given course. Often each course's set of prerequisites can be completed in multiple ways (just like a set of degree requirements!). Thus, the length of a prerequisite chain, as defined here, is the **minimum number of courses that must be taken before a given course**.

Let's look at a few examples:


```bash
%%bash
python len_prereq_chain.py 'BIO 41'
```

    2



```bash
%%bash
Python len_prereq_chain.py 'MATH 104'
```

    4



```bash
%%bash
python len_prereq_chain.py 'ECON 52'
```

    2


This process is a little opaque, so if you wanted to know what was happening behind the scenes, simply enter any character at the end of this command to trigger verbosity:


```bash
%%bash
python len_prereq_chain.py 'ECON 52' v
```

    0
    Course: ECON 52	Prereqs: {'And': [{'Takes': 'ECON 50'}]}
    Course: ECON 52	Coreqs: {}
    	1
    	Course: ECON 50	Prereqs: {'And': [{'Or': [{'Takes': 'ECON 1'}, {'Takes': 'ECON 1V'}]}, {'Or': [{'Takes': 'MATH 51'}, {'Takes': 'ENGR 154'}, {'Takes': 'CME 100A'}]}]}
    	Course: ECON 50	Coreqs: {}
    		2
    		Course: ECON 1	Prereqs: {}
    		Course: ECON 1	Coreqs: {}
    		2
    		Course: ECON 1V	Prereqs: {}
    		Course: ECON 1V	Coreqs: {}
    		2
    		Course: MATH 51	Prereqs: {'And': [{'Or': [{'Takes': 'MATH 21'}, {'Takes': 'MATH 42'}]}]}
    		Course: MATH 51	Coreqs: {}
    			3
    			Course: MATH 21	Prereqs: {'And': [{'Or': [{'Takes': 'MATH 20'}]}]}
    			Course: MATH 21	Coreqs: {}
    				4
    				Course: MATH 20	Prereqs: {'And': [{'Or': [{'Takes': 'MATH 19'}]}]}
    				Course: MATH 20	Coreqs: {}
    					5
    					Course: MATH 19	Prereqs: {'And': []}
    					Course: MATH 19	Coreqs: {}
    			3
    			Course: MATH 42	Prereqs: {'And': [{'Or': [{'Takes': 'MATH 41'}]}]}
    			Course: MATH 42	Coreqs: {}
    				4
    				Course: MATH 41	Prereqs: {'And': []}
    				Course: MATH 41	Coreqs: {}
    		2
    		Course: ENGR 154	Prereqs: {'And': [{'Or': [{'Takes': 'MATH 41'}]}]}
    		Course: ENGR 154	Coreqs: {}
    			3
    			Course: MATH 41	Prereqs: {'And': []}
    			Course: MATH 41	Coreqs: {}
    		2
    		Course: CME 100A	Prereqs: {'And': []}
    		Course: CME 100A	Coreqs: {}
    2


# IV. Future Directions

## 1. Integration of the CoursePath and Prerequisite-Chain Length Features

The CoursePath exhaustive search is computationally expensive, and soon becomes intractable with increases in either (i) the number of quarters over which to search or (ii) the number of courses relevant to the degree requirements. So far, it has only been possible to consider subsets of degree requirements over a relatively short period of time.

Part of this shortcoming is due to the forward-search approach employed by the CoursePath analysis. Specifically, the CoursePath analysis runs an exhaustive search by choosing all possible course schedules in quarter 1, then appending all possible subsequent schedules in quarter 2, then appending all possible subsequent schedules in quarter 3, and so on, until quarter *T*. (Well, technically uses a depth-first search, but you get the idea.)

A more efficient approach may involve an extension of the prerequisite-chain feature to search *backwards*. Such an approach may take the following broad steps:

1. Generate all possible course sets (i.e. courses taken by the student) that would satisfy the degree requirements.
2. For each course set, construct a tree that represents the prerequisite-dependencies among the courses in the set. The **constraint.py** module in python_scripts may be useful for this step.
3. For each course set, consider the *primary prerequisites* (made-up name; i.e. the courses that are not prerequisites to any other courses in the set). For each primary prerequisite, list the quarters in the course path where such a course could have been scheduled. (Surely no sooner than the length of the course's prerequisite chain.)
4. Next, for each course set, consider the *secondary prerequisites* (i.e. the courses that are prerequisites to just *one* other course in the set). For each secondary prerequisite, list the quarters in the course path where such a course could have been scheduled.
5. Et cetera, until the entire prerequisite tree has been explored.
6. In the end, you will have generated a list of all possible course paths that satisfy the degree requirements. (Or will you? I'm not sure yet.)

**Notes:**

* This project would require an error-free parsing of the prerequisite structures from the course descriptions in ExploreCourses. Unfortunately, this is the only place where prerequisite information is publicly available, and the descriptions are prone to both typos and non-standard writing formats.
* I would recommend using the **constraint.py** module for this project, as it can be used to encode both degree requirements and course prerequisites. It may even be useful to extend the module to handle cases where one is required to "choose two courses from a menu" - for example.

# V. Appendix

## A. Data Collection from ExploreCourses API


```bash
%%bash

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
```


```bash
%%bash

# Filter only the courses for which a schedule is given
# This is done to filter out courses that are not restrictive to degree completion
awk -F "\t" '{if ($16 != "None" && $17 != "None" && $18 != "None") print}' ../ec_data/output_allcourses.txt > ../ec_data/output_courses_w_times.txt
```
