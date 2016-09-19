# Stanford CoursePath Project


## 1. Premise

*How many different paths can I possibly take to fulfill my degree requirements in time, and what would these paths look like?*

Every academic year, hundreds of first-year undergraduates at Stanford refer to the Bulletin, Stanford’s course catalog, to create their own ideal four-year plan. While this planning process may help students to gauge how much flexibility is allowed by their academic goals, many students come to realize that the plan itself is highly speculative. Because the times and availabilities of course offerings are subject to change year after year, it can be difficult to plan ahead - at least past the current academic year. In particular, there is a risk that a student who planned their courses meticulously may nonetheless fail to complete their degree requirements in time. Perhaps they were counting on a course being offered in a particular quarter, or perhaps the department’s requirements became unintentionally restrictive.

In hindsight, it is possible to assess the difficulty of completing a degree program given a set of constraints, based on publicly-available data from the Stanford Bulletin’s archives and associated websites (e.g. exploredegrees.stanford.edu and explorecourses.stanford.edu). With this information, we can identify all of the paths that were available to a student at any point in their undergraduate career, and note potential pitfalls and bottlenecks. Therefore, the goal of this project is not to predict the future; instead, the goal is to explore the full range of course paths that were allowed under a set of existing degree requirements, and in doing so, to inform broad-scale education initiatives at Stanford University.

## 2. Features

This project has two features that are in the process of being integrated:

1. An exhaustive search of all possible ways to successfully complete a given set of degree requirements - the output of which produces a summary chart.

2. A function that returns the length of a *prerequisite chain* - that is, the number of courses that must precede any given course, based on the pre/corequisites listed in the descriptions of the 2015-2016 ExploreCourses course descriptions.

## 3. Data Sources

All data used in this project is publicly available from the Stanford Bulletin and its archives:
* exploredegrees.stanford.edu
* exploredegrees.stanford.edu/archive/
* explorecourses.stanford.edu

### For detailed description of the analysis, please refer to python_scripts/Stanford_CoursePath_Project.ipynb.