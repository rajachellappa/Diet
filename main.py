# Importing 'pandas' for importing excel data as dictionary and PulP for
# the LP Solver routines
import pandas as pd
from pulp import *
# Import relevant excel data (in same directory)
diet = pd.read_excel('diet.xls', nrows=64)
# I found it easier to create a manual dictionary due to asymmetry in the data
# presentation in the excel file. Also iloc method is easier compared to loc
# method due to the naming. We exclude Serving Size column which is not needed
# for this problem
food_names = list(diet.iloc[:,0])
costs = dict(zip(food_names,diet.iloc[:,1]))
calories = dict(zip(food_names,diet.iloc[:,3]))
cholestrol = dict(zip(food_names,diet.iloc[:,4]))
total_fat = dict(zip(food_names,diet.iloc[:,5]))
sodium = dict(zip(food_names,diet.iloc[:,6]))
carb = dict(zip(food_names,diet.iloc[:,7]))
fiber = dict(zip(food_names,diet.iloc[:,8]))
protein = dict(zip(food_names,diet.iloc[:,9]))
vit_A = dict(zip(food_names,diet.iloc[:,10]))
vit_C = dict(zip(food_names,diet.iloc[:,11]))
calcium = dict(zip(food_names,diet.iloc[:,12]))
iron = dict(zip(food_names,diet.iloc[:,13]))
# Define the LP problem called "Diet LP Problem" for minimizing cost subject
# to daily intake bounds
diet_lp = LpProblem("Diet LP Problem", LpMinimize)
# Bound for the food serving amount >= 0
food_variables = LpVariable.dicts("Food", food_names, lowBound=0)
# We now include the additional constraints for the second part of the question
chosen_food_vars = LpVariable.dicts("ChosenFood", food_names, lowBound=0, upBound=1, cat = "Binary")
# Objective Function is the summation of costs[i]*food_variables[i]
diet_lp += lpSum([costs[i]*food_variables[i] for i in food_names]), "TotalCost"
# Constraints are given in Rows 67 & 68 of the excel file
diet_lp += lpSum([calories[i]*food_variables[i] for i in food_names]) >= 1500, "MinCalories"
diet_lp += lpSum([calories[i]*food_variables[i] for i in food_names]) <= 2500, "MaxCalories"
diet_lp += lpSum([cholestrol[i]*food_variables[i] for i in food_names]) >= 30, "MinCholestrol"
diet_lp += lpSum([cholestrol[i]*food_variables[i] for i in food_names]) <= 240, "MaxCholestrol"
diet_lp += lpSum([total_fat[i]*food_variables[i] for i in food_names]) >= 20, "MinFat"
diet_lp += lpSum([total_fat[i]*food_variables[i] for i in food_names]) <= 70, "MaxFat"
diet_lp += lpSum([sodium[i]*food_variables[i] for i in food_names]) >= 800, "MinSodium"
diet_lp += lpSum([sodium[i]*food_variables[i] for i in food_names]) <= 2000, "MaxSodium"
diet_lp += lpSum([carb[i]*food_variables[i] for i in food_names]) >= 130, "MinCarb"
diet_lp += lpSum([carb[i]*food_variables[i] for i in food_names]) <= 450, "MaxCarb"
diet_lp += lpSum([fiber[i]*food_variables[i] for i in food_names]) >= 125, "MinFiber"
diet_lp += lpSum([fiber[i]*food_variables[i] for i in food_names]) <= 250, "MaxFiber"
diet_lp += lpSum([protein[i]*food_variables[i] for i in food_names]) >= 60, "MinProtein"
diet_lp += lpSum([protein[i]*food_variables[i] for i in food_names]) <= 100, "MaxProtein"
diet_lp += lpSum([vit_A[i]*food_variables[i] for i in food_names]) >= 1000, "MinVitaminA"
diet_lp += lpSum([vit_A[i]*food_variables[i] for i in food_names]) <= 10000, "MaxVitaminA"
diet_lp += lpSum([vit_C[i]*food_variables[i] for i in food_names]) >= 400, "MinVitaminC"
diet_lp += lpSum([vit_C[i]*food_variables[i] for i in food_names]) <= 5000, "MaxVitaminC"
diet_lp += lpSum([calcium[i]*food_variables[i] for i in food_names]) >= 700, "MinCalcium"
diet_lp += lpSum([calcium[i]*food_variables[i] for i in food_names]) <= 1500, "MaxCalcium"
diet_lp += lpSum([iron[i]*food_variables[i] for i in food_names]) >= 10, "MinIron"
diet_lp += lpSum([iron[i]*food_variables[i] for i in food_names]) <= 40, "MaxIron"
# (a) Additional Variable for Chosen Food (binary) with a chosen food must be
# atleast 0.1 serving and that it must always be eaten (10^9 multiplier arbitrary)
for i in food_names:
    diet_lp += food_variables[i] >= (.1)*chosen_food_vars[i]
    diet_lp += food_variables[i] <= (1000000000)*chosen_food_vars[i]
# (b) Choose either Celery or Frozen Broccoli. Note that the food names have been
# passed as argument while defining the chosen food variable
diet_lp += chosen_food_vars['Frozen Broccoli'] + chosen_food_vars['Celery, Raw'] <=1
# (c) Choose atleast 3 kinds of meat/poultry/egg. This can be selected using the
# food names
diet_lp += chosen_food_vars['Roasted Chicken'] + chosen_food_vars['Poached Eggs'] \
+ chosen_food_vars['Scrambled Eggs']+ chosen_food_vars['Bologna,Turkey'] \
+ chosen_food_vars['Frankfurter, Beef']+ chosen_food_vars['Ham,Sliced,Extralean'] \
+ chosen_food_vars['Kielbasa,Prk']+ chosen_food_vars['Pizza W/Pepperoni'] \
+ chosen_food_vars['Hamburger W/Toppings']+ chosen_food_vars['Hotdog, Plain'] \
+ chosen_food_vars['Pork']+ chosen_food_vars['Sardines in Oil'] \
+ chosen_food_vars['White Tuna in Water']+ chosen_food_vars['Chicknoodl Soup'] \
+ chosen_food_vars['Vegetbeef Soup']+ chosen_food_vars['Neweng Clamchwd'] \
+ chosen_food_vars['New E Clamchwd,W/Mlk']+ chosen_food_vars['Beanbacn Soup,W/Watr'] >= 3
diet_lp.solve()
print(LpStatus[diet_lp.status])
# We can now loop through the solution using the varValue method to retrieve
# variables with non-zero coefficients
for var in diet_lp.variables():
    if var.varValue>0:
        print("{} = {}".format(var.name, var.varValue))
# We also print out the Total Cost
        print(value(diet_lp.objective))
