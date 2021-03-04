# Convert ePRTR data to CLRTAP LPS submission

Germany's thru.de website offers the German ePRTR dataset as a SQLITE database. In this repository, we provide means to convert the data given to the LRTAP convention's Excel template format using for large point source (LPS) reporting.
On the way, some additional information is augmented from other sources, in particular stack heights and GNFR categories.

Steps involved:

### 1. Load and transform database content

We start by downloading the database from https://www.thru.de/thrude/downloads/. The database contains a couple of tables, but we are mainly interested in `facilities`, `activities` and `releases`. The `facilities`
table already has the list of point sources we need and offers some properties right away. We can simply grap the names and coordinates, for example. As we only need the most current data, we will also filter on the `year` column.
As we only need the most current data, we will also filter on the year column. Next, we need to match the point source's category (`prtr_id`) and the emissions from the `activities` and `releases` tables respectively.
Note that `releases` has more data than just emissions, so we need to filter for the correct `compartment`.

### 2. Add GNFR and stack height information

We need to map the PRTR activities to their GNFR equivalents and use the information given to derive stack heights.

### 3. Quality check the result

### 4. Write result out as csv

The final list of point sources is then copied to the Excel template as provided by the LRTAP convention. 
