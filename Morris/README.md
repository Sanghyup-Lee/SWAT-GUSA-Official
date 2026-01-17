# Morris
Morris method application in our main SWAT-GUSA project.

# Objective
- SWAT-GUSA has a change of landuse and tree canopy cover data.
- A numerous parameters influence to change hydrological results via landuse and canopycover changes.
- Limitation of computational cost to analysis uncertainty as considered all parameters.
- We decided to use Morris method at first to screen the most influential parameters from our model.

# Morris method description

## Step of Morris application in SWAT-GUSA

### Phase 1: Model setting
- Baseline model set to run the morris

### Phase 2: Factor file generation
- All parameters listup influence to streamflow related with landcover and canopy cover change based on SWAT manual (Arnold et al., 2012)

### Phase 3: Sample file generation
- Use simlab to generate sample file for Morris method

### Phase 4: Build parallel system to modify model factors based on sample
- Use SWATswapper to change values of model

### Phase 5: Run model
- Run SWAT parallel by using batch file.
