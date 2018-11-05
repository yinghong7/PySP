{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "WARNING: DEPRECATION WARNING: Using the 'Model' class is deprecated.  Please\n",
      "\tuse the AbstractModel or ConcreteModel class instead.\n"
     ]
    }
   ],
   "source": [
    "from coopr.pyomo import *\n",
    "\n",
    "scenario_tree_model = Model()\n",
    "\n",
    "scenario_tree_model.Stages = Set(ordered = True)\n",
    "scenario_tree_model.Nodes = Set()\n",
    "scenario_tree_model.NodeStage = Param(scenario_tree_model.Nodes, \\\n",
    "                                     within=scenario_tree_model.Stages)\n",
    "scenario_tree_model.Children = Set(scenario_tree_model.Nodes, \\\n",
    "                                  within=scenario_tree_model.Nodes, \\\n",
    "                                  ordered = True)\n",
    "scenario_tree_model.ConditionalProbability = \\\n",
    "                            Param (scenario_tree_model.Nodes)\n",
    "scenario_tree_model.Scenarios=Set(ordered = True)\n",
    "scenario_tree_model.ScenarioLeafNode = \\\n",
    "            Param (scenario_tree_model.Scenarios, \\\n",
    "                  within = scenario_tree_model.Nodes)\n",
    "scenario_tree_model.StageVariables = Set (scenario_tree_model.Stages)\n",
    "scenario_tree_model.StageCostVariable = \\\n",
    "            Param(scenario_tree_model.Stages)\n",
    "scenario_tree_model.ScenarioBasedData = Param(within = Boolean, \\\n",
    "                                             default = True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
