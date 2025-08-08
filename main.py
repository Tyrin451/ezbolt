import ezbolt

# initialize bolt group
bolt_group = ezbolt.BoltGroup(units="SI")

# add bolts    
bolt_group.add_bolts(xo=0, yo=0, width=76.2, height=152.4, nx=1, ny=3)

# preview geometry
ezbolt.preview(bolt_group)

# calculate bolt force with elastic method
results = bolt_group.solve(Vx=0, Vy=-222.4, torsion=-11298.5)

# plot bolt forces
ezbolt.plot_elastic(bolt_group)
ezbolt.plot_ECR(bolt_group)
ezbolt.plot_ICR(bolt_group)

# look at the bolt force tables
df1 = results["Elastic Method - Superposition"]["Bolt Force Table"]
df2 = results["Elastic Method - Center of Rotation"]["Bolt Force Table"]
df3 = results["Instant Center of Rotation Method"]["Bolt Force Table"]