import pandas as pd
#Determine data attributes
def data_period(df):
    max_year = df.Year.max()
    min_year = df.Year.min()
    return max_year, min_year
  

#This function computes global capacities, average feed compositions and utilization rates of each asset configuration
def module_global(df, max_year):
    dt_wide = df.groupby(['Configuration', 'Year']).agg(
      CAP=('CAP', 'sum'), LSO=('LSO', 'sum'), LSW=('LSW', 'sum'), MSO=('MSO', 'sum'), MSW=('MSW', 'sum'), HSO=('HSO', 'sum'), HSW=('HSW', 'sum'), count_config=('Configuration', 'count'))
    dt_wide = dt_wide.reset_index()

    dt_long = dt_wide[['Configuration','Year','LSO','LSW','MSO','MSW','HSO','HSW']]
    dt_long = pd.melt(dt_long, id_vars=['Configuration', 'Year'], value_vars=['LSO','LSW','MSO','MSW','HSO','HSW'],
              var_name='Feed', value_name='Volume')

    #Calculating current capacities of the configurations and utilization
    dt_wideA = dt_wide.loc[(dt_wide.Year == max_year)]

    #Calculating yearly percentage compositions of crude feed blends for the refinery configurations
    dt_longA= dt_long
    dt_longA['Composition'] = '--'
    configs = dt_longA['Configuration'].unique()
    years = dt_longA['Year'].unique()
    dTemps = pd.DataFrame(columns=['Configuration', 'Year', 'Feed', 'Volume', 'Composition'])
    for config in configs:
        idx = dt_longA.Configuration==config
        dTemp_1 = dt_longA.loc[idx, :]
        for year in years:
            idx = dTemp_1.Year==year
            dTemp_2 = dTemp_1.loc[idx, :]
            if dTemp_2.Volume.sum() > 0:
                dTemp_2.loc[:, 'Composition'] = (dTemp_2.Volume/(dTemp_2.Volume.sum()))*100
            else:
                dTemp_2.loc[:, 'Composition'] = 0
          
            dTemp_2.Composition = round(dTemp_2.Composition) 
            dTemps = pd.concat([dTemps, dTemp_2], axis=0, join="outer", ignore_index=True)    
    dt_longA = dTemps

    #Calculating aggregated (for all years) percentage compositions of feed mix for the asset configurations
    dt_longB = dt_long.groupby(['Configuration', 'Feed']).agg(Volume=('Volume', 'sum'))
    dt_longB = dt_longB.reset_index()
    dt_longB['Composition'] = '--'
    configs = dt_longB['Configuration'].unique()
    dTemps = pd.DataFrame(columns=['Configuration', 'Feed', 'Volume', 'Composition'])
    for config in configs:
        idx = dt_longB.Configuration==config
        dTemp = dt_longB.loc[idx, :]
        if dTemp.Volume.sum() > 0:
            dTemp.loc[:, 'Composition'] = (dTemp.Volume/(dTemp.Volume.sum()))*100
        else:
            dTemp.loc[:, 'Composition'] = 0
        dTemp.Composition = round(dTemp.Composition, 2)
        dTemps = pd.concat([dTemps, dTemp], axis=0, join="outer", ignore_index=True)
    dt_longB = dTemps

    #Calculating historical min and max percentages of each feed type to each of the asset configurations
    dt_longB['min_comp'] = '--'
    dt_longB['max_comp'] = '--'
    configs = dt_longB['Configuration'].unique()
    feeds = dt_longB['Feed'].unique()
    dTemps = pd.DataFrame(columns=['Configuration', 'Feed', 'Volume', 'Composition', 'min_comp', 'max_comp'])
    for config in configs:
        idx_1 = dt_longA.Configuration==config
        idx_2 = dt_longB.Configuration==config
        dTemp_1 = dt_longA.loc[idx_1, :]
        dTemp_2 = dt_longB.loc[idx_2, :]
        for feed in feeds:
            idx_1 = dTemp_1.Feed==feed
            idx_2 = dTemp_2.Feed==feed
            dTemp_3 = dTemp_1.loc[idx_1, :]
            dTemp_4 = dTemp_2.loc[idx_2, :]
            dTemp_4.min_comp = dTemp_3.Composition.min()
            dTemp_4.max_comp = dTemp_3.Composition.max()

            dTemps = pd.concat([dTemps, dTemp_4], axis=0, join="outer", ignore_index=True)
    dt_longB = dTemps

    global_cap=dt_wideA[['Configuration','CAP']]
    global_comp=dt_longB[['Configuration','Feed','Composition']]
    comp_limit=dt_longB[['Configuration','Feed','min_comp', 'max_comp']]

    return global_cap, global_comp, comp_limit
