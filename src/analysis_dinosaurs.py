from helpers.config import config_paths
import pandas as pd
from os.path import join
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.offline import plot

#--------------------------------------------------
# load data

dinosaurs = pd.read_csv(
    join(
        config_paths().get("data_path"),
        "dinosaurs.csv"
    )
)

#--------------------------------------------------
# Questions to address

# 1. How many different dinosaur names are present in the data?
# 2. Which was the largest dinosaur? What about missing data in the dataset?
# 3. What dinosaur type has the most occurrences in this dataset? Create a visualization (table, bar chart, or equivalent) to display the number of dinosaurs per type. Use the AI assistant to tweak your visualization (colors, labels, title...).
# 4. Did dinosaurs get bigger over time? Show the relation between the dinosaur length and their age to illustrate this.
# 5. Use the AI assitant to create an interactive map showing each record. 
# 6. Any other insights you found during your analysis?

#--------------------------------------------------
# Question 1:
# How many different dinosaur names are present in the data?
#--------------------------------------------------

# Mere number of different dinosaurs
n_dinos = dinosaurs["name"].nunique()
print(f"There are {n_dinos} in the data.")

#--------------------------------------------------
# plot the number of dinosaurs by diet

diet_count = dinosaurs.groupby(["diet"]).size().reset_index()
print(diet_count)
print(dinosaurs["diet"].isna().sum())

# customize the colors of the bars
pal = {
    "carnivorous": "#AE415E",
    "herbivorous": "#2D793E",
    "omnivorous": "#2D4279"
}

diet_plot = sns.catplot(
    x = "diet",
    kind = "count",
    palette = pal,
    data = dinosaurs 
)

# extract x labels and capitalize them
xlab = [item.get_text().capitalize() for item in diet_plot.ax.get_xticklabels()]
diet_plot.ax.set_xticklabels(xlab)

# set axis title
diet_plot.ax.set(xlabel = "Diet", ylabel = "Count")

# export figure
diet_plot.savefig(
    join(
        config_paths().get("output_path"),
        "graphs",
        "diet_count.png"
    ),
    dpi = 400,
    bbox_inches = "tight"
)

# Surprisingly, relatively few dinosaurs are omnivorous, i.e., consume plants
# and animals.

#--------------------------------------------------
# Question 2:
# Which was the largest dinosaur? What about missing data in the dataset?
#--------------------------------------------------

max_length = dinosaurs["length_m"].max()

largest_dinosaur = dinosaurs[
    dinosaurs["length_m"] == max_length
]["name"].unique()

for name in largest_dinosaur:
    print(name)
    
    
# Answer: There are actually 2 dinosaurs that can claim the title of the largest
# dinosaur: Supersaurus and Argentinosaurus. Both are recorded with a maximum
# length of 35 meters (from head to tail). This, of course, only holds for the
# recorded dinosaurs (see below with respect to missing information).

#--------------------------------------------------
# plot the distribution of size

displot = sns.displot(
    x = "length_m",
    kind = "kde",
    data = dinosaurs
)

displot.set(xlabel = "Length (in m)")

displot.figure.savefig(
    join(
        config_paths().get("output_path"),
        "graphs",
        "length_distribution.png"
    ),
    dpi = 400,
    bbox_inches = "tight"
)

#--------------------------------------------------
# What about missing data?

missing_lengths = dinosaurs[dinosaurs["length_m"].isna()]
missing_lengths_count = missing_lengths["name"].nunique()
missing_lengths_perc = (missing_lengths_count / n_dinos) * 100

print(
    f"""
    There are {missing_lengths_count} or {round(missing_lengths_perc, 1)}%
    dinosaurs for which no length was recorded.
    """
)

# Answer: With 72% of the dinosaurs having no length information, it could be
# that the largest dinosaurs is actually not recorded, i.e. has missing information.

# Another issue is sample selection. The data set only contains the recorded,
# i.e. the discovered fossils. It is possible that the largest dinosaur has not
# been discovered yet.

#--------------------------------------------------
# Question 3:
# What dinosaur type has the most occurrences in this dataset?
#--------------------------------------------------

count_type = dinosaurs.groupby(["type"]).size().sort_values(ascending = False).reset_index()

print(
    f"""
    The most common dinosaur type in the data set is {count_type.iloc[0, 0].capitalize()}.
    """
)

#--------------------------------------------------
# visualization

type_plot = sns.catplot(
    x = "type",
    kind = "count",
    order = count_type["type"],
    data = dinosaurs    
)

# define axis titles
type_plot.ax.set(xlabel = "Type", ylabel = "Count")

# rotate x-labels
type_plot.set_xticklabels(rotation = 90)

# capitalize x labels
xlab = [item.get_text().capitalize() for item in type_plot.ax.get_xticklabels()]
type_plot.ax.set_xticklabels(xlab)

# export
type_plot.savefig(
    join(
        config_paths().get("output_path"),
        "graphs",
        "type_count.png"
    ),
    dpi = 400,
    bbox_inches = "tight"
)

#--------------------------------------------------
# Question 4:
# Did dinosaurs get bigger over time? Show the relation between the dinosaur length and their age to illustrate this.
#--------------------------------------------------

dinosaurs["age"] = dinosaurs["max_ma"] - dinosaurs["min_ma"]

age_plot = sns.regplot(
    x = "age",
    y = "length_m",
    ci = None,
    scatter_kws = {"alpha": 0.5, "color": "black"},
    line_kws = {"color": "blue"},
    data = dinosaurs
)

# set axis titles
age_plot.set(xlabel = "Age (in million years)", ylabel = "Length (in meters)")

# export
age_plot.get_figure().savefig(
    join(
        config_paths().get("output_path"),
        "graphs",
        "age_plot.png"
    ),
    dpi = 400,
    bbox_inches = "tight"
)

# There is a decreasing relationship between the age of the fossil and the
# its length.

#--------------------------------------------------
# Question 5:
# Interactive map of records
#--------------------------------------------------

interactive_map = px.scatter_geo(
    dinosaurs,
    lat = "lat",
    lon = "lng",
    hover_name = "occurrence_no",
    color = "length_m",
    labels={"length_m": "Length (in m)"}
)

interactive_map.update_geos(
    projection_type = "natural earth"
)

# show map
plot(interactive_map)

# export
interactive_map.write_html(
    join(
        config_paths().get("output_path"),
        "graphs",
        "interactive_fossil_length_map.html"
    )
)

#--------------------------------------------------
# Question 6:
# Any other insights you found during your analysis?
#--------------------------------------------------

boxplot = sns.boxplot(
    x = "diet",
    y = "length_m",
    data = dinosaurs
)

# define axis titles
boxplot.set(xlabel = "Diet", ylabel = "Length (in m)")

# capitalize x labels
xlab = [item.get_text().capitalize() for item in boxplot.get_xticklabels()]
boxplot.set_xticklabels(xlab)

# export
boxplot.figure.savefig(
    join(
        config_paths().get("output_path"),
        "graphs",
        "diet_boxplot.png"
    ),
    dpi = 400,
    bbox_inches = "tight"
)

# Herbivorous dinosaurs seem to be larger than the other dinosaur types. Their
# median length, as well as Q1 and Q3, are larger than those of carnivorous and
# omnivorous dinosaurs. This is interesting because a plant-based diet is harder
# to process and provides less energy. So herbivorous dinosaurs have to eat a
# lot more (in volume) to get that big. Carnivorous dinosaurs have an advantage
# in this category. However, plants are widely available compared to meat, so
# they can be easily consumed, so eating large amounts is not a challenge.
