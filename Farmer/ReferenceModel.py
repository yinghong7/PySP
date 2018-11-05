{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Pyomo: Python optimisation modelling objects"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from pyomo.core import *"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "#model\n",
    "model = AbstractModel ()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "#parameters\n",
    "model.CROPS = Set ()\n",
    "model.TOTAL_ACREAGE = Param (within=PositiveReals)\n",
    "model.PriceQuota = Param (model.CROPS, within=PositiveReals)\n",
    "model.SubQuotaSellingPrice = Param (model.CROPS, within=PositiveReals)\n",
    "\n",
    "def super_quota_selling_price_validate (model, value, i):\n",
    "    return model.SubQuotaSellingPrice[i] >= model.SuperQuotaSellingPrice[i]\n",
    "\n",
    "model.SuperQuotaSellingPrice = Param (model.CROPS, validate=super_quota_selling_price_validate)\n",
    "model.CattleFeedRequirement = Param (model.CROPS, within=NonNegativeReals)\n",
    "model.PurchasePrice = Param (model.CROPS, within=PositiveReals)\n",
    "model.PlantingCostPerAcre = Param (model.CROPS, within=PositiveReals)\n",
    "model.Yield = Param (model.CROPS, within=NonNegativeReals)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "#variables\n",
    "model.DevotedAcreage = Var (model.CROPS, bounds=(0.0, model.TOTAL_ACREAGE))\n",
    "model.QuantitySubQuotaSold = Var (model.CROPS, bounds=(0.0, None))\n",
    "model.QuantitySuperQuotaSold = Var (model.CROPS, bounds=(0.0, None))\n",
    "model.QuantityPurchased = Var (model.CROPS, bounds=(0.0, None))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "#constraints\n",
    "def ConstrainTotalAcreage_rule(model):\n",
    "    return summation(model.DevotedAcreage) <= model.TOTAL_ACREAGE\n",
    "model.ConstrainTotalAcreage = Constraint (rule=ConstrainTotalAcreage_rule)\n",
    "\n",
    "def EnforceCattleFeedRequirement_rule(model, i):\n",
    "    return model.CattleFeedRequirement[i] <= (model.Yield[i] * model.DevotedAcreage[i])\n",
    "model.EnforeCattleFeedRequirement = Constraint (model.CROPS, rule=EnforceCattleFeedRequirement_rule)\n",
    "\n",
    "def LimitAmountSold_rule(model, i):\n",
    "    return model.QuantitySubQuotaSold[i] + model.QuantitySuperQuotaSold [i] - (model.Yield[i] * model.DevotedAcreage[i]) <= 0.0\n",
    "model.LimitAmountSold = Constraint(model.CROPS, rule=LimitAmountSold_rule)\n",
    "\n",
    "def EnforceQuotas_rule(model, i):\n",
    "    return (0.0, model.QuantitySubQuotaSold[i], model.PriceQuota[i])\n",
    "model.EnforceQuotas = Constraint(model.CROPS, rule=EnforceQuotas_rule)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "#stage_specific cost computations\n",
    "def ComputeFirstStageCost_rule(model):\n",
    "    return summation(model.PlantingCostPerAcre, model.DevotedAcreage)\n",
    "model.FirstStageCost = Expression(rule=ComputeFirstStageCost_rule)\n",
    "\n",
    "def ComputeSecondStageCost_rule(model):\n",
    "    expr = summation(model.PurchasePrice, model.QuantityPurchased)\n",
    "    expr -= summation(model.SubQuotaSellingPrice, model.QuantitySubQuotaSold)\n",
    "    expr -= summation(model.SuperQuotaSellingPrice, model.QuantitySuperQuotaSold)\n",
    "    return expr\n",
    "\n",
    "model.SecondStageCost = Expression(rule=ComputeSecondStageCost_rule)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "#PySP auto-generated objectives, minimise sum of stagecost\n",
    "def total_cost_rule(model):\n",
    "    return model.FirstStageCost + model.SecondStageCost\n",
    "model.Total_Cost_Objective = Objective(rule=total_cost_rule, sense=minimize)"
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
